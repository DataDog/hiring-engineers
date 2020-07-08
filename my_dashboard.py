from datadog import initialize, api
import time                                                                                                                                                                                      my_time = time.ctime(time.time())                                                                                                                                                                

options = {
        'api_key': '3163017dc099bcab6c9860e05f3a7ade',
        'app_key': '0c8be5163923b75f191e4e63c35f098dd172be3a'
        }

initialize(**options)

# Dashboard information
title = "My dashboard using API "+ my_time                                                                                                                                                       description = "Dashboard created through the API"
layout_type = "ordered"

#Widgets
widgets = [{
    'definition': {
        'type' : 'timeseries',
        'requests' : [{'q' : 'avg:my_metric.gauge{host:mymachine.learning}'}],
        'title' : 'Avg of my_metric over mymachine.learning'
        }},

        {
    'definition' : {
        'type' : 'timeseries',
        'requests' : [{'q' : "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}],
        'title' : 'Avg of Mysql CPU_time over * w/ anomaly'
        }},
        {
    'definition' : {
         'type' : 'timeseries',
         'requests' : [{'q' : "sum:my_metric.gauge{*}.rollup(avg, 3600)", "display_type": "bars" }],
         'title' : 'my_metric summed over 1hr'
         }}
     ]

#Create Dashboard
api.Dashboard.create(title=title, description=description, layout_type=layout_type, widgets=widgets)