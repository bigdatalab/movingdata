# 
# Represents the IEEE test workflow
#
# Copyright (c) 2013 by Michael Luckeneder
#

from workflow.abstract_workflow import AbstractWorkflow
import sys
import random
from time import time
from urlparse import urlparse

def generate_output(a):
    """returns the host part of a url"""
    u = urlparse(a)
    host = u.netloc.split(":")[0]
    return host


class IEEETestWorkflow(AbstractWorkflow):
    """Represents the IEEE workflow"""
    def __init__(self,workflow_file):
       """Initialize the workflow class"""
        f = open(workflow_file).read()
        endpoints = f.split("\n")

        self.workflow = endpoints
        self.output = ['upload.wikimedia.org'] + map(generate_output,self.workflow)
        self.fname = int(time())
        



    def init(self,conn):
        """Initialize the workflow; copy workflow execution file to server"""
        print >> sys.stderr, "Initializing workflow"
        conn.upload_file("./ieee-workflow/ieee.py", "ieee.py")
        conn.invoke_ssh("mkdir temp")

    def run(self,conn):
        """Run the workflow"""
        return conn.invoke_ssh("python ieee.py 4 %s" % (",".join(self.get_endpoints())))

    def get_workflow_hosts(self):
        """Extract workflow endpoint URLs"""
        return self.output

    def get_endpoints(self):
        """Extract workflow hosts"""
        return self.workflow
