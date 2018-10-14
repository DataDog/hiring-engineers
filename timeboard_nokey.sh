#!/bin/sh

api_key=xxx
app_key=xxx

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "My custom metric scoped over my host",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:bamboo01}"}
              ]
          },
          "viz": "timeseries"
      }, {
          "title": "Any metric from the Integration on my Database with the anomaly function applied",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      }, {
          "title": "Any metric from the Integration on my Database with the anomaly function applied",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Timeboard from API",
      "description" : "A dashboard created by API",
      "template_variables": [{
          "name": "host",
          "prefix": "host",
          "default": "host:bamboo01"
      }],
      "read_only": "True"
    }' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"