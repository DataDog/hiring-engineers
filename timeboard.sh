# Curl command
curl -X POST "https://api.datadoghq.com/api/v1/dashboard" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_CLIENT_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_CLIENT_APP_KEY}" \
-d @- << EOF

{
    "description": "API Timeboard",
    "is_read_only": false,
    "layout_type": "ordered",
    "notify_list": [],
    "title": "API Custom Metric Timeboard",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "title": "My Metric Widget",
                "requests": [
                    {
                        "q": "my_metric{host:vagrant}",
                        "style": {
                            "palette": "dog_classic"
                        }
                    }
                ]
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "title": "Number of MongoDB Queries Per Second.",
                "requests": [
                    {
                        "q": "mongodb.opcounters.queryps{*}",
                        "style": {
                            "palette": "dog_classic"
                        }
                    }
                ]
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "title": "My Metric with Rollup Function",
                "requests": [
                    {
                        "q": "sum:my_metric{*}.rollup(sum, 3600)",
                        "style": {
                            "palette": "dog_classic"
                        }
                    }
                ]
            }
        }
    ]
    }
