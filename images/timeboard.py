from datadog import initialize, api

options = {
    'api_key': 'API',
    'app_key': 'APP'
}

initialize(**options)



title = 'Delaney\'s Dashboard'
widgets = [
    { #Step 1: My Custom Metric scoped over my host Khalils-MBP
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:Delaneys-MacBook-Air.local}'}],
        'title': 'my_metric timeboard'
    }
},

    { #Step 2: MongoDB memory resident metric with the anomaly function applied
     'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mongodb.mem.resident{*}, 'basic', 2)"}],
        'title': 'MongoDB mem.resident anomalies'
    }  
},

    { # Step 3: My Custom Metric with the rollup function applied 
      #to sum up all the points for the past hour into one bucket (1 hour = 3600 seconds)
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}.rollup(sum, 3600)'}],
        'title': 'my_metric rolling hour sum'   
    }
}]

layout_type = 'ordered'
description = 'A customized dashboard'
is_read_only = True
notify_list = ['delaneydickson@gmail.com']
template_variables = [{
    'name': 'Custom Timeboard',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_views = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': 'test'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)               