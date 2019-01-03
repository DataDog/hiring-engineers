from datadog import initialize, api

options = {'api_key': '',
           'app_key': ''}

initialize(**options)


title = "API Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
          {"q": "avg:my_metric{host:exercisevm}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric on exercisvm"
},
{    "definition": {
        "events": [],
        "requests": [
          {"q": "anomalies(avg:postgresql.rows_returned{host:exercisevm}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Integration with anomaly"
},
{    "definition": {
        "events": [],
        "requests": [
          {"q": "avg:my_metric{host:exercisevm}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My metric rolled up to an hour"
}
]


response = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     )
print response