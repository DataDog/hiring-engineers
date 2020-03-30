from datadog import initialize, api
import random

options = {'api_key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
           'app_key': ' XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
           'api_host': 'https://api.datadoghq.com'}
initialize(**options)

random_value = random.randint(0,1000)

api.Metric.send(metric='my_metric', points=random_value)