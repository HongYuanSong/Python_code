__author__ = 'shy'
__date__ = '2018/3/20 16:37'

import time

import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.web import Future



# 先来个同步阻塞的Tornado（大部分web框架基本都是同步方式）：多个用户访问时用户一等10s，用户二等用户一拿到请求结果才开始请求，再等十秒。。。。


# class SyncHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.doing()
#         self.write('同步执行doing，等10s才会显示')
#
#     def doing(self):
#         time.sleep(10)
#
#
# application = tornado.web.Application([
#     (r"/index", SyncHandler),
# ])
#
# if __name__ == "__main__":
#     application.listen(8888)
#     tornado.ioloop.IOLoop.instance().start()


# Tornado异步非阻塞使用：装饰器+Future对象+生成器


class AsyncHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        future = Future()
        # 通过设置超时时间释放socket
        # tornado.ioloop.IOLoop.current().add_timeout(time.time() + 10, self.doing)

        # 接收socket请求，不返回结果，一直阻塞住，直到future对象调用set_result方法时，才会执行doing方法
        future.add_done_callback(self.doing)
        yield future

    def doing(self, *args, **kwargs):
        self.write('async')
        self.finish()


application = tornado.web.Application([
    (r"/index", AsyncHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



