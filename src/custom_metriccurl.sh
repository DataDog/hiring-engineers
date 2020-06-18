#!/bin/bash
curl --location --request POST 'https://api.datadoghq.eu/api/v1/dashboard' \
--header 'Content-Type: application/json' \
--header 'DD-API-KEY: 7725c7d6cef083415b42e74df22fd9f1' \
--header 'DD-APPLICATION-KEY: 1ac4081cb26ecc7ba50fe2fac77add43af52268d' \
--data-raw '{
  "layout_type": "ordered",
  "template_variables": [
    {
      "name": "my_key"
    }
  ],
  "title": "My Dashboard",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [
            {"q": "sum:my.metric{*}.rollup(sum)"}
        ],
        "title": "My Metric sum"
    },
      "layout": {
        "height":10,
        "width":10,
        "x": 0,
        "y":0
      }
    },
    {
        "definition": {
        "type": "timeseries",
        "requests": [
            {"q": "avg:mysql.performance.user_time{*}"}
        ],
        "title": "Average MySQL CPU time (per sec)"
    },
      "layout": {
        "height":10,
        "width":10,
        "x": 10,
        "y":10
      }
    }
  ]
}'