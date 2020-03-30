#the documentation says that the timeboard endpoint is deprecated
#and that it is best to use the dashboard endpoint

from datadog import initialize, api

with open("../config.json") as f:
    config = json.load(f)

options = {
    'api_key': config["api_key"],
    'app_key': config["app_key"]
}

initialize(**options)

