#!/usr/bin/env python
from pprint import pprint
from myapi import api

# monitors
mntrs=api.Monitor.get_all()
# my custom monito
pprint (mntrs[1])

#pprint (api.Monitor.search(query="metric:my_metric"))

