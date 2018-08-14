from datadog import initialize, api

options = {'api_key': '0df5392e3fcf52b4ee65fef26c2f0cb7',
           'app_key': '958de7a7ae45656320a630d7de70ae4efbddac5f'}

initialize(**options)

title = "My Timeboard"
description = "This is utilizing the DataDog API"
graphs = [{
    "definition": {
        "events": [],
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
        "viz": "timeseries"
    },
    "title": "My_Metric"
},
    {
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:postgresql.buffer_hit{*}",
                "type": "bars",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "avg"
            }
        ],
        "viz": "timeseries"
    },
    "title": "PostgreSQL"
},
    {
    "definition": {
        "requests": [
            {
                "q": "avg:my_metric{*}.rollup(avg, 3600)",
                "type": "line",
                "style": {
                    "palette": "purple",
                    "type": "solid",
                    "width": "thick"
                },
                "conditional_formats": [],
                "aggregator": "avg"
            }
        ],
        "viz": "timeseries",
        "autoscale": "true",
        "status": "done"
    },
    "title": "My_Metric_AVG_H"
}
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
temp = api.Timeboard.create(title=title,
                            description=description,
                            graphs=graphs,
                            template_variables=template_variables,
                            read_only=read_only)
print(temp)
