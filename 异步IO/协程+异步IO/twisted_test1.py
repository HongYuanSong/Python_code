__author__ = 'shy'
__date__ = '2018/3/20 13:15'

from twisted.internet import defer
from twisted.web.client import getPage
from twisted.internet import reactor


def one_done(arg):
    print(arg)


def all_done(arg):
    print('all done')
    reactor.stop()


@defer.inlineCallbacks
def task(url):
    # 发送Http请求
    res = getPage(bytes(url, encoding='utf8'))
    res.addCallback(one_done)
    yield res


if __name__ == '__main__':
    url_list = [
        'http://www.baidu.com',
        'http://www.bing.com',
    ]

    defer_list = []

    for url in url_list:
        # step1
        v = task(url)
        # step2
        defer_list.append(v)

    # step3
    d = defer.DeferredList(defer_list)
    # step4
    d.addBoth(all_done)

    # step5
    reactor.run()