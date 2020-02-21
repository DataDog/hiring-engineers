#!/usr/bin/env bash
#copy screen id to timeboard
#params
#api_key=<DATADOG_API_KEY>
#app_key=<DATADOG_APPLICATION_KEY>
# screen_id=
export api_key=
export app_key=

curl -X POST -H "Content-type: application/json" \
-d '{
  "title": "heroku timeboard",
  "description": "heroku timeboard metrics and graphs",
  "graphs" :
  [
    {
      "title": "heroku.my_metric scoped host (app dyno)",
      "definition": {
        "events": [],
        "requests": [
          {"q": "avg:heroku.my_metric{host:morning-tundra-95593.web.1}"}
        ]
      },
      "viz": "timeseries"

    },
    {
      "title": "heroku collection Anomaly w/ deviation 3",
      "definition": {
        "events": [],
        "requests": [
          {"q": "anomalies(avg:heroku.my_metric{host:morning-tundra-95593.web.1}, \"basic\", 3)"}
        ]
      },
      "viz": "timeseries"
    },
    {
      "title": "Custom heroku.my_metric rollup sum of collection",
      "definition": {
        "events": [],
        "requests": [
          {"q": "avg:heroku.my_metric{host:morning-tundra-95593.web.1}.rollup(\"sum\", 3600)"}
        ]
      }
    }
  ]
}' \
"https://api.datadoghq.eu/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
