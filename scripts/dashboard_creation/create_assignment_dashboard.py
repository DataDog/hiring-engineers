#the documentation says that the timeboard endpoint is deprecated
#and that it is best to use the dashboard endpoint

# Utilize the Datadog API to create a Timeboard that contains:

# * Your custom metric scoped over your host.
# * Any metric from the Integration on your Database with the anomaly function applied.
# * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

# Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

# Once this is created, access the Dashboard from your Dashboard List in the UI:

# * Set the Timeboard's timeframe to the past 5 minutes
# * Take a snapshot of this graph and use the @ notation to send it to yourself.
# * **Bonus Question**: What is the Anomaly graph displaying?

from datadog import initialize, api
import json

with open("../../config.json") as f:
    config = json.load(f)

options = {
    'api_key': config["api_key"],
    'app_key': config["app_key"]
}

initialize(**options)


title = 'Bills Second Dashboard'
widgets = [
    {'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric.rollup(sum,3600)'}
        ],
        'title': 'Custom Metric, Randomly Generated Numbers'
    }
}]
layout_type = 'ordered'
description = 'A dashboard with metric information'
notify_list = ['sheltowt@gmail.com']


api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     notify_list=notify_list)
