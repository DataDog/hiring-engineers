from os import environ

# options = {'api_key': '<DATADOG_API_KEY>',
#            'app_key': '<DATADOG_APPLICATION_KEY>',
#            'api_host': 'https://api.datadoghq.com'}

app_key = environ.get('DD_APP_KEY', '')    # Needed for READ access
api_key = environ.get('DD_API_KEY', '')    # Needed for WRITE access
api_host = environ.get('DD_HOSTNAME', 'https://api.datadoghq.com/api/')

options = {'api_key' : api_key,
            'app_key' : app_key,
            'api_host' : api_host,
}
