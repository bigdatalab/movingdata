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