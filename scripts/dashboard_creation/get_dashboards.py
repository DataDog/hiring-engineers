import json
from datadog import initialize, api

with open("../../config.json") as f:
    config = json.load(f)

options = {
    'api_key': config["api_key"],
    'app_key': config["app_key"]
}

initialize(**options)

dashboards = api.Dashboard.get_all()

print(dashboards)