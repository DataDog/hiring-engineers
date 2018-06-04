from datadog import initialize, api

options = {
  'api_key': '1c49036ff30b19fd22f02185eff55bd0',
  'app_key': '97f688a956fab5a0e06154a561ef501aa541eeab'
}

initialize(**options)

title = "Jordans Timeboard"
description = "A simple example"
graphs = [
  {
  "title": "My_metric avg",
  "definition": {
    "viz": "timeseries",
    "requests": [
      {
        "q": "avg:my_metric{host:jordans-pc}",
        "type": "line",
        "style": {
          "width": "thin",
          "palette": "cool",
          "type": "solid"
        }
    }]}
  },
  {
  "title": "Mongo connection anomalies",
  "definition": {
    "viz": "timeseries",
    "requests": [
      {
        "q": "anomalies(avg:mongodb.connections.available{host:jordans-pc}, 'basic', 2)",
        "type": "line",
        "style": {
          "palette": "warm",
          "type": "solid",
          "width": "normal"
        }
    }]}
  },
  {
  "title": "My_metric rollup",
  "definition": {
    "viz": "timeseries",
    "requests": [
      {
        "q": "avg:my_metric{host:jordans-pc}.rollup(sum, 3600)",
        "type": "line",
        "style": {
          "palette": "dog_classic",
          "type": "solid",
          "width": "normal"
        }
    }]}
  }
]

api.Timeboard.create(title=title, description=description, graphs=graphs)