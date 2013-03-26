#!/usr/bin/env python
# 
# Automatically generates workflow specifications
#
# Copyright (c) 2013 by Michael Luckeneder
#

import random
import sys
from urlparse import urlparse

# get number of workflow hosts
num = int(sys.argv[1])
# generate random number
i = random.randrange(num,num+1)
# read available nodes
f = open("../eg/planetlab/nodes.txt").read()

# create endpoint URLS
endpoints_hosts = f.split("\n")
endpoints = ["http://"+s+":31415/process" for s in endpoints_hosts]

# random generation with replacement
workflow = [random.sample(endpoints,1)[0] for _ in xrange(i)]

# print workflow to STDOUT
for l in workflow:
	print l