#!/usr/bin/env python
#
# Create EC2 connections
#
# Copyright (c) 2013 by Michael Luckeneder
#

from ec2 import ec2_multi_region_connection as mr


def make_connection(t="ec2"):
    """create an EC2 MultiRegion Connection"""
    if t == "ec2":
        return mr.EC2MultiRegionConnection()
