require 'rubygems'
require 'dogapi'

api_key = 'fec0a0f32f58d8c7ba58fe74a63e8422'
app_key = 'a4e55205fb08b4f214904ae94170e72027a25fb4'

dog = Dogapi::Client.new(api_key, app_key)

title = 'Visualizing Data Timeboard'
description = 'This is my timeboard'
graphs = [{
              "definition" => {
                  "events" => [],
                  "requests" => [{
                                     "q": "my_metric{host:precise64}"
                                 }],
                  "viz" => "timeseries"
              },
              "title" => "Custom Metric over Host"
          },
          {
    "definition" => {
        "events" => [],
        "requests" => [{
                           "q": "anomalies(mysql.performance.cpu_time{host:precise64}, 'basic', 2)"
                       }],
        "viz" => "timeseries"
    },
    "title" => "Anomaly"
          },
          {
              "definition" => {
                  "events" => [],
                  "requests" => [{
                                     "q": "my_metric{host:precise64}.rollup(sum, 3600)"
                                 }],
                  "viz" => "timeseries"
              },
              "title" => "Custom Metric with Rollup"
          }]

dog.create_dashboard(title, description, graphs)
