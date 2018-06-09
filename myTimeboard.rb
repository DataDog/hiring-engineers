require 'rubygems'
require 'dogapi'

api_key = '5ac8fd2b5d54f1dbe20ab426f983a251'
app_key = '764cdf93411341dd0dda6f061be2d3a7668e7ee1'

dog = Dogapi::Client.new(api_key, app_key)

# Create a timeboard.
title = 'hello Test Timeboard'
description = 'Metrics of hello'
graphs = [{
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "avg:hello{host:sarahs-Macbook-Pro.local}"
        }],
        "viz" => "timeseries"
    },
    "title" => "HELLO"
}]
template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "host:my-host"
}]

dog.create_dashboard(title, description, graphs, template_variables)
