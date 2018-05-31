from datadog import initialize, api

options = {
    'api_key': #redacted,
    'app_key': #redacted
}

initialize(**options)

title = "Timeboard_my_metric_Rollup_Anomalies"
description = "4_Graphs"
graphs = [{
      "definition": {
        "events": [],
        "requests": [
          {
            "q": "avg:my_metric{*}"
          },
        ],
        "viz": "timeseries",
        "status": "done",
        "autoscale": "true"
      },
      "title": "my_metric_random_number"
    },
    {
      "definition": {
        "events": [],
        "requests": [
          {
            "q": "avg:my_metric{*}.rollup(sum, 3600)"
          }
        ],
        "viz": "query_value",
		    "status": "done",
		    "autoscale": "true"
      },
      "title": "my_metric_rollup"
    },
    {
      "definition": {
        "events": [],
        "requests": [
          {
            "q": "anomalies(avg:postgresql.rows_inserted{db:mydb}, 'basic', 2)"
          }
        ],
        "autoscale": 'true',
        "status": "done",
        "viz": "timeseries"
      },
      "title": "anomalies_row_insert"
    },
    {
    "definition": {
      "events": [],
      "requests": [
        {
          "q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 6)",
        }
      ],
        "autoscale": 'true',
        "status": "done",
        "viz": "timeseries"
    },
    "title": "anomalies_percent_use"
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
