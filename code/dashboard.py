from datadog import initialize, api

options = {
    'api_key': '<API_KEY>',
    'app_key': '<APP_KEY>'
}

initialize(**options)

title = 'SE Hiring Example'
description = 'A dashboard used to illustrate the Dashboard enpoint in the Datadog API.'
is_read_only = False
layout_type = 'ordered'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            # q provides the basic query for a particular metric following the schema <METRIC>{HOST:<HOST>}
            # in this case, since we have multiple agents present, this is scoped over the host:vagrant
            {'q': 'my_metric{host:vagrant}'}
        ],
        'title': 'My Metric'
        }
    },{
        'definition': {
        'type': 'query_value',
        'requests': [
            # the rollup() function is appended to the end of our query with parameters <METHOD>, <TIME>
            # in this case, we are performing a sum over the time period of 3600 seconds (1 hour)
            {'q': 'my_metric{host:vagrant}.rollup(sum, 3600)'}
        ],
        'title': 'My Metric'
        }
    }, {
        'definition': {
        'type': 'timeseries',
        'requests': [
            # anomalies function with the params METRIC_NAME{*}, '<ALGORITHM>', <BOUNDS>
            # in this case we are performing an anomly analysis over our postgresql.max_connections with the basic algorithm with a standard deviation of 3
            {'q': "anomalies(postgresql.max_connections{host:vagrant}, 'basic', 3)"}
        ],
        'title': 'Max Connections Anomolies'
        }
    }]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,)