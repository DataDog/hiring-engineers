import os
from datadog import initialize, api

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# KEYS
options = {
    'api_key': os.getenv("API_KEY"),
    'app_key': os.getenv("APP_KEY")
}

initialize(**options)

# Create Graphs
custom_metrics_graph = {
    "title": "Hello World Instance",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:hello.world{*}"}
        ],
        "viz": "timeseries"
    }
}
anomaly_graph = {
    "title": "Anomaly Graph of PostgresQL",
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.commits{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    }
}

custom_rollup_graph = {
    "title": "Sum Rollup of Hello World for past hour",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:hello.world{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    }
}

title       = "DataDog Solutions Engineer"
description = "A dashboard for DataDog Solutions Engineer"
graphs      = []

graphs.append(custom_metrics_graph)
graphs.append(anomaly_graph)
graphs.append(custom_rollup_graph)

template_variables = [{
    "name": "Ben",
    "prefix": "host",
    "default": "host:ben-basuni"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
