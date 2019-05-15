#!/bin/bash


api_key=29df0174a45acb5a3bf99f1b619fc1f9
app_key=0c8c550b9d5c08306d08bc03af07a0570e68f089

curl  -X POST -H "Content-type: application/json" \
-d '
{
  "notify_list": [],
  "description": "",
  "template_variables": [],
  "is_read_only": false,
  "id": "kfz-vxx-isv",
  "title": "Visualizing Data API 2",
  "widgets": [
    {
      "definition": {
        "requests": [
          {
            "q": "avg:my_metric{*}",
            "style": {
              "line_width": "normal",
              "palette": "dog_classic",
              "line_type": "solid"
            },
            "display_type": "line"
          }
        ],
        "type": "timeseries",
        "title": "Avg of my_metric over *"
      },
      "id": 594120172197994
    },
    {
      "definition": {
        "autoscale": false,
        "requests": [
          {
            "q": "sum:my_metric{*}.rollup(sum)",
            "aggregator": "sum"
          }
        ],
        "type": "query_value",
        "precision": 2,
        "title": "Rollup my_metric"
      },
      "id": 147631327658473
    }
  ],
  "layout_type": "ordered"
}
' \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"
