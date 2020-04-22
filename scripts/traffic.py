#!/usr/bin/python

import time
import urllib
import random
i=1

while True:
    i=i+1
    time.sleep(random.randrange(0,10))

    url = 'http://0.0.0.0:5050/api/trace'
    nw_source = urllib.urlopen(url).read()
    url2='http://0.0.0.0:5050'
    nw_source2 = urllib.urlopen(url2).read()

    print i
    if i>1000:
        break
