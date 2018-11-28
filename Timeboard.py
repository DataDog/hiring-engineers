from datadog import initialize, api

options = {
    'api_key': 'Blocked out for security reasons',
    'app_key': 'Blocked out for security reasons'
}

initialize(**options)



title = "My_Custom_Timeboard"
description = "My_Metric_timeboard"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:Jorges-MacBook-Air.local}"},
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric values"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(system.cpu.system{*}, 'basic', 3)"},
        ],
        "viz": "timeseries"
    },
    "title": "anomolies of my system cpu"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:Jorges-MacBook-Air.local}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Roll up of my metric over the past 1hr"
},

        
          ]

read_only = True
response = api.Timeboard.create(title=title,
                      description=description,
                      graphs=graphs,
                      read_only=read_only)
print(response)

