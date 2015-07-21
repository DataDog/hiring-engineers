##Level 1

####•	Sign up for Datadog, get the agent reporting metrics from your local machine

Metrics from my laptop, Design-PC:
![Local Dashboard](https://36.media.tumblr.com/2e1cc4782a36345409d1e3361bed6fc1/tumblr_nrqz5qGxjL1ubyepco1_1280.png)

####•	Bonus question: what is the agent?

The Datadog Agent is a piece of open-source software that runs on the host computer. Once downloaded, it begins collecting metrics from your system and applications. The backend server that is bundled with the agent, Dogstatsd, then receives and aggregates these metrics so they can be forwarded to Datadog and displayed graphically.

####•	Submit an event via the API.

First I setup my API and Application Keys:

![API Keys](https://40.media.tumblr.com/a4a118f20c9e8c9d90d550907c785856/tumblr_nrr01j1osZ1ubyepco1_1280.png)<br>


Then I downloaded the Datadog Python Library...<br>
![Download DD Python Lib](https://41.media.tumblr.com/f34674423e9d73b3b3d0bbea12ffb334/tumblr_nrqzimrVZL1ubyepco1_500.png)<br>
and submitted an event via the API using Python in the terminal:
![Submit Event in Terminal](https://41.media.tumblr.com/cdc3014223313cb75497c1d22c5b3cd2/tumblr_nrqzv8a10y1ubyepco1_1280.png)<br>

The above commands result in an event posting to my Datadog event feed:
![Event](https://41.media.tumblr.com/ef1fe79ee280423dbb0decaf381b09b1/tumblr_nrr0aiZswe1ubyepco1_1280.png)

####•	Get an event to appear in your email inbox (the email address you signed up for the account with)####

You can send an event to a particular email address by tagging the email in the event's text:
![Tag Email](https://40.media.tumblr.com/0ad9f16b8df09e3d5df99d9e7d738b65/tumblr_nrr0jl9Fha1ubyepco1_1280.png)<br>

Here's the event appearing in my inbox:

![Email](https://40.media.tumblr.com/f65236a3d1bbf0645279046299f36e8d/tumblr_nrr0uzFjm01ubyepco1_1280.png)

##Level 2
####•	Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

I created a very basic app using Python and the Flask framework. The user inputs two numbers into a form and then clicks a button that adds the numbers and displays the sum (nothiing flashy, just bare bones for the sake of this exercise). This could be expanded to include more mathematical operations and build a full calculator. 
App link: https://mysterious-bastion-5857.herokuapp.com/

####•	While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

Once my code was instrumented with the Datadog API imports and metric functions, I did a load test using Pylot Web Performance Tool (http://www.pylot.org/). As seen in the image below, the GUI allows me to specify the number of agents, total rampup time, interval between requests, and test duration. The test urls are specified in an XML file that is provided as a command line argument when starting Pylot.<br>
![Pylot](https://40.media.tumblr.com/7fc5c66ae23e422db41deda77ab09405/tumblr_nrr2ifpjR51ubyepco1_1280.png)

The graph below (http://tinyurl.com/o7aekh5) shows the average page views per second while running the above test:

![Load Test Page Views](https://36.media.tumblr.com/aed0b8901c935ad953ca2041f9b54b4b/tumblr_nrr2wgcKrl1ubyepco1_1280.png)

####•	Create a histogram to see the latency; also give us the link to the graph
Here is some code that determines the latency and implements the histogram metric anytime the page view count is incremented:

![Latency Code](https://41.media.tumblr.com/dd3ae7b64bf31c28f0c9aa439f2293f2/tumblr_nrr3ksAsFp1ubyepco1_400.png)<br>

The graph below (http://tinyurl.com/oqkpk86) shows the avg (blue) and 95th percentile (yellow) page view latency while running the load test:

![Latency Graph](https://40.media.tumblr.com/2fc7f19bf40f7da42076f55da60abee7/tumblr_nrr3o8Zugp1ubyepco1_540.png)

##Level 3
####Using the same web app from level 2:
####•	tag your metrics with support (one tag for all metrics)

Code showing the page view count increment function now tagged with "support":
![Support Tag](https://40.media.tumblr.com/0470364449266ac2549ac18de4923775/tumblr_nrrf3n4Lop1ubyepco1_500.png)

With the above code in place, I can edit my graph now so it plots over the "support" tag. The tag is then visible when I scroll over the graph:

![Graph Tagged with "support"](https://40.media.tumblr.com/6969c5fc13b7b8bc76ce13889457aa0b/tumblr_nrrfg6I2H41ubyepco1_1280.png)

####•	tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1with page:page1)

Metrics are now tagged by page name (either home_page or addition_page). The page name is passed into the function based on which page calls it.

![Tags by Page](https://41.media.tumblr.com/9e11d1e1461df8a1d5859761af96a619/tumblr_nrrgauBR4Z1ubyepco1_1280.png)

####•	visualize the latency by page on a graph (using stacked areas, with one color per page)

![Stacked Areas](https://41.media.tumblr.com/513e351298560ca97a73c1ad283632a9/tumblr_nrrgtypUl21ubyepco1_1280.png)

##Level 4
####Same web app:
####•	count the overall number of page views using dogstatsd counters.

Graph showing the total page views at any given time:
![Total Page Views](https://40.media.tumblr.com/c647efd3344827890b29312201e1933f/tumblr_nrrhns6CiK1ubyepco1_1280.png)

The function can be integrated over this time period to display the total number of page views with a Toplist visualization:

![Integrated](https://40.media.tumblr.com/e1d1a7449f733263cd88b5c50aa72b99/tumblr_nrrif4NvW01ubyepco1_1280.png)

####•	count the number of page views, split by page (hint: use tags)
####•	visualize the results on a graph

The same amount of requests were sent to each page so the view counts of each individual page are equal and add up to the combined page view count:
![Graph Page Views By Page](https://40.media.tumblr.com/2db6aa0bde8ce8d00a9dd3bf8a1e5ce5/tumblr_nrrjlxsi9h1ubyepco1_1280.png)

####•	Bonus question: do you know why the graphs are very spiky?
I believe the graphs are spiky because not all the raw data is plotted, which would result in a smoother curve. Dogstatsd aggregates many data points into one metric every 10 seconds (by default). It doesn't know the exact metric at an exact point in time (i.e. the exact number of page views at a given second); rather, it knows there were a certain number of page views in a certain interval, and normalizes over that interval.

##Level 5
####Let's switch to the agent.
####•	Write an agent check that samples a random value. Call this new metric: test.support.random

Configuration file that goes into C:\ProgramData\Datadog\conf.d
```
init_config:

instances:
[{}]

```
Python script that generates a random number and sends metric to Datadog goes into C:\Program Files (x86)\Datadog\Datadog Agent\checks.d

![Agent Check](https://41.media.tumblr.com/15d9402d2f2b7899a55dd05e85120272/tumblr_nrropr0FHt1ubyepco1_500.png)

####•	Visualize this new metric on Datadog, send us the link.

I launch the Python Shell and enter the commands shown below but am getting a scanner error that's expecting a colon in a .pyc file. This is preventing me from outputting the random value metric to Datadog. Currently troubleshooting.

![Python Shell](https://36.media.tumblr.com/a0f94ac6f1deac8ebd60c4b520e9ed1a/tumblr_nrtd8gKS6k1ubyepco1_1280.png)
