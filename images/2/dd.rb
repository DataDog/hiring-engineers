require 'dogapi'
require 'byebug'

api_key = 'a54df78148c51ce5fd4e2e6b85f37b44'
app_key = 'fbd21af523830e6f55cef9dbdce1c5e332ba287a'

dog = Dogapi::Client.new(api_key, app_key)

# Create a timeboard.
title = 'My Metric 4'
description = 'Scope over my host'
graphs = [{
    "definition" => {
        "events" => [],
        "requests" => [
          {"q" => "avg:my_metric{*}"},
          {"q": "avg:my_metric{*}.rollup(sum, 60)" },
          {"q" => "anomalies(avg:postgresql.max_connections{*}, 'basic', 2)"}
        ],
        "viz" => "timeseries"
    },
    "title" => "My Metric Scoped over Ubuntu Xenial"
}]
template_variables = [{
    "name" => "ubuntu-xenial",
    "prefix" => "ubuntu-xenial",
    "default" => "host:ubuntu-xenial"
}]

dog.create_dashboard(title, description, graphs, template_variables)
