require 'rubygems'
require 'dogapi'

api_key = '4e3a684e711fad80cb15525c81eba1d7'
app_key = '17afad07c14ae643c0e4a94e5202c737df868131'

dog = Dogapi::Client.new(api_key, app_key)


# Create a timeboard.
title = 'Peters First Timeboard'
description = 'And it is amazing!'
graphs = [{
    "definition" => {
        "events" => [],
        "requests" => [
        {
            "q" => "my_metric{host:Peters-MacBook-Pro.local}"
        }
      ],
        "viz" => "timeseries"
    },
    "title" => "My Custom Metric"
  },
  {
    "definition" => {
        "events" => [],
        "requests" => [
        {
            "q" => "anomalies(avg:postgresql.percent_usage_connections{host:Peters-MacBook-Pro.local}, 'basic', 2)"
        }
      ],
        "viz" => "timeseries"
    },
    "title" => "CPU Anomalies"
  },
  {
    "definition" => {
        "events" => [],
        "requests" => [
        {
            "q" => "my_metric{*}.rollup(sum,60)"
        }
      ],
        "viz" => "timeseries"
    },
    "title" => "My Custom Metric with rollup function"
}]

p dog.create_dashboard(title, description, graphs)
