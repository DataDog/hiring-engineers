api_key=ba43f5ff300b9342eb4d993e32500157
app_key=631a76043f9c6825b5913e5d10b97e5c697409ac

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "Combined",
          "definition": {
              "events": [],
              "requests": [
                  {
      "q": "avg:my_metric{*}, anomalies(avg:postgresql.rows_returned{*}, 'basic', 2), avg:my_metric{*}.rollup(sum, 60)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": []
        },

              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Combined Metrics Dashboard",
      "description" : "A dashboard with info around custom metrics.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
