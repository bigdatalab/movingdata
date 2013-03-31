#
# Prettifies metrics output
#
# Copyright (c) 2013 by Michael Luckeneder
#

def display_metrics(metrics, title):
    """Prettify metrics output"""
    x = PrettyTable(["EC2 endpoint", title])
    x.align="l"
    
    for k,v in sorted(metrics.items(), key=itemgetter(1)):
        x.add_row([k,str(v)])
    return x.get_string()