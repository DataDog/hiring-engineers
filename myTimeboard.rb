require 'rubygems'
require 'dogapi'

api_key = '5ac8fd2b5d54f1dbe20ab426f983a251'
app_key = '764cdf93411341dd0dda6f061be2d3a7668e7ee1'

dog = Dogapi::Client.new(api_key, app_key)

title = 'Timeboard with my_metric, my_metric rollup, and anomolies on DB Color 2'
description = 'Test on My_Metric'
graphs = [
  {
      "definition" => {
          "events" => [],
          "requests" => [{
              "q" => "avg:my_metric{*}"
          }],
          "viz" => "timeseries"
      },
      "title" => "My_metric"
  },
  {
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "anomalies(avg:mongodb.locks.collection.acquirecount.intent_exclusiveps{*}, 'basic', 3)",
            "style" => {
              "palette" => "purple"
            }
        }],
        "viz" => "timeseries"
    },
    "title" => "Anomalies on DB"
  },
  {
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "sum:my_metric{*}.rollup(avg, 3600)"
        }],
        "viz" => "timeseries"
    },
    "title" => "Sum of my_metric 1hr Rollup"
  }
]
template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "host:my-host"
}]
dog.create_dashboard(title, description, graphs, template_variables)

# "q" => "avg:my_metric{*}"
# "q" => "sum:my_metric{*}.rollup(avg, 3600)"
