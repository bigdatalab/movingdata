#
# Represents multiple EC2 regions
#
# Copyright (c) 2013 by Michael Luckeneder
#

import sys
import multiprocessing
import config
from ec2_region import *


def start_worker(i):
    """Starts an asynchronous worker"""
    i.start()


class EC2MultiRegionConnection(object):
    """Manages instances in multiple EC2 regions"""

    def __init__(self):
        """Set up EC2 regions"""
        self.amis = config.AMIS

        # set up multithreading
        manager = multiprocessing.Manager()
        self.results = multiprocessing.Queue()
        self.regions = dict()

        # define EC2 regions
        for region, ami in self.amis.iteritems():
            self.regions[region] = EC2Region(region, ami)

    def start(self):
        """Launch instances in all regions"""
        workers = []
        # iterate over regions
        for i in self.regions.values():

            # start instances asynchronously
            i.start()
            worker = multiprocessing.Process(target=i.wait_for_running)
            worker.start()
            workers.append(worker)

        # wait for all instances to start
        for w in workers:
            w.join()

    def terminate(self):
        """Terminate instance"""
        for r in self.regions.values():
            print >> sys.stderr, "Instance %s terminated" % (r.url())
            r.terminate()

    def get_instances(self):
        """Returns a list of instances"""
        return self.regions

    def terminate_all_instances(self):
        """Terminate all instances in all regions"""
        for r in self.regions.values():
            r.terminate_all()

    def invoke_ssh(self, cmd, regions=[]):
        """Invoke SSH command in all or a subset of regions handled"""
        result = {}

        # if regions attribute is specified, only invoke command on these regions
        if regions:
            regions = {k: self.regions[k] for k in regions}
        else:
            regions = self.regions

        # invoke command on all or specified regions
        for region, i in regions.iteritems():
            result[i.url()] = i.invoke_ssh(cmd=cmd)

        return result

    def upload_file(self, localfile, remotefile):
        """Uploads file to all instances using SCP"""
        regions = self.regions

        for region, i in regions.iteritems():
            i.upload_file(localfile, remotefile)
