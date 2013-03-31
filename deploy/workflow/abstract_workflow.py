#
# Represents an abstract workflow
#
# Copyright (c) 2013 by Michael Luckeneder
#
from abc import ABCMeta, abstractmethod


class AbstractWorkflow(object):
    """Represents an abstract workflow"""
    __metaclass__ = ABCMeta

    def __init__(self):
        """Initialize workflow"""
        self.conn = None

    def set_connection(self, conn):
        """Inject connection"""
        self.conn = conn

    @abstractmethod
    def init(self, conn):
        """Initialize workflow"""
        return

    @abstractmethod
    def run(self, conn):
        """Execute the workflow"""
        return

    @abstractmethod
    def get_endpoints(self):
        """Extract workflow endpoint URLs"""
        return

    @abstractmethod
    def get_workflow_hosts(self):
        """Extract workflow hosts"""
        return
