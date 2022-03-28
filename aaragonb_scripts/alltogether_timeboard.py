from datadog import initialize, api

options = {
    'api_key': 'b98216ae8a00972158a23043efa01c0f',
    'app_key': 'c0dedc641535463d62af2fefabcf7be342a60dae'
}

initialize(**options)


title = 'My_metric2, Anomaly and Rollup functions applied to my_metric2'

widgets = [#begining of widgets
{
    	'definition': {
        	'type': 'timeseries',
        	'requests': [
           		{'q': 'avg:my_metric2{*}'}
     
       		 ],
       		 'title': 'w1: my_metric2'
   		 },
},#widget 1
{
    	'definition': {
       	 'type': 'timeseries',
       	 'requests': [
         	  {'q': "anomalies(avg:my_metric2{*},'basic',2)"}
     
       	 ],
       	 'title': 'w2: anomalies applied to my_metric2'
       	 
    	},
    },#widget 2
{ 
	   'definition': {
    	    'type': 'timeseries',
    	    'requests': [
    	       {'q': 'avg:my_metric2{*}.rollup(sum,3600)'}
     
    	    ],
    	    'title': 'This is the rollup function applied to my_metric2 to sum the metrics collected in the past hour'
    	},
}#widget 3

]#end of widgets
layout_type = 'ordered'
description = 'My_metric2, Anomaly and Rollup functions applied to my_metric2'
is_read_only = True
notify_list = ['azucenadelmar78@gmail.com']
template_variables = [{
    'name': 'Air13-Azu',
    'prefix': 'Air13-Azu',
    'default': 'Air13-Azu'
}]

saved_views = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': '<HOSTNAME_2>'}]}
]

api.Dashboard.create(title=title,				 
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)
