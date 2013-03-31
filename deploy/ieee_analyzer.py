#!/usr/bin/env python
#
# Invokes the pre-deployment analysis for the IEEE workflow
#
# Copyright (c) 2013 by Michael Luckeneder
#

from ieee_test_workflow import *
from pre_deployer import PreDeployer
import traceback
from prettytable import PrettyTable
from operator import itemgetter
import pydot
import itertools
import sys


def build_graph(wf, aws, outfile):
    """Generates graphviz graph output"""
    hosts = wf.get_workflow_hosts()

    # load graph
    graph = pydot.Dot(graph_type='graph')
    j = 1
    # iterate over host pairs
    for i in itertools.izip(hosts, hosts[1:]):
        # create nodes
        aws = pydot.Node("AWS"+str(j))
        n1 = pydot.Node(i[0]+"("+str(j)+")")
        j += 1
        n2 = pydot.Node(i[1]+"("+str(j)+")")

        # add edges
        graph.add_edge(pydot.Edge(n1, aws))
        graph.add_edge(pydot.Edge(aws, n2))

    # write graph to output
    graph.write_png(outfile, prog='dot')


try:
    # load workflow specification filename
    fname = sys.argv[1]
    # initialize workflow
    wf = IEEETestWorkflow("../ieee/inputs/%s" % (fname))

    # redirect STDOUT
    sys.stdout = open("../ieee/outputs/%s_pre" % (fname), "w")

    # load pre deployer and generate GraphViz output
    pre = PreDeployer(wf)
    build_graph(wf, pre.conn.get_instances().values(), "../ieee/outputs/%s_graph.png" % (fname))

    # analyze workflow
    distances = pre.analyze_workflow()

    # display metrics
    print display_metrics(distances['geo'], "dist")
    print display_metrics(distances['rtts'], "rtt")
    print display_metrics(distances['ping'], "ping")

    print display_metrics(distances['combination'], "final")


except Exception as e:
    # print stack trace
    print traceback.format_exc()
finally:
    # ensure that all instance are terminated
    pre.cleanup_regions()
