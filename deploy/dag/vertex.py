# 
# Represents a vertex in a DAG
#
# Copyright (c) 2013 by Michael Luckeneder
#

class Vertex(object):
    """Represents a vertex in a DAG"""
    def __init__(self, name):
        """Initialize the vertex"""
        self.name = name
        
    def __str__(self):
        """Returns String representation of vertex"""
        return self.name

