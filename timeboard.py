#!/usr/bin/env python

from datadog import initialize, api
from datadog.api.constants import CheckStatus
from pprint import pprint as pp


options = {'api_key': '31c27cf5e8049caa99b81d4e152e3550',
           'app_key': '196dbbff93b320f9fb788e22ea05d1978c15c253'}

initialize(**options)

check = 'app.k'
host = 'app1'
status = CheckStatus.OK  # equals 0
tags = ['env:test']

res = api.ServiceCheck.check(check=check, host_name=host, status=status,
                       message='Response: 200 OK', tags=tags)

pp(res)


title = "Vsanz Timeboard"
description = "The timeboard exercise in  Visualizing Data section."
graphs = [
{
    "definition" :{
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:nuevecuatrouno.cloud}"}
        ],
        "viz": "timeseries"
    },
    "title": "My metric"
},
{
    "definition" :{
        "events": [],
        "type" : "metric alert",
        "requests": [
            {"q":
             "avg:mysql.net.connections{host:nuevecuatrouno.cloud}"}
        ],
        "viz": "timeseries"
    },
    "title": "Database Anomaly"
},
{
    "definition" :{
        "events": [],
        "requests": [
            {"q": "abs(sum:my_metric{*}.rollup(avg, 60))"}
        ],
        "viz": "timeseries"
    },
    "title": "My metric with rolloup"
}
]

template_variables = [{
}]

read_only = True
res = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
pp(res)

#print res['dash']['id']

#{
#    "definition" :{
#        "events": [],
#        "type" : "metric alert",
#        "requests": [
#            {"q": "avg(last_5m):sum:system.net.bytes_rcvd{host:host0} > 100"}
#        ],
#        "viz": "timeseries"
#    },
#    "title": "Database Anomaly"
#},

#api.Monitor.create(
#    type="metric alert",
#    query="avg(last_5m):sum:system.net.bytes_rcvd{host:host0} > 100",
#    name="Bytes received on host0",
#    message="We may need to add web hosts if this is consistently high.",
#    tags=tags,
#    options=options
#)

