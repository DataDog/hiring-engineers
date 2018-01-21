require 'rubygems'
require 'dogapi'

api_key = '50663355ce3333d93aa7b783bba228e1'
app_key = 'bf46db6ab748a561ad806d6e2b6d866a81e91930'

dog = Dogapi::Client.new(api_key, app_key)


# Create a timeboard.
title = 'Timeboard from API'
description = 'This should be a duplicate of the Manual Test Timeboard'
graphs = [
    {
        "definition" => {
            "events" => [],
            "requests": [
                {
                    "q": "anomalies(avg:system.load.1{host:Brians-MBP-3}, 'basic', 2)",
                    "type": "line",
                    "style": {
                        "palette": "dog_classic",
                        "type": "solid",
                        "width": "normal"
                    },
                    "conditional_formats": [],
                    "aggregator": "avg"
                },
                {
                    "q": "anomalies(avg:system.load.1{host:precise64}, 'basic', 2)",
                    "type": "line",
                    "style": {
                        "palette": "dog_classic",
                        "type": "solid",
                        "width": "normal"
                    }
                }
            ],
            "viz": "timeseries",
            "autoscale": true,
            "status": "done"
        },
        "title" => "Comparing Hosts - with Anomalies"
    },{
        "definition" => {
            "events" => [],
            "requests": [
                {
                    "q": "avg:my_metric{*}",
                    "type": "line",
                    "style": {
                        "palette": "dog_classic",
                        "type": "solid",
                        "width": "normal"
                    },
                    "conditional_formats": [],
                    "aggregator": "avg"
                },
                {
                    "q": "avg:my_metric{host:precise64}",
                    "type": "line",
                    "style": {
                        "palette": "dog_classic",
                        "type": "solid",
                        "width": "normal"
                    }
                }
              ],
              "viz": "heatmap",
              "autoscale": true,
              "status": "done"
        },
        "title" => "How Random"
    },{
        "definition" => {
            "events" => [],
            "requests": [
                {
                    "q": "avg:my_metric{*}.rollup(avg, 3600)",
                    "type": "line",
                    "style": {
                        "palette": "dog_classic",
                        "type": "solid",
                        "width": "normal"
                    },
                    "conditional_formats": [],
                    "aggregator": "avg"
                }
              ],
              "viz": "query_value",
              "autoscale": true,
              "status": "done",
              "precision": "0"
        },
        "title" => "Average of Random Numbers this hour"
    }
]

dog.create_dashboard(title, description, graphs)