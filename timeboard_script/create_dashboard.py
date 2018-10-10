import os

from datadog import initialize, api

options = {'api_key': os.getenv('my_metric_tb_key')}

initialize(**options)
