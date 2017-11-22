api_key=107440a2879bb7d0e3da8e4cac17ac57
app_key=67543f3a2978ec8e7b6beb892928f9df8ba69ff5

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [
        {
          "title": "Random Numbers",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "my_metric{*} by {Andrews-Air.home}"}
              ]
          },
          "viz": "timeseries"
        },
        {
          "title": "PSQL Metric with Anomaly",
          "definition": {
            "events": [],
            "requests": [
              {"q": "postgresql.commits{*} by {Andrews-Air.home}"}
            ]
          },
          "viz": "timeseries"
        },
        {
          "title": "Random Numbers with Rollup",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "my_metric{*} by {Andrews-Air.home}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
        }
      ],
      "title" : "My Timeboard",
      "description" : "Timeboard for Hiring Exercise"
    }' \
"https://app.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"