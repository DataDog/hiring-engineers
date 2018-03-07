from datadog import initialize, api

options = {
    'api_key': 'API_KEY',
    'app_key': 'APP_KEY'
}

initialize(**options)

title = "Aint No Timeboard Like the Present"
description = "A timeboard of mymetric."
graphs = [
  {
    "definition": {
      "events": [],
      "requests": [{
          "q": "anomalies(sum:postgresql.rows_returned{host:seanclarke.test}, 'basic', 2)"
      }],
      "viz": "timeseries"
  },
  "title": "Graph: Postgres"
},
{
  "definition": {
      "events": [],
      "requests": [{
          "q": "sum:mycheck.val{host:seanclarke.test}.rollup(sum,3600)"
      }],
      "viz": "timeseries"
  },
  "title": "Graph: My Metric (Rollup)"
}
]

read_only = True
api.Timeboard.create(title=title,
                   description=description,
                   graphs=graphs,
                   read_only=read_only)
