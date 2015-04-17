###Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.

Here are some metrics from my laptop:
![https://app.datadoghq.com/dash/46764](http://i.imgur.com/ysGS9y3.png "sdfd") 

* Bonus question: what is the agent?

The agent is a mysterious program/dog who collects server events/metrics from the host computer and reports them to Datadog so they can be displayed in cool graphs. Metrics are collected both from the system (CPU load, available memory, etc) and apps using dogstatsd.

* Submit an event via the API.

Here's the code I used to submit an event in case a user forgot to fill out a form on my [GitHub FollowBack](http://githubfollowback.projects.benhgreen.com) app:
```
title = 'Empty form!'
text = 'Someone didn\'t fill out the page\'s form :( ' \
       'better notify @ben@benhgreen.com!'
print api.Event.create(title=title, text=text)
```

and here's the event appearing on the site!

![](http://i.imgur.com/MCJc5kC.png) 


* Get an event to appear in your email inbox (the email address you signed up for the account with)

Here's that same event appearing in my inbox:
![](http://i.imgur.com/rdArpYa.png) 

##Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.

Here's some code ready to collect views (and latency) on the project's main page:
```
@app.route('/', methods=['GET', 'POST'])
def root():
    start_time = time.time()
    form = SubmitForm()
    if form.validate_on_submit():
        return redirect("https://github.com/login/oauth/authorize?"
                        "client_id=%s"
                        "&scope=user:follow"
                        "&state=%s" % (GITHUB_CLIENT_ID, form.group.data))
    duration = time.time()-start_time
    statsd.increment('web.page_views')
    statsd.histogram('home.render.time', duration)
    return render_template('base.html', welcome='welcome', form=form)
```

* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

Here's a graph showing some *sick* traffic to my site:
![https://app.datadoghq.com/graph/embed?from_ts=1429152158097&to_ts=1429238558097&token=a82cd3097e0a0dc4faf585220d9d4bad1dc702d559a4a0d7367e6384d5fb0394&height=400&width=800&tile_size=m&live=true](http://i.imgur.com/NEOWfU9.png) 

* Create a histogram to see the latency; also give us the link to the graph

!["https://app.datadoghq.com/graph/embed?token=09438077384e7fcde67579df56f125f819c8b20d33998ce13072dfb138b5542d&height=300&width=600&legend=true" width="600" height="300" frameborder="0"](http://i.imgur.com/tLOxmax.png)

* Bonus points for putting together more creative dashboards.

This is easily the most useful graph that I have ever thought of in my career as a dev.
![](http://i.imgur.com/aocSGN7.png)  

### Level 3

Using the same web app from level 2:
* tag your metrics with `support` (one tag for all metrics)

```
statsd.increment('web.page_views', tags=['support'])
```
* tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with `page:page1`)

```
statsd.increment('web.page_views', tags=['support', 'page:home'])
statsd.increment('web.page_views', tags=['support', 'page:success'])
```
...and so on.

* visualize the latency by page on a graph (using stacked areas, with one color per `page`)

![https://app.datadoghq.com/graph/embed?token=e8c8c16227c1d6dd49feb8d144b1e534ca2e48256a1e476c6574bb5d6c36acb8&height=300&width=600&legend=true" width="600" height="300" frameborder="0"](http://i.imgur.com/PM3Lezq.png)

Light grey is the home page, darker grey is the success page. The success page doesn't have too much to generate (no forms) so it's way faster.

### Level 4

Same web app:

* count the overall number of page views using dogstatsd counters.

!["https://app.datadoghq.com/graph/embed?token=a1ec740198653230dd9c184dd7e8cb988c78a9ee7978fc0f133503b085edc3bf&height=300&width=600&legend=true" width="600" height="300" frameborder="0"](http://i.imgur.com/6KuU9UK.png) 

* count the number of page views, split by page (hint: use tags)
* visualize the results on a graph

!["https://app.datadoghq.com/graph/embed?token=5a55cb1003dfcf1631e66e7f3c21711e82747679aa80ea79aee075557f4829af&height=300&width=600&legend=true" width="600" height="300" frameborder="0"](http://i.imgur.com/bNMx8yx.png) 
* Bonus question: do you know why the graphs are very spiky?

My graphs weren't zoomed in very much, but if I had to guess I'd say the agent is separating the events into time frames such that the 'natural' smooth curve is lost (basically the same thing that would happen if you took a very fine graph of page views per millisecond and converted it to a bar graph with 5sec in each bucket).

### Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`

Here's my .py file from `/opt/datadog-agent/agent/checks.d/ben.py`...
```
import random
from checks import AgentCheck

class BenCheck(AgentCheck):
	def check(self, instance):
		self.gauge('test.support.random', random.random())
```
...and my config from `/etc/dd-agent/conf.d/ben.yaml` 
```
init_config:

instances:
    [{}]
```
* Visualize this new metric on Datadog, send us the link.

!["https://app.datadoghq.com/graph/embed?token=eba6c06059d62a4129ca1d07a45d3a55fca962946332d6b580a469a22cdf84af&height=300&width=600&legend=true" width="600" height="300" frameborder="0"](http://i.imgur.com/XAEpevH.png) 

Here are links to [my system metrics dash](https://app.datadoghq.com/dash/46764), and [my web app metrics dash.](https://app.datadoghq.com/dash/46759) Links to each graph can be found in the graph image's alt-text.
