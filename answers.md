Your answers to the questions go here.

### Level 1

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the agent reporting metrics from your local machine.
![Successful Signup](./imgs/agent_setup.png "Signup")
![Metrics](./imgs/reporting_metrics.png "Metrics")

* Bonus question: what is the agent?

The Agent collects events and metrics to send them back to DataDog for monitoring purposes. The agent has three components - the collector, dogstatsd, and the forwarder. The collector captures system metrics on a local machine like memory and CPU. The dogstatsd is a backend server that collects custom metrics from an app. The forwarder consolidates information from both the collector and dogstatsd to send to DataDog.

* Submit an event via the API.
* Get an event to appear in your email inbox (the email address you signed up for the account with)

![Submit Event Code](./imgs/event_submit_code.png "Submit Event Code")
![Submit Event Email](./imgs/event_submitted_email.png "Submit Event Email")

### Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.
* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

I ran a few load tests from between 100 and 1000 requests, and here's the graph:
[Page Views](https://app.datadoghq.com/graph/embed?token=d9e3121636f7d3d9886f5fd13fe40c2cd0f4b53dac505bb6f21dce508b7b37e9&height=300&width=600&legend=true)
![Page Views](./imgs/page_views.png "Page views")
* Create a histogram to see the latency; also give us the link to the graph
![Average Latency](./imgs/latency.png "Average Latency")
[Average Latency](https://app.datadoghq.com/graph/embed?token=6387f0c7caba0fa2e0506dd60cf52e403b5dc263bd4a0daf3f8f40af84e8ccd3&height=300&width=600&legend=true)

* Bonus points for putting together more creative dashboards.

### Level 3

Using the same web app from level 2:
* tag your metrics with `support` (one tag for all metrics)
I've added this code to my application controller:
![Tag metrics with Support](./imgs/tags_part_1.png "Support tag")
* tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)
To do this, I added a few methods in the controller to add tags for the main page (questions/index), and the user signup page (users/new).
![Tag metrics part 2](./imgs/tags_part_2.png "Support tag part 2")
* visualize the latency by page on a graph (using stacked areas, with one color per `page`)
Here the dark blue shows the questions page and light blue shows new user page.
![Latency with tags](./imgs/latency_by_page.png "Latency with tags")

### Level 4

Same web app:
* count the overall number of page views using dogstatsd counters.
* count the number of page views, split by page (hint: use tags)
I can count the number of page views by page using the tags we created in level 3. In the chart options, if I select the following, I can see each page as a different color.
![Chart Selection](./imgs/chart_selection.png "Chart Selection")
* visualize the results on a graph
![Page views by page](./imgs/tags_part_3.png "Page views by page")
* Bonus question: do you know why the graphs are very spiky?
The graphs are spiky because the load tests executes the page calls at once. In my case in particular, I was telling the load test to send 100 requests at once for both kinds of pages, so that's when the spike occus.

### Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`
* Visualize this new metric on Datadog, send us the link.

Here is a snippet that prints a random value in python:

```python
import random
print(random.random())
```

I followed the instructions but could not get the visualization to work, and I'm not sure why. First, I created a file called random.yaml in the conf.d directory:
![YAML file](./imgs/five_one.png "YAML file")
Then I created a Python file in the checks.d folder implementing the random number generator:
![Python file](./imgs/five_two.png "Python file")
But after running PYTHONPATH=. python checks.d/http.py, I could not get the metrics to generate. Not sure what's going on here.