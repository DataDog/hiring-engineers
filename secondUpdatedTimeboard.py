# Create a dashboard to get. Use jq (http://stedolan.github.io/jq/download/) to get the dash id.
curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "Database Analysis",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:system.mem.free{*}"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "",
      "description" : "A dashboard with info around the custom metric created, as well as integration with the database (anomaly function included), and custom metric with rollup function applied to sum up all the points for the past hour into one.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

