from datadog import initialize, api
import dd_secrets

options = {
    'api_key': dd_secrets.dd_keys['DD_API_KEY'],
    'app_key': dd_secrets.dd_keys['DD_APP_KEY']
}

initialize(**options)

title = "My Awesome Timeboard2"
description = "The seed of something great."
graphs = [
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{name:dd-assessment-centos-docker}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric over time"
  },
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.percent_usage_connections{name:dd-assessment-centos-docker}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "postgresql.max_connection anomalies"
  }
]

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs)
