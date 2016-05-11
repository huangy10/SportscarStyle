import urllib

from tornado.httpclient import HTTPClient

client = HTTPClient()


def send_string_message(message):

    response = client.fetch(
        "http://localhost:8887/notification/general",
        body=urllib.urlencode({"message": message})
    )
    print response