#!/usr/bin/env python
from pprint import pprint
from myapi import api

# board lists - containers for boards 
brdlst=[brdlst['id'] for brdlst in api.DashboardList.get_all()['dashboard_lists']]

# boards in a board boardlist 0
brds=api.DashboardList.get_items(brdlst[0])['dashboards']

# timeboards in a board 0
graphs=api.Timeboard.get(brds[0]['id'])['dash']['graphs']

#['dash']
pprint (graphs)

