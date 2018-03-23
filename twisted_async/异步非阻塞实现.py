__author__ = 'shy'
__date__ = '2018/3/21 17:18'

from twisted.internet import reactor   # 事件循环（所有的socket都已经移除，终止事件循环）
from twisted.web.client import getPage # socket对象（下载完成，自动从事件循环中移除）
from twisted.internet import defer     # defer.Deferred 特殊的socket对象 （不会发请求，只能通过手动移除）


# 1.通过调用getPage，自动创建socket
# 2.通过装饰器、yield defer对象，将socket添加到事件循环中（执行函数）
# 3.通过调用reactor.run，开始事件循环
# 4.将task返回的defer对象加入列表，将列表作为参数实例化DeferredList，给实例对象添加回调，回调中调用reactor.stop，终止事件循环

# def response(content):
#     print(content)
#
#
# def done(*args, **kwargs):
#     reactor.stop()
#
#
# @defer.inlineCallbacks
# def task():
#     url = "http://www.baidu.com"
#     d = getPage(url.encode('utf-8'))
#     d.addCallback(response)
#     yield d
#
#
# d = task()
# dd = defer.DeferredList([d, ]) # 循环task，传入多个defer对象可监听多个socket对象
# dd.addBoth(done)
#
# reactor.run()


_close = None
count = 0


def response(content):
    global count
    count += 1
    print(content)

    if count == 2:
        print("=====>", count)
        _close.callback(None)


def done(*args, **kwargs):
    reactor.stop()


@defer.inlineCallbacks
def task():
    url = "http://www.baidu.com"
    d1 = getPage(url.encode('utf-8'))
    d1.addCallback(response)

    url = "http://www.bing.com"
    d2 = getPage(url.encode('utf-8'))
    d2.addCallback(response)


    global _close
    _close = defer.Deferred()
    yield _close


spider1 = task()
# spider2 = task()
dd = defer.DeferredList([spider1,]) # 循环task，传入多个defer对象可监听多个socket对象
dd.addBoth(done)

reactor.run()



# 通过创建类实现scrapy框架



