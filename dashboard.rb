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
        "requests" => [{
            "q" => "avg:my_metric{$host}"
        }],
        "viz" => "timeseries"
    },
    "title" => "Metric details"
}]
template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "host:my-host"
}]

dog.create_dashboard(title, description, graphs, template_variables)
