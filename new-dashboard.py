from datadog import initialize, api
import os

api_key = os.getenv("DATADOG_API_KEY")
app_key = os.getenv("DATADOG_APP_KEY")

options = {
    'api_key': api_key,
    'app_key': app_key
}

initialize(**options)

title = 'My New Dashboard'
widgets = [
{'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:ubuntu-xenial}'}
        ],
        'title': 'Avg of my_metric over host:ubuntu-xenial'
    }
},
{'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(avg:mongodb.opcounters.queryps{*}, "basic", 2)'}
        ],
        'title': 'Avg of mongodb.opcounters.queryps over * with anomalies'
    }
},
{'definition': {
        'type': 'query_value',
        'requests': [
            {'q': 'avg:my_metric{*}.rollup(sum, 3600)'}
        ],
        'title': 'Rollup sum of my_metric over *',
        'precision': 2
    }
}]
layout_type = 'ordered'
description = 'A new dashboard created by API'

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description)
