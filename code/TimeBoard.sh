curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
  "title": "my_metric over host",
  "viz": "query_value",
  "autoscale": false,
  "precision": "0",
  "definition": {
  "requests": [
    {
      "q": "avg:se_exercise.my_metric{host:i-0345bdee5ec9b2a19}",
      "aggregator": "last"
    }
  ]
  }
}, {
  "title": "Postgres rows fetched with anomaly function",
  "viz": "timeseries",
"definition": {
  "requests": [
    {
      "q": "anomalies(avg:postgresql.rows_fetched{host:i-0345bdee5ec9b2a19}, '"'"'basic'"'"', 2)",
      "type": "line",
      "aggregator": "avg"
    }
  ]
  }
}, {
  "title": "sum of my_metric over past hour rolled up into one bucket",
  "viz": "timeseries",
 "definition": {
  "requests": [
    {
      "q": "avg:se_exercise.my_metric{host:i-0345bdee5ec9b2a19}.rollup(sum, 3600)",
      "type": "bars",
      "aggregator": "avg"
    }
  ]
  }
}],
      "title" : "Visualizing Data",
      "description" : "Use the API to generate a TimeBoard.",
      "read_only": "True"
}' \
"https://app.datadoghq.com/api/v1/dash?api_key=d7f4bec1845da424d47fc653e0c5555f&application_key=0512d47f70ebfdd5ebdbc1b02c4da3b7da2e70e9"