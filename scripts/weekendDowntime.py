from datadog import initialize, api # import our modules from data dog
import time

# set our api and app keys so we can authorise with datadog
options = {
    'api_key': 'de80ad2a1bffe3273e4765ac1b8a85d7',
    'app_key': '490954065d91b99b46fc59efc4a748141fae365b'
}
# pass in our options dictionary object
initialize(**options)

recurrence = {
    'type': 'weeks',
    'period': 1,
    'week_days': ['Sat', 'Sun'],
}

start = 1539349199 # friday the 12th of october at 11:59:59pm gmt+11
finish = 1539521999 # sunday the 14th of october at 11:59:59pm gmt+11
message = 'There will be scheduled downtime of alerts from 11:59:59pm friday to 11:59:59pm sunday. @edmundcong1@gmail.com'

resp = api.Downtime.create(
    scope='host:ubuntu-xenial',
    start=start,
    end=finish,
    message=message,
    monitor_id=6611157,
    timezone='Australia/NSW',
    recurrence=recurrence
)

