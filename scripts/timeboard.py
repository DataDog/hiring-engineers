#!/usr/bin/python

from datadog import initialize, api


def initialize_connection():
	options = {
		'api_key': 'bfe6403b626fd36d7568c4895745c8a4',
		'app_key': 'c9608fcb58fb7ef08750a1a24dd3e2e5a96f5878'
	}
	initialize(**options)

def get_timeboard_title():
	title = raw_input('Please enter a title for your timeboard: ')
	return title

def get_timeboard_description():
	description = raw_input('Please enter a brief description for your timeboard: ')
	return description

def get_widgets():
    widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{*}'}
        ],
    'title': 'My Metric Over katelyn.localhost'}
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:postgresql.buffer_hit{*}, 'basic', 2)"}
        ],
    'title': 'Postgres Buffer Hit'}
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "avg:my_metric{*}.rollup(sum, 3600)",
             'display_type': 'bars'}
        ],
    'title': 'Sum of My Metric'}
    }]

    return widgets

	
	
def create_timeboard(title,widgets,description):
	layout_type = 'ordered'
	is_read_only = True
	notify_list = ['kglassman18@gmail.com']
	template_variables = [{
    'name': 'host',
    'prefix': 'host',
    'default': 'katelyn.localhost'}]
    
	saved_view = [{
    'name': 'Saved views for hostname',
    'template_variables': [{'name': 'host', 'value': 'localhost'}]}]
	
	api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_view)
                     

def main():
	initialize_connection()
	title = get_timeboard_title()
	description = get_timeboard_description()
	widgets = get_widgets() 
	create_timeboard(title,widgets,description)
	
if __name__ == '__main__':
	main()
