# Level 1

## Sign up for Datadog, get the agent reporting metrics from your local machine.

Successful installation!

![installation](images/level1-1-1.png)

Metrics reported from my local machine!

![local_metrics](images/level1-1-2.png)

## Bonus question: What is the agent?

The Datadog agent is software that runs on host machines to collect events and metrics. The data is then sent to
Datadog where it is presented in an easy to read format for clients.

The Datadog agent is comprised of

* The Collector - Runs checks on the host and captures system metrics.
* Dogstatsd - A statsd backend server that receives custom metrics from applications.
* The Forwarder - Responsible for forwarding data from "The Collector" and "Dogstatsd" to Datadog.

## Submit an event via the API.

[Full code found here!](code/level1.py)

"""
# Submit an event via the API.
print api.Event.create(title="My First Event!", text="This event was created via the Datadog API.")
"""

"""
Response:
{
    u'status': u'ok',
    u'event': {
        u'date_happened': 1430266475,
        u'handle': None,
        u'title': u'My First Event!',
        u'url': u'https://app.datadoghq.com/event/event?id=2785078421481329528',
        u'text': u'This event was created via the Datadog API.',
        u'tags': None,
        u'priority': None,
        u'related_event_id': None,
        u'id': 2785078421481329528
    }
}
"""

![api_event](images/level1-3-1.png)

## Get an event to appear in your email inbox (the email address you signed up for the account with)

[Full code found here!](code/level1.py)

"""
# Submit an event via the API and send out an email notification.
print api.Event.create(title="My First Email Event!", text="@cs.Li.Kevin@gmail.com This event was created via the Datadog API.")
"""

"""
Response:
{
    u'status': u'ok',
    u'event': {
        u'date_happened': 1430267871,
        u'handle': None,
        u'title': u'My First Email Event!',
        u'url': u'https://app.datadoghq.com/event/event?id=2785101829824845689',
        u'text': u'@cs.Li.Kevin@gmail.com This event was created via the Datadog API.',
        u'tags': None,
        u'priority': None,
        u'related_event_id': None,
        u'id': 2785101829824845689
    }
}
"""

![email_event_1](images/level1-4-2.png)

![email_event_2](images/level1-4-1.png)