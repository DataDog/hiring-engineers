from datadog import initialize, api

options = {
    'api_key': 'xxx',
    'app_key': 'xxx'
}

initialize(**options)

title = "Andy Roberts Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
        {
          "q": "avg:my_metric{host:precise64}",
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
          "q": "anomalies(avg:mysql.innodb.buffer_pool_free{host:precise64}, 'basic', 2)",
          "type": "line",
          "style": {
          "palette": "dog_classic",
          "type": "solid",
          "width": "normal"
          }
        },
        {
          "q": "sum:my_metric{host:precise64}.rollup(sum, 3600)",
          "type": "line",
          "style": {
          "palette": "dog_classic",
          "type": "solid",
          "width": "normal"
          }
        }
        ],
        "viz": "timeseries"
    },
    "title": "Andy 3"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
