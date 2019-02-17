from datadog import initialize, api
from random import *
import time
options ={
         'api_key': 'a8d19abdc4c005c53685a789ac57d07c',
         'app_key': 'a7ecb7ea0cc4a208ad942e8845fa7bc7cafdca6d'
         }
initialize(**options)

end = int(time.time())
start = end - (5 * 60)
title = "Custom Timeboard"
description = "metrics"
graphs = [
        {
    "definition":{
        "events": [],
        "requests": [

            {"q": "anomalies(avg:mysql.performance.queries{*},'basic', 2)"}
            ],        
        "viz": "timeseries"
          },
    "title": "mysqlmetric"
    },
                {
                "definition":{
                     "events": [],
                     "requests": [

            { "q": "avg:my_metric{host:shruti-VirtualBox}"}
            ],
         "viz": "timeseries"
          },
    "title": "mymetric average"
    },
                {
                "definition":{
        "events": [],
        "requests": [

            {"q": "avg:my_metric{*}.rollup(sum, 60)"}
            ],
        "viz": "timeseries"
        },
    "title": "mymetric rollup"
    }]
template_variables = [{
    "name": "shruti-VirtualBox",
    "prefix": "host",
    "default": "host:shruti-VirtualBox"
    }]
read_only = True
api.Timeboard.create(end=end, start=start, title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

