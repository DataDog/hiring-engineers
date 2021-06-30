from datadog import initialize, api

options = {
    'api_key': '4798216c7b644a06d2bb734420eb4ccd',
    'app_key': 'f800304019165b9f90666fbe15b0e5195245320d'
}

initialize(**options)

title = 'Khalil\'s Dashboard'
widgets = [
    { #First Visualization: My Custom Metric scoped over my host Khalils-MBP
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:Khalils-MBP}'}],
        'title': 'my_metric timeboard'
    }
},

    { #Second Visualization: MongoDB's memory resident metric with the anomaly function applied
     'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mongodb.mem.resident{*}, 'basic', 2)"}],
        'title': 'MongoDB mem.resident anomalies'
    }  
},

    { # Third Visualization: My Custom Metric with the rollup function applied 
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
notify_list = ['khalilfaraj22@gmail.com']
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