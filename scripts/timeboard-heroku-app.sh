#!/usr/bin/env bash
#copy screen id to timeboard
#params
#api_key=<DATADOG_API_KEY>
#app_key=<DATADOG_APPLICATION_KEY>
# screen_id=
#replace host with dyno (app server name) and API endpoint with EU or US
export api_key=<YOUR APP KEY HERE>
export app_key=<YOUR APP KEY HERE>

curl -X POST -H "Content-type: application/json" \
-d '{
  "title": "heroku timeboard",
  "name": "heroku test application",
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
      "title": "heroku collection basic anomaly w/ deviation 3",
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
