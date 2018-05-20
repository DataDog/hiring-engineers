from datadog import initialize, api

options = {
    'api_key': '2acf23a25b2f5b5286e9cbfb83fb612d',
    'app_key': 'df7063887cd81f2e02eae387ab2a01193e130a94'
}

initialize(**options)

title = "My Timeboard"
description = "Hiring Challenge Timeboard."
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {ubuntu-dd-agent.c.foreshopapp.internal}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Custom Metric"
},
{
	"definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}.rollup(sum, 3600)"}       
       ],
        "viz": "timeseries"
    },
    "title": "Rolled Up Custom Metric"
},
{   
	"definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.mem.virtual{*}, 'basic', 3)"}            
        ],
        "viz": "timeseries"
    },
    "title": "Number of DB Connections"
}
]

read_only = True 
api.Timeboard.create(title=title,
	description=description,
	graphs=graphs,
	read_only=read_only)

