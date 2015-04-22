Thank you taking the time to review my coding challenge and I look forward to speaking with members of the team regarding this opportunity.

Obligatory Excitement Gif
![StormTroopersDance](http://i.giphy.com/mzTKsByk8Xl6g.gif)

### Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.

![Screen Shot of the Datadog dashboard after initial setup](dashboarddd.png)
![Screen Shot of Terminal Success Message](terminalsuccess.png)

* Bonus question: what is the agent?

The Datadog Agent is a program that collects metrics and events and sends this information to Datadog for analysis.  The Agent serves as the worker for the online portal which displays all the information to the user in easy to use dashboards.

* Submit an event via the API.

Code for initial event creation from API Docs

```ruby
require 'rubygems'
require 'dogapi'


api_key = "f1ef993e5fb3d4d7eddf8bd3be232971"

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new("This is the intial setup event for the datadog support engineer hiring challenge", :msg_title => "First Event Submission"))
```
And the screenshot showing successful submission:

![Screen Shot of Terminal Success Message](event1.png)

* Get an event to appear in your email inbox (the email address you signed up for the account with)

Code for creation of email notification event:

```ruby
require 'rubygems'
require 'dogapi'


api_key = "f1ef993e5fb3d4d7eddf8bd3be232971"

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new("Now submitting a second event to showcase the email alert system, @asdvaughan@gmail.com", :msg_title => "Email Notification"))

```

Email screenshot from Gmail:

![Screen Shot of Terminal Success Message](email.png)

Datadog Screenshot:

![Screen Shot of Terminal Success Message](emaildata.png)

### Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.
* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!
* Create a histogram to see the latency; also give us the link to the graph
* Bonus points for putting together more creative dashboards.

### Level 3

Using the same web app from level 2:
* tag your metrics with `support` (one tag for all metrics)
* tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)
* visualize the latency by page on a graph (using stacked areas, with one color per `page`)

### Level 4

Same web app:
* count the overall number of page views using dogstatsd counters.
* count the number of page views, split by page (hint: use tags)
* visualize the results on a graph
* Bonus question: do you know why the graphs are very spiky?

### Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`
* Visualize this new metric on Datadog, send us the link.

Here is a snippet that prints a random value in python:

```python
import random
print(random.random())
```
