from datadog import initialize, api

options = {
    'api_key': 'bb2513edece1ffacaecd04703b3db9dd',
    'app_key': '67678c72c507fd188697846665e338333517a249'
}

initialize(**options)

title = "Solutions Engineer Timeboard"
description = "Create a timeboard for hiring challenge"
graphs = [{
    "definition": {
        "events":[],
        "requests": [
            {"q": "avg:my_metric{host:lahorton.machinehost}"},
            {"q": "anomalies(avg:my_metric{*}, 'basic', 3)"}
            {"q": "my_metric.rollup(sum,60)"}],
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
