#!/usr/bin/env python3

import pika
from multiprocessing import Process
import random
import time

MAX_NUM=2**32

def boot():
	# gera num do id
	nodeid=random.randint(0, MAX_NUM)

	# msg q ele vai enviar pro broker
	# no caso eu to tentando fazer o processo dele publicar o id do seu noh para o broker
	message=f"Nodeid: {nodeid}"

	# conecta no rabbitmq
	connection = pika.BlockingConnection(
    	pika.ConnectionParameters(host='rabbitmq'))
	channel = connection.channel()

	channel.exchange_declare(exchange='logs', exchange_type='fanout')

	result = channel.queue_declare(queue='', exclusive=True)
	queue_name = result.method.queue

	channel.queue_bind(exchange='logs', queue=queue_name)

	time.sleep(2.5)

	# publica msg em todas as filas (routing_key='')
	channel.basic_publish(exchange='logs', routing_key='', body=message)
	
	time.sleep(2.5)
	#print(f'[*] {queue_name} is waiting for logs. To exit press CTRL+C')

	channel.basic_consume(
    	queue=queue_name, on_message_callback=callback, auto_ack=True)

	channel.start_consuming()

	# pega msg da fila
	#mf, hf, body = channel.basic_get(queue=queue_name, auto_ack=True)
	#if mf:
	#	print(body)

	# fecha conexao
	connection.close()

def callback(ch, method, properties, body):
	print(f"I  recieved", body)

random.seed()

jobs=[]
for i in range(8):
	p=Process(target=boot)
	jobs.append(p)
for job in jobs:
	job.start()
for finishedjob in jobs:
	finishedjob.join()

