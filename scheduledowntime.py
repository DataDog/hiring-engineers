# I wrote this code with the plan of using the REST API to schedule downtime for my monitor before I figured out that I could do it
# with the UI.  So, I did not actually use this.

# One problem I had with the API is that the syntax and example only talked about specifying a scope, not about specifying a monitor id.

from datadog import initialize, api
import time

options = {
    'api_key': 'hidden',
    'app_key': 'hidden'
}

initialize(**options)

# Repeat for 14  hours starting at 7pm each night until 9am the next morning indefinitely.
start_ts = int(1479686400)
end_ts = start_ts + (14 * 60 * 60)

recurrence = {
    'type': 'days',
    'period': 1
}

# Schedule downtime
api.Downtime.create(scope='env:staging', start=start_ts, end=end_ts, recurrence=recurrence)
