from datadog import initialize, api

options = {
    'api_key': '<deleted>',
    'app_key': '<deleted>'
}

initialize(**options)

title = "DDSE Timeboard"
description = "DataDog Solutions Engineer Timeboard Excercise"
graphs = [
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "ddse.my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Custom Metric"
  },
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.performance.user_time{*}, 'basic', 2)"},
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies - MySQL Performance User Time"
  },
  {
    "definition": {
      "viz": "query_value",
      "events": [],
      "requests": [
        {"q": "avg:ddse.my_metric{*}.rollup(sum, 3600)"}
      ]
    },
    "title": "Average Custom Metric RollUp Sum last hour",
  } 
]

template_variables = [{
    "name": "ddse",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
#creation
#response = api.Timeboard.create(title=title, 
#                     description=description, 
#                     graphs=graphs,
#                     template_variables=template_variables,
#                     read_only=read_only)

#print(response)

# update to get the right metric

response = api.Timeboard.update(
  630736,
  title=title,
  description=description,
  graphs=graphs,
  template_variables=template_variables,
  read_only=read_only,
)
print(response)