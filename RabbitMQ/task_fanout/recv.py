__author__ = 'shy'
__date__ = '2018/3/19 16:01'

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# 配置临时队列，server关闭后自动删除
result = channel.queue_declare(exclusive=True)

# 获取队列名，例如：amq.gen-JzTY20BRgKO-HjmUJj0wLg
queue_name = result.method.queue

# 绑定exchange和queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)


def callback(ch, method, properties, body):
    print("[x] %r" % (body,))
    ch.basic_ack(delivery_tag=method.delivery_tag)


print('[*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(callback,
                      queue=queue_name)

channel.start_consuming()
