from datadog import initialize, api

options = {
    'api_key': '45e60fd7093756732f22bbe731c2238c',
    'app_key': 'de4e086314090cadf4cda99b6228bc755e2f0bf6'
}

initialize(**options)

title = "My_Metric API Created Timeboard Graph"
description = "An API creted timeboard."
graphs = [{
      "graphs" : [{
          "title": "Rhys My_Metric API Graph",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:My.Metric{host:precise64}"} ,
			      {"q": "anomalies(avg:mongodb.network.bytesoutps{*}, 'basic', 2)"},			
			      {"q": "sum:my_metric{*}.rollup(3600)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Rhys My_Metric Dashboard API Created",
      "description" : "A dashboard with the average My_Metric data.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:precise64"
      }],
      "read_only": "True"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)