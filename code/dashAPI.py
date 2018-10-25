from datadog import initialize, api

options = {
    'api_key': 'ffc569bfd80d03e7c81eff56223e49bc',
    'app_key': '4cb2bc3be5a304ab9e2a32d9ee0e08f9d6b195af'
}

initialize(**options)

title = "Tech-Exercise Timeboard"
description = "Showing off all our awesome data"
graphs = [{
      "title": "MySQL Performance Timeline",
      "definition": {
        "events": [],
        "requests": [
        {
          "q": "anomalies(avg:mysql.performance.cpu_time{tech-exercise,host:ubuntu-xenial}, 'basic', 2)",
          "type": "line",
          "conditional_formats": [],
          "aggregator": "avg"
        }
        ],
        "viz": "timeseries"
      }
},{    
      "title": "My Metric - Agent Check",
      "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:samir{host:ubuntu-xenial}",
                "type": "bars",
                "style": {
                  "palette": "cool",
                  "type": "solid",
                  "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "avg"
            }
        ],
        "viz": "timeseries",
        "autoscale": True,
        "xaxis": {}
      }
},{
      "title": "My_Metric Rollup Over Last Hour",
      "definition": {
        "events": [],
        "viz": "timeseries",
        "requests": [{
            "q": "my_metric{host:ubuntu-xenial}.rollup(count,3600)",
            "type": "bars",
            "style": {
                "palette": "grey",
                "type": "solid",
                "width": "normal"
            }
        }],
        "autoscale": True
      }  
}]

template_variables = [{
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
'''
{
  "viz": "timeseries",
  "requests": [
    {
      "q": "my_metric{host:ubuntu-xenial}.rollup(count,3600)",
      "type": "bars",
      "style": {
        "palette": "grey",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true,
  "xaxis": {},
  "status": "done"
}



{
      "title": "My_Metric Timeline",
      "definition": {
        "events": [],
        "requests": [
        {
        "viz": "timeseries",
  "requests": [
    {
      "q": "my_metric{host:ubuntu-xenial}.rollup(count,3600)",
      "type": "bars",
      "style": {
        "palette": "grey",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true,
  "xaxis": {},
  "status": "done"
      }
},{

"graphs" : [
        {
          "title": "Average Memory Free",
          "definition": {
              "events": [],
              "requests": [
                      {
                        "q": "avg:samir{host:ubuntu-xenial}",
                        "type": "bars",
                        "style": {
                          "palette": "cool",
                          "type": "solid",
                          "width": "normal"
                        },
                        "conditional_formats": [],
                        "aggregator": "avg"
                      }
              ],
                    "viz": "timeseries",
                    "autoscale": true,
                    "xaxis": {}
          }
        }
      ],
      "title" : "SG-Test_timeboard",
      "description" : "A Sample Timeboard for Testing",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"

      '''