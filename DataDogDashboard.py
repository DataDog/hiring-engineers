#!/usr/bin/python3.7

from datadog import initialize, api

options = {
    'api_key': 'API_KEY',
    'app_key': 'APP_KEY'
}

initialize(**options)

description: "DataDog Dashboard for colorado"
is_read_only: false
layout_type: "ordered"
title: "API Dashboard for Data Visualization"
widgets: [
{
  "definition":{
      "type":"timeseries",
      # Using the average value of "my_metric" check with a widlcard scope
      "requests": [
          {
              "q":"avg:my_metric.gauge{*}"
          }
      ],
      "title":"Average of my_metric"
  }
},
{
    "definition":{
        "type":"timeseries",
        # Using the anomalies function of "my_metric" check using  
        # and "basic" algorithm and standard deviation of 2
        "requests":[
            {
                "q":"anomalies(avg:mysql.performance.kernel_time{*},'basic',2)"
            }
        ],
        "title":"Anomalies function graph"
    }
},
{
    "definition":{
        "type":"timeseries",
        # Using the rollup function to sum all values 
        # in the last 1 hour
        "requests":[
            {
                "q":"avg:my_metric.gauge{*}.rollup(sum,3600)"
            }
        ],
        "title":"Rollup function graph"
    }
}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only)
