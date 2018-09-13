api_key=1535c45ebf647f9fff6178537796cc97
app_key=341e0889a84319bbd9c23ca1f181e331bd185cb4
# Extracted the Dash_ID from the JSON Object
dash_id=912943

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
      "title" : "Custom Metric Timeboard",
      "description" : "A dashboard with info around the custom metric created, as well as integration with the database (anomaly function included), and custom metric with rollup function applied to sum up all the points for the past hour into one.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

# Bash used for the first time to update the code for metric
curl  -X PUT -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "Sum of Memory Free",
          "definition": {
              "events": [],
              "requests": [
                  {"my_metric": "env:prod"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "My Custom Metric Display over Host",
      "description" : "An updated dashboard with memory info.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }]
}' \
"https://api.datadoghq.com/api/v1/dash/${dash_id}?api_key=${api_key}&application_key=${app_key}"

# Second Bash command used to update the Timeboard
curl  -X PUT -H "Content-type: application/json" \
-d '{
{
  "requests": [
    { "q": "avg:system.mem.free{*}"
      "avg(last_1h)": "anomalies(avg:system.cpu.system{name:cassandra}, 'basic', 3, direction='above', alert_window='last_5m', interval=20, count_default_zero='true') >= 1,"
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "status": "done",
  "viz": "timeseries",
  "autoscale": true
}' \




