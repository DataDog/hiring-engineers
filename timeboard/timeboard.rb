require 'rubygems'
require 'dogapi'

api_key=ENV['DD_API_KEY']
app_key=ENV['DD_APP_KEY']

dog = Dogapi::Client.new(api_key, app_key)


# Create a timeboard.
title = 'Scott Ford - Timeboard'
description = 'A basic timeboard generated via the API'
graphs = [{
  "definition" => {
    "events" => [],
    "requests"=> [
      {
        "q" => "avg:my_metric{host:mongodb-ubuntu-1804}",
        "type" => "line"
      }
    ],
  "viz" => "timeseries"
  },
  "title" => "My metric over host"
},
{
  "definition" => {
    "events" => [],
    "requests"=> [
      {
        "q" => "anomalies(avg:mongodb.mem.virtual{*}, 'basic', 2)",
        "type" => "line"
      }
    ],
  "viz" => "timeseries"
  },
  "title" => "MongoDB anomolies"
},
{
"definition" => {
    "events" => [],
    "requests"=> [
      {
        "q" => "avg:my_metric{*}.rollup(sum, 3600)",
        "type" => "line"
      }
    ],
  "viz" => "timeseries"
  },
  "title" => "my_metric rollup sum over one hour"
}]
template_variables = [{
	"name" => "mongodb-ubuntu-1804",
	"prefix" => "host",
	"default" => "host:mongodb-ubuntu-1804"
}]

res = dog.create_dashboard(title, description, graphs, template_variables)
