__author__ = 'shy'
__date__ = '2018/3/19 17:03'

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

# 配置severities获取方式(加入.作为分割符，可以匹配更多表现形式),同时支持特殊字符*：任意一个单词、特殊字符#：0个或者多个单词
severities = sys.argv[1:]

if not severities:
    print(sys.stderr, "Usage: %s [xxx.info]" % (sys.argv[0],))
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=severity)

print('[*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print("[x] %r:%r" % (method.routing_key, body,))


channel.basic_consume(callback,
                      queue=queue_name)

channel.start_consuming()