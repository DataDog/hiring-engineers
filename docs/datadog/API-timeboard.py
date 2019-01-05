from datadog import initialize, api

# setup DataDog access
options = {
    'api_key': <API_KEY>,
    'app_key': <APP_KEY>
}

initialize(**options)


# timeboard details
title = 'Sara Burke\'s API exercise'
description = "Visualizing Data exercise in Solutions Engineer coding challenge. Created via API."

# graphs to include on timeboard
graphs = [{
    # my_metric scoped over my primary machine
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:Primary.machine}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric over Primary.machine"
},

{# any metric on the database using an anomalies function
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.kernel_time{host:Primary.machine}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL kernel_time over Primary machine w/anomalies"
},

{# my_metric with rollup function applied to sum up all the points for the past hour into one bucket
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:Primary.machine}.rollup(avg)",
            "aggregator": "sum"}
        ],
        "viz": "query_value"
    },
    "title": "my_metric with rollup on Primary machine 60 min bucket"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:Primary.machine"
}]

read_only = True

# create the timeboard
print(
    api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
)