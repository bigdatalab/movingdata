#!/usr/bin/env python
#
# Runs the IEEE example workflow
#
# Copyright (c) 2013 by Michael Luckeneder
#

import sys
import os
import time
start_time = time.time()

files = []
i = 0

# download images from wikimedia several times
while True:
    if i >= int(sys.argv[1]):
        break
    else:
        i += 1

    file = "./temp/"+str(time.time())
    os.system("/usr/bin/env curl http://upload.wikimedia.org/wikipedia/commons/2/28/Keri_majakas.jpg > %s" % (file+".0.jpg"))
    files.append(file)

# parse workflow text
workflow = sys.argv[2].split(",")
l = range(len(workflow)+1)
allocation = zip(l, l[1:])

# execute workflow
for f in files:
    f0 = (file+".0.jpg")
    for i, a in enumerate(allocation):
        f1 = f+"."+str(a[1])+".jpg"

        c = "/usr/bin/env curl -X POST -F file=@%s %s > %s" % (f0, workflow[i], f1)
        os.system(c)

# calculate and display total run time
print str(time.time() - start_time)
