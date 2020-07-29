#!/usr/bin/env python

from datadog import initialize, api

options = {
    'api_key': "<datadog_api_key>",
    'application_key': "<datadog_app_key>",
}

initialize(**options)

title = "Custom API Timeboard"
description = "Timeboard for random metrics"
graphs = [{
    "title": "API Custom Metric Timeboard",
    "description": "My custom metric scoped over my host",
    "widgets": [
        {
            "id": 1675288027479194,
            "definition": {
                "type": "query_value",
                "requests": [
                    {
                        "q": "sum:mc.my_metric{*}.rollup(sum, 3600)",
                        "aggregator": "avg",
                        "conditional_formats": [
                            { "comparator": ">", "value": 100, "palette": "green_on_white", "hide_value": false }
                        ]
                    }
                ],
                "title": "The Sum of My Metric's Data Points Rolled up from the past Hour into One Bucket",
                "time": { "live_span": "5m" },
                "autoscale": true,
                "precision": 2,
                "text_align": "center"
            }
        },
        {
            "id": 7902384906052379,
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:mc.my_metric{*}, 'basic', 2)",
                        "display_type": "line",
                        "style": { "palette": "cool", "line_type": "solid", "line_width": "normal" }
                    }
                ],
                "markers": [{ "value": "y = 0", "display_type": "error dashed" }],
                "title": "My  Metric  w/ Basic Anomaly Function",
                "show_legend": false,
                "legend_size": "0"
            }
        },
        {
            "id": 9000061510194927,
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:mc.my_metric{*}.rollup(sum)",
                        "metadata": [
                            { "expression": "avg:mc.my_metric{*}.rollup(sum)", "alias_name": "My Metric Gauge" }
                        ],
                        "display_type": "line",
                        "style": { "palette": "purple", "line_type": "solid", "line_width": "thin" }
                    }
                ],
                "yaxis": { "min": "0", "include_zero": false },
                "markers": [
                    { "value": "y = 800", "display_type": "error solid", "label": "y = 800" },
                    { "value": "501 < y < 799", "display_type": "warning dashed", "label": " Waring Zone " },
                    { "value": "1 < y < 500", "display_type": "ok solid", "label": " The Good Range " }
                ],
                "title": "Sweet Spot Metric Check",
                "time": { "live_span": "1h" },
                "show_legend": false,
                "legend_size": "0"
            }
        }
    ],
    "template_variables": [],
    "layout_type": "ordered",
    "is_read_only": true,
    "notify_list": [],
    "id": "dmr-k5f-gkb"
}

]


read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)





