```
curl --location --request POST 'https://api.datadoghq.com/api/v1/dashboard' \
--header 'Content-Type: application/json' \
--header 'DD-API-KEY: $APIKEY' \
--header 'DD-APPLICATION-KEY: $APPKEY' \
--header 'Content-Type: text/plain' \
--header 'Cookie: DD-PSHARD=133' \
--data-raw '{
    "title": "Hiring Timeboard 2",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{host:i-067449ac755ba08bf}"
                    }
                ],
                "title": "My_Metric Average"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:mysql.innodb.read_views{host:i-067449ac755ba08bf}, '\''basic'\'', 2)"
                    }
                ],
                "title": "MySql Reads (Anomalies)"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{host:i-067449ac755ba08bf}.rollup(sum, 3600)"
                    }
                ],
                "title": "My_Mytric Rollup (Hourly)"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "A dashboard created to display custom metrics for the Datadog Solutions Engineer hiring exercise",
    "is_read_only": true,
    "notify_list": [
        "test@datadoghq.com",
        "iain.m.carr@gmail.com"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "i-067449ac755ba08bf"
        }
    ]
}'
```
