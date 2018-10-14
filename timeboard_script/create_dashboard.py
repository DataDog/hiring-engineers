#!/usr/bin/env python

import os
from datadog import initialize, api

def main():
    options = {
        'api_key': os.getenv('dd_api_key'),
        'app_key': os.getenv('dd_app_key')
        }

    initialize(**options)

    title = 'my_metric, mongodb.connections.totalcreated'
    description = 'This is a timeboard for the hiring exercise.'
    graphs = [
        {
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:my_metric{host:ubuntu-xenial}"},
                ],
                "viz": "timeseries",
            },
            "title": "my_metric scoped over ubuntu-xenial"
        },
        {
            "definition": {
                "events": [],
                "requests": [
                    {"q": "anomalies(avg:mongodb.connections.totalcreated{host:ubuntu-xenial}, 'basic', 2)"}
                ],
                "viz": "timeseries"
            },
            "title": "Basic Anomaly Graph of mongodb.connections.totalcreated"
        },
        {
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
                ],
                "viz": "timeseries"
            },
            "title": "Rollup of my_metric with the sum of the values in a time period of one hour",
        }
    ]

    my_timeboard = api.Timeboard.create(title=title, description=description, graphs=graphs)
    print(my_timeboard)

if __name__ == '__main__':
    main()