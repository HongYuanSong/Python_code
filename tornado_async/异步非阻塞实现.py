__author__ = 'shy'
__date__ = '2018/3/20 16:37'

import tornado
import time
from tornado.web import RequestHandler

# 先来个同步阻塞的Tornado（大部分web框架基本都是同步方式）：多个用户访问时用户一等10s，用户二等用户一拿到请求结果才开始请求，再等十秒。。。。


# class SyncHandler(RequestHandler):
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


# Tornado异步非阻塞使用


class AsyncHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        future = Future()
        future.add_done_callback(self.doing)
        yield future
        # 或
        # tornado.ioloop.IOLoop.current().add_future(future,self.doing)
        # yield future

    def doing(self, *args, **kwargs):
        self.write('async')
        self.finish()

application = tornado.web.Application([
    (r"/index", AsyncHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
