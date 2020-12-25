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
                "title": "Timeseries Widget",
                "requests": [
                    {
                        "q": "avg:system.cpu.user{*} by {host}",
                        "style": {
                            "palette": "dog_classic"
                        }
                    }
                ]
            },
            "id": 123,
            "layout": {
                "height": 0,
                "width": 0,
                "x": 0,
                "y": 0
            }
        }
    ]
}
