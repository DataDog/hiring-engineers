import datadog_setup
from datadog import api

# Submit an event via the API.
print api.Event.create(title="My First Event!", text="This event was created via the Datadog API.")

# Submit an event via the API and send out an email notification.
print api.Event.create(title="My First Email Event!", text="@cs.Li.Kevin@gmail.com This event was created via the Datadog API.")