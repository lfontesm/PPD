#!/usr/bin/env python3

import pika
import sys

connection = pika.BlockingConnection( pika.ConnectionParameters(host='rabbitmq') )

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message=' '.join(sys.argv[1:])
channel.basic_publish(exchange='logs', routing_key='', body=message)

print("[x] Sent %r" % message)

connection.close()
