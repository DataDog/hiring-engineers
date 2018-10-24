api_key=b506b3f2df684f9a984aba34cf16f1f4
app_key=05659995c7fce78fb1265d16193d89bc1440f4d0

curl  -X POST -H "Content-type: application/json" \
-d '
{
        "graphs": [{
                        "title": "MyMetric over Time",
                        "definition": {
                                "events": [],
                                "requests": [{
                                        "q": "avg:tobel.mymetric{*}"
                                }],
                                "viz": "timeseries"
                        }
                },
                {
                        "title": "MyMetric Rollup",
                        "definition": {
                                "events": [],
                                "requests": [{
                                        "q": "avg:tobel.mymetric{*}.rollup(avg, 3600)"
                                }],
                                "viz": "timeseries"
                        }
                },
                {
                        "title": "Postgres Anomaly Connections",
                        "definition": {
                                "events": [],
                                "requests": [{
                                        "q":"anomalies(avg:postgresql.percent_usage_connections{*},basic,1)"
                                }],
                                "viz": "timeseries"
                        }
                }
        ],
        "title": "Tobleboard",
        "description": "Datadog hire test",
        "template_variables": [{
                "name": "host1",
                "prefix": "host",
                "default": "host:my-host"
        }],
        "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
