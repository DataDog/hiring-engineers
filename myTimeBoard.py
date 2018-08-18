#Configure the module according to your needs
from datadog import initialize , api

options = {
    'api_key':'aad675abc709aa6422cc19ee7c881a5b',
    'app_key':'e2af02692da4b07919b74d4a6c4d893ef4471577'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "mycustom metric"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.com_select{*}, 'basic', 1)"}
        ],
        "viz": "timeseries"
    },
    "title": "MYSQL Anomalies"
    

},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my custom metric rollup by 1h"
    

}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)