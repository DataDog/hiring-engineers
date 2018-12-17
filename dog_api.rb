require 'rubygems'
require 'dogapi'

api_key = 'b8ee48b461422f624cfdf4989d4fe74b'
app_key = 'cfa7f9b48c3a74fd8e2e6241cb6d67a670a9d05b' #INTERVIEW_APP key
dog = Dogapi::Client.new(api_key, app_key)
#Check to make sure everything is running
dog.service_check('app.is_still_ok', 'INTERVIEW_APP', 0, :message => 'Response: 200 OK', :tags => ['env:test'])
# Edit Timeboard.
api_metrics_id = '1021540'
title = 'API_Metrics'
description = 'Timeboard created from the API'
graphs = [{
    "definition" => {
        "events" => [],
        "requests" => [{
          "q": "avg:my_metric{host:Jeds-MacBook-Pro.local}",
          "type": "line"
        }],
        "viz" => "timeseries"
      },
    "title" => "My_Metric_Timeseries"
},
{
    "definition" => {
        "events" => [],
        "requests" => [{"q" => "sum:my_metric{host:Jeds-MacBook-Pro.local}.rollup(sum, 3600)",
        "type": "line"
        }],
        "viz" => "query_value"
      },
    "title" => "My_Metric_Query_Value_Rollup"
},
{
    "definition" => {
        "events" => [],
        "requests" => [{"q" => "anomalies(avg:mongodb.connections.available{server:mongodb://datadog:_localhost:27017}, 'basic', 2)",
        "type": "line"
        }],
        "viz" => "timeseries"
      },
    "title" => "Mongodb_Connections"
}]

dog.update_dashboard(api_metrics_id, title, description, graphs)
