#!/bin/bash
# Curl command
# https://docs.datadoghq.com/api/v1/dashboards/

curl -X POST https://api.datadoghq.com/api/v1/dashboard \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_CLIENT_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_CLIENT_APP_KEY}" \
-d @- << EOF
{
    "title": "Visualizing Data",
    "description": "",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{*}"
                    }
                ],
                "title": "my_metric",
                "show_legend": false,
                "legend_size": "0"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{*}.rollup(sum, 3600)",
                        "display_type": "line",
                        "style": {
                            "palette": "classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    }
                ],
                "yaxis": {
                    "scale": "linear",
                    "min": "auto",
                    "max": "auto",
                    "include_zero": true
                },
                "title": "my_metric 1hr rollup",
                "show_legend": false,
                "legend_size": "0"
            }
        },
        {
            "definition": {
                "type": "group",
                "layout_type": "ordered",
                "widgets": [
                    {
                        "definition": {
                            "type": "timeseries",
                            "requests": [
                                {
                                    "q": "anomalies(avg:postgresql.rows_returned{*}.as_count(), 'basic', 1)",
                                    "display_type": "line",
                                    "style": {
                                        "palette": "classic",
                                        "line_type": "solid",
                                        "line_width": "normal"
                                    }
                                }
                            ],
                            "yaxis": {
                                "scale": "linear",
                                "min": "auto",
                                "max": "auto",
                                "include_zero": true
                            },
                            "title": "Rows returned",
                            "show_legend": false,
                            "legend_size": "0"
                        }
                    }
                ],
                "title": "Postgres"
            }
        }
    ],
    "template_variables": [],
    "layout_type": "ordered",
    "is_read_only": false}
EOF
