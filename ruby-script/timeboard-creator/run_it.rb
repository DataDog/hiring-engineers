require 'rubygems'
require 'dogapi'
require 'dotenv'
require 'json'
Dotenv.load

api_key = ENV.fetch("DD_API_KEY")
application_key = ENV.fetch("DD_APPLICATION_KEY")

# by default the API Url will be set to https://api.datadoghq.com
dog = Dogapi::Client.new(api_key, application_key)
p dog.datadog_host  # prints https://api.datadoghq.com

# Source from API Reference
new_dashboard = true

if new_dashboard
  # Create a timeboard.
  title = 'My Second Metrics'
  description = 'And they are marvelous.'
  
  f = File.open('anomoly.json')
  an = JSON.parse(f.read())
  f.close()

  f = File.open('metric.json')
  metric = JSON.parse(f.read())
  f.close()

  f = File.open('rollup.json')
  rollup = JSON.parse(f.read())
  f.close()
  
  graphs = [metric, an, rollup]
  p dog.create_dashboard(title, description, graphs)
end
