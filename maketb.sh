#!/bin/sh

api_key=4b95c86418ff04b87fd79f2831944a46
app_key=68f8ec338e9930b7c76f0743860dd01cb1142631

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "My Metric on Host Tinux",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:tinux}"}
              ]
          },
          "viz": "timeseries"
      },
      {
          "title": "Anomalies with Mongo Usage Total",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mongodb.usage.total.count{*}, \u0027basic\u0027, 2)"}
              ]
          },
          "viz": "timeseries"
      },
      {
          "title": "My Metric Rolled Up Hourly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Test Visualizations",
      "description" : "A dashboard with random stuff.",
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"