#!/usr/bin/env python

from datadog import initialize, api

options = {
    'api_key': "<datadog_api_key>",
    'application_key': "<datadog_app_key>",
}

initialize(**options)

title = "Custom Metric Timeboard via API"
description = "Creating a timeboard with the Datadog API"
layout_type = "ordered"
widgets = [{
        "definition": {
            "type": "timeseries",
            "title": "Custom metric scoped over Host ",
            "requests": [{
                    "q": "avg:custom_metric.my_metric{host:playground}",
                    "display_type": "line",
                    "style": { "palette": "cool", "line_type": "solid", "line_width": "normal"}
                }],
            "yaxis": { "label": "", "scale": "linear", "min": "auto", "max": "auto",},
            "markers": [{"value": "y = 0","display_type": "error dashed"}],
        }
    },
    {
        "definition": {
            "type": "timeseries",
            "title": " PostgreSQL Commit Anomalies",
            "requests": [{
                    "q": "anomalies(avg:postgresql.commits{*}, 'basic', 1)",
                    "display_type": "line",
                    "style": { "palette": "dog_classic", "line_type": "solid", "line_width": "normal"}
                }],
            "yaxis": {"label": "", "scale": "linear","min": "auto","max": "auto",},  
        }
    },
    {
        "definition": {
            "type": "query_value",
            "title": "Custom metric rollup sum for the past hour",
            "requests": [{
                    "q": "sum:custom_metric.my_metric{host:playground}.rollup(sum, 3600)",
                    "aggregator": "sum",
                    "conditional_formats": [{
                            "comparator": ">",
                            "value": 100,
                            "palette": "green_on_white",
                        }]
                }],
            "precision": 2,
            "text_align": "center"
        }
    }]

api.Dashboard.create(title=title, 
                    widgets=widgets,
                    layout_type=layout_type, 
                    description=description)