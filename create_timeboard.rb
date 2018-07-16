require 'dogapi'
require 'dotenv/load'
require 'colorize'
require 'pry'


api_key = ENV["API_KEY"]
app_key = ENV["APP_KEY"]

dog = Dogapi::Client.new(api_key, app_key)



title = "My Awesome Metrics"

description = "Gonna visualize the heck out of that data"

# graphs = [
#   {
#     "viz": "timeseries",
#     "status": "done",
#     "requests": [
#       {
#         "q": "avg:my_metric{host:ubuntu-xenial}",
#         "type": "line",
#         "style": {
#           "palette": "dog_classic",
#           "type": "solid",
#           "width": "normal"
#         },
#         "conditional_formats": [],
#         "aggregator": "avg"
#       }
#     ],
#     "autoscale": true
#   },
#   {
#     "viz": "query_value",
#     "status": "done",
#     "requests": [
#       {
#         "q": "hour_before(sum:my_metric{*}.rollup(sum, 3600))",
#         "type": "line",
#         "style": {
#           "palette": "dog_classic",
#           "type": "solid",
#           "width": "normal"
#         },
#         "conditional_formats": [],
#         "aggregator": "sum"
#       }
#     ],
#     "autoscale": true
#   },
#   {
#     "viz": "timeseries",
#     "status": "done",
#     "requests": [
#       {
#         "q": "anomalies(avg:postgresql.rows_inserted{*}, 'basic', 2)",
#         "type": "line",
#         "style": {
#           "palette": "dog_classic",
#           "type": "solid",
#           "width": "normal"
#         },
#         "conditional_formats": [],
#         "aggregator": "avg"
#       }
#     ],
#     "autoscale": true
#   }
# ]



response = dog.create_dashboard(title, description, graphs)

binding.pry
if response.include?("400")
  puts "Something went wrong:".colorize(:red)
  puts response.last["errors"]
else
  puts "You can visit your new timeboard at " + "https://app.datadoghq.com#{response.last["url"]}".colorize(:light_blue)
end