__author__ = 'shy'
__date__ = '2018/3/20 14:17'

# 前戏：
# 1.socket
#     1）非阻塞：setblocking(False)==>connect无响应；recv无数据==>报错
#     2）只要连接不管是不是非阻塞都会向服务器发送数据（客户端）
#
# 2.IO多路复用
#     客户端：
#     try:
#         socket_obj1.connect()
#         socket_obj2.connect()
#         socket_obj3.connect()
#     except Exception:
#         pass
#
#     while True:
#         r, w, e = select.select(
#                     [socket_obj1, socket_obj2, socket_obj3, ], [socket_obj1, socket_obj2, socket_obj3, ], [], 0.05
#                      )
#
#         r = [socket_obj1, ]  # socket_obj1接收到数据时
#         data = socket_obj1.recv()
#
#         w = [socket_obj1, ]  # socket_obj1连接到服务器端时
#         socket_obj1.send(b"""GET /index HTTP/1.0\r\nHost: baidu.com\r\n\r\n""")
#
# 3.类中定义fileno方法，封装socket，传给select监听(select监听的是具有fileno方法，且返回文件描述符的对象)
#     class Foo:
#         def fileno(self):
#             obj = socket()
#             return obj.fileno()


import socket
import select

# # 一、通过socket发送HTTP请求(阻塞)
#
#
# sk = socket.socket()
#
# # 1.连接(IO阻塞)
# sk.connect(('www.baidu.com',80,))
# print('Connect Success...')
#
# # 2. 连接成功发送消息
# sk.send(b'GET / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\n')
# # sk.send(b'POST / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\nk1=v1&k2=v2')
#
# # 3. 等待服务端响应（IO阻塞）
# data = sk.recv(1024)
# print(data)
#
# # 关闭连接
# sk.close()
#
#
# # 二、通过socket发送HTTP请求(非阻塞)
#
#
# sk = socket.socket()
# sk.setblocking(False)
#
# # 1.连接(非阻塞)，可以再干别的事
# try:
#     sk.connect(('www.baidu.com',80,))
#     print('Connecting...')
# except BlockingIOError as e:
#     print(e)
#
# # 2. 连接成功发送消息（需要添加判断条件，socket连接有返回结果了再发送）
# sk.send(b'GET / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\n')
# # sk.send(b'POST / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\nk1=v1&k2=v2')
#
# # 3. 等待服务端响应（非阻塞）（需要添加判断条件，socket接收到响应了再接收数据）
# data = sk.recv(1024)
# print(data)
#
# # 关闭连接
# sk.close()


# 三、建立非阻塞socket，通过IO多路复用，实现并发请求（异步IO模块）
#
# 实现思路：
# 1.定义HttpRequest类：
#     封装socket对象；
#     定义host、callback属性；
#     定义fileno方法，返回self.socket对象的filno方法
# 2.定义HttpResponse类：
#     通过split对响应数据进行分割并分别赋值给对应属性
# 3.定义AsyncRequest类：
#     1）初始化conn、connection列表（__init__）
#     2）创建非阻塞的socket连接（try），并将sockt对象分别加入conn、connection列表（add_request方法）
#     3）定义事件循环，调用select监听conn、connction；遍历writable；若有w，连接成功，调用send发送HTTP请求；在connection中删除w；\
#     遍历readable；若有r，循环中调用recv接收data（try）；\
#     实例化HttpResponse进行数据分割并将结果赋值给response；调用callback传入response处理响应数据；\
#     调用close；在conn中删除r
# 4.创建AsyncRequest实例req，定义url_list（host、callback），遍历url_list，调用req的add_request方法（传入host、callback）创建请求
# 5.调用req的run方法
#
# ==>对于使用者是异步的（传入url、callback可以在IO请求结束自动执行回调），但模块本身不是异步的（非阻塞socket+IO多路复用-select）


class HttpRequest:
    def __init__(self, sk, host, callback):
        self.socket = sk
        self.host = host
        self.callback = callback

    def fileno(self):
        return self.socket.fileno()


class HttpResponse:
    def __init__(self, recv_data):
        self.recv_data = recv_data
        self.header_dict = {}
        self.body = None

        self.initialize()

    def initialize(self):
        headers, body = self.recv_data.split(b'\r\n\r\n', 1)
        self.body = body
        header_list = headers.split(b'\r\n')
        for h in header_list:
            h_str = str(h,encoding='utf-8')
            v = h_str.split(':',1)
            if len(v) == 2:
                self.header_dict[v[0]] = v[1]


class AsyncRequest:
    def __init__(self):
        self.conn = []
        self.connection = [] # 用于检测是否已经连接成功

    def add_request(self, host, callback):
        try:
            sk = socket.socket()
            sk.setblocking(False)
            sk.connect((host, 80))
        except BlockingIOError as e:
            print(e)

        request = HttpRequest(sk, host, callback)
        self.conn.append(request)
        self.connection.append(request)

    def run(self):
        while True:
            readable, writable, error = select.select(self.conn, self.connection, self.conn, 0.05)
            for w in writable:
                print(w.host, '连接成功...')
                # 只要循环中取到w，表示socket和服务器端已经连接成功

                request_header = "GET / HTTP/1.0\r\nHost:{0}\r\n\r\n".format(w.host,)
                w.socket.send(bytes(request_header, encoding='utf-8'))

                self.connection.remove(w)

            for r in readable:
                # 只要循环中取到r,表示socket中有数据可读（HttpRequest对象）
                recv_data = bytes()
                while True:
                    try:
                        chunk = r.socket.recv(2048)
                        recv_data += chunk
                    except Exception as e:
                        break

                response = HttpResponse(recv_data)
                r.callback(response)

                r.socket.close()
                self.conn.remove(r)

            # windows中conn为空会报错
            if len(self.conn) == 0:
                break


def f1(response):
    print('保存到文件', response.header_dict)


def f2(response):
    print('保存到数据库', response.header_dict)


url_list = [
    {'host':'www.baidu.com','callback': f1},
    {'host':'cn.bing.com','callback': f2},
    {'host':'www.cnblogs.com','callback': f2},
]


req = AsyncRequest()
for item in url_list:
    req.add_request(item['host'], item['callback'])

req.run()





