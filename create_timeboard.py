from datadog import initialize, api

# NOTE: the keys have already been changed by the time of this submission
options = {
    'api_key': '63c86b4892256eddad50b7300c157a18',
    'app_key': '1f7ff10c5bca98f7b2037617fa0808072778d06a'
}

initialize(**options)

title = 'My Timeboard Made Using Python'
description = 'Timeboard that contains: \n1) Your custom metric scoped over your host. \n2) Any metric from the Integration on your Database with the anomaly function applied. \n3) Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket'
# cross-referenced the JSON data from the UI and made test boards first to get the data I needed.
graphs = [
    {
        'definition': {
            'type': 'timeseries',
            'requests': [
                {
                    'q': 'avg:my_metric{host:Kevins-Air.home}',
                }
            ]
        },
        'title': 'Avg of my_metric over host:Kevins-Air.home'
    },
    {
        'definition': {
            'autoscale': True,
            'precision': 2,
            'type': 'query_value',
            'requests': [
                {
                    'q': 'avg:my_metric{host:Kevins-Air.home}.rollup(sum, 3600)',
                    'aggregator': 'sum',
                    'conditional_formats': []
                }
            ]
        },
        'title': 'Rollup Sum of my_metric by the hour'
    },
    {
        'definition': {
            'type': 'timeseries',
            'requests': [
                {
                    'q': 'anomalies(avg:postgresql.commits{host:Kevins-Air.home}, "basic", 2)',
                }
            ]
        },
        'title': 'PostgreSQL metric with anomaly algo applied'
    }
]
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'host:my-host'
}]
read_only = True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
