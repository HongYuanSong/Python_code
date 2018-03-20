__author__ = 'shy'
__date__ = '2018/3/19 17:23'

import pika
import uuid


class FibRPCClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)

        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, queue=self.callback_queue)

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            # 建立进程事件循环，监听返回结果
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibRPCClient()

print("[x] Requesting fib(5)")

response = fibonacci_rpc.call(5)
print("[.] Got %r" % (response,))