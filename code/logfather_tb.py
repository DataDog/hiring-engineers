# Import necessary entities
from datadog import initialize, api

options = {
    # Find your keys here:
    # https://app.datadoghq.com/account/settings#api
    'api_key': '****************************************',
    'app_key': '****************************************'
}

initialize(**options)

# Title displayed on the top of the Timeboard
title = "Logfathers Timemachine"

# Let everyone know your intentions as to what this timeboard was created for.
description = "This timeboard presents everything that is necessary to become a successful sales engineer for Datadog. Arf." 

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:logfather_cpu{*}"},
            {"q": "avg:logfather_cpu{*}.rollup(sum, 60)" }
        ],
        "viz": "timeseries"
    },
    "title": "CPU usage scoped over the host Logfather"
},

{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:logfather_cpu{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "# of CPU Anomalies"
}]

template_variables = [{
    "name": "Logfathers Timemachine", # REQUIRED. The name of the variable
    "prefix": "", #OPTIONAL. The tag prefix associated with the variable. Only tags with this prefix appear in the variable dropdown.
    "default": "" # OPTIONAL. The default value for the template variable on dashboard load.
}]

read_only = True # Make sure nobody can manipulate your timeboard

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
