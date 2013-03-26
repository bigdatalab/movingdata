#!/usr/bin/env python

# 
# Create EC2 connections
#
# Copyright (c) 2013 by Michael Luckeneder
#

from ec2 import ec2_multi_region_connection as mr

# create an EC2 MultiRegion Connection
def make_connection(t="ec2"):
	if t == "ec2":
		return mr.EC2MultiRegionConnection()