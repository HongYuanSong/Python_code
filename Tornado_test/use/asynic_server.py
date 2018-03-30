__author__ = 'shy'
__date__ = '2018/3/30 9:37'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

from tornado.options import define, options


define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous  # 添加异步装饰器
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()  # 生成AsyncHTTPClient实例,必须使用此类，否则无效果
        client.fetch("http://www.cnblogs.com/lianzhilei", callback=self.on_response)  # 绑定回调

    def on_response(self, response):  # response访问返回结果
        self.write("""                                                 
                <div style="text-align: center">
                    <div style="font-size: 72px">Time Cost</div>
                    <div style="font-size: 72px">%s</div>
                </div>""" % (response.request_time))
        self.finish()  # 结束


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()