__author__ = 'shy'
__date__ = '2018/3/19 15:28'

import pika

# step1:connection
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

# step2:create channel
channel = connection.channel()

# step3:declare queue
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))


# step4:consume msg
print('[*] Waiting for messages. To exit press CTRL+C')
channel.basic_consume(callback,
                      queue='hello',
                      # 未设定消息确认
                      no_ack=True)

# step5:start consuming
channel.start_consuming()
