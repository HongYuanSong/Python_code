__author__ = 'shy'
__date__ = '2018/3/20 17:26'

import re
import time
import socket
import select


# # 同步非阻塞web框架原理
#
# socket = socket.socket()
# socket.setblocking(False)
#
# conn_list = []
# conn_list.append(socket)
#
# while True:
#     # 调用select方法监听conn_list中的文件描述符对象，\
#     # 当conn_list中某个文件描述符发生变化时（socket有新的连接或conn接收到数据），该文件描述符会添加到readable列表中
#     readable, writable, error = select.select(conn_list, [], [], 0.05)
#     for r in readable:
#         if r == socket:
#             # socket对象发生变化（接收到用户连接）
#             conn, addr = r.accept()
#             conn_list.append(conn)
#         else:
#             # conn对象发生变化（接收到用户发送的数据）
#             recv_data = bytes()
#             while True:
#                 try:
#                     chunk = r.socket.recv(1024)
#                     recv_data += chunk
#                 except Exception as e:
#                     break
#
#             # 1）分析recv_data中请求头获取url；\
#             # 2) 根据路由系统中url和函数的对应关系执行对应函数，结果赋值resp；\
#             # 3) 通过r.sendall(resp)向客户端发送函数执行结果；\
#             # 4) 调用r.close()关闭客户端连接，调用conn_list.remove(r)将删除客户端socket对象
#             # ==>实现同步模式的web框架
#
#
# # 异步非阻塞web框架原理
#             # 假设上面过程2）返回了一个对象resp1（不是字符串），将resp1以request_dict={r:resp1}的形式保存到request_dict，\
#             # 遍历request_dict.items(),取到k=客户端socket对象、v=返回resp对象，\
#             # 判断v.status为True（默认False）时调用k.send（resp）；可以通过有下一个socket连接改变上一个结果的status或者设置超时时间改变status
#             # ==>实现异步非阻塞web框架
#
#
# # 自定义异步非阻塞web框架：非阻塞的socket+IO多路复用（select）+自定义future对象
# # 自定义future对象：
# # 1）判断函数结果，如果是str直接返回，如果是生成器对象则保存到字典，不直接返回
# # 2）根据结果的状态决定是否调用sendall发送response并关闭连接


class HttpResponse(object):
    """封装响应信息"""

    def __init__(self, content=''):
        self.content = content

        self.headers = {}
        self.cookies = {}

    def response(self):
        return bytes(self.content, encoding='utf-8')


class Http404(HttpResponse):

    def __init__(self):
        super(Http404, self).__init__('404 Not Found')


class HttpRequest:
    """接收、封装用户请求"""

    def __init__(self, conn):
        self.conn = conn

        self.req_header_bytes = bytes()
        self.req_header_str = ""
        self.req_body = bytes()
        self.req_header_dict = {}

        self.method = ""
        self.url = ""
        self.protocol = ""

        self.initialize()
        self.initialize_req_headers()

    def initialize(self):

        recv_data = bytes()
        while True:
            try:
                chunk = self.conn.recv(1024)
                recv_data += chunk
            except Exception as e:
                break
            req = recv_data.split(b'\r\n\r\n', 1)
            if len(req) == 1:
                self.req_header_bytes += req
            else:
                header, body = req
                self.req_header_bytes += header
                self.req_body += body

    def initialize_req_headers(self):

        self.req_header_str = str(self.req_header_bytes, encoding='utf-8')
        headers = self.req_header_str.split('\r\n')
        first_line = headers[0].split(' ')
        if len(first_line) == 3:
            self.method, self.url, self.protocol = headers[0].split(' ')
            for line in headers[1]:
                kv = line.split(':')
                if len(kv) == 2:
                    k, v = kv
                    self.req_header_dict[k] = v


class Future(object):
    """异步非阻塞模式时封装回调函数以及是否准备就绪"""

    def __init__(self, callback):
        self.callback = callback
        self._ready = False
        self.value = None

    def set_result(self, value=None):
        self.value = value
        self._ready = True

    @property
    def ready(self):
        return self._ready


class TimeoutFuture(Future):
    """异步非阻塞超时"""

    def __init__(self, timeout):
        super(TimeoutFuture, self).__init__(callback=None)
        self.timeout = timeout
        self.start_time = time.time()

    @property
    def ready(self):
        current_time = time.time()
        if current_time > self.start_time + self.timeout:
            self._ready = True
        return self._ready


class MyTornado:
    """自定义异步非阻塞web框架"""

    def __int__(self, url_routes):
        self.url_routes = url_routes
        self.request = None
        self.conn_set = set()
        self.async_request_handler = {}

    def run(self, host='localhost', port=8888):
        sk = socket.socket()
        sk.setblocking(False)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.bind((host, port))
        sk.listen(128)
        self.conn_set.add(sk)
        try:
            while True:
                readable, writable, error = select.select(self.conn_set, [], self.conn_set, 0.05)
                for conn in readable:
                    if conn == sk:
                        client, addr = conn.accept()
                        client.setblocking(False)
                        self.conn_set.add(client)
                    else:
                        gen = self.process(conn)
                        if isinstance(gen, HttpResponse):
                            conn.sendall(gen.response())
                            conn.close()
                            self.conn_set.remove(conn)
                        else:
                            yielded = next(gen)
                            self.async_request_handler[conn] = yielded

                    self.polling_callback()

        except Exception as e:
            print(e)
        finally:
            sk.close()

    def process(self, conn):
        """通过路由系统调用相应函数"""

        self.request = HttpRequest(conn)
        func = None

        for route in self.url_routes:
            if re.match(route[0], self.request.url):
                func = route[1]
                break
            if not func:
                return Http404()
            else:
                return func(self.request)

    def polling_callback(self):
        """遍历触发异步非阻塞的回调函数"""

        for conn in list(self.async_request_handler.keys()):
            yielded = self.async_request_handler[conn]
            if not yielded.ready:
                continue
            if yielded.callback:
                ret = yielded.callback(self.request, yielded)
                conn.sendall(ret.response())
            conn.close()
            self.conn_set.remove(conn)
            del self.async_request_handler[conn]


if __name__ == '__main__':
    # 同步调用

    def index(request):
        return HttpResponse('OK')


    routes = [
        (r'/index/', index),
    ]

    app = MyTornado(routes)
    app.run()

    # 异步调用（等待）

    request_list = []

    def callback(request, future):
        return HttpResponse(future.value)

    def req(request):
        obj = Future(callback=callback)
        request_list.append(obj)
        yield obj

    def stop(request):
        obj = request_list[0]
        del request_list[0]
        obj.set_result('done')
        return HttpResponse('stop')

    routes = [
        (r'/req/', req),
        (r'/stop/', stop),
    ]

    app = MyTornado(routes)
    app.run()

    # 异步调用（超时）

    request_list = []

    def async(request):
        obj = TimeoutFuture(5)
        yield obj

    def home(request):
        return HttpResponse('home')

    routes = [
        (r'/home/', home),
        (r'/async/', async),
    ]

    app = MyTornado(routes)
    app.run(port=8012)

