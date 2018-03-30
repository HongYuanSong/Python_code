__author__ = 'shy'
__date__ = '2018/3/30 9:19'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient


from tornado.options import define, options

define('port', default=8080, help='run on the given port', type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        client = tornado.httpclient.HTTPClient()
        response = client.fetch("http://www.baidu.com")
        self.write("""
                <div style="text-align: center">
                    <div style="font-size: 50px">Time Cost</div>
                    <div style="font-size: 50px">{time}</div>
                </div>
                """.format(time=response.request_time))


if __name__ == "__main__":
    # tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()