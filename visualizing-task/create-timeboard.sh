#!/usr/bin/env bash

api_key=be24eb3b14a2bfc7dff74558dc4c864f
app_key=126425e26aa1ea273c6db63f3ea4b824a017648a

curl  -X POST -H "Content-type: application/json" \
-d '{
  "graphs": [
    {
      "title": "My metric",
      "definition": {
        "events": [],
        "requests": [
          {
            "q": "my_metric{env:ubuntu:local}"
          }
        ],
        "viz": "timeseries"
      }
    },
    {
      "title": "Mysql performance anomalies",
      "definition": {
        "events": [],
        "requests": [
          {
            "q": "anomalies(mysql.performance.cpu_time{env:ubuntu:local}, '\''basic'\'', 1, direction='\''above'\'')"
          }
        ],
        "viz": "timeseries"
      }
    },
    {
      "title": "My metric count for the last hour",
      "definition": {
        "events": [],
        "requests": [
          {
            "q": "my_metric{env:ubuntu:local}.rollup(sum, 3600)"
          }
        ],
        "viz": "query_value"
      }
    }
  ],
  "title": "My metric Timeboard",
  "description": "A dashboard that shows custom metrics and mysql insights.",
  "template_variables": [
    {
      "name": "datadog-vm",
      "prefix": "host",
      "default": "env:ubuntu:local"
    }
  ],
  "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"