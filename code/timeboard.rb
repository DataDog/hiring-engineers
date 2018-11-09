require 'byebug' # Import necessary entities
require 'dogapi'

# Find your keys here:
# https://app.datadoghq.com/account/settings#api

api_key = '719d714d7132af72ce6e1f2d8b67b618' 
app_key = 'ad4336c11c87bab29da8da02b46921f83314c922' 

# To bark really loud, you need an impressive dog!
chihuahua = Dogapi::Client.new(api_key, app_key) 

# In the next section we are going to create a simple Timeboard.

# Title displayed on the top of the Timeboard
title = 'Logfathers Timemachine'

# Let everyone know your intentions as to what this timeboard was created for.
description = 'This timeboard presents everything that is necessary to become a successful sales engineer for Datadog. Arf.' 

# Define the new graph to be displayed
graphs = [{
    "definition" => {
        "events" => [],
        "requests" => [
          {"q" => "avg:logfather_cpu{*}"},
        ],
        "viz" => "timeseries"
    },
    "title" => "CPU usage scoped over the Logfather host"
}]
template_variables = [{
    "name" => "Logfathers Timemachine",
    "prefix" => "Logfathers Timemachine",
    "default" => "host:Logfathers Timemachine"
}]

chihuahua.create_dashboard(title, description, graphs, template_variables)