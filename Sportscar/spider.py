# coding=utf-8
import os
import sys
import re
import string
import json
import time
import StringIO

from bs4 import BeautifulSoup
from tornado import httpclient, gen, ioloop, queues
from django.core.wsgi import get_wsgi_application
from tornado.httpclient import HTTPError
from django.core.files.uploadedfile import InMemoryUploadedFile

sys.path.extend([os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SportscarStyle.settings')
application = get_wsgi_application()

from Sportscar.models import Manufacturer, Sportscar

# template to generate the url of car details
CAR_DETAIL_URL_TEMPLATE = "http://car.autohome.com.cn/config/series/{0}.html"
CAR_IMAGE_URL_TEMPLATE = "http://car.autohome.com.cn/pic/series/{0}.html"
DOMAIN_NAME = "http://car.autohome.com.cn"

PROJECT_PATH = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
MODULE_PATH = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))

# path for index.html
INDEX_FILE_PATH = os.path.join(MODULE_PATH, "data", "index.html")


def parse_index_block(soup):
    if soup is None:
        return
    manufacturer = parse_brand(soup.find("dt"))
    cars = soup.find_all("li", {"class": None})
    for car in cars:
        parse_car_record(car, manufacturer)


def parse_brand(soup):
    brand_logo = soup.find("a").find("img")["src"]
    brand_name_element = soup.find("div").find("a")
    brand_name = brand_name_element.getText()
    brand_detial_url = brand_name_element["href"]
    brand_id = re.match(r".*-(\d+).html", brand_detial_url).groups()[0]
    manufacturer, _ = Manufacturer.objects.get_or_create(
        remote_id=brand_id, name=brand_name, detail_url=brand_detial_url, logo_remote=brand_logo
    )
    return manufacturer


def parse_car_record(soup, manufacturer):
    # skip the first "s" letter
    remote_id = soup["id"][1:]
    car_name = soup.find("a").getText()
    Sportscar.objects.get_or_create(remote_id=remote_id, name=car_name, manufacturer=manufacturer)


def index_resolver():
    """main entrance of index solver, this function would load basic information of alll manufacturers and cars
    """
    print "Start parsing from index.html"
    with open(INDEX_FILE_PATH) as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        alphabet = string.ascii_uppercase
        for alpha in alphabet:
            brands = soup.find("div", {"id": "html{0}".format(alpha)})
            if brands is None:
                continue
            brands = brands.find_all("dl")
            for brand_block in brands:
                parse_index_block(brand_block)
    print "done parsing"


def parse_detail_data(html):
    """ Parse data from detail page of a car
    """
    soup = BeautifulSoup(html, "html.parser")
    js_blocks = soup.find_all("script", {"src": None})
    for js in js_blocks:
        data_string = js.text.replace("\r\n", "")
        result = re.match(r".*var config = (.*?);.*", data_string)
        if result is not None:
            return json.loads(result.groups()[0])
    return None


def json_data_analyse(data, car, save=True):
    """ Extract data from the json object parsed from detail page
    """
    param_type_items = data["result"]["paramtypeitems"]
    for param_type_item in param_type_items:
        param_items = param_type_item["paramitems"]
        for param_item in param_items:
            name = param_item["name"]
            value_items = param_item["valueitems"]
            value = value_items[0]["value"]
            if name == u"厂商指导价(元)":
                car.price = value
            elif name == u"发动机":
                car.engine = value
            elif name == u"车身结构":
                car.body = value
            elif name == u"官方0-100km/h加速(s)":
                car.zeroTo60 = value
            elif name == u"最高车速(km/h)":
                car.max_speed = value
            elif name == u"工信部综合油耗(L/100km)":
                car.fuel_consumption = value
            elif name == u"最大扭矩(N·m)":
                car.torque = value
    if save:
        car.save()


def parse_image_url(html, car, save=True):
    soup = BeautifulSoup(html, "html.parser")
    target_elements = soup.find("div", {"class": "cartab-title"}).parent.find_all("img")
    if target_elements is not None and len(target_elements) > 0:
        target_element = target_elements[0]
        car.remote_thumbnail = target_element["src"]
        if save:
            car.save()
        big_image_view_url = target_element.parent["href"]
        if not big_image_view_url.startswith(DOMAIN_NAME):
            big_image_view_url = DOMAIN_NAME + big_image_view_url
        return big_image_view_url
    else:
        return None


def parse_big_image_url(html, car, save=True):
    soup = BeautifulSoup(html, "html.parser")
    target_element = soup.find("img", {"id": "img"})
    if target_element is None:
        return False
    car.remote_image = target_element["src"]
    if save:
        car.save()
    return True


