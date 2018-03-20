__author__ = 'shy'
__date__ = '2018/3/20 13:15'

from twisted.internet import defer
from twisted.web.client import getPage
from twisted.internet import reactor


def one_done(arg):
    # 每一个执行结束执行
    print(arg)


def all_done(arg):
    # 只有全部执行完才执行
    print('all done')
    reactor.stop()


@defer.inlineCallbacks
def task(url):
    # 发送Http请求
    res = getPage(bytes(url, encoding='utf8'))
    res.addCallback(one_done)
    yield res


url_list = [
    'http://www.baidu.com',
    'http://www.bing.com',
]

# 存放obj，已经向url发送请求
defer_list = []

for url in url_list:
    v = task(url)
    defer_list.append(v)

d = defer.DeferredList(defer_list)
d.addBoth(all_done)

# 死循环
reactor.run()