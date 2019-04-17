from datadog import initialize, api

options = {
    'api_key': 'KEY',
    'app_key': 'KEY'
}

initialize(**options)

dashboard_id = 'hxm-ggf-6mz'

api.Dashboard.get(dashboard_id)