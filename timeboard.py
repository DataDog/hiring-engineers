from datadog import initialize, api

options = {
    'api_key': '<<source API key>>',
    'app_key': '<<source APP key>>'
}

initialize(**options)

title = "Solutions Engineer Timeboard"
description = "Create a timeboard for hiring challenge"
graphs = [{
    "definition": {
        "events":[],
        "requests": [
            {"q": "avg:random.data{host:trialhostname}"},
            {"q": "avg(last_1h):anomalies(avg:system.cpu.system{name:cassandra}, 'basic', 3, directions='above', alert_window='last_5m', interval=20, count_default_zero='true') >= 1"},
            {"q": "avt:random.data.rollup(sum,60)"}],
        "viz": "query_value"
    },
    "title": "Random Timeboard Trial"
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