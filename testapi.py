POST 'https://api.datadoghq.com/api/v1/dash'
from datadog import initialize, api

options = {
    'api_key': '6dde5873456f6a9b66b98930161cdbd8',
    'app_key': 'b16780246a98509d1ea03c064b1097b5ba5a4cae'
}

initialize(**options)

title = "My_Metric_TimeBoard"
description = "Really cool Timeboard for Metrics"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:mysql.performance.cpu_time{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL CPU Performance"
}
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:My_Rand_Num{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "MyRandom Number"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

