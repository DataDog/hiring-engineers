Your answers to the questions go here.

##Level 1

####•	Sign up for Datadog, get the agent reporting metrics from your local machine

Metrics from my laptop, Stephens-MBP(Clone):
![Stephen-MBP](http://s4.postimg.org/5lfzxjoi5/Screen_Shot_2015_07_23_at_10_03_56_AM.png "My MBP")


####•	Bonus question: what is the agent?

The datadog agent is an open-source software that runs on your hosts. The agent's job is to collect data, including metrics and events, which is sent to the Datadog dashboard. 

####•	Submit an event via the API.

Step 1: Setup API and APP keys:

![API key](http://s28.postimg.org/881loryzh/Screen_Shot_2015_07_23_at_10_12_59_AM.png "Logo Title Text 1")
![APP key](http://s4.postimg.org/mqbjothhp/Screen_Shot_2015_07_23_at_11_02_29_AM.png "Logo Title Text 1")

Event was created and send to my datadog Event feed:
![Event Feed](http://s2.postimg.org/gzyy04o6h/Screen_Shot_2015_07_23_at_10_16_39_AM.png "Event Feed")
####•	Get an event to appear in your email inbox (the email address you signed up for the account with)####

Event appeared in my email:
![Emailed Event](http://s13.postimg.org/n1qqbp8jb/Screen_Shot_2015_07_23_at_10_15_29_AM.png "Event sent to email")


##Level 2
####•	Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

For this exercise in particular I decided to create a test application in flask. This amateur local web application has two views, home page and page one, so that I can gather and compare metrics for both pages. I used vegeta for load testing as a personal preference. 

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

####•	Create a histogram to see the latency; also give us the link to the graph

<a href="">Latency Graph</a>
Further description of graphs
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

##Level 3
####Using the same web app from level 2:

####•	tag your metrics with support (one tag for all metrics)

Showing support tags in graph

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

####•	tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1with page:page1)

image with tags
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

####•	visualize the latency by page on a graph (using stacked areas, with one color per page)

Displaying latency using stacked areas of home page and page one
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

##Level 4
####Same web app:
####•	count the overall number of page views using dogstatsd counters.

Graph showing the overall number of page views using dogstatsd counters:
image
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")


####•	count the number of page views, split by page (hint: use tags)
####•	visualize the results on a graph

image
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

####•	Bonus question: do you know why the graphs are very spiky?


##Level 5
####Let's switch to the agent.
####•	Write an agent check that samples a random value. Call this new metric: test.support.random



####•	Visualize this new metric on Datadog, send us the link.