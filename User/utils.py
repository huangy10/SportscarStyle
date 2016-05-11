# coding=utf-8
"""这个文件是参考云片网给出的python参考代码写的"""

import re
import httplib
import urllib
import random

import jwt

from django.conf import settings


class JWTUtil(object):
    SECRET = settings.SECRET_KEY

    @classmethod
    def jwt_encode(cls, user_id, device_id):
        """
        Encode jwt header information
        :param user_id:         identifier for the user
        :param device_id:       identifier for the device
        :return:
        """
        return jwt.encode({"user_id": user_id,
                           "device_id": device_id},
                          cls.SECRET)

    @classmethod
    def jwt_decode(cls, token):
        try:
            return jwt.decode(token, cls.SECRET)
        except jwt.InvalidTokenError:
            return None



# 服务地址
host = "yunpian.com"
# 端口号
port = 80
# 版本号
version = "v1"
# 通用短信接口的uri
sms_send_uri = "/" + version + "/sms/send.json"
# 短信内容模板
SMS_TEMPLATE = '您的验证码是%s【找米网】'
SMS_KEY = "b2bc04ed9bbc52b10b3b68e5656eb08f"


def send_sms(code, mobile):
    """
    This utility function enables sending sms to the user given its phone number, api key
     and the message content.
     :param code authentication code
     :param mobile phone number
     :return True on success
    """
    text = SMS_TEMPLATE % code
    params = urllib.urlencode({'apikey': SMS_KEY, 'text': text, 'mobile': mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    status_code = int(re.match(r'\{"code":(-?\d+),.*', response_str).group(1))
    if status_code == 0:
        return True
    else:
        return False


def create_random_code():
    """ This utility function creates and returns a random code with length of 6
    """
    code = ''
    for _ in range(6):
        code += random.choice("1234567890")
    return code


def star_sign_from_date(date, name=('Capricorn', 'Aquarius', 'Pisces', 'Aries', 'Taurus', 'Gemini',
                                    'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius')):
    month = date.month
    day = date.day
    d = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))
    return name[len(filter(lambda y:y <= (month, day), d)) % 12]
