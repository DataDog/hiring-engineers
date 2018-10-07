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
    'week_days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
}

start = 1538985600 # monday 7th of october 19:00:00
finish = 1539036000 # tuesday 8th of october 09:00:00
message = 'There will be scheduled downtime of alerts from 7pm to 9am each weekday. @edmundcong1@gmail.com'

resp = api.Downtime.create(
    scope='host:ubuntu-xenial',
    start=start,
    message=message,
    end=finish,
    timezone='Australia/NSW',
    monitor_id=6611157,
    recurrence=recurrence
)

