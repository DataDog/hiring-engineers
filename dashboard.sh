#!/bin/bash

#export datadog API and APP keys before running script
api_key=$DD_API_KEY
app_key=$DD_APP_KEY

curl -X POST \
  https://api.datadoghq.com/api/v1/dashboard \
  -H 'Content-Type: application/json' \
  -H "DD-API-KEY: ${api_key}" \
  -H "DD-APPLICATION-KEY: ${app_key}" \
  -d '{
    "template_variables": [],
    "is_read_only": false,
    "title": "API_created_dashboard",

    "widgets": [
        {
            "definition": {
                "requests": [
                    {
                        "q": "avg:my_metric{host:nuc}",
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line"
                    }
                ],
                "type": "timeseries",
                "legend_size": "0",
                "show_legend": false,
                "title": "My custom metric NUC"
            },
            "id": 1704705437551796
        },
        {
            "definition": {
                "requests": [
                    {
                        "q": "anomalies(avg:postgresql.rows_fetched{*}, '\''basic'\'', 2)",
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line"
                    }
                ],
                "type": "timeseries",
                "legend_size": "0",
                "show_legend": false,
                "title": "Postgres rows with anomoly"
            },
            "id": 8349229258489624
        },
        {
            "definition": {
                "autoscale": true,
                "requests": [
                    {
                        "q": "hour_before(avg:my_metric{*}.rollup(sum, 3600))",
                        "aggregator": "avg"
                    }
                ],
                "type": "query_value",
                "precision": 2,
                "title": "Metric SUM 1HR"
            },
            "id": 1620708753834362
        }
    ],
    "layout_type": "ordered"
}
'