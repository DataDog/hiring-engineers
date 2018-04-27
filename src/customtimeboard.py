#! /usr/bin/python3
from datadog import initialize, api
#sys.path.append("/usr/local/lib/python2.7/dist-packages/datadog")
options = {
    'api_host': 'https://app.datadoghq.com/',
    'api_key': '22089f47d7c7cd9285ad8cd7b94b9663',
    'app_key': 'd3a238f120fc730ddf663a58eb72dac600bafc71'}

initialize(**options)

title = "My Exercice Timeboard"
description = "An API generated timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{$host1}"}
        ],
        "viz": "timeseries"
    },
    "title": "Custom Metric"
},
{
    "definition": {
        "events": [],
  "requests": [
    {
      "q": "sum:postgresql.connections{*} by {db}",
      "type": "area",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "viz": "timeseries"
  },
  "title": "Database Connections"
},
{
    "definition": {
        "events": [],
  "requests": [
    {
      "q": "anomalies(sum:postgresql.connections{$host1}, 'basic', 2)",
      "type": "area",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "viz": "timeseries"
},
"title": "Anomalies for Postgresql Connections"
},
{
    "definition": {
        "events": [],

  "requests": [
    {
      "q": "sum:my_metric{$host1}.rollup(sum, 3600)",
      "type": "bars",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "viz": "timeseries"
},
"title": "Rollup Sum Last Hour on Custom Metric"
} ]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:plambert.exercice"
},
{
    "name": "db1",
    "prefix": "db",
    "default": "db:*"
}]

read_only = True

res=api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
print(res)
