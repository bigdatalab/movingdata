#!/usr/bin/env python
#
# The core pre-deployment and execution engine
#
# Copyright (c) 2013 by Michael Luckeneder
#
import itertools as it
import sys
import traceback
from prettytable import PrettyTable
from operator import itemgetter
from dag.digraph import *
from dag.edge import *
import connection_factory
from geo import geo_locate as geo
from urlparse import urlparse

geolocate_cache = dict()


def geolocate(urls):
    """Caches geolocation queries"""
    global geolocate_cache
    return geo.find_distance_between_ips(urls[0], urls[1])


def handle_empty_item(item):
    """Handles faulty return values from SSH calls"""
    try:
        return float(item)
    except:
        return float(999999)


def create_vertices(sl):
    """Creates a list of vertices from a list or single String"""
    if isinstance(sl, list):
        return [Vertex(x) for x in sl]
    else:
        return Vertex(sl)


def flatten(foo):
    """Flattens a list of lists"""
    for x in foo:
        if hasattr(x, '__iter__'):
            for y in flatten(x):
                yield y
        else:
            yield x


class PreDeployer(object):
    """Handles pre-deployment analysis and execution"""
    def __init__(self, workflow):
        """Initializes pre-deployer"""
        self.conn = connection_factory.make_connection()
        self.workflow = workflow
        self.workflow.set_connection(self.conn)

        self.workflow_hosts = self.workflow.get_workflow_hosts()

    def calculate_distance(self, distance_function, aws, workflow_vertices):
        """Builds candidate graph for a certain metric"""

        # initialize DAG
        dag = DirectedGraph()

        # sentinel - needed for complex workflows
        sentinel = Vertex("---")

        # iterate over pairs of AWS and web service nodes
        for index, i in enumerate(it.izip(workflow_vertices, workflow_vertices[1:])):

            # create AWS vertex
            aws_vertex = Vertex(aws.url())

            # account for 'fanned' workflow layout
            if isinstance(i[0], list):
                for j in i[0]:

                    # build edge with weight
                    e = Edge(j, aws_vertex)
                    e.weight = distance_function((j.name, aws_vertex.name))
                    dag.add_edge(e)

                    if index == 0:
                        e2 = Edge(sentinel, j)
                        e2.weight = 0
                        dag.add_edge(e2)
            else:
                e1 = Edge(i[0], aws_vertex)
                e1.weight = distance_function((i[0].name, aws_vertex.name))
                dag.add_edge(e1)

            # account for 'fanned' workflow layout
            if isinstance(i[1], list):
                for j in i[1]:

                    # build edge with weight
                    e = Edge(aws_vertex, j)
                    e.weight = distance_function((j.name, aws_vertex.name))
                    dag.add_edge(e)
            else:
                e2 = Edge(aws_vertex, j)
                e2.weight = distance_function((j.name, aws_vertex.name))
                dag.add_edge(e2)

        return dag.calculate_least_cost()

    def analyze_workflow(self):
        """Analyze a workflow"""
        self.init()

        # flatten list
        flat_workflow_hosts = flatten(self.workflow_hosts)

        # filter localhost and uniquify list
        hosts = list(set(filter(lambda x: (not "localhost" in x), map(lambda x: x, flat_workflow_hosts))))

        # containers for ping and rtt results
        pings = {}
        rtts = {}

        # iterate over hosts
        for h in hosts:
            # extract hostname
            host = urlparse(h).netloc.split(":")[0]

            # gather RTT metrics
            try:
                rtts[h] = self.conn.invoke_ssh("curl -w '%%{time_total}' -o /dev/null/ -s %s" % (h))
            except:
                rtts[h] = float(999999)

            # gather ping metrics
            try:
                pings[h] = self.conn.invoke_ssh("ping -c 5 %s | tail -1| awk '{print $4}' | cut -d '/' -f 2" % (h))
            except:
                pings[h] = float(999999)

        distances = {}
        distances['ping'] = dict()
        distances['geo'] = dict()
        distances['rtts'] = dict()

        distances['combination'] = dict()

        aws_locations = self.conn.get_instances().values()

        for aws in aws_locations:
            workflow_vertices = map(create_vertices, self.workflow_hosts)

            # calculate candidate graph distances
            distances['geo'][aws.url()] = self.calculate_distance(geolocate, aws, workflow_vertices)
            distances['ping'][aws.url()] = float(self.calculate_distance(lambda x: handle_empty_item(pings[x[0]][x[1]]), aws, workflow_vertices))
            distances['rtts'][aws.url()] = float(self.calculate_distance(lambda x: handle_empty_item(rtts[x[0]][x[1]]), aws, workflow_vertices))

            # calculate (\sum{RTT}+\sum{pings})/2
            distances['combination'][aws.url()] = (distances['ping'][aws.url()]*1000 + distances['rtts'][aws.url()])/2
        return distances

    def init(self):
        """Initializes the pre-deployer"""
        # initialize the connection
        self.conn.start()

    def cleanup_regions(self):
        """Cleans up all regions - i.e. terminates all instances in all regions"""
        self.conn.terminate_all_instances()

    def run_workflow(self, regions=[]):
        """runs/orchestrates the workflow remotely"""

        # initialize workflow
        self.init()
        self.workflow.init(self.conn)

        results = {}
        # retrieve list of regions
        conn_regions = self.conn.get_instances()

        # filter regions
        if regions:
            regions = {k: conn_regions[k] for k in regions}
        else:
            regions = conn_regions

        # run workflow in every region
        for r, i in regions.iteritems():
            print i
            results[i.url()] = self.workflow.run(i)

        return results

