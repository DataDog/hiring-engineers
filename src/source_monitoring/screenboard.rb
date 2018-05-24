require 'rubygems'
require 'dogapi'
require 'pp'

api_key = '6caaef27352ea09f824410ddeea49c52'
app_key = '9db5175a1867abf3532c5cd6807277a70d40295d'

dog = Dogapi::Client.new(api_key, app_key)

# Create a timeboard.
title = "Iliyan's Timeboard"
description = 'Sample timeboards'
graphs = [
  {
    "definition" => {
      "requests" => [{
        "q" => "avg:my_metric{host:service-db-a-1}",
        "type" => "line",
        "style" => {
          "palette" => "dog_classic",
          "type" => "solid",
          "width" => "normal"
        },
        "conditional_formats" => [],
        "aggregator" => "avg"
      }],
      "viz" => "timeseries",
      "autoscale" => true
    },
    "title" => "Avg of my_metric over host:service-db-a-1"
  },
  {  
    "definition" => {
      "requests" => [{
        "q" => "anomalies(avg:my_metric{*}, 'basic', 2)",
            "type" => "line",
        "style" => {
          "palette" => "dog_classic",
          "type" => "solid",
          "width" => "normal"
        },
        "conditional_formats" => [],
        "aggregator" => "avg"
      }],
      "viz" => "timeseries",
      "autoscale" => true
    },
    "title" => "Avg of my_metric over with anomalies function"
  },
  {
    "definition" => {
      "requests" => [{
        "q" => "avg:my_metric{*}.rollup(sum, 3600)",
        "type" => "line",
        "style" => {
          "palette" => "dog_classic",
          "type" => "solid",
          "width" => "normal"
        },
        "conditional_formats" => [],
        "aggregator" => "avg"
      }],
      "viz" => "timeseries",
      "autoscale" => true
    },
    "title" => "Custom metric with a rollup function"
  }]  



template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "host:my-host"
}]

dog.create_dashboard(title, description, graphs, nil)

