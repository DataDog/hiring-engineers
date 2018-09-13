# from datadog import initialize, api

# options = {'api_key': '1535c45ebf647f9fff6178537796cc97',
#            'app_key': '341e0889a84319bbd9c23ca1f181e331bd185cb4'}

# initialize(**options)

# title = "My Timeboard"
# description = "An informative timeboard that will go over the custom metric, includes a metric from the integration of the Database with an anomaly function, and a custom metric with the rollup function applied to sum up all the points for the past hour."
# graphs = [{
#     "definition": {
#         "events": [],
#         "requests": [
#             {"q": "avg:system.mem.free{*}"}
#         ],
#         "viz": "timeseries"
#     },
#     "title": "Custom Metric Analysis"
# }]

# template_variables = [{
#     "name": "host1",
#     "prefix": "host",
#     "default": "host:my-host"
# }]

# read_only = True
# api.Timeboard.create(title=title,
#                      description=description,
#                      graphs=graphs,
#                      template_variables=template_variables,
#                      read_only=read_only)

# In order to initialize and learn how the Timeboard worked I utilized
# Curl in the bash and I was able to create the Timeboard now I would need to update the fields and make it display everything correctly using scripts


api_key=1535c45ebf647f9fff6178537796cc97
app_key=341e0889a84319bbd9c23ca1f181e331bd185cb4

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

