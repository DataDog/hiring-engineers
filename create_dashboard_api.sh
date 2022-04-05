curl --request POST \
  --url https://api.datadoghq.com/api/v1/dashboard \
  --header 'Content-Type: application/json' \
  --header 'DD-API-KEY: REDACTED' \
  --header 'DD-APPLICATION-KEY: REDACTED' \
  --data '{
  "title": "Vagrant metrics",
  "description": "Solutions engineer assessment",
  "widgets": [
        {
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "my_metric{host:vagrant}"
                  }
                ],
                "title": "My metric"
          }
        },
				{
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "anomalies(avg:mysql.queries.lock_time{host:vagrant}, 'basic', 2)"
                  }
                ],
                "title": "SQL locks"
          }
        },
        {
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "sum:my_metric{host:vagrant}.rollup(sum, 3600)"
                  }
                ],
                "title": "My Metric hourly",
														  "time": {
    					"live_span": "1d"
  					}
          }
        }
  ],
  "layout_type": "ordered"
}'