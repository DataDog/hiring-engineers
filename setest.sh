api_key=97699c2cb32e130ff70bcf5122ff93a3
app_key=da9027ba326548349f73f13d1d16d1f012845aa0

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "My_Metric",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ],
              "viz": "timeseries"
          }
      },
		  {
          "title": "my_metric_rollup",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(avg, 3600)"}
              ],
              "viz": "timeseries"
          }
      }],
      "title" : "SE Timeboardtest",
      "description" : "SE Test Dashboard",
      "template_variables": [{
          "name": "scope",
          "prefix": "host",
          "default": "host:ubuntu-xenial"
      }],
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"