#!/usr/bin/env python3

import random
import pika
import sys

# from dht import MAX_NUM
MAX_NUM = 2**4

message = ' '.join(sys.argv[1::])
random.seed()

connection = pika.BlockingConnection( pika.ConnectionParameters(host='localhost') )
channel = connection.channel()

if 'new' in message:
    channel.queue_declare(queue='main_queue')
    channel.basic_publish(exchange='', routing_key='main_queue', body=message)
    connection.close()

else:
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    if 'put' in message:
        msgTmp = message.split(" ")
        number = random.randint(0, MAX_NUM)
        message = msgTmp[0] + " " + str(number) + " " + msgTmp[1]

    channel.basic_publish(exchange='logs', routing_key='', body=message)
    connection.close()

print(" [x] Sent %r" % message)

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