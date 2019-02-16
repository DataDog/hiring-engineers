#!/usr/bin/env python
from datadog import initialize,api
import os

options = {
    'api_key': os.environ['DD_API_KEY'],
    'app_key': os.environ['DD_APP_KEY']
}

initialize(**options)

if (__name__ == "__main__"):
	print(api.Hosts.search())

