__author__ = 'shy'
__date__ = '2018/3/20 12:59'

import aiohttp
import asyncio


@asyncio.coroutine
def fetch_async(url):
    print(url)
    response = yield from aiohttp.request('GET', url)
    # data = yield from response.read()
    # print(url, data)
    print(url, response)
    response.close()


tasks = [fetch_async('http://www.baidu.com/'), fetch_async('http://www.bing.com/')]

event_loop = asyncio.get_event_loop()
results = event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()