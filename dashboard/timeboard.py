from datadog import initialize, api

options = {
    'api_key': '166778f02f524bf7e00573d19a7d5ae1',
    'app_key': '9696fae0b4e16460e2f30fa5eb2e25dba29993ef'
}

initialize(**options)

title = 'Example Timeboard '
widgets = [
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "avg:my_metric{host:docker-desktop}"}
        ],
        'title': 'My Metric'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)",
            "display_type": "bars"}
        ],
        'title': 'Sum of My Metric - Rolled up in 1 hour buckets  '
    }
}
,
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {"q":"anomalies(avg:docker.cpu.system{container_name:datadog_postgres_1}, 'basic', 2)"}
        ],
        'title': 'Postgres Container CPU - Anomaly Graph '
    }
}
]
layout_type = 'ordered'
description = 'A custom dashboard'
is_read_only = True
notify_list = ['brunolin@bu.com']


api.Dashboard.create(title=title,
                    widgets=widgets,
                    layout_type=layout_type,
                    description=description,
                    is_read_only=is_read_only,
                    notify_list=notify_list)
