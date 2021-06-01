curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [
      {
          "title": "My Metric [host: vagrant] (avg)",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:vagrant}"}
              ],
              "viz": "timeseries"
          }
      },
      {
          "title": "My Metric (hourly sum)",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "sum:my_metric{*}.rollup(sum, 3600)"}
              ],
              "viz": "timeseries"
          }
      },
      {
          "title": "MongoDB Insertion Anomalies",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mongodb.metrics.document.insertedps{*},\" basic\",2)"}
              ],
              "viz": "timeseries"
          }
      }
      ],
      "title" : "My First Timeboard",
      "description" : "A timeboard with very KPIs",
      "template_variables": [{
          "name": "host",
          "prefix": "host",
          "default": "host:*"
      },{
          "name": "ip",
          "prefix": "ip",
          "default": "ip:*"
      }],
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=dee9d3624afd71145a88ce4d2648d687&application_key=79d68b29ca25783024005521ae730bc6ec61beb4"
