require 'rubygems'
require 'dogapi'

api_key = '736b97f01509c71840ed1b7007c15c3d'
app_key = 'ccefaa0962b4e69865dc4f172f8ed91c2881eb55'

dog = Dogapi::Client.new(api_key, app_key)

# Create a new monitor
#options = {
#    'notify_no_data' => true,
#    'no_data_timeframe' => 20
#}
#tags = ['app:webserver', 'frontend']
#dog.monitor("metric alert", "avg(last_1h):my_metric{host:datadog}", : name => "average of my_metric on my host", : message => "metric on host", : tags => tags, : options => options)

# Create a timeboard.

title = 'My Timeboard'
description = 'Metrics and more'
graphs = [{
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "avg:my_metric{*} by {host}"
        }],
        "viz" => "timeseries"
    },
    "title" => "Average of my metric on my host"
}, 
{
	"definition" => {
        "events" => [],
        "requests" => [{
            "q" => "anomalies(avg:mongodb.network.bytesinps{*}, 'agile', 2)"
        }],
        "viz" => "timeseries"
    },
    "title" => "Mongo network bytes anomalies"
},
{
 	"definition"=> {
        "events" => [],
        "requests" => [{
	     "q"=> "avg:my_metric{*}.rollup(sum,3600)"
	}],
	"viz" => "timeseries"
    },
    "title" => "my_metric sum rollup on 3600s"
}]
template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "host:my-host"
}]

dog.create_dashboard(title, description, graphs, template_variables)
