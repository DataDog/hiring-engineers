#!/usr/bin/env python
from pprint import pprint
from myapi import api

title = 'First Board via API'
graphs =  [{'definition': {'requests': [{'q': 'avg:my_metric{*}',
                                'style': {'palette': 'dog_classic',
                                          'type': 'solid',
                                          'width': 'normal'},
                                'type': 'line'}],
                  'viz': 'timeseries'},
   'title': 'Avg of my_metric over *'},
  {'definition': {'requests': [{'metadata': {"anomalies(avg:mysql.performance.open_tables{host:en}, 'basic', 2)": {'alias': 'ot'}},
                                'q': 'anomalies(avg:mysql.performance.open_tables{host:en}, '
                                     "'basic', 2)",
                                'style': {'palette': 'dog_classic',
                                          'type': 'solid',
                                          'width': 'normal'},
                                'type': 'line'}],
                  'viz': 'timeseries'},
   'title': 'Avg of mysql.performance.open_tables over host:en'},
  {'definition': {'requests': [{'q': 'avg:my_metric{host:en}.rollup(sum,3600)',
                                'style': {'palette': 'dog_classic',
                                          'type': 'solid',
                                          'width': 'normal'},
                                'type': 'line'}],
                  'viz': 'timeseries'},
   'title': 'Avg of my_metric over host:en'}]
layout_type = 'ordered'
description = 'A dashboard created via API.'
is_read_only = True
notify_list = ['edennuriel@hotmail.com']
template_variables = [{
    'name': 'en',
    'prefix': 'host',
    'default': 'en'
}]
res = api.Timeboard.create(title=title,
                     graphs=graphs,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
print (res)
