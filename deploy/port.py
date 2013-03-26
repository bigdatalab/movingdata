# 
# Checks if a specific port is reachable on an IP/host
#
# Copyright (c) 2013 by Michael Luckeneder
#

import socket

def scan_server(address, port):
	"""Checks for a reachable port on an IP/host"""
    s = socket.socket()
    
    try:
        s.connect((address,port))
        return True
    except socket.error, e:
        return False


