api_key=22a62687a16651ff40ac350700bd1489
app_key=5f391773d79ec9ec871d5b1015ca2bd59f86a1de

curl  -X POST -H "Content-type: application/json" \
-d '{
        "title" : "Gerds API Timeboard",
        "description" : "API generated timeboard",
        "template_variables": [{
            "name": "host1",
            "prefix": "host",
            "default": "precise64"
            }],
        "graphs" : [{
            "title": "Gerds custom metric",
            "definition": {
                "events": [],
                "requests": [
                    {"q": "my_metric{host:precise64} "}
                ],
                "viz": "timeseries"
            }
        },
        {
            "title": "MYSQL anomalies"
            "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:mysql.performance.user_time{host:precise64}, 'basic', 2)"}
                ],
            "viz": "timeseries"}
        },
        {
            "title": "Rollup",
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:my_metric{host:precise64}.rollup(sum,3600)"}
                ],
                "viz": "query_value"
            }
        }
      ]
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
