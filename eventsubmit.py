# Submits an event to datadog

from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

title = "This is an event"
text = 'And it was submitted via the API @myemailhere'
tags = ['version:1', 'application:web']

api.Event.create(title=title, text=text, tags=tags)
