__author__ = 'shy'
__date__ = '2018/3/19 16:17'

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         # 组播形式发送消息到指定队列
                         exchange_type='direct')
# 配置severity获取方式
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='direct_logs',
                      # 将severity传入的值作为组播参数
                      routing_key=severity,
                      body=message)
print("[x] Sent %r:%r" % (severity, message))

connection.close()
