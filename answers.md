Your answers to the questions go here.

PART - 1

Task1 (Host Map and tags)
![Optional Text](../master/images/host-mapping.png)

Task2 (Datadog integration for MySQL)


PART - 2 (Visualizing Data)

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
"https://api.datadoghq.com/api/v1/dashboard?api_key=d0fb7ff855aae9da4ff10d64f7b349c8&application_key=ff39af49beae031a78ca6b9b1435a596d7715b75" 
```

Response and dashboard
```
{"notify_list":[],"description":"A dashboard with custom timeseries.","template_variables":[{"default":"my-host","prefix":"host","name":"host1"}],"is_read_only":true,"id":"yke-yz3-v2s","title":"Custom Metric API mapping","url":"/dashboard/yke-yz3-v2s/custom-metric-api-mapping","created_at":"2019-05-26T13:38:18.435269+00:00","modified_at":"2019-05-26T13:38:18.435269+00:00","author_handle":"supra33.b@gmail.com","widgets":[{"definition":{"requests":[{"q":"avg:my_metric{*}"}],"type":"timeseries","title":"Custom Metric timeseries"},"id":8489546693992828}],"layout_type":"ordered"} 
```
