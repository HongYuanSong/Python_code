__author__ = 'shy'
__date__ = '2018/3/20 11:31'

import requests


def fetch_async(url):
    response = requests.get(url)
    return response


url_list = ['http://www.baidu.com', 'http://www.bing.com']

for url in url_list:
    fetch_async(url)