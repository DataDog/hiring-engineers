from datadog import initialize, api

options = {
    'api_key': '4dc7304832d0ab2d0d1048ab35c0b86f',
    'app_key': '7e8dffc303beb44b4f83d36c3c22a6a84561db87'
}

initialize(**options)

title = "Siobhan's DataViz Timeboard"

description = "Timeboard with my_metric metric, database integration metric, and sum of my_metric metrics."

graphs = [
  {
    "definition": {
      "events": [],
      "requests": [
        {
          "q": "avg:my_metric{*}"
          }
      ],
      "viz": "timeseries"
    },
    "title": "my_metric Graph"
  },
  {
    "definition": {
      "events": [],
      "requests": [
        {
          "q": "anomalies(avg:postgresql.rows_fetched{*}, 'basic', 1)"
        }
      ],
      "viz": "timeseries"
    },
    "title": "Postgres rows_fetched Metric Anomaly"
  },
  {
    "definition": {
      "events": [],
      "requests": [
        {
          "q": "avg:my_metric{*}.rollup(sum, 3600)"
        }
      ],
      "viz": "timeseries"
    },
    "title": "my_metric Rollup Graph"
  }
]


template_variables = [{
"name": "SiobhanMahoney",
"prefix": "host",
"default": "host:siobhan"
}]


api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables)
