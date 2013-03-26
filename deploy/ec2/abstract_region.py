# 
# Represents an abstract EC2 region
#
# Copyright (c) 2013 by Michael Luckeneder
#

from abc import ABCMeta, abstractmethod

class AbstractRegion(object):
    """Represents an abstract EC2 region - this can either be 
    a single region or multiple regions"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """Launch an instance in the region(s)"""
        return

    @abstractmethod
    def terminate(self):
        """Terminate the instances in the region(s)"""
        return

    @abstractmethod
    def invoke_ssh(self):
        """Invoke an SSH command in all instances in the region(s)"""
        return

    @abstractmethod
    def upload_file(self):
        """Upload a file via SFTP"""
        return