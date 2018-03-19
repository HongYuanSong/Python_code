__author__ = 'shy'
__date__ = '2018/3/19 17:23'

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def fib(n):
    if n in (0, 1):
        return 1
    first, second = 1, 1
    while n > 2:
        first, second = second, first + second
        n -= 1
    return second


def on_request(ch, method, properties, body):
    n = int(body)
    response = fib(n)
    print("[.] fib(%s)=%s" % (n, response))

    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id= properties.correlation_id),
                     body=str(response))

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print("[x] Awaiting RPC requests")

channel.start_consuming()