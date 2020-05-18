#!/usr/bin/python

from datadog import initialize, api
from cryptography.fernet import Fernet

def decrypt_key(encrypted_key):
    fernet_key=b'kLBTXhXvcUqVYbdZ7yE59C8GMoKbU9qsrWE3LO-xR7I='
    dc=Fernet(fernet_key)
    res=dc.decrypt(encrypted_key)
    return res.decode("utf-8")
    
def initialize_connection(api_key, app_key):
    options = {
		'api_key': api_key, 
		'app_key': app_key 
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
    encrypted_api_key = 'gAAAAABewdqJm8Mn4Svz1G7unkksRZz89dIRv74bpqcnFjofgguloVPuC0O-K527neTE3X6PrvAWEZJv-oQQ9i9bVkhfttLKKZW_KPcQDW30C144MFdByFZ-Ld6ZEsobOTwicvY7kfp8' 
    encrypted_app_key = 'gAAAAABewdky86ngsNurE7mZdjYM7PXsDEl4prLIpzW5mYC346RJ1mukkqrlMVjy4u6zbG_mZneFnBhpa5QtqC2PpI8ruAchnalh6qj6UBzXaljZNNF-ryvjN0n2Rm-DO1lwPH0TQPML'
    api_key = decrypt_key(encrypted_api_key)
    app_key = decrypt_key(encrypted_app_key)  
    initialize_connection(api_key,app_key)
    title = get_timeboard_title()
    description = get_timeboard_description()
    widgets = get_widgets() 
    create_timeboard(title,widgets,description)
	
if __name__ == '__main__':
    main()
