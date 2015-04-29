from os import environ
from datadog import initialize

# The api_key and app_key should be set via environment variables.
api_key = environ.get("DATADOG_API_KEY")
app_key = environ.get("DATADOG_APP_KEY")
if not api_key or not app_key:
    raise Exception("You must set both the DATADOG_API_KEY and DATADOG_APP_KEY environment variables.")
initialize(api_key=api_key, app_key=app_key)