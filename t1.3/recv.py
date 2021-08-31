#!/usr/bin/env python3

import pika
from multiprocessing import Process
import random
import time

MAX_NUM=2**10
PROCESS_NUM=4
HASH_TABLE={}
NODEID=-1

def join():
	########## GENERATES NODEID AND SENDS IT TO BROKER ##########
	# gerenates a random id
	global NODEID
	NODEID=random.randint(0, MAX_NUM)

	# message that will be sent to broker
	message=f"{NODEID}"

	# connects to rabbitmq
	connection = pika.BlockingConnection(
    	pika.ConnectionParameters(host='rabbitmq'))
	channel = connection.channel()

	channel.exchange_declare(exchange='logs', exchange_type='fanout')

	result = channel.queue_declare(queue='', exclusive=True)
	queue_name = result.method.queue

	channel.queue_bind(exchange='logs', queue=queue_name)

	time.sleep(2.5)

	# publishes the message to all queues (routing_key='')
	channel.basic_publish(exchange='logs', routing_key='', body=message)
	
	time.sleep(2.5)

	########## DONE. BELOW IS THE ROUTINE WHERE WE RETRIEVE THE NODEIDS FROM THE MESSAGE QUEUE #########

	# Get all messages until the queue is empty
	nodeidlist=[]
	while True:
		mf,pr,body=channel.basic_get(queue=queue_name, auto_ack=True)
		if mf:
			nodeidlist.append(body)
		else:
			break

	# Debug
#	print('am here!')

	return NODEID, nodeidlist, (connection, result, channel)

# decides which nodes are the neighbors from the current one
def boot():
	nodeid, nodeidlist, connectioninfo=join()

	# Convert the elements in the list to int
	int_nodeidlist=list( map(lambda x: int(x), nodeidlist) )

	# Check if there are duplicates
	if contains_duplicates(int_nodeidlist):
		print("ABORTING: Duplicate nodes detected")

	# Remove it's own nodeid from list
	int_nodeidlist.remove(nodeid)

	# Check if the current nodeid is either the highest or lowest valu
	if is_outermost_val(nodeid, int_nodeidlist):
		predecessor, successor = max(int_nodeidlist), min(int_nodeidlist)
	else:
		lowerbound_index, upperbound_index = boundaries(int_nodeidlist, nodeid)
		predecessor=int_nodeidlist[lowerbound_index]
		successor=int_nodeidlist[upperbound_index]

	print(f"I'm {nodeid} and my predecessor is {predecessor} and my successor is {successor}")

	start_storing(nodeid, predecessor, connectioninfo)

def start_storing(nodeid, predecessor, connectioninfo):
	connection, result, channel=connectioninfo
	queue_name=result.method.queue

	channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
	
	print("ESTOU PRONTO CAPITAO")
	channel.start_consuming()
	# k, v

	# closes the connection
	connection.close()

def callback(ch, method, properties, body):
	with open("messages.log", "a") as f:
		body=body.decode('utf-8').split(",")
		f.write(f"key:{body[0]}, val:{body[1]}--SIGNED BY: {NODEID}\n\n")


def is_outermost_val(num, list_):
	return num > max(list_) or num < min(list_)

def contains_duplicates(list_):
	for elem in list_:
		if list_.count(elem) > 1:
			return True
	return False

def get_first_val(list_, positive=True):
		for i in list_:
			if positive and i>0:
				return i
			elif not positive and i<0:
				return i

# Returns the predecessor's and successor's index for the current node neighbors list 
def boundaries(list_, nodeid):
	# Subtract nodeid from the nodeid list to get the decimal distance from the current node
	# Ex: The decimal distance between 1 and 9 is 8, bcz 9-1=8
	distance_list=list( map(lambda x: x-nodeid, list_) )

	sorted_distance_list=sorted(distance_list, key=abs)

	lowerbound=get_first_val(sorted_distance_list, positive=False)
	upperbound=get_first_val(sorted_distance_list)

	return distance_list.index(lowerbound), distance_list.index(upperbound)

random.seed()

jobs=[]
for i in range(PROCESS_NUM):
	p=Process(target=boot)
	jobs.append(p)
for job in jobs:
	job.start()
for finishedjob in jobs:
	finishedjob.join()

