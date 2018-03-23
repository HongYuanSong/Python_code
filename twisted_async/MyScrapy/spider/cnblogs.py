__author__ = 'shy'
__date__ = '2018/3/22 7:56'

from engine import Request


class CnblogsSpider(object):
    name = 'cnblogs'

    def start_requests(self):
        start_url = ['http://www.cnblogs.com', ]
        for url in start_url:
            yield Request(url, self.parse)

    def parse(self, response):
        print(response)  # response是下载的页面
        yield Request('http://www.cnblogs.com', callback=self.parse)
