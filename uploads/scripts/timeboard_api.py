from datadog import initialize, api

options = {
    'api_key': '320ce1a454ac2ff47bad4eab03549f41',
    'app_key': 'b91a5c4f3f6fef3464b980ccc7a85459dc782ac0'
}

initialize(**options)

title = "Larry's Timeboard via API"
description = "An informative timeboard."
graphs = [
{
  "title": "Sum Up - Last Hour",
  "definition": {
    "viz": "query_value",
    "requests": [
      {
        "q": "avg:my_metric{owner:larry.song}.rollup(sum, 3600)",
        "type": None,
        "style": {
          "palette": "dog_classic",
          "type": "solid",
          "width": "normal"
        },
        "aggregator": "sum",
        "conditional_formats": []
      }
    ],
    "autoscale": True,
    "precision": 2
  }
},
{
  "title": "Mysql Max Connections - Anomaly detection",
  "definition": {
    "viz": "timeseries",
    "requests": [
      {
        "q": "anomalies(sum:mysql.net.max_connections{owner:larry.song}, 'robust', 1)",
        "type": "line",
        "style": {
          "palette": "dog_classic",
          "type": "solid",
          "width": "normal"
        },
        "conditional_formats": []
      }
    ],
    "autoscale": True,
    "precision": 2
  }
}
]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
