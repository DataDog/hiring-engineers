from datadog import initialize, api
import random


with open("../config.json") as f:
    config = json.load(f)

options = {'api_key': config["api_key"],
           'app_key': config["app_key"],
           'api_host': 'https://api.datadoghq.com'}

initialize(**options)

random_value = random.randint(0,1000)

api.Metric.send(metric='my_metric', points=random_value)