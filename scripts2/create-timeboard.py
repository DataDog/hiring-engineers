from datadog import initialize, api

options = {
    'api_key': 'eea2d9e3fd1b5380ee97f922f676dc47',
    'app_key': 'db3a57b9b8f4d0102da33ce58b9c05e804180bea'
}

initialize(**options)

title = "David's Timeboard created via API!"
description = "David's custom informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
    {
      "q": "anomalies(avg:mongodb.uptime{*}, 'basic', 2)",
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
        "viz": "timeseries"
    },
    "title": "Average of mongodb.uptime with anomaly function applied"
},

{
    "definition": {
        "events": [],
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
    }
  ],
        "viz": "timeseries"
    },
    "title": "My custom metric scoped over all hosts"
},

{
    "definition": {
        "events": [],
        "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 3600)",
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
        "viz": "timeseries"
    },
    "title": "My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket"
}

]

template_variables = [{
    "name": "var-env",
    "default": "dev"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
