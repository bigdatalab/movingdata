# 
# Represents a directed graph
#
# Copyright (c) 2013 by Michael Luckeneder
#

from edge import *
from vertex import *
from collections import OrderedDict

class DirectedGraph(object):
    """Represents a directed graph (DAG)"""
    def __init__(self):
        """Initialize DAG"""
        self.E = OrderedDict()
        self.V = list()
    
    def add_edge(self, edge):
        """Add an edge to DAG"""
        self.E[edge.begin] = edge

    def calculate_least_cost(self):
        """Calculate the total cost of the graph"""
        v = self.E.keys()[0]

        total_weight = 0

        # iterate over edges and sum edge weight
        for k,e in self.E.iteritems():
            total_weight += e.weight

        return total_weight
