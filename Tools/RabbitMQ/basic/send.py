__author__ = 'shy'
__date__ = '2018/3/19 15:27'

import pika


# step1:connection
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

# step2:create channel
channel = connection.channel()

# step3:declare queue
channel.queue_declare(queue='hello')

# step4:publish msg
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print("[x] Sent 'Hello World!'")

# step5:close connection
connection.close()
