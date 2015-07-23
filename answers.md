Your answers to the questions go here.

##Level 1

####•	Sign up for Datadog, get the agent reporting metrics from your local machine

Metric from my laptop, Stephens-MBP(Clone):
![Stephen-MBP](http://s4.postimg.org/5lfzxjoi5/Screen_Shot_2015_07_23_at_10_03_56_AM.png "My MBP")


####•	Bonus question: what is the agent?

The datadog agent is an open-source software that runs on your hosts. The agent's job is to collect data, including metrics and events, which is sent to the Datadog dashboard. 

####•	Submit an event via the API.

Step 1: Setup API and APP keys:

Images
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

The above event was sent to my Events tab on Datadog.

Event appeared in my email:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")


##Level 2
####•	Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

For this exercise in particular I decided to create a test application in flask. The amateur application has two views, home and page one, so that I can gather and compare metrics for both pages. I used vegeta for load testing as a personal preference. 

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

####•	Create a histogram to see the latency; also give us the link to the graph
Latency of the graph avg
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