"""Represents a directed graph""" 
# Represents a directed graph
#
# Copyright (c) 2013 by Michael Luckeneder
#

from dag.edge import Edge
from dag.vertex import Vertex
from collections import OrderedDict

class DirectedGraph(object):
    """Represents a directed graph (DAG)"""
    def __init__(self):
        """Initialize DAG"""
        self.edges = OrderedDict()
        self.vertices = list()
    
    def add_edge(self, edge):
        """Add an edge to DAG"""
        self.edges[edge.begin] = edge

    def calculate_least_cost(self):
        """Calculate the total cost of the graph"""

        total_weight = 0

        # iterate over edges and sum edge weight
        for start, edge in self.edges.iteritems():
            total_weight += edge.weight

        return total_weight
