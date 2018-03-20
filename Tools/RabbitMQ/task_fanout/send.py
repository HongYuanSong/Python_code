__author__ = 'shy'
__date__ = '2018/3/19 16:01'

import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

# declare exchange
channel.exchange_declare(exchange='logs',
                         # 广播形式将消息放到所有队列
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print("[x] Sent %r" % (message,))

connection.close()