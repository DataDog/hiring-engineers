##Your answers to the questions go here.

### Level 1 - Collecting your Data

* Bonus question: In your own words, what is the Agent?

> The Agent is a program that runs on my local machines. It's responsible for collecting various information, including custom metrics, and sending it to Datadog to be analyzed.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

```
# Set the host's tags
tags: mytag, env:prod, role:database, eric_rocks
```

<img src="http://imgur.com/YJ8eODc.png">

* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

test.py:

```python
from random import random

from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random())
```

test.yaml:

```YAML
init_config:

instances:
    [{}]
```

### Level 2 - Visualizing your Data
* Since your database integration is reporting now, clone your database intergration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.

<img alt = "timeboard" src="http://imgur.com/RwzF4DJ.png">

* Bonus question: What is the difference between a timeboard and a screenboard?

> A timeboard is a synchronized dashboard used for viewing a number of metrics at once. The entire dashboard can be adjusted based on the range in time needed. Additionally each metric is locked into identically sized boxes. A screenboard is a much more flexible and open ended dashboard. It does not force synchronicity and allows elements to take any size. Rather than being used to compare metrics, it's simply used as a common location for any type of element one might want on screen at a time. This includes custom notes and images.

* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

<img name="box" src="http://imgur.com/6uHcw2J.png">

### Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  
* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes 

<img alt="set_alert" src="http://imgur.com/VuKbnof.png">

* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  

<img alt="multialert" src="http://imgur.com/nSFHLu7.png">

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.
* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

<img class = "email" src="http://imgur.com/Vo2HOmZ.png">

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

<img alt="scheduled_downtime" src="http://imgur.com/4g6Vy1b.png">
