require 'rubygems'
require 'dogapi'

api_key = 'ecbd45124ceb08ca54c84272f8b644be'
app_key = '055fcbc8b2b9f58fef9bc5f5cd29a8c5d69f2c14'

dog = Dogapi::Client.new(api_key, app_key)

# Create a timeboard.
title = 'My First api_timeboard'
description = 'Hopefully it s working'
graphs = [{
    "title" => "My Random Metrics",
    "definition" => {
      "events" => [],
      "requests" => [{
        "q": "hello.world{*} by {host}"
      }],
      "viz" => "timeseries"
    }
  },
  {
    "title": "Database Size",
    "definition": {
      "events": [],
      "requests": [{
        "q": "anomalies(avg:postgresql.database_size{*}, 'basic', 4)",
        "type": "bars"
      }]
    }
  },
  {
    "title": "My Metrics 1h-Rollup",
    "definition": {
      "events": [],
      "requests": [{
      "q": "avg:hello.world{*}.rollup(sum, 3600)",
      "type": "bars",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": []
    }]
    }
  }]
template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "host:pesoury.myapply"
}]

answer = dog.create_dashboard(title, description, graphs, template_variables)
puts answer
