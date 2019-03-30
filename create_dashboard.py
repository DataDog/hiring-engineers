from datadog import initialize, api

options = {
    'api_key': 'c0ad951348b229c986ffe627fcb50bcc',
    'app_key': '64b421dd36844d8091749e6493c55859cac40656'
}

initialize(**options)

title = 'Timeboard API v0.2'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:Inspiron-5759}'}
        ],
        'title': 'My Metric - Avg - Inspiron-5759'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mysql.performance.threads_running{*}, 'basic', 2)"}
        ],
        'title': 'MySql Perf Threads'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        'title': 'My Metric - Rollup 1hr'
    }
}]
layout_type = 'ordered'
description = 'v.0.1'
is_read_only = False
notify_list = ['ajvillarroelp@gmail.com']
template_variables = [{
    'name': 'Inspiron-5759',
    'prefix': 'host',
    'default': 'my-host'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)

