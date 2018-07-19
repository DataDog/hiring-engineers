from datadog import initialize, api

options = {
   'api_key': '6b6a115b9b59143d541f0d4defc98151',
   'app_key': '4868ee1447ad0185bd0db86ade32416d74554527'
}

initialize(**options)

title = "Visualizing Data Timeboard"
description = "Timeboard containing three metrics for the Hiring Solutions Engineer Exercise"
graphs = [{
   "definition": {
       "events": [],
       "requests": [{"q":"avg:my_metric{host:ubuntu-xenial}"}],
       "viz": "timeseries"
   },
   "title": "my_metric vs time" },
   {
   "definition": {
       "events": [],
       "requests": [{"q":"anomalies(avg:mysql.performance.cpu_time{host:ubuntu-xenial},'basic', 3)"}],
       "viz": "timeseries"
   },
   "title": "Anomaly function applied to mysql.performance.cpu_time vs time" },
   {
   "definition": {
       "events": [],
       "requests": [{"q":"avg:my_metric{host:ubuntu-xenial}.rollup(avg, 120)"}],
       "viz": "timeseries"
   },
   "title": "Rollup function applied to my_metric vs time"
}]

template_variables = [{
   "name":"ubuntu-xenial",
   "prefix": "host",
   "default": "host:ubuntu-xenial"
}]

read_only = True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
