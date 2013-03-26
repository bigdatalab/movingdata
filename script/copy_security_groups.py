#!/usr/bin/env python

# 
# Copies security groups to all AWS regions
#
# Copyright (c) 2013 by Michael Luckeneder

import config, boto

conn = boto.connect_ec2(config.AWS_ACCESS_KEY, config.AWS_SECRET_KEY)


for g in conn.get_all_security_groups():
    for r in conn.get_all_regions():
        if g.name != "default":
            print "Copying group %s to region %s" %(g.name,r.name)
            g.copy_to_region(r)
        