#!/usr/bin/env python3

from cll import *

class DHTNode:
	def __init__(self, lo, hi, nodeid):
		self.lo=lo
		self.hi=hi
		self.nodeid=nodeid
	def __repr__(self):
		return "DHTNode()"
	def __str__(self):
		return "Node %d is responsible for the range: %d->%d" % (self.nodeid, self.lo, self.hi)

MAX_NUM=1000

def get_range_list(max_num):
	rangelist=[]
	increment=hi=max_num//8
	lo, hi = 0, hi
	while hi <= max_num:
		rangelist.append( (lo, hi) )
		lo=hi
		hi+=increment
	return rangelist
	

a = DHTNode(100, 200, 1)
cll = CLL()

print(a.lo, a.hi, a.nodeid)
rlist=get_range_list(MAX_NUM)
print(rlist)

for index, rangetuple in enumerate(rlist):
	n = DHTNode(rangetuple[0], rangetuple[1], index)
	cll.append(n)
#	print(rangetuple[0])



cll.display()
