__author__ = 'shy'
__date__ = '2018/3/20 12:42'

import asyncio
import requests
# 支持TCP不支持HTTP（可以自定义请求头和请求体，依据TCP实现基于HTTP的异步IO）


# step4：定义任务函数（asyncio.coroutine装饰器、yield from）
@asyncio.coroutine
def func1():
    print('before...func1......')
    yield from asyncio.sleep(5)
    print('end...func1......')


# step3：定义task列表，传入任务函数
tasks = [func1(), func1()]

# step1:创建事件循环
loop = asyncio.get_event_loop()

# step2：调用run_until_complete,传入task
loop.run_until_complete(asyncio.gather(*tasks))

# step5：关闭事件循环
loop.close()


# 根据TCP自定义基于HTTP的异步IO

@asyncio.coroutine
def fetch_async(host, url='/'):
    print(host, url)
    reader, writer = yield from asyncio.open_connection(host, 80)

    request_header_content = """GET %s HTTP/1.0\r\nHost: %s\r\n\r\n""" % (url, host,)
    request_header_content = bytes(request_header_content, encoding='utf-8')

    writer.write(request_header_content)
    yield from writer.drain()
    text = yield from reader.read()
    print(host, url, text)
    writer.close()


tasks = [
    fetch_async('www.baidu.com',),
    fetch_async('www.bing.com',)
]

loop = asyncio.get_event_loop()
results = loop.run_until_complete(asyncio.gather(*tasks))
loop.close()


# asyncio+requests

@asyncio.coroutine
def fetch_async(func, *args):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, func, *args)
    response = yield from future
    print(response.url, response.content)


tasks = [
    fetch_async(requests.get, 'http://www.baidu.com/'),
    fetch_async(requests.get, 'http://www.bing.com/')
]

loop = asyncio.get_event_loop()
results = loop.run_until_complete(asyncio.gather(*tasks))
loop.close()

