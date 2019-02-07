#!/usr/bin/python
from datadog import initialize, api

options = {'api_key': '0f4ed1330465ec78f05d13b39c865135',
           'app_key': '02aa01821ed3826e6ae0837649f256df3dea11aa'
          }

initialize(**options)

# Call Embed API function
api.Embed.get_all()

title = "My Special Timeboard"
description = "My SA sample timeboard for testvm.localdomain!"
graphs = [
{
  "title": "My_metric Timeboard",
  "definition": {
      "events": [],
      "requests": [
        {
           "q": "avg:my_metric{*}",
           "type": "line",
           "style": {
               "palette": "dog_warm",
               "type": "solid",
               "width": "normal"
          },
          "conditional_formats": [],
          "aggregator": "avg"
        }
      ],
      "autoscale": "true",
      "viz": "timeseries"
  }
},
{
  "title": "MySQL anonmalies Applied",
  "definition": {
  "viz": "timeseries",
      "events": [],
      "requests": [
        {
           "q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)",
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
      "autoscale": "true",
    }
  },
{
  "title": "My_metric Rollup Timeboard",
  "definition": {
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 60)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": []
    }
  ],
  "autoscale": "true"
 }
}
]
api.Timeboard.create(title=title, description=description, graphs=graphs)
