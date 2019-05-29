Your answers to the questions go here.

<h2>PART - 1 (Collecting metrics)</h2>

Task1 (Host Map and tags)
![Optional Text](../master/images/host-mapping.png)

---

Task2 (Datadog integration for MySQL)
![Optional Text](../master/images/sql_integration.png)

---

Task3 (Setup custom agent check for my_metric) <br/> 
![Optional Text](../master/images/custom_metric_collection.png)

---

Task4 (Script to generate random number < 1000) <br/>
[link to custom_my_metric.py python script](../master/script/checks.d/custom_my_metric.py)

---

Task5 (Bonus Question : change the collection interval without modifying the Python file) <br/>
[link to custom_metric.yaml](../master/script/conf.d/custom_my_metric.yaml)

---

<h2>PART - 2 (Visualizing Data)</h2>

Task1 - Datadog API to create a Timeboard for custom metric scoped over host.

Curl request below
```
curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "Custom Metric API mapping",
      "widgets" : [{
          "definition": {
              "type": "timeseries",
"requests": [
{
"q": "avg:my_metric{*}"
}
],
              "title": "Custom Metric timeseries"
          }
      }],
      "layout_type": "ordered",
      "description" : "A dashboard with custom timeseries.",
      "is_read_only": true,
      "notify_list": ["user@domain.com"],
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "my-host"
      }]
}' \
"https://api.datadoghq.com/api/v1/dashboard?api_key=<masked>&application_key=<masked>" 
```

Response and dashboard
```
{"notify_list":[],"description":"A dashboard with custom timeseries.","template_variables":[{"default":"my-host","prefix":"host","name":"host1"}],"is_read_only":true,"id":"yke-yz3-v2s","title":"Custom Metric API mapping","url":"/dashboard/yke-yz3-v2s/custom-metric-api-mapping","created_at":"2019-05-26T13:38:18.435269+00:00","modified_at":"2019-05-26T13:38:18.435269+00:00","author_handle":"supra33.b@gmail.com","widgets":[{"definition":{"requests":[{"q":"avg:my_metric{*}"}],"type":"timeseries","title":"Custom Metric timeseries"},"id":8489546693992828}],"layout_type":"ordered"} 
```
---

Task2 - Datadog API to create a Timeboard for the database with the anomaly function applied

Curl request below
```
curl -X POST -H "Content-type: application/json" \
-d '{  
   "type":"metric alert",
   "query":"avg(last_5m):per_minute(max:mysql.performance.com_select{env:vagrant}) > 9",
   "name":"MySQL Select statement threshold",
   "message":"{{#is_alert}}\nExcessive SQL activity. Check for bots/scrapers\n{{/is_alert}} \n\n{{#is_alert_recovery}}\nTrend of SQL activity returning back to normal.\n{{/is_alert_recovery}}  @supra33.b@gmail.com",
   "tags":[  
      "server:mysql",
      "load"
   ],
   "options":{  
      "notify_no_data":false,
      "no_data_timeframe":null,
      "thresholds":{  
         "critical":9,
         "warning":8,
         "warning_recovery":4,
         "critical_recovery":5
      }
   }
}' \
    "https://api.datadoghq.com/api/v1/monitor?api_key=<masked>&application_key=<masked>"
```
Response
```
{"tags":["server:mysql","load"],"deleted":null,"query":"avg(last_5m):per_minute(max:mysql.performance.com_select{env:vagrant}) > 9","message":"{{#is_alert}}\nExcessive SQL activity. Check for bots/scrapers\n{{/is_alert}} \n\n{{#is_alert_recovery}}\nTrend of SQL activity returning back to normal.\n{{/is_alert_recovery}}  @supra33.b@gmail.com","id":9992094,"multi":false,"name":"MySQL Select statement threshold","created":"2019-05-29T02:32:24.780119+00:00","created_at":1559097144000,"creator":{"id":1272943,"handle":"supra33.b@gmail.com","name":"Supradeep","email":"supra33.b@gmail.com"},"org_id":299890,"modified":"2019-05-29T02:32:24.780119+00:00","overall_state_modified":null,"overall_state":"No Data","type":"query alert","options":{"notify_audit":false,"locked":false,"silenced":{},"include_tags":true,"no_data_timeframe":null,"new_host_delay":300,"notify_no_data":false,"thresholds":{"critical":9.0,"warning":8.0,"critical_recovery":5.0,"warning_recovery":4.0}}} 
```

Screenshot of the timeseries - https://tinyurl.com/y2wefmum

---
Task3 - Custom metric with the rollup sum function into 1hr buckets.

Curl request
```
{  
   "title":"Custom Metric rollup in 1 hr buckets",
   "widgets":[  
      {  
         "definition":{  
            "type":"timeseries",
            "requests":[  
               {  
                  "q":"avg:my_metric{*}.rollup(sum, 3600)"
               }
            ],
            "title":"Custom Metric rollup in 1 hr buckets"
         }
      }
   ],
   "layout_type":"ordered",
   "is_read_only":true,
   "notify_list":[  
      "supra33.b@gmail.com"
   ],
   "template_variables":[  
      {  
         "name":"host1",
         "prefix":"host",
         "default":"my-host"
      }
   ]
}
```
Response and dashboard
```
"https://api.datadoghq.com/api/v1/dashboard/qhh-jsp-jfv?api_key=c21d0fba6cf7fd6347cbc1f57b0f1e22&application_key=3c7911780905fefea18aab8f47d7099328bb1d51"
{"notify_list":["supra33.b@gmail.com"],"description":null,"template_variables":[{"default":"my-host","prefix":"host","name":"host1"}],"is_read_only":true,"id":"qhh-jsp-jfv","title":"Custom Metric rollup in 1 hr buckets","url":"/dashboard/qhh-jsp-jfv/custom-metric-rollup-in-1-hr-buckets","created_at":"2019-05-26T13:37:12.554359+00:00","modified_at":"2019-05-29T03:41:34.108916+00:00","author_handle":"supra33.b@gmail.com","widgets":[{"definition":{"requests":[{"q":"avg:my_metric{*}.rollup(sum, 3600)"}],"type":"timeseries","title":"Custom Metric rollup in 1 hr buckets"},"id":7558535943651744}],"layout_type":"ordered"}
```
