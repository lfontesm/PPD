#!/usr/bin/env python3

import pika
import random
import time

MAX_NUM=2**10

connection = pika.BlockingConnection( pika.ConnectionParameters(host='rabbitmq') )

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

random.seed()

# Puts
for i in range(MAX_NUM//2):
    num = random.randint(0, MAX_NUM)
    message=f'{num}, new message -> {num}'

    channel.basic_publish(exchange='logs', routing_key='', body=message)

# Gets
for i in range(MAX_NUM//2):
    num = random.randint(0, MAX_NUM)
    message=f'{num}'

    channel.basic_publish(exchange='logs', routing_key='', body=message)

time.sleep(1)

channel.basic_publish(exchange='logs', routing_key='', body="print")

connection.close()
