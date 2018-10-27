require 'rubygems'
require 'dogapi'


api_key = '<api_key>'
app_key = '<app_key>'

dog = Dogapi::Client.new(api_key, app_key)


# Create a timeboard.
title = 'My Metric TimeBoard'
description = 'Test Graphs'
graphs = [
  {
    "definition" => {
      "viz" => "timeseries",
      "status" => "done",
      "requests" => [
        {
          "q" => "avg:my_metric{host:precise64}"
        }
      ],
      "events" => []
    },
    "title" => "my_metric test_graph"
  },
  {
    "definition" => {
      "status" => "done",
      "autoscale" => true,
      "xaxis" => {},
      "viz" => "timeseries",
      "requests" => [
        {
          "q" => "anomalies(avg:postgresql.max_connections{host:precise64}, 'basic', 2)",
          "aggregator" => "avg",
          "style" => {
            "width" => "normal",
            "palette" => "dog_classic",
            "type" => "solid"
          },
          "type" => "line",
          "conditional_formats" => []
        }
      ],
      "events" => [
        {
          "q" => "avg(last_4h):anomalies(avg:postgresql.max_connections{host:precise64} 'agile' 2 direction='both' alert_window='last_15m' interval=60 count_default_zero='true' seasonality='hourly') >= 1 ",
          "tags_execution" => "and"
        }
      ]
    },
    "title" => "Anomaly Graph"
  },
  {
    "definition" => {
      "viz" => "timeseries",
      "status" => "done",
      "requests" => [
        {
          "q" => "avg:my_metric{host:precise64} by {name}.rollup(sum, 3600)",
          "aggregator" => "avg",
          "style" => {
            "width" => "normal",
            "palette" => "dog_classic",
            "type" => "solid"
          },
          "type" => "line",
          "conditional_formats" => []
        }
      ],
      "autoscale" => true,
      "xaxis" => {}
    },
    "title" => "my_metric with rollup function"
  }
]


dog.create_dashboard(title, description, graphs)
