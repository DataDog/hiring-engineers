from datadog import initialize, api

options = {
    'api_key': 'XXXXXXdfef6bec6dcfc6f15a8d4ec379',
    'app_key': 'XXXXXXccf02dccbf91c631eabf8391e29081adc7'
}

initialize(**options)

title = "Hiring Timeboard"
description = "A Dashboard with custom metric from agent check as well as anomaly function for MongoDB."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:hiring.my_metric{host:vagrant-ubuntu-trusty-64}",
                "type": "line",
                "metadata": {
                    "avg:hiring.my_metric{host:vagrant-ubuntu-trusty-64}": {
                      "alias": "my_metric"
                    }
                },
                "style": {
                    "palette": "grey",
                    "type": "solid",
                    "width": "normal"
                }
            },
            {
                "q": "avg:hiring.my_metric{host:vagrant-ubuntu-trusty-64}.rollup(sum, 3600)",
                "type": "bars",
                "metadata": {
                    "avg:hiring.my_metric{host:vagrant-ubuntu-trusty-64}.rollup(sum, 3600)": {
                        "alias": "my_metric_sum_by_hour"
                     }
                },
                "style": {
                    "palette": "cool",
                    "type": "solid",
                    "width": "normal"
                }
            },
            {
                "q": "anomalies(avg:mongodb.connections.totalcreated{host:vagrant-ubuntu-trusty-64}, 'basic', 1)",
                "type": "line",
                "metadata": {
                    "anomalies(avg:mongodb.connections.totalcreated{host:vagrant-ubuntu-trusty-64}, 'basic', 1)": {
                        "alias": "mongodb_connections_anomalies"
                     }
                }
            }

        ],
        "viz": "timeseries"
    },
    "title": "My Metric and MongoDB Connections Created"
}]

template_variables = []

read_only = True

result = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print (result)