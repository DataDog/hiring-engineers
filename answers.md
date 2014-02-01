<strong>Level 1</strong>

Sign up for Datadog, get the agent reporting metrics from your local machine. (done)


Bonus question: what is the agent?  

The agent is called: ddagent.exe.  It looks like software running on my computer that collects events and metrics from it and sends that to Datadog.


Submit an event via the API.


Get an event to appear in your email inbox (the email address you signed up for the account with)


<strong>Level 2</strong>

Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.
While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!
Create a histogram to see the latency; also give us the link to the graph
Bonus points for putting together more creative dashboards.


<strong>Level 3</strong>

Using the same web app from level 2:

tag your metrics with support (one tag for all metrics)
tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1 with page:page1)
visualize the latency by page on a graph (using stacked areas, with one color per page)


<strong>Level 4</strong>

Same web app:

count the overall number of page views using dogstatsd counters.
count the number of page views, split by page (hint: use tags)
visualize the results on a graph
Bonus question: do you know why the graphs are very spiky?


<strong>Level 5</strong>

Let's switch to the agent.

Write an agent check that samples a random value. Call this new metric: test.support.random
Here is a snippet that prints a random value in python:
