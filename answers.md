Your answers to the questions go here.

### Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.
I successfully installed the agent on my macbook pro running OS X 10.11 beta without
any issues.

* Bonus question: what is the agent?
The agent is the software that runs on your hosts. It collects metrics and events and stores them on Datadog so you can view them all in one place. 

There are three parts to the agent. The collector checks on your current machine integrations and captures system metrics such as CPU usage and memory. Dogstatsd is the statsd backend server that allows you to send custom metrics to and from an application. The forwarder queues and sends the data from collector and dogstatsd to Datadog.

* Submit an event via the API.
To send an event through the API I installed datadog with pip and used the example template for posting an event from the Datadog API reference page. I plugged in my api and app keys and changed the strings used for the event to the following:

title = "This is an event"
text = 'And it was submitted via the API @jeremygbrubaker@gmail.com'

Then I ran the Python file "eventsubmit.py" from the command line and the event posted successfully.

This could be useful since we could set the title and text to error message strings within our applications and send them to our Datadog events list.

Links to images
Command Line: http://jeremygbrubaker.com/images/level1-command.png
API Python Code: http://jeremygbrubaker.com/images/level1-eventsubmit.png

* Get an event to appear in your email inbox (the email address you signed up for the account with)
To send an email to someone you just use @ followed by their email (though I believe their username works too). The event I submitted through the API made it to my inbox as well.

Email: http://jeremygbrubaker.com/images/level1-email.png


### Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.
* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!
* Create a histogram to see the latency; also give us the link to the graph
* Bonus points for putting together more creative dashboards.