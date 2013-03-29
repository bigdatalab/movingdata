#
# Represents an edge in a DAG
#
# Copyright (c) 2013 by Michael Luckeneder
#


class Edge(object):
    """Represents an edge in a DAG"""
    def __init__(self, begin, end):
        """Initialize edge"""
        self.begin, self.end = begin, end
        self.weight = 0

    def __str__(self):
        """Returns String representation of edge"""
        return "(%s,%s,%i)" % (self.begin, self.end, self.weight)
