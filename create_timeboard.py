from datadog import initialize, api

options = {
    'api_key':'09bfe4731c2e130124847e3dfc01a7d9',
    'app_key':'c937d1279200a7694fcb913ce6a9a497203d9f5f'
}

initialize(**options)

title = "Fernando's Timeboard for the Excersice"

description = "Hopefully got this one right!"

graphs = [{

    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric Over my Host"},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{host:ubuntu-xenial}, 'basic', 2)"}
        ],
        "viz": "query_value"
    },
    "title": "Trying to Detect Anomalies in mySQL"},{
    "definition": {
        "events": [],
        "requests":[
            {"q": "avg:my_metric{*} by {host}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
     },
     "title": "My Metric Rolled Up in 1 Hour Buckets"}             
]

template_variables =[{
    "name": "MyLinuxBox",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

read_only = True

response = api.Timeboard.create(title=title, 
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     ready_only=read_only)


print response
