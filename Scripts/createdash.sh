api_key=e1a22fee8e8fbe1a2494782a464c86d7
app_key=9de2d3fc36bea83878061781b6f07d80a6c906bb

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" :  [
      {
        "definition": {
          "viz": "timeseries",
          "status": "done",
          "requests": [
            {
              "q": "avg:system.load.1{*}",
              "aggregator": "avg",
              "style": {
                "width": "normal",
                "palette": "dog_classic",
                "type": "solid"
              },
              "type": "line",
              "conditional_formats": []
            },
            {
              "q": "avg:http.response_time{http_check}",
              "style": {
                "width": "normal",
                "palette": "dog_classic",
                "type": "solid"
              },
              "type": "line"
            }
          ],
          "autoscale": true
        },
        "title": "Overlay of Custom Metric over System Load"
      },
      {
        "definition": {
          "viz": "timeseries",
          "status": "done",
          "requests": [
            {
              "q": "anomalies(avg:mysql.performance.bytes_sent{host:ubuntu}, '\''basic'\'', 2)",
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
        "title": "MySQL Timeseries with anomalies applied"
      },
      {
        "definition": {
          "viz": "query_value",
          "status": "done",
          "requests": [
            {
              "q": "avg:http.response_time{http_check}.rollup(sum, 60)",
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
        "title": "Custom metric with rollup function applied - sum up points for the past hour ..."
      }
    ],
      "title" : "Datadog Awesome Demo Dashboard",
      "description" : "A dashboard to show Datadog Awesomeness.",
      "read_only": "False"
}' \
"https://app.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
