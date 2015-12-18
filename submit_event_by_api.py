__author__ = 'stephenlechner'

# This is just a test file to demonstrate how to submit an event to datadog
# via the API.

# I took this and altered it from "http://docs.datadoghq.com/api/"

from datadog import initialize, api

options = {
    'api_key': 'b79f2e891614183a0a6fded2c1d2301b',
    'app_key': 'test_api_key123asd145124gw5987'
}

initialize(**options)

title = 'this is an event'
text = 'but it is really just a test. in fact, nothing much happened. ' \
       '@stephenlechner@gmail.com'
tags = ['tag:test']

api.Event.create(title=title, text=text, tags=tags)

