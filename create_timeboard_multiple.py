from datadog import initialize, api
import json



"""
Timeboard with multiple graphs created via the Datadog API showing:
  - The average of my_metric scoped over my host.
  - The rollup sum of my_metric into one hour buckets
  - Rows returned metrics from the integration on my Postgresql database with the anomaly function applied.

Reference: https://docs.datadoghq.com/api/?lang=python#timeboards
"""



options = {
    'api_key': '57bbb89561459466cccaaaeb4d356007',
    'app_key': '4547384785b778295067b09598fc321e598ed2c8'
}

initialize(**options) 
title = "My_Metric Timeboard"
description = "Timeboard to displaying my_metric average, roll up sum as well as metrics from Postgresql with an anomaly function applied (created via API)."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:my_metric{*}",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                },
                "conditional_formats": []
                }
        ],
        "viz": "timeseries",
        "status": "done",
        "autoscale": True
    },
    "title": "My_Metric Information (Avg)"
},

{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "sum:my_metric{*}.rollup(sum, 3600)",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                },
                "conditional_formats": []
                }
        ],
        "viz": "timeseries",
        "status": "done",
        "autoscale": True
    },
    "title": "My_Metric Information (Roll up sum over 1 hour)"
},

{
    "definition": {
        "events": [],
        "requests": [
            {
                "q":  "anomalies(sum:postgresql.rows_returned{*}, 'basic', 2)",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                },
                "conditional_formats": []
                }
        ],
        "viz": "timeseries",
        "status": "done",
        "autoscale": True
    },
    "title": "My_Metric Information (Postgresql with anomalies noted)"
}

]


read_only = True
my_metric_board = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)

print (json.dumps(my_metric_board, indent=4))