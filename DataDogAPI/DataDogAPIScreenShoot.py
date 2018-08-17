import time
import json
from datadog import initialize, api

options = {'api_key': '0df5392e3fcf52b4ee65fef26c2f0cb7',
           'app_key': '958de7a7ae45656320a630d7de70ae4efbddac5f'}

initialize(**options)

# Take a graph snapshot
end = int(time.time())
start = end - (60 * 5)
response = api.Graph.create(
    graph_def='''
    {
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:my_metric{*}",
      "type": "area",
      "style": {
        "palette": "warm",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "status": "done",
  "autoscale": true
}
    ''',
    start=start,
    end=end,
    title="My_Metric_5_min"
)
img = "![](" + response['snapshot_url'] + ")"
message = '@alexander.guesnon@gmail.com' + '\n\n' + img

api.Comment.create(
     handle='alexander.guesnon@gmail.com',
    message = message
)

print(message)
