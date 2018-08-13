require 'rubygems'
require 'dogapi'

api_key = '_removed_for_security_'
app_key = '_removed_for_security_'

dog = Dogapi::Client.new(api_key, app_key)

# Create a timeboard.
title = 'Erics Example TimeBoard'
description = 'Times Arrow, its a thing'
graphs = [{
  "definition" => {
    "events" => [],
    "requests" => [{
      "q" => "avg:checking.my_metric{*}"
    }],
    "viz" => "timeseries"
  },
  "title" => "My Metric Scoped over Host"
},
{
  "definition" => {
    "events" => [],
    "requests" => [{
        "q" => "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"
      }],
    "viz" => "timeseries"
  },
  "title" => "PostgreSQL Anomalies for Checkpoints"
},
{
  "definition" => {
    "events" => [],
    "requests" => [{
        "q" => "avg:checking.my_metric{*}.rollup(sum, 3600)"
      }],
    "viz" => "timeseries"
  },
  "title" => "My Metric Rolled up over 1hr"
}]

template_variables = [{
  "name" => "ubuntu-xenial",
  "prefix" => "host",
  "default" => "host:ubuntu-xenial"
}]

response = dog.create_dashboard(title, description, graphs, template_variables)

puts response
