__author__ = 'shy'
__date__ = '2018/3/23 17:23'


import socketserver
import struct
import json
import os


class FtpServer(socketserver.BaseRequestHandler):
    coding = 'utf-8'

    max_packet_size = 1024

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SERVER_DIR = {'put': 'file_upload'}

    def handle(self):
        # print(self.request)
        while True:
            # 接收头文件长度
            head = self.request.recv(4)
            head_len = struct.unpack('i', head)[0]

            if not head:
                break

            # 接收头文件
            head_json = self.request.recv(head_len).decode(self.coding)
            head_dic = json.loads(head_json)
            # print(head_dic)

            cmd = head_dic['cmd']
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(head_dic)

    def put(self, args):
        file_path = os.path.normpath(os.path.join(
            self.BASE_DIR,
            self.SERVER_DIR[args['cmd']],
            args['file_name']
        ))

        # 保存文件
        file_size = args['file_size']
        received_size = 0
        # print(file_path)

        with open(file_path, 'wb') as f:
            while received_size < file_size:
                received_data = self.request.recv(self.max_packet_size)
                f.write(received_data)
                received_size += len(received_data)
                print('received_size:{0} file_size:{1}'.format(received_size, file_size))


if __name__ == '__main__':

    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), FtpServer)
    server.serve_forever()