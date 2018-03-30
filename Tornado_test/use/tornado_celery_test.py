__author__ = 'shy'
__date__ = '2018/3/30 10:43'

import time
import logging
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen

import tcelery

from . import tasks

tornado.options.parse_command_line()
tcelery.setup_nonblocking_producer()


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("Hello, world")
        self.finish()


class CeleryHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        response = yield gen.Task(tasks.sleep.apply_async, args=[5])
        self.write('CeleryBlocking Request: {}'.format(response.result))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/celery-block", CeleryHandler),
    ], autoreload=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()