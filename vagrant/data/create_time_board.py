from datadog import initialize, api

options = {
    'api_key': '9c0cb7a55b78e7f90723f91defeb6f5d',
    'app_key': 'e8a20d49949bc3a41c768c2c5ef62aced91d28fb'
}

initialize(**options)

title = "Data Visualisation"
description = "This is a data visualisation exercise."

graphs = [{
    "definition" : {
        "events" : [],
        "requests" : [{"q": "avg:my_metric{host:vagrant}"}],
        "viz" : "timeseries"
        },
    "title" : "my_metric average scoped overthe host"
    },{ 
    "definition" : {
        "events" : [],
        "requests" : [{"q" : "avg:my_metric{*}.rollup(sum, 3600)"}],
        "viz" : "query_value"
        },
    "title" : "my_metric rollup sum over an hour"
    },{
    "definition" : {
        "events" : [],
        "requests": [{"q": "anomalies(avg:postgresql.rows_returned{*}, 'basic', 2)"}],
        "viz" : "timeseries"
        },
    "title" : "Database anomoly for postgresql.rows_returned"
    }]
      
template_variables = [{
        "name" : "host1",
        "prefix" : "host",
        "default" : "host:my-host"
    }]

read_only = True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)