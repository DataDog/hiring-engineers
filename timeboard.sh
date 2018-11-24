#!/bin/bash
set -x -e

api_key=44777b5614adfe98cfc78886cbea1eba
app_key=2c6d52538a7cb1c66ebade0e19cdbb8eed2efa32

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "My custom metric scoped over my host",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:lionh-vm}"}
              ],
              "viz": "timeseries"
          }
      },{
          "title": "MongoDB amount of virtual memory used by the mongod process",
          "definition": {
              "events": [],
              "requests": [
	      {"q": "anomalies(mongodb.mem.virtual{host:lionh-vm}, \"basic\", 3)"}
              ],
              "viz": "timeseries"
          }
      },{
          "title": "My custom metric summed over the last hour",
          "definition": {
              "events": [],
              "requests": [
	      {"q": "my_metric{host:lionh-vm}.rollup(sum,3600)"}
              ],
              "viz": "timeseries"
          }
      }],
      "title" : "My custom Dashboard",
      "description" : "A dashboard with memory info.",
      "template_variables": [{
          "name": "host",
          "prefix": "host",
          "default": "host:lionh-vm"
      }],
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
