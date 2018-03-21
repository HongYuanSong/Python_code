__author__ = 'shy'
__date__ = '2018/3/20 11:59'

# 多进程可实现并发，但请求发出后及返回前进程存在IO阻塞（空闲）


from concurrent.futures import ProcessPoolExecutor
import requests
import time

# 方式1：直接在函数中处理任务


def task(url):
    response = requests.get(url)
    print(url, response)
    # 可对response进行其他处理


pool = ProcessPoolExecutor(3)
url_list = [
    'http://www.bing.com',
    'http://www.zhihu.com',
    'http://www.baidu.com',
]

for url in url_list:
    # 所有处理均在task函数中执行
    pool.submit(task, url)

pool.shutdown(wait=True)


# 方式2：通过回调函数分步处理任务，实现低耦合

def task(url):
    """下载页面"""
    response = requests.get(url)
    return response


def done(future, *args, **kwargs):
    res = future.result()
    print(res.status_code, res.content)


pool = ProcessPoolExecutor(3)
url_list = [
    'http://www.bing.com',
    'http://www.zhihu.com',
    'http://www.baidu.com',
]

for url in url_list:
    response = pool.submit(task, url)
    # 通过回调函数出里返回的response，可定义多个回调函数，实现低耦合
    response.add_done_callback(done)

pool.shutdown(wait=True)