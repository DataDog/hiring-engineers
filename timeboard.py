from datadog import initialize, api

options = {
    'api_key': '72fdb42db3c939880977b6b32ea31cbd',
    'app_key': '31e8b0547d314e638dd14a4106bd417e420ea39b'
}

initialize(**options)

title = "Redman Timeboard"
description = "An informative timeboard."
graphs = [
  {
   "definition": {
   "events": [],
   "requests": [
              {"q": "avg:my_metric{host:i-02dd61a0045470207}"}
          ],
   "viz": "timeseries"
   },
   "title": "My Metric"
  },
  {
   "definition": {
   "events": [],
   "requests": [
              {"q": "anomalies(avg:mysql.net.max_connections{*}, 'basic', 2)"}
          ],
   "viz": "timeseries"
   },
   "title": "Anomalies SQL Max Connections"
  },
  {
   "definition": {
   "events": [],
   "requests": [
              {"q": "avg:my_metric{*}.rollup(sum, 3600)",
   "aggregator": "sum",
   "style": {
   "width": "normal",
   "palette": "dog_classic",
   "type": "solid"
                }
              }
          ],
   "viz": "query_value"
   },
   "title": "Sum of My Metric - One Hour Buckets"
  }
]

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs)

