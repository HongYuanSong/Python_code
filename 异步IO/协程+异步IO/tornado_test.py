from __future__ import absolute_import, unicode_literals
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado import ioloop


COUNT = 0


def handle_response(response):

    global COUNT
    COUNT -= 1

    if response.error:
        print("Error:", response.error)
    else:
        print(response.body)

    if COUNT == 0:
        # step5
        ioloop.IOLoop.current().stop()


def func():
    url_list = [
        'http://www.baidu.com',
        'http://www.bing.com',
    ]
    global COUNT
    COUNT = len(url_list)

    for url in url_list:
        print(url)
        # step3
        http_client = AsyncHTTPClient()
        # step4
        http_client.fetch(HTTPRequest(url), handle_response)


# step1
ioloop.IOLoop.current().add_callback(func)
# step2
ioloop.IOLoop.current().start()