#!/usr/bin/env python3

import pika
from multiprocessing import Process
import random
import time
import os

MAX_NUM = 2**4
global NODEID
global QUEUE_NAME
global NODEID_LIST
NODEID_LIST = []
PREDECESSOR = 1
AM_CHILD = False

def is_outermost_val(num, list_):
    return num > max(list_) or num < min(list_)

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

# Calculate responsibility interval
def accept_join(ch, method):
    ch.stop_consuming()
    queue_name = QUEUE_NAME


    message = f"{NODEID}"

    # publishes the message to all queues (routing_key='')
    ch.basic_publish(exchange='logs', routing_key='', body=message)
    
    time.sleep(1)

    ########## DONE. BELOW IS THE ROUTINE WHERE WE RETRIEVE THE NODEIDS FROM THE MESSAGE QUEUE #########

    # Get all messages until the queue is empty
    nodeidlist=[]
    while True:
        mf,pr,body=ch.basic_get(queue=queue_name, auto_ack=True)
        if mf:
            print(f"{NODEID} read from it's queue -> {body}")
            nodeidlist.append(body)
        else:
            break
    
    # Convert the elements in the list to int
    int_nodeidlist=list( map(lambda x: int(x), nodeidlist) )

    # Remove it's own nodeid from list
    print(NODEID, 'and', int_nodeidlist)
    int_nodeidlist.remove(NODEID)

    # Check if the current nodeid is either the highest or lowest valu
    if is_outermost_val(NODEID, int_nodeidlist):
        predecessor, successor = max(int_nodeidlist), min(int_nodeidlist)
    else:
        lowerbound_index, upperbound_index = boundaries(int_nodeidlist, NODEID)
        predecessor=int_nodeidlist[lowerbound_index]
        successor=int_nodeidlist[upperbound_index]

    global NODEID_LIST
    NODEID_LIST=int_nodeidlist

    print(f"{NODEID} my queue is ->", NODEID_LIST)

    global PREDECESSOR
    PREDECESSOR=predecessor

    global SUCCESSOR
    SUCCESSOR=successor

    ch.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # ch.start_consuming()


# def accept_leave():

def callback(ch, method, properties, body):
    body=body.decode('utf-8')
    if 'new' in body:
        request_join()
    elif 'join' in body:
        print('this mf wants to join', end=' ')
        print(body)
        accept_join(ch, method)
    elif 'show' in body:
        print(NODEID_LIST)

def rabbit_connect(nodeid):
    # message that will be sent to broker
    message=f"join {nodeid}"
    
    # connects to rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    global QUEUE_NAME
    QUEUE_NAME = queue_name

    channel.basic_publish(exchange='logs', routing_key='', body=message)
    
    channel.queue_bind(exchange='logs', queue=queue_name)
    
    time.sleep(1)
    
    message = f"{nodeid}"
    # publishes the message to all queues (routing_key='')
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    
    time.sleep(1)

    ########## DONE. BELOW IS THE ROUTINE WHERE WE RETRIEVE THE NODEIDS FROM THE MESSAGE QUEUE #########

    # Get all messages until the queue is empty
    nodeidlist=[]
    while True:
        mf,pr,body=channel.basic_get(queue=queue_name, auto_ack=True)
        if mf:
            print(f"{nodeid} read from it's queue -> {body}")
            nodeidlist.append(body)
        else:
            break

    # Convert the elements in the list to int
    int_nodeidlist=list( map(lambda x: int(x), nodeidlist) )

    # Remove it's own nodeid from list
    int_nodeidlist.remove(NODEID)

    global NODEID_LIST
    NODEID_LIST=int_nodeidlist

    print(f"{NODEID} my queue is ->", NODEID_LIST)

    # Executes this routine only if node is not the only one in DHT
    if int_nodeidlist:
        # Check if the current nodeid is either the highest or lowest valu
        if is_outermost_val(NODEID, int_nodeidlist):
            predecessor, successor = max(int_nodeidlist), min(int_nodeidlist)
        else:
            lowerbound_index, upperbound_index = boundaries(int_nodeidlist, NODEID)
            predecessor=int_nodeidlist[lowerbound_index]
            successor=int_nodeidlist[upperbound_index]

        global PREDECESSOR
        PREDECESSOR=predecessor

        global SUCCESSOR
        SUCCESSOR=successor

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

def allocate_new_nodeid():
    while True:
        nodeid = random.randint(0, MAX_NUM)

        if nodeid not in NODEID_LIST:
            NODEID_LIST.append(nodeid)
            return nodeid

def request_join(ch, method, properties, body):
    global AM_CHILD
    global NODEID

    NODEID = allocate_new_nodeid()

    print(f"New id joining in DHT: {NODEID}")

    print(f'Recieved {body}')
    # gerenates a random id
    # join()
    if (os.fork() == 0):
        AM_CHILD = True
        rabbit_connect(NODEID)

        # join(NODEID)

        print(AM_CHILD)
    else:
        print(AM_CHILD)


# Main loop
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='main_queue')

    channel.basic_consume(queue='main_queue', on_message_callback=request_join, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

random.seed()
main()