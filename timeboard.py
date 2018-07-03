from datadog import initialize, api
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

options = {'api_key': '45ce8ac40bfa283bbd78de659d836ca4',
           'app_key': 'c7d07578b114715ad6e826104a937377924f132e'}

initialize(**options)

title = "David's Timeboard"
description = "Timeboard for Solutions Engineer Exercise."
graphs = [{
        "definition": {
                "events": [],
                "requests": [
                        {"q":"avg:my_metric{*}"}
                ],
                "viz": "timeseries"
        },
        "title": "My_metric",
}, {
        "definition": {
                "events":[],
                "requests": [
                        {"q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{role:database:postgresql}, 'basic', 3)"
                        }],
                "viz": "timeseries"
        },
        "title": "PostgreSQL database scheduled checkpoints anomalies"
}, {
        "definition": {
                "events": [],
                "requests": [
                        {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
                ],
                "viz": "timeseries"
        },
        "title": "Hourly Rollup Sum of my_metric"
}]

read_only = True

api.Timeboard.create(title=title,
        description=description,
        graphs=graphs,
        read_only=read_only)
