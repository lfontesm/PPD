#!/usr/bin/env python3

import pika
import random
import time
import os

MAX_NUM = 2**4
global NODEID
global QUEUE_NAME
global NODEID_LIST
NODEID_LIST = []
PREDECESSOR = 1
HASH_TABLE = {}

####### Helper methods to handle the nodes list #######

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


####### DHT logic #######

# Publishes the join message, calculates the node neighbors and defines the callback
def prepare_join(channel, queue_name):
    # Join message
    message = f"{NODEID}"

    # publishes the message to all queues (routing_key='')
    channel.basic_publish(exchange='logs', routing_key='', body=message)

    ########## DONE. BELOW IS THE ROUTINE WHERE WE RETRIEVE THE NODEIDS FROM THE MESSAGE QUEUE #########

    # Get all messages until the queue is empty
    nodeidlist=[]
    while True:
        mf,pr,body=channel.basic_get(queue=queue_name, auto_ack=True)
        if mf:
            nodeidlist.append(body)
        else:
            break

    # Convert the elements in the list to int
    try:
        int_nodeidlist=list( map(lambda x: int(x), nodeidlist) )
    except:
        print(f"Error fetching the nodeid list in {NODEID}")
        exit(1)

    # Remove it's own nodeid from list
    int_nodeidlist.remove(NODEID)

    global NODEID_LIST
    NODEID_LIST=int_nodeidlist

    global PREDECESSOR
    global SUCCESSOR
    # Executes this routine only if node is not the only one in DHT
    if int_nodeidlist:
        # Check if the current nodeid is either the highest or lowest valu
        if is_outermost_val(NODEID, int_nodeidlist):
            predecessor, successor = max(int_nodeidlist), min(int_nodeidlist)
        else:
            lowerbound_index, upperbound_index = boundaries(int_nodeidlist, NODEID)
            predecessor=int_nodeidlist[lowerbound_index]
            successor=int_nodeidlist[upperbound_index]

        PREDECESSOR=predecessor
        SUCCESSOR=successor
    else:
        PREDECESSOR=NODEID
        SUCCESSOR=NODEID

    print(f"I'm {NODEID} with predecessor {PREDECESSOR} and successor {SUCCESSOR}")
    print("\t",NODEID_LIST)

    time.sleep(.5)

    recycle_keys(channel, queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

def killNode(tgt):
    if NODEID == tgt:
        exit(0)

# Calculate responsibility interval
def accept_join(ch):
    ch.stop_consuming()
    queue_name = QUEUE_NAME

    prepare_join(ch, queue_name)

def action_show():
    show = f"I'm {NODEID}. My predecessor is {PREDECESSOR} and my successor is {SUCCESSOR}\n\t"
    show += f"My hash table is {HASH_TABLE}"
    print(show)

def store(key, val):
    print(f"key:{key}, val:{val} -- SIGNED BY: {NODEID}\n")
    HASH_TABLE[key]=val
    print(f"hash table: {HASH_TABLE}\n")

def callback(ch, method, properties, body):
    body=body.decode('utf-8')
    if 'new' in body:
        request_join()
    elif 'join' in body:
        accept_join(ch)
    elif 'show' in body:
        action_show()
    elif 'remove' in body:
        targetNode = int( body.split(" ")[1] )
        if NODEID == targetNode:
            time.sleep(2)
            recycle_keys(ch, QUEUE_NAME)
            exit(1)
        accept_join(ch)
    elif 'put' in body:
        bodyTmp = body.split(" ")
        key = int( bodyTmp[1] )
        val = bodyTmp[2]

        # Checks if the node is the only one in the DHT
        if not NODEID_LIST:
            store(key, val)
            return

        try:
            # Special case in the node is the first from the list
            if NODEID < min(NODEID_LIST) and (key >= PREDECESSOR and key <= MAX_NUM or key >= 0 and key < NODEID):
                store(key, val)
            elif key >= PREDECESSOR and key < NODEID:
                store(key, val)
        except:
            print(f"Error storing new key in {NODEID}")


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

    time.sleep(0.5)

    channel.basic_publish(exchange='logs', routing_key='', body=message)

    channel.queue_bind(exchange='logs', queue=queue_name)
        
    prepare_join(channel, queue_name)

    channel.start_consuming()


def allocate_new_nodeid():
    while True:
        nodeid = random.randint(0, MAX_NUM)

        if nodeid not in NODEID_LIST:
            print(f"New node {nodeid} is joining")
            NODEID_LIST.append(nodeid)
            return nodeid


def recycle_keys(channel, queuename):
    if not HASH_TABLE:
        return

    keys = list( HASH_TABLE.keys() )
    for k in keys:
        message = f"put {k} {HASH_TABLE.pop(k)}"
        print(f"{message}")
        channel.basic_publish(exchange='logs', routing_key='', body=message)
            

def request_join(ch, method, properties, body):
    global NODEID

    NODEID = allocate_new_nodeid()
    if (os.fork() == 0):
        rabbit_connect(NODEID)


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