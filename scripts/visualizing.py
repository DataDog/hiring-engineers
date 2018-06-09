from datadog import initialize, api
from datadog.api.constants import CheckStatus

options = {'api_key': 'caecf54c05497610bd221b11423fbf1d',
           'app_key': '505f3113a164f647a92a5bf6ced19c746677c118'}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
      "events": [],
      "requests": [
        {"q": "avg:my_metric{host:EZH-LT}"}
      ],
      "viz": "timeseries"
    },
    "title": "My Metric"
  },
  {
    "definition": {
      "events": [],
      "requests": [
        {"q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{host:EZH-LT}.as_count(), 'basic', 2)"}
      ],
      "viz": "timeseries"
    },
    "title": "PostgreSQL Integration with Anomaly"
  },
  {
    "definition": {
      "events": [],
      "requests": [
        {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
      ],
      "viz": "timeseries"
    },
    "title": "My Metric with Rollup Sum 1hr"
  }
]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