@gen.coroutine
def car_detail_resolver():
    data = Sportscar.objects.all()

    car_queue = queues.Queue()
    client = httpclient.AsyncHTTPClient()

    for car in data:
        yield car_queue.put(car)

    @gen.coroutine
    def worker(worker_id):
        print "WORKER %s START!" % worker_id
        while True:
            car = yield car_queue.get()
            if car is None:
                print u"[worker %s] 退出" % worker_id
                break

            # 找到缩略图链接
            image_set_url = CAR_IMAGE_URL_TEMPLATE.format(car.remote_id)
            print u"[worker %s]==获取[%s]的图片: %s" % (worker_id, car.name, image_set_url)
            try:
                result = yield client.fetch(image_set_url)
            except Exception, e:
                print e
                car_queue.task_done()
                yield car_queue.put(car)
                time.sleep(1)
                continue
            big_image_view_url = parse_image_url(result.body, car, save=False)
            if big_image_view_url is None:
                print u"[worker %s]!! 没有找到图片: %s" % (worker_id, image_set_url)
            else:
                # 找到大图链接
                try:
                    result = yield client.fetch(big_image_view_url)
                except Exception, e:
                    print e
                    car_queue.task_done()
                    yield car_queue.put(car)
                    time.sleep(1)
                    continue

                res = parse_big_image_url(result.body, car, save=False)
                if not res:
                    print u"[worker %s]@@ 没有找到大图: %s" % (worker_id, image_set_url)

            # 找到详情数据
            detail_url = CAR_DETAIL_URL_TEMPLATE.format(car.remote_id)
            print u"[worker %s]++ 获取[%s]的数据FROM: %s" % (worker_id, car.name, detail_url)
            try:
                result = yield client.fetch(detail_url)
            except Exception, e:
                print e
                car_queue.task_done()
                yield car_queue.put(car)
                time.sleep(1)
                continue
            car_data = parse_detail_data(result.body)
            if car_data is not None:
                json_data_analyse(car_data, car, save=True)
            else:
                car.save()
                print u"[worker %s]?? 没有找到数据: %s" % (worker_id, detail_url)
            car_queue.task_done()

    print '###############爬虫开始！##################'
    for i in range(4):
        worker(i)
    yield car_queue.join()
    print '###############爬虫停止！##################'


def start_car_detail_resolver():
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(car_detail_resolver)


@gen.coroutine
def image_downloader():

    data = Sportscar.objects.all()

    thumbnail_task_queue = queues.Queue()
    image_task_queue = queues.Queue()
    client = httpclient.AsyncHTTPClient()

    for car in data:
        yield thumbnail_task_queue.put(car)
        yield image_task_queue.put(car)

    @gen.coroutine
    def worker(worker_id, worker_type, car_queue):
        """
         :param worker_type thumbnail or image
        """
        if worker_type != "thumbnail" and worker_type != "image":
            print u"[worker %s] 错误的配置,worker退出" % worker_id
            return
        while True:
            car = yield car_queue.get()
            if car is None:
                print u"[worker %s] 退出" % worker_id
                break

            if worker_type == "thumbnail":
                image_url = car.remote_thumbnail
            else:
                image_url = car.remote_image

            print u"[worker %s] == 为汽车%s下载图片: %s" % (worker_id, car.name, image_url)
            if image_url == "":
                car_queue.task_done()
                continue
            try:
                response = yield client.fetch(image_url)
            except Exception, e:
                print e
                car_queue.task_done()
                yield car_queue.put(car)
                time.sleep(1)
                continue
            io = StringIO.StringIO()
            io.write(response.body)
            ext = car.remote_image.split(".")[-1]
            if worker_type == "thumbnail":
                car.thumbnail = InMemoryUploadedFile(
                    file=io, field_name=None, name="foo.%s" % ext, size=io.len,
                    charset=None, content_type="image/%s" % ext
                )
            else:
                car.image = InMemoryUploadedFile(
                    file=io, field_name=None, name="foo.%s" % ext, size=io.len,
                    charset=None, content_type="image/%s" % ext
                )
            car.save()
            io.close()
            print u"[worker %s] 成功!" % worker_id
            car_queue.task_done()

    print '###############爬虫开始！##################'
    for i in range(3):
        worker(i, "thumbnail", thumbnail_task_queue)
    for i in range(3, 6):
        worker(i, "image", image_task_queue)
    yield thumbnail_task_queue.join()
    yield image_task_queue.join()
    print '###############爬虫停止！##################'


def start_image_downloader():
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(image_downloader)
