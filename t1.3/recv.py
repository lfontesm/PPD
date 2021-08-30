#!/usr/bin/env python3

import pika
from multiprocessing import Process
import random
import time

MAX_NUM=2**32

def boot():
	########## PROCEDIMENTO PARA QUE TODOS OS NOS ENVIEM SEUS RESPECTIVOS NODEID PARA O BROKER ##########
	# gera num do id
	nodeid=random.randint(0, MAX_NUM)

	# msg q ele vai enviar pro broker
	# no caso eu to tentando fazer o processo dele publicar o id do seu noh para o broker
	message=f"{nodeid}"

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
	########## FIM. ABAIXO DESTA LINHA DEVE ESTAR O PROCEDIMENTO PARA OS NOS RECUPERAREM OS NODEID DA FILA DE MESSAGERIA #########

	# Pega mensagens da fila ate esvaziar
	nodeidlist=[]
	while True:
		mf,pr,body=channel.basic_get(queue=queue_name, auto_ack=True)
		if mf:
			nodeidlist.append(body)
		else:
			break

	# Debug
#	print('am here!')

	# fecha conexao
	connection.close()
	return nodeid, nodeidlist

# Funcao que faz o calculo para saber quais nos sao vizinhos do no atual.
def calculate_neighbors():
	nodeid, nodeidlist=boot()
	
	# Convert the elements in the list to int
	int_nodeidlist=list( map(lambda x: int(x), nodeidlist) )

	# Remove it's own nodeid from list
	int_nodeidlist.remove(nodeid)

	# print(f"{nodeid} -> {int_nodeidlist}")
	# Subtract nodeid from the nodeid list to get the decimal distance from the current node
	# Ex: The decimal distance between 1 and 9 is 8, bcz 9-1=8
	distancelist=list( map(lambda x: x-nodeid, int_nodeidlist) )

	sorted_distancelist=sorted(distancelist, key=abs)

	upperbound=get_first_val(sorted_distancelist)
	lowerbound=get_first_val(sorted_distancelist, positive=False)

	print(upperbound, lowerbound)

	#print(f"Index of upperbound in {nodeid}:", distancelist.index(upperbound))
	#print(f"Index of lowerbound in {nodeid}:", distancelist.index(lowerbound))

	#successor=int_nodeidlist[distancelist.index(upperbound)]
	#predecessor=int_nodeidlist[distancelist.index(lowerbound)]

	#print(f"My successor is {successor} and my predecessor is {predecessor}")


def get_first_val(list_, positive=True):
		for i in list_:
			if positive and i>0:
				return i
			elif not positive and i<0:
				return i


def callback(ch, method, properties, body):
	print(f"I  recieved", body)

random.seed()

jobs=[]
for i in range(8):
	p=Process(target=calculate_neighbors)
	jobs.append(p)
for job in jobs:
	job.start()
for finishedjob in jobs:
	finishedjob.join()

