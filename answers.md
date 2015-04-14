Hi there, Datadog Support Engineering Team - I'm Kaleigh.  I currently live/work in Seattle, WA and I am very excited about the oportunity to work with you! 

Level 1

1.1 Sign up for Datadog, get the agent reporting metrics from your local machine.

After signing up for a free trial I installed the Datadog Agent and started seeing metrics reported from my local machine (we'll call him Mac, heh). 
Here is a screenshot: 
http://cl.ly/image/011F3Z1E351t
Here is a screenshot of my local machine's Datadog dashboard: 
http://cl.ly/image/192j3s0q0d2D

1.2 Bonus question: what is the agent? 
The agent is a piece of software that interacts with a host (in this case, Mac), collects metrics and events, and sends that information back to Datadog.  The user can then display/graph/analyze their metrics in a variety of useful and aesthetically pleasing ways!

1.3 Submit an event via the API.
I submitted an event via the API (using Terminal) following the syntax in the API docs.
Here is a screenshot of the Terminal input/response: 
http://cl.ly/image/383G3J3z3b1B
Here is a screenshot of the event on the Datadog Events page: 
http://cl.ly/image/0U3E1p382h2S

1.4 Get an event to appear in your email inbox.
Getting an event to appear in your email inbox is as easy as commenting on an event using "@user_email@mailclient.com" then adding a message.  In my case, it looked like this: 
http://cl.ly/image/3F0Z2I1y2M04

Alright team, thanks for reading along so far.  For Levels 2 through 5 I made a simple guestbook web app (using Python) and deployed it on GAE. You can find the app here: 
http://academic-ocean-89522.appspot.com

I decided to install Datadog's Google App Engine Integration prior to instrumenting my code with dogstatsd - I was curious to see if I could get the 'default' metrics reporting prior to adding custom metrics. Configuration went well until I tried to set up my application URL (http://academic-ocean-89522.appspot.com/datadog) - then I got an Error 500 - Interal Server Error.  Interestingly, I didn't get this error if I left the /datadog off the application URL, but I didn't see metrics reporting either.

Level 2

2.1 Take a simple web app and instrument your code with dogstatsd.
I ran into various ImportErrors while using DataDogPy with my existing Google App Engine project - a couple of examples of error text:
http://cl.ly/image/0a141b180407
http://cl.ly/image/2d00061d1c3s

Here is my proposed strategy for the rest of this exercise - as a member of the Support Team, if a client reported a similar issue or asked for guidance completing any of the remaining tasks in Levels 2-5, I would have a variety of resources at my disposal to present to the client (i.e., documentation, example code snippets, example metric visualizations, the development team, etc.) For the remainder of the challenge, I would like to approach each question from a "here is what I/the client could do to complete this task" standpoint.  I realize it is a somewhat unorthodox approach - but I would argue that it still provides a valuable perspective on the way I approach and solve problems. Thanks for sticking with me so far! Now, let's get back to instrumenting code with dogstatsd.

After library installation (from pip or source), the Datadog.api Python client library requires us to run the initialize method first, as shown in the Quick Start Guide (https://github.com/DataDog/datadogpy).
Here is a screenshot of instrumented example code:
http://cl.ly/image/1C0E1X3Y0j0m

2.2 While running a load test for a few minutes, visualize page views per second. 

There are several tools for running load tests: ab and Tsung (as mentioned in the References), as well as services like Load Impact (https://loadimpact.com/).

As for visualizing page views per second, we can use statsd and follow the syntax shown in the documentation (http://docs.datadoghq.com/guides/metrics/) to count page views. In this case, we can set up a counter which is normalized over the flush interval to report per-second units.  
Here is a screenshot of instrumented example code, as well as a screenshot of an example Web Page Views graph from the documentation:
http://cl.ly/image/2n0f3P0K0m0d
http://cl.ly/image/3U3Y2j200x3C

2.3 Create a histogram to see the latency.
When visualizing latency, we can again use statsd and follow the syntax shown in the documentation (http://docs.datadoghq.com/guides/metrics/). In this case, we measure the response time of a webpage and we can sample each response time with the metric 'web.page.latency'.
Here is a screenshot of instrumented example code, as well as a screenshot of an example histogram from the documentation:
http://cl.ly/image/3X2T140U2A3X
http://cl.ly/image/0Q3F0Z081X0m

2.4 Bonus points for putting together more creative dashboards.
Here is a screenshot of an additional dashboard I created using the metrics from my local machine: 
http://cl.ly/image/3g1C343M2U0l

Level 3

3.1 Tag your metrics with support (one tag for all metrics). 
We can add a tag to all metrics following the syntax shown in the documentation "Add Tags To A Host" section (http://docs.datadoghq.com/api/#tags). 
Here is a screenshot of instrumented example code: 
http://cl.ly/image/0A1D1r1l1x2R

3.2 Tag your metrics per page.
Similar to the above case, we can follow the syntax shown in the documentation "Add Tags To A Host" section, but this time we can take advantage of the key-value structure of tags to break down metrics per page (example pages: home, about, portfolio, contact). 
Here is a screenshot of instrumented example code: 
http://cl.ly/image/072d2p3n0J0M

3.3 Visualize the latency by page on a graph (using stacked areas, with one color per page).
Using our 'web.page.latency' metric from earlier, we can visualize latency per page by opening up our Graph Editor and following the syntax shown in the documentation for Stacked Areas (http://docs.datadoghq.com/graphing/). 
Here is a screenshot of what our Graph Editor JSON tab looks like for this task:
http://cl.ly/image/2L3U1p3B1j27
Here is a screenshot of an example graph using stacked areas from the Top Dog Training (https://www.datadoghq.com/top_dog_training/great-dane/) sections:
http://cl.ly/image/0s3w0X0V0n1H

Level 4

4.1 Count the overall number of page views using dogstatsd counters.
To count overall page views, we can use statsd and follow the syntax shown in the documentation (http://docs.datadoghq.com/guides/metrics/).  
Here's a screenshot of instrumented example code:
http://cl.ly/image/2n0f3P0K0m0d

4.2 Count the number of page views, split by page.
To count page views, split by page, we can use statsd and follow the syntax shown in the Datadogpy documentation Increment section (http://datadogpy.readthedocs.org/en/latest/index.html).
Here is a screenshot of instrumented example code:
http://cl.ly/image/1F2y3G2S2y36

4.3 Visualize the results on a graph.
Using the 'web.page_views' metric, we can visualize page views, split by page, by opening up our Graph Editor and editing the JSON tab following the documentation syntax for Timeseries graphs (http://docs.datadoghq.com/graphing/). We could also use a Stacked Areas graph like the one explored in Level 3, question 3. 
Here is a screenshot of what our Graph Editor JSON tab looks like for this task, as well as a screenshot of an example multi-line time series:
http://cl.ly/image/1m3G2s2q1016
http://cl.ly/image/0W0P3U1p2t3a 

4.4 Bonus question: do you know why the graphs are very spiky?
Counters are normalized over the flush interval to report per-second units. This small timescale leads to spiky graphs since data is refreshed and a datapoint is added each second- if the timescale were per-minute or per-hour, the graphs would likely be less spiky since second-to-second fluctuations would not be captured between datapoints. 

Level 5

5.1 Write an agent check that samples a random value. Call this new metric: test.support.random.
The agent check that samples a random value follows similar syntax to the "My First Check" example shown in the documentation (http://docs.datadoghq.com/guides/agent_checks/) - notable changes were importing the 'random' library and altering the self.gauge() method to include the 'test.support.random' metric and it's sampled value of random.random().
Here are screenshots of the config file (random_test.yaml) and the check file (random_test.py):
http://cl.ly/image/0e23120L3G0o
http://cl.ly/image/0H3X2o162m3T

5.2 Visualize this new metric on Datadog. 
This challenge wouldn't be complete without one more ImportError, would it? 
Here is a screenshot from the Terminal:
http://cl.ly/image/3e0k2F401M1p

In any case, if we wanted to visualize this new metric in Datadog we would first check that the metric (test.support.random) was showing up in our Metrics Summary.  Using the Metrics Explorer, we could graph test.support.random and save this graph to a new or existing dashboard.  The graph will be a timeseries and will likely be as spiky as the other graphs we've seen throughout the exercise - with values ranging between [0.0, 1.0).  

This concludes my submission to the challenge - I would like to take this opportunity to thank you all for your consideration! I still have a lot to learn and I am very much looking forward to the opportunity to meet/work with you.  Also, special thanks to the two Marketing Team members (David Tritto and Darren Hazeltine) who reached out to me during my Free Trial!  Please let me know if you have any questions or if any additional information is needed - I can be reached via email at gerlich.kaleigh@gmail.com or at (720)988-6887.

Cheers!
Kaleigh




