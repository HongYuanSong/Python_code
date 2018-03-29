__author__ = 'shy'
__date__ = '2018/3/23 17:23'

import socket
import struct
import json
import os


class TCPClient:
    address_family = socket.AF_INET

    socket_type = socket.SOCK_STREAM

    allow_reuse_address = False

    max_packet_size = 8192

    coding = 'utf-8'

    request_queue_size = 5

    def __init__(self, server_address, connect=True):
        self.server_address = server_address
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)
        if connect:
            try:
                self.client_connect()
            except Exception:
                self.client_close()
                raise

    def client_connect(self):
        self.socket.connect(self.server_address)

    def client_close(self):
        self.socket.close()

    def run(self):
        while True:
            inp = input(">>please input your command(cmd file_path):").strip()
            if not inp: continue
            args = inp.split()
            cmd = args[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(args)
            elif inp == 'exit':
                break
            else:
                print('>>invalid command')

    def put(self, args):
        cmd = args[0]
        file_path = args[1]
        if not os.path.isfile(file_path):
            print('>>file:{0} is not exists'.format(file_path))
            return
        else:
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            # 构建头文件并转json格式（bytes）,将头文件长度通过struct包装成4bit字符
            head_dic = {'cmd': cmd, 'file_name': file_name, 'file_size': file_size}
            # print(head_dic)
            head_json = json.dumps(head_dic)
            head_json_bytes = bytes(head_json, encoding=self.coding)
            head_struct = struct.pack('i', len(head_json_bytes))

            # 先发送头文件长度，再发送头文件
            self.socket.sendall(head_struct)
            self.socket.sendall(head_json_bytes)

            # 发送文件
            send_size = 0
            with open(file_path, 'rb') as f:
                for line in f:
                    self.socket.sendall(line)
                    send_size += len(line)
                    print(send_size)
                else:
                    print('>>upload successful')



if __name__ == '__main__':
    client = TCPClient(('127.0.0.1', 8080))
    client.run()
