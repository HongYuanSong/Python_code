__author__ = 'shy'
__date__ = '2018/3/20 13:05'


# gevent=greenlet+异步IO
# gevent也只实现了TCP没有实现HTTP请求的异步IO
# grequests模块（gevent+requests）


import gevent
import requests
from gevent import monkey

monkey.patch_all()


def fetch_async(method, url, req_kwargs):
    print(method, url, req_kwargs)
    response = requests.request(method=method, url=url, **req_kwargs)
    print(response.url, response.content)


# 发送请求

gevent.joinall([
    gevent.spawn(fetch_async, method='get', url='https://www.python.org/', req_kwargs={}),
    gevent.spawn(fetch_async, method='get', url='https://www.baidu.com/', req_kwargs={}),
    gevent.spawn(fetch_async, method='get', url='https://github.com/', req_kwargs={}),
])


# 发送请求（协程池控制最大协程数量）

from gevent.pool import Pool
pool = Pool(5)
gevent.joinall([
    pool.spawn(fetch_async, method='get', url='https://www.python.org/', req_kwargs={}),
    pool.spawn(fetch_async, method='get', url='https://www.baidu.com/', req_kwargs={}),
    pool.spawn(fetch_async, method='get', url='https://www.github.com/', req_kwargs={}),
])