from datadog import initialize, api

options = {
    'api_key': '9233a03edb3556b8347ac52a4f61a82d',
    'app_key': '0b8b5e2b80741e6a4fe2c59ac74173dcfcf939d2'
}

initialize(**options)



title = "Custom_Timeboard"
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
{
          "definition": {
          "events": [],
          "requests": [
                       {"q": "my_metric{host:Jorges-MacBook-Air.local}.rollup(sum, 3600)"}
                       ],
          "viz": "query_value"
          },
          "title": "Roll up of my metric over the past 1hr as query value for sake of visual"
}
        
          ]



read_only = True
response = api.Timeboard.create(title=title,
                      description=description,
                      graphs=graphs,
                      read_only=read_only)
print(response)

