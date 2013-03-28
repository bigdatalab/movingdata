#!/usr/bin/env python
#
# Invokes the pre-deployment analysis for the IEEE workflow
#
# Copyright (c) 2013 by Michael Luckeneder
#

from ieee_test_workflow import *
from pre_deployer import PreDeployer
import traceback
import sys
from display_metrics import *

try:
    # load workflow specification filename and regions
    fname = sys.argv[1]
    region = sys.argv[2].split(",")

    # initialize workflow
    wf = IEEETestWorkflow("../ieee/inputs/%s" % (fname))

    # redirect STDOUT
    sys.stdout = open("../ieee/outputs/%s_output" % (fname), "w")

    # initialize pre_deployer
    pre = PreDeployer(wf)

    # run workflow
    wf_results = pre.run_workflow(region)

    # display execution time
    print display_metrics(wf_results, "exec time")


except Exception as e:
    # print stack trace
    print traceback.format_exc()
finally:
    # ensure that all instance are terminated
    pre.cleanup_regions()
