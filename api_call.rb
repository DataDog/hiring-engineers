require 'rubygems'
require 'dogapi'
require 'pry'
require 'dotenv/load'

api_key = ENV['DATADOG_API_KEY']
app_key = ENV['DATADOG_APP_KEY']

dog = Dogapi::Client.new(api_key, app_key)

title = 'My_Metric_API'
description = 'Doing the my_metric through the API'
graphs = [{
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "anomalies(avg:postgresql.rows_fetched{*}, 'basic', 2)",
            "type" => "line"
        }],
        "viz" => "timeseries"
    },
    "title" => "Rows Fetched With Anomoly Function"
},
{
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "max:my_metric{host:Alekss-MBP.fios-router.home}",
            "type" => "bars"
        }],
        "viz" => "timeseries"
    },
    "title" => "My Metric API Timeseries"
},
{
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "sum:my_metric{host:Alekss-MBP.fios-router.home}.rollup(sum, 60)",
            "aggregator": "sum"
        }],
        "viz" => "query_value",
        "precision": 0,
        "autoscale": false
    },
    "title" => "My Metric With Rollup Function"
}]
template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "host:Alekss-MBP.fios-router.home"
}]

dog.create_dashboard(title, description, graphs, template_variables)