from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

title = "My Programatic Timeboard"
description = "Where the important stuff is managed"
graphs = [{"definition": {
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "sum:hello.world{*}.rollup(sum, 3600)",
      "type": "bars",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true"
},
  "title": "Hourly Rollup of Hello World Metric"
},
{"definition": {
  "requests": [
    {
      "q": "sum:hello.world{host:swarm-master}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": []
    }
  ],
  "viz": "timeseries",
  "autoscale": "true"
},
"title": "Custom Metric"
},
{"definition": {
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "anomalies(sum:redis.info.latency_ms{host:swarm-master}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "purple",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true"
},
    "title": "Redis Latency Anomolies"
}]

read_only = True
print api.Timeboard.update(816029, title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
