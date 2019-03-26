from datadog import initialize, api

options = {
    'api_key': '<API_KEY>',
    'app_key': '<APP_KEY>'
}

initialize(**options)

title = 'Example Timeboard'

widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
          {'q': 'avg:my_metric{host:verbanic-exercise}'}
        ],
        'title': 'my_metric over verbanic-exercise host'
    }
},{
    'definition': {
        'type': 'timeseries',
        'requests': [
          {'q': 'sum:my_metric{*}.rollup(sum,3600)'}
        ],
        'title': 'my_metric rollup over last hour'
    }
},{
    'definition': {
        'type': 'timeseries',
        'requests': [
          {'q': 'anomalies(avg:mysql.performance.cpu_time{*}, "basic", 2)'}
        ],
        'title': 'MySql cpu_time Anomalies'
    }
}]

layout_type = 'ordered'

description = 'An example timeboard for technical exercise.'

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description)