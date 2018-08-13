from datadog import initialize, api

options = {
    'api_key': '377fd636da3480ab9e95434af48ca9ae',
    'app_key': '67362375ca4d77cf13df57e5e528b6e8ce650997'
}

initialize(**options)

title = "Final timeboard"
description = "An informative timeboard."
a_graph = {
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My_metric"
}

anomaly_graph = {
   "title": "Anomaly Graph",
  "definition": {
        "events": [],
        "requests": [
           {"q": "anomalies(avg:mysql.performance.cpu_time{*}.as_count(), 'basic', 2)"}
        ],
        "viz": "timeseries"
    }
}

rollup_graph = {
    "title": "My_Metric over one hour",
    "definition": {
        "events": [],
        "requests": [
             {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
   }
	
}

graphs      = []

graphs.append(a_graph)
graphs.append(anomaly_graph)
graphs.append(rollup_graph)


template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:tony-VirtualBox"
}]

read_only = True
print(api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only))

