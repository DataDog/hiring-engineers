Your answers to the questions go here.

DataDog Support Engineer

Questions

Level 1

Sign up for Datadog, get the agent reporting metrics from your local machine.

Bonus question: what is the agent? The agent is a python application.

Submit an event via the API.
Get an event to appear in your email inbox (the email address you signed up for the account with)


Level 2

Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!



Create a histogram to see the latency; also give us the link to the graph

Bonus points for putting together more creative dashboards.

Level 3

Using the same web app from level 2:



tag your metrics with support (one tag for all metrics)
tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1 with page:page1)
visualize the latency by page on a graph (using stacked areas, with one color per page)

I wasn’t too sure about the tags.  I just added the tags:support in the JSON file.






Level 4

Same web app:
count the overall number of page views using dogstatsd counters.
count the number of page views, split by page (hint: use tags)

from datadog import statsd
from datadog import initialize, api

options = {
'api_key': 'ac81c6ade2a16a2f03454b85f2454d98',
'app_key': '3d97cba3556209ca74fb88d4c16e21c3adcad133'
}

initialize(**options)

statsd.gauge('web.page_views', 1000)

visualize the results on a graph


Bonus question: do you know why the graphs are very spiky?
Graphs are spiky because of the sampling rate.


Level 5

Let's switch to the agent.

Write an agent check that samples a random value. Call this new metric: test.support.random

Unfortunately, I keep getting:
ImportError: No module named checks

Visualize this new metric on Datadog, send us the link.
