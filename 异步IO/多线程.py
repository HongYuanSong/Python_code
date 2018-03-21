__author__ = 'shy'
__date__ = '2018/3/20 11:42'

# 多线程可实现并发，但请求发出后及返回前线程存在IO阻塞（空闲）

# 在python中，多线程方式在处理IO密集型任务时效果要优于多进程，而在处理计算密集型任务时，多进程方式效果更好\
# 因为计算密集型任务需要调用CPU进行处理，而使用cpython作为解释器的python中存在全局解释器锁，\
# 使得同一时刻只有一个线程被CPU调度执行任务，即使开了多个线程，也不会同时利用多核CPU，同时开启线程也会消耗一定资源，\
# 所以使用多进程执行计算密集型任务,使用多线程执行IO密集型任务（开启进程开销远大于开启进程）\
# HTTP请求为IO密集型任务，所以使用多线程效果更好


from concurrent.futures import ThreadPoolExecutor
import requests
import time

# 方式1：直接在函数中处理任务


def task(url):
    response = requests.get(url)
    print(url, response)
    # 可对response进行其他处理


pool = ThreadPoolExecutor(3)
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


pool = ThreadPoolExecutor(3)
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