# 
# Geolocates a URL using ipinfodb.com
#
# Copyright (c) 2013 by Michael Luckeneder
#

import config
import time
import urllib2
import socket
import re
import subprocess as sub
import geo_calc

def locate(ip=""):
    """Find the coordinates of an IP"""
    
    if ip and ip != "localhost":
        query_string = "&ip=%s" % str(socket.gethostbyname(ip))
    else:
        query_string = ""
        
    f = urllib2.urlopen("http://api.ipinfodb.com/v3/ip-city/?key=%s%s" % (config.IPINFODB_API_KEY,query_string))
    data = f.read()
    
    status, body = data.split(";;")
    
    if status=="OK":
        geoinfo = body.split(";")
        state,city = geoinfo[3:5]
        lat,lng = geoinfo[6:8]
    else:
        pass

    f.close()
        
    
    return (float(lng),float(lat),(city,state))
    

    
def find_distance_to_ip(destination):
    """Find geographical distance from current location to IP"""
    return find_distance_between_ips("",destination)
    
    
def find_distance_between_ips(one,other):
    """Find geographical distance between two IPs"""
    one = locate(one)
    other = locate(other)
    
    coordinates_one = geo_calc.xyz(one[0],one[1])
    coordinates_other = geo_calc.xyz(other[0],other[1])

    return int(geo_calc.distance(coordinates_one,coordinates_other))
    

def find_latency_to_ip(destination):
    """Uses ping to find latency from current host to destination IP"""
    p = sub.Popen(["ping","-c","10",socket.gethostbyname(destination)],stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()

    # extract info from ping output
    matcher = re.compile(r'(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)')
    return float(matcher.search(output).groups()[1])

def find_http_rtt_to_ip(destination):
    """Find HTTP RTT latency from current host to destination IP"""
    import requests
    from requests.exceptions import HTTPError

    start_time = time.time()
    for i in xrange(10):
        try:
            r = requests.get("http://"+destination)
            r.raise_for_status()
        except HTTPError:
            pass

    return (time.time() - start_time)*1000/5
    