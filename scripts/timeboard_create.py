from datadog import initialize, api

options = {
    'api_key': '04bc19c387c40c38952ccf650807ced2',
    'app_key': '81fb25b5736dd9c01c1a7c6e434cce868d9fbefe'
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

