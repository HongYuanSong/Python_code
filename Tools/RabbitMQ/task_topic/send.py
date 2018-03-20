__author__ = 'shy'
__date__ = '2018/3/19 17:03'

import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         # 有条件的组播形式发送消息到指定队列
                         exchange_type='topic')

# 配置severity获取方式(加入.作为分割符，可以匹配更多表现形式)
severity = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'

message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='topic_logs',
                      routing_key=severity,
                      body=message)

print("[x] Sent %r:%r" % (severity, message))

connection.close()