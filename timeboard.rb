require 'pry'
require 'dogapi'

api_key = "KEY"
app_key = "KEY"

datadog_timeboard = Dogapi::Client.new(api_key, app_key)

title = "Brendan's Code Project Timeboard"
widgets = [{
    "definition": {
        "type" => "timeseries",
        "requests" => [
            {"q" => "my_metric{host:precise64}"},
            {"q" => "anomalies(postgresql.bgwriter.buffers_backend{*}, 'basic', 2)"},
            {"q" => "my_metric{*}.rollup(sum, 3600)"},
        ],
        "title" => "my_metric scoped over host, my_metric with rollup(1 hour) and postgresql anomalies"
    }
}]
layout_type = "ordered"

description = "A dashboard with code challenge info."
is_read_only = true
notify_list = ["MY EMAIL"]
template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "my-host"
}]

config = {
  "description" => description,
  "is_read_only" => is_read_only,
  "notify_list" => notify_list,
  "template_variables" => template_variables
}

datadog_timeboard.create_board(title, widgets, layout_type, config)
