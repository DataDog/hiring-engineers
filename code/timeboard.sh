#!/bin/bash

export DD_CLIENT_API_KEY=cf19e05244fc603958244f7bffe3ba15
export DD_CLIENT_APP_KEY=bef3a7d4836db864fe557b1ecef1544a801f8c29

curl -X POST "https://api.datadoghq.com/api/v1/dashboard" -H "Content-Type: application/json" -H "DD-API-KEY: ${DD_CLIENT_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_CLIENT_APP_KEY}" -d @- << EOF
{
  "layout_type": "ordered",
  "template_variables": [
    {
      "name": "pihole"
    }
  ],
  "title": "Utilize the Datadog API to create a Timeboard",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:my_metric{*}"
          }
          ],
          "title": "my_metric"
      },
      "layout": {
        "height": 0,
        "width": 0,
        "x": 0,
        "y": 0
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"
          }
          ],
          "title": "anomalies on mysql cpu_time"
      },
      "layout": {
        "height": 0,
        "width": 0,
        "x": 0,
        "y": 0
      }
    },
    {
      "definition": {
        "type": "query_value",
        "precision": 1,
        "requests": [
          {
            "q":"avg:my_metric{*}.rollup(sum,3600)",
            "aggregator":"sum"
          }
          ],
          "time": {
            "live_span":"1h"
          },
          "title": "rollup my_metric 1 hr"
      },
      "layout": {
        "height": 0,
        "width": 0,
        "x": 0,
        "y": 0
      }
    }
  ]
}
EOF
