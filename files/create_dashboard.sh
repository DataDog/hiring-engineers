# Curl command
curl -X POST https://api.datadoghq.eu/api/v1/dashboard \
-H "Content-Type: application/json" \
-H "DD-API-KEY: f3169fdcaca5be37f8151760edf68ba3" \
-H "DD-APPLICATION-KEY: 37b541e18bbfd6885be4f1ac08b504c8ae3136d5" \
-d @- << EOF
{
    "description": "",
    "template_variables": [],
    "is_read_only": false,
    "title": "API Created Dashboard 1",
    "widgets": [
        {
            "definition": {
                "title": "My Metric over 742evergreenterrace",
                "yaxis": {
                    "max": "auto",
                    "include_zero": true,
                    "scale": "linear",
                    "min": "auto",
                    "label": ""
                },
                "show_legend": false,
                "time": {},
                "requests": [
                    {
                        "q": "avg:my_metric{host:742evergreenterrace}",
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line"
                    }
                ],
                "type": "timeseries"
            },
            "id": 4250379309206026
        },
        {
            "definition": {
                "title": "Avg of mongodb.opcounters.queryps over host:742evergreenterrace",
                "requests": [
                    {
                        "q": "anomalies(avg:mongodb.opcounters.queryps{host:742evergreenterrace},'basic',2)",
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line"
                    }
                ],
                "time": {},
                "type": "timeseries",
                "yaxis": {
                    "max": "auto",
                    "include_zero": true,
                    "scale": "linear",
                    "min": "auto",
                    "label": ""
                }
            },
            "id": 142489420056070
        },
        {
            "definition": {
                "title": "Avg of my_metric over *",
                "yaxis": {
                    "max": "auto",
                    "include_zero": true,
                    "scale": "linear",
                    "min": "auto",
                    "label": ""
                },
                "show_legend": false,
                "time": {},
                "requests": [
                    {
                        "q": "avg:my_metric{*}.rollup(sum, 360)",
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line"
                    }
                ],
                "type": "timeseries"
            },
            "id": 7357541063156372
        }
    ],
    "layout_type": "ordered"
}
EOF
