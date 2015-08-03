Your answers to the questions go here.

### Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.
I successfully installed the agent on my macbook pro running OS X 10.11 beta without
any issues.

* Bonus question: what is the agent?
The agent is the software that runs on your hosts. It collects metrics and events and stores them on Datadog so you can view them all in one place. 

There are three parts to the agent. The collector checks on your current machine integrations and captures system metrics such as CPU usage and memory. DogStatsD is the statsd backend server that allows you to send custom metrics to and from an application. The forwarder queues and sends the data from the collector and DogStatsD to Datadog.

* Submit an event via the API.
To send an event through the API I installed datadog with pip and used the example template for posting an event from the Datadog API reference page. I plugged in my api and app keys and changed the strings used for the event to the following:

title = "This is an event"
text = 'And it was submitted via the API @jeremygbrubaker@gmail.com'

Then I ran the Python file "eventsubmit.py" from the command line and the event posted successfully.

This could be useful since we could set the title and text to error message strings within our applications and send them to our Datadog events list.

![Command Line] (http://jeremygbrubaker.com/images/level1-command.png)
![API Python Code] (http://jeremygbrubaker.com/images/level1-eventsubmit.png)

* Get an event to appear in your email inbox (the email address you signed up for the account with)
To send an email to someone you just use @ followed by their email (though I believe their username works too). The event I submitted through the API made it to my inbox as well.

![Email] (http://jeremygbrubaker.com/images/level1-email.png)


### Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.
I recently learned Python and played a bit with Django by creating a Polling App using their tutorial. I went ahead and instrumented that project with dogstatsd. 

By following the metrics guide I installed datadog using pip so that I able to import statsd into my python code. Then I created a file called 'dogstatsd.py' which had the methods that could help create the **metrics**.

'''
def increase_counter():
    """ Increments page view count """
    statsd.increment('web.page_views')
    return "It works!"
'''

Then in my views.py I had to include 'dogstatsd' and modify the method for retrieving the index so that it would have statsd increment the page counter for that webpage.

'''
# From views.py
def index(request):
	increase_counter()
	# If we don't flush the session the datadog graph only shows one page view.
	request.session.flush()
	return render_to_response('home/index.html', context_instance=RequestContext(request))
'''

Then running 'ab -n 8000 -c 10 http://127.0.0.1:8000/' on the command line would load the page multiple times over a couple of minutes. I messed around with the command until the graphs turned out satisfactory looking.

**NOTE:** I noticed when I first did this my page views for "web.page_views" would only show one view . When I flushed the session (like in the code above) then each page load actually counted. This wouldn’t be a problem if multiple users from around the world were loading the page.


* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

I must have a very popular website!

![Page views from 4 minutes] (http://www.jeremygbrubaker.com/images/level2-pageviews.png)

* Create a histogram to see the latency; also give us the link to the graph
Next, when it came to latency I added another method in my "dogstatsd.py" file. It looked like this:

'''
def latency():
	""" Creates histogram showing latency """
	start = time.time()
	duration = time.time() - start
	statsd.histogram('web.page_latency', duration)
	increase_counter()
	return "It's done!"
'''

This also increased the counter, so in the views.py file I called "latency()" instead of "increase_counter()". Now dogstatsd is reporting latency and page hit count!

![Latency histogram] (http://www.jeremygbrubaker.com/images/level2-latency.png)

* Bonus points for putting together more creative dashboards.

![Dashboard] (http://www.jeremygbrubaker.com/images/level2-dashboard.png)


### Level 3

Using the same web app from level 2:
* tag your metrics with `support` (one tag for all metrics)
This was simple enough. To tag my metrics with 'support' I modified my dogstatsd.py methods to include tags like so:

'''
statsd.histogram('web.page_latency', duration, tags = ["support"])
statsd.increment('web.page_views', tags = ["support"])
'''

When testing this again I noticed that my graphs now had the support tag, and I would see 'support' when I highlighted that data within the graph.

* tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)

Since the tag would change depending on which page was being visited, I had to do some modifications to my dogstasd.py file again.

'''
def latency(page_tag):
	""" Creates histogram showing latency """
	start = time.time()
	duration = time.time() - start
	statsd.histogram('web.page_latency', duration, tags = ["support", page_tag])
	increase_counter(page_tag)
	return "It's done!"

def increase_counter(page_tag):
    """ Increments page view count """
    statsd.increment('web.page_views', tags = ["support", page_tag])
    return "cool"
'''

Now when the latency method was called from a view, it provided a string specifying what page it was. That was used so statsd knew which page to create a histogram for, and which page to increase the counter for. If someone visited /results, that page count was increased instead of index.

For this to work I had to fix some classes and methods in the views.py file.

'''
class IndexView(generic.ListView):
	"""
	Displays all current polls.
	"""
	latency("page:polls")
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	def get_queryset(self):
		return Question.objects.filter(
        	pub_date__lte=timezone.now()
    	).order_by('-pub_date')[:5]

def index(request):
	latency('page:home')
	# If we don't flush the session the datadog graph only shows one page view.
	request.session.flush()
	return render_to_response('home/index.html', context_instance=RequestContext(request))

def page(request):
	latency('page:page2')
	request.session.flush()
	return render_to_response('home/page.html', context_instance=RequestContext(request))
'''

...and so forth. 

* visualize the latency by page on a graph (using stacked areas, with one color per `page`)

Here we have three different colors. One for each page. In this case I had only run AB to load 3 different pages at the same time.

![Histogram 1] (http://www.jeremygbrubaker.com/images/level3-histogram1.png)
![Histogram 2] (http://www.jeremygbrubaker.com/images/level3-histogram2.png)

### Level 4

Same web app:
* count the overall number of page views using dogstatsd counters.
To count the overall number of page views I used toplist and selected the sum of the host for 'web.page_views'. This gave an overall large number, as it should since they were all summed up.

![Sum of all hits] (http://www.jeremygbrubaker.com/images/level4-sum.png)

* count the number of page views, split by page (hint: use tags)
To split the results I had it display each by tag, ordered by most hits. It was as easy as setting 'break it down by' to 'page' instead of ‘host’. In this case page2 won!

![Hits split up] (http://www.jeremygbrubaker.com/images/level4-split.png)

* visualize the results on a graph

![Hits split up visualized on graph] (http://www.jeremygbrubaker.com/images/level4-all.png)

* Bonus question: do you know why the graphs are very spiky?
DogStatsD aggregates many points into a single metric over 10 seconds by default (according to the guide). Since the Apache benchmark was sending so many requests at once not all of the raw data was able to be plotted, so I guess you could say it's more of an estimate.

### Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`
* Visualize this new metric on Datadog, send us the link.

Following the guide to writing the agent check I started by creating a 'agentcheck.yaml' file with the following contents:

'''
init_config:

instances:
    [{}]
'''

This was placed in datadog-agent/etc/conf.d/. There was no 'datadog-agent/agent/conf.d/' as the instructions had said. 

Next I created the agentcheck.py file and placed it within 'datadog-agent/agent/checks.d/'

'''
from checks import AgentCheck
import random

class Check(AgentCheck):
	"""Samples a random value using 'test.support.random' as the metric"""
	def check(self, instance):
		self.gauge('test.support.random', random.random())
'''

I ran a test to make sure it worked:

![Test from command line] (http://www.jeremygbrubaker.com/images/level5-test.png)


Here is the visualization of test.support.random:

![test.support.random] (http://www.jeremygbrubaker.com/images/level3-visualization.png)