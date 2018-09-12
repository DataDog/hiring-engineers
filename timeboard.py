from datadog import initialize, api
#import urllib3
#urllib3.disable_warnings()

options = {
    'api_key': '5f2ec4a8761c36c75db5cb1a21eae420',
    'app_key': '2038604d7302d1ad4a9bfcfc040a10a0de48be9f'
}

initialize(**options)

title = "CSTimeboard2"
description = "Christinas informative timeboard."



graphs = [
{
  "definition" : {
  "events": [],
  "viz": "heatmap",
  "requests": [
    {
      "q": "avg:my_metric{*}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    },
    {
      "q": "avg:my_metric{*}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    }
  ]},
'title': "CSTimeboard2" } ]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
res = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print ("results",res)
