#!/usr/bin/env python3

import pika
import sys

message = ' '.join(sys.argv[1:])

if 'new' in message:
    connection = pika.BlockingConnection( pika.ConnectionParameters(host='localhost') )

    channel = connection.channel()

    message=' '.join(sys.argv[1:])
    channel.queue_declare(queue='main_queue')
    channel.basic_publish(exchange='', routing_key='main_queue', body=message)
    print("[x] Sent %r" % message)
    connection.close()

else:
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(" [x] Sent %r" % message)
    connection.close()


#     print('haha')
#     channel.exchange_declare(exchange='logs', exchange_type='fanout')
#     channel.basic_publish(exchange='logs', routing_key='', body=message)


# connection.close()

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='main_queue')

# channel.basic_publish(exchange='', routing_key='main_queue', body='Hello World!')
# print(" [x] Sent 'Hello World!'")
# connection.close()