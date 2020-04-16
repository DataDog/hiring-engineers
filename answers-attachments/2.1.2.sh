{
    "title": "API Data Visualization Timeboard",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "my_metric{host:vagrant}"
                    }
                ],
                "title": "Custom metric my_metric scoped to 'vagrant' host"
            }
        },
        {"definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"
                    }
                ],
                "title": "Postgres percent usage of connections with anomaly detection, basic"
            }
        },
        {"definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "sum:my_metric{*}.rollup(sum,3600)"
                    }
                ],
                "title": "Custom metric rollup to the sum of all my_metric in last hour"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "API Data Visualization: Custom Host-Specific Metric, Postgres Connection Usage Anomaly Detection, and Custom Metric Rollup (1 hr)",
    "is_read_only": true,
    "notify_list": [
        "EMAIL-REDACTED"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "<HOSTNAME_1>"
        }
    ],
    "template_variable_presets": [
        {
            "name": "Saved views for hostname 2",
            "template_variables": [
                {
                    "name": "host",
                    "value": "<HOSTNAME_2>"
                }
            ]
        }
    ]
}

------------------------------------------------------
curl --request POST \
  --url https://api.datadoghq.com/api/v1/dashboard \
  --header 'Content-Type: application/json' \
  --header 'DD-API-KEY: REDACTED' \
  --header 'DD-APPLICATION-KEY: REDACTED' \
  --header 'Postman-Token: REDACTED' \
  --header 'cache-control: no-cache' \
  --data '{\n    "title": "API Data Visualization Timeboard",\n    "widgets": [\n        {\n            "definition": {\n                "type": "timeseries",\n                "requests": [\n                    {\n                        "q": "my_metric{host:vagrant}"\n                    }\n                ],\n                "title": "Custom metric my_metric scoped to '\''vagrant'\'' host"\n            }\n        },\n        {"definition": {\n                "type": "timeseries",\n                "requests": [\n                    {\n                        "q": "anomalies(avg:postgresql.percent_usage_connections{*}, '\''basic'\'', 2)"\n                    }\n                ],\n                "title": "Postgres percent usage of connections with anomaly detection, basic"\n            }\n        },\n        {"definition": {\n                "type": "timeseries",\n                "requests": [\n                    {\n                        "q": "sum:my_metric{*}.rollup(sum,3600)"\n                    }\n                ],\n                "title": "Custom metric rollup to the sum of all my_metric in last hour"\n            }\n        }\n    ],\n    "layout_type": "ordered",\n    "description": "API Data Visualization: Custom Host-Specific Metric, Postgres Connection Usage Anomaly Detection, and Custom Metric Rollup (1 hr)",\n    "is_read_only": true,\n    "notify_list": [\n        "EMAIL-REDACTED"\n    ],\n    "template_variables": [\n        {\n            "name": "host",\n            "prefix": "host",\n            "default": "<HOSTNAME_1>"\n        }\n    ],\n    "template_variable_presets": [\n        {\n            "name": "Saved views for hostname 2",\n            "template_variables": [\n                {\n                    "name": "host",\n                    "value": "<HOSTNAME_2>"\n                }\n            ]\n        }\n    ]\n}\n'

  ------------------------------------------------------
import requests

url = "https://api.datadoghq.com/api/v1/dashboard"

payload = "{\n    \"title\": \"API Data Visualization Timeboard\",\n    \"widgets\": [\n        {\n            \"definition\": {\n                \"type\": \"timeseries\",\n                \"requests\": [\n                    {\n                        \"q\": \"my_metric{host:vagrant}\"\n                    }\n                ],\n                \"title\": \"Custom metric my_metric scoped to 'vagrant' host\"\n            }\n        },\n        {\"definition\": {\n                \"type\": \"timeseries\",\n                \"requests\": [\n                    {\n                        \"q\": \"anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)\"\n                    }\n                ],\n                \"title\": \"Postgres percent usage of connections with anomaly detection, basic\"\n            }\n        },\n        {\"definition\": {\n                \"type\": \"timeseries\",\n                \"requests\": [\n                    {\n                        \"q\": \"sum:my_metric{*}.rollup(sum,3600)\"\n                    }\n                ],\n                \"title\": \"Custom metric rollup to the sum of all my_metric in last hour\"\n            }\n        }\n    ],\n    \"layout_type\": \"ordered\",\n    \"description\": \"API Data Visualization: Custom Host-Specific Metric, Postgres Connection Usage Anomaly Detection, and Custom Metric Rollup (1 hr)\",\n    \"is_read_only\": true,\n    \"notify_list\": [\n        \"EMAIL-REDACTED\"\n    ],\n    \"template_variables\": [\n        {\n            \"name\": \"host\",\n            \"prefix\": \"host\",\n            \"default\": \"<HOSTNAME_1>\"\n        }\n    ],\n    \"template_variable_presets\": [\n        {\n            \"name\": \"Saved views for hostname 2\",\n            \"template_variables\": [\n                {\n                    \"name\": \"host\",\n                    \"value\": \"<HOSTNAME_2>\"\n                }\n            ]\n        }\n    ]\n}\n"
headers = {
    'Content-Type': "application/json",
    'DD-API-KEY': "REDACTED",
    'DD-APPLICATION-KEY': "REDACTED",
    'cache-control': "no-cache",
    'Postman-Token': "REDACTED"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
