from datadog import initialize, api

options = {
    'api_key': ‘—‘,
    'app_key': ‘—‘
}

initialize(**options)

title = "Jacky Timeboard for Exercise"
description = "Timeboard exercise in Visualizing Data."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:jacky-datadog-exercise}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average My metric"
},
{
      "definition": {
        "events": [],
        "requests": [
             {"q": "anomalies(avg:mysql.net.connections{*}, 'basic', 3)"},
        ],
        "viz": "timeseries"
    },
    "title": "Mysql connection Anomalies trend"
},
{
      "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{host:jacky-datadog-exercise}.rollup(sum, 60)", "aggregator": "sum"},
        ],
        "viz": "query_value",
	"precision": 0
    },
    "title": "My metric Rollup Sum"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)