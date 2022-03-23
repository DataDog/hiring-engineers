# Curl command
curl -X POST "https://api.datadoghq.com/api/v1/dashboard" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
-d @- << EOF
{
  "layout_type": "ordered",
  "reflow_type": "auto",
  "template_variables": [
    {
      "name": "host1"
    }
  ],
  "title": "TestDashboard7",
  "widgets": [
        {
            "definition": {
                "title_size": "16",
                "legend_columns": [
                    "avg",
                    "min",
                    "max",
                    "value",
                    "sum"
                ],
                "title": "",
                "title_align": "left",
                "legend_layout": "auto",
                "show_legend": true,
                "requests": [
                    {
                        "formulas": [
                            {
                                "formula": "query1"
                            }
                        ],
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line",
                        "response_format": "timeseries",
                        "queries": [
                            {
                                "query": "avg:my_metric{host:vagrant}",
                                "data_source": "metrics",
                                "name": "query1"
                            }
                        ]
                    }
                ],
                "type": "timeseries"
            },
            "id": 7625515718984686
        },
        {
            "definition": {
                "title_size": "16",
                "legend_columns": [
                    "avg",
                    "min",
                    "max",
                    "value",
                    "sum"
                ],
                "title": "",
                "title_align": "left",
                "legend_layout": "auto",
                "show_legend": true,
                "time": {},
                "requests": [
                    {
                        "formulas": [
                            {
                                "formula": "anomalies(query1, 'basic', 2)"
                            }
                        ],
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line",
                        "response_format": "timeseries",
                        "queries": [
                            {
                                "query": "avg:postgresql.bgwriter.checkpoints_timed{*}",
                                "data_source": "metrics",
                                "name": "query1"
                            }
                        ]
                    }
                ],
                "type": "timeseries"
            },
            "id": 3320042100254578
        },
        {
            "definition": {
                "title_size": "16",
                "legend_columns": [
                    "avg",
                    "min",
                    "max",
                    "value",
                    "sum"
                ],
                "title": "",
                "title_align": "left",
                "legend_layout": "auto",
                "show_legend": true,
                "time": {},
                "requests": [
                    {
                        "formulas": [
                            {
                                "formula": "cumsum(query1)"
                            }
                        ],
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line",
                        "response_format": "timeseries",
                        "queries": [
                            {
                                "query": "avg:my_metric{*}",
                                "data_source": "metrics",
                                "name": "query1"
                            }
                        ]
                    }
                ],
                "type": "timeseries"
            },
            "id": 1432038341027246
        }
  ]
}
EOF
