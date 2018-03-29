__author__ = 'shy'
__date__ = '2018/3/29 9:45'

from tornado.httpclient import HTTPClient


# 基础的同步调用
def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body


# 通过回调参数callback进行异步调用
from tornado.httpclient import AsyncHTTPClient


def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()

    def handle_response(response):
        callback(response.body)

    http_client.fetch(url, callback=handle_response)


# 使用Future对象进行异步调用
from tornado.concurrent import Future


def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future


# 通过协程进行异步请求
from tornado import gen


@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    # raise gen.Return(response.body) # python2
    return response.body # python3.3


if __name__ == '__main__':
    pass
