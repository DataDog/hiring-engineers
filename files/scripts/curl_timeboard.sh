#!/bin/bash
# tsn timeboard script
api_key=<api_key>
app_key=<app_key>



curl  -X POST -H "Content-type: application/json" "https://app.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}" \
--data @<(cat <<EOF 
{
        "graphs": [
        {
            "definition": {
                "viz": "timeseries",
                "requests": [
                    {
                        "q": "my_metric.my_metric{*} by {host}",
                        "style": {
                            "width": "normal",
                            "palette": "dog_classic",
                            "type": "solid"
                        },
                        "type": "line",
                        "conditional_formats": []
                    }
                ],
                "autoscale": true
            },
            "title": "Custom Metric over Host"
        },
        {
            "definition": {
                "viz": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:mysql.net.connections{host:i-0ad10d62b065d545b}, 'basic', 6)",
                        "aggregator": "avg",
                        "style": {
                            "width": "normal",
                            "palette": "dog_classic",
                            "type": "solid"
                        },
                        "type": "line",
                        "conditional_formats": []
                    }
                ],
                "autoscale": true
            },
            "title": "MySQL Net Connection /w Anomaly Detection"
        },
        {
            "definition": {
                "viz": "query_value",
                "requests": [
                    {
                        "q": "avg:my_metric.my_metric{*} by {host}.rollup(sum,3600)",
                        "style": {
                            "width": "normal",
                            "palette": "dog_classic",
                            "type": "solid"
                        },
                        "type": null,
                        "conditional_formats": []
                    }
                ],
                "autoscale": true
            },
            "title": "Custom Metric Rollup"
        }
    ],
    "title": "Datadog Excercise",
    "description": "SE job exercise",
    "template_variables": [{
        "name": "ENV",
        "prefix": "host:",
        "default": "host:i-0ad10d62b065d545b"
    }],
    "read_only": "True"
}
EOF
)
