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

### Event was created and sent to my datadog Event feed via API:
![Event Feed](http://s2.postimg.org/gzyy04o6h/Screen_Shot_2015_07_23_at_10_16_39_AM.png "Event Feed")
####•	Get an event to appear in your email inbox (the email address you signed up for the account with)####


![Emailed Event](http://s13.postimg.org/n1qqbp8jb/Screen_Shot_2015_07_23_at_10_15_29_AM.png "Event sent to email")


##Level 2
####•	Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

For this exercise in particular I decided to create a test application in flask. This amateur local web application has two views, home page and page one, so that I can gather and compare metrics for both pages. I used vegeta for load testing as a personal preference. 

Average Page View Per Second <a href="https://app.datadoghq.com/graph/embed?from_ts=1437584620112&to_ts=1437671020112&token=5dfb1586fcad56d9d558c727f3142c533ebe45e34c8a13475eac2886cacd01ea&height=300&width=600&legend=true&tile_size=m&live=true">Link</a> while running load test

![alt text](http://s23.postimg.org/s1wy9r4x7/Screen_Shot_2015_07_23_at_1_02_46_PM.png "Average Page View Per Second")



####•	Create a histogram to see the latency; also give us the link to the graph


Shows average latency in blue and 95th percentile latency, for page views, while running the load test.
![alt text](http://s12.postimg.org/6v4bnfn8t/Screen_Shot_2015_07_23_at_12_02_15_PM.png "Logo Title Text 1")

##Level 3
####Using the same web app from level 2:

####•	tag your metrics with support (one tag for all metrics)

Showing support tag in page views graph.

![Support Tag](http://s29.postimg.org/4g53h6o5z/Screen_Shot_2015_07_23_at_1_07_55_PM.png "Page Views with Support Tag")

####•	tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1with page:page1)

Created a decorator function so that the view names, 'page:hello_word' and 'page:page_one', would be appended to tags. 
![Decorator](http://s24.postimg.org/kv3m7l385/Screen_Shot_2015_07_23_at_1_28_56_PM.png "Decorator")

####•	visualize the latency by page on a graph (using stacked areas, with one color per page)

Displaying latency using stacked areas of home page and page one
![alt text](http://s23.postimg.org/n3immpfvv/Screen_Shot_2015_07_23_at_11_59_11_AM.png "Logo Title Text 1")

##Level 4
####Same web app:
####•	count the overall number of page views using dogstatsd counters.

Graph showing the overall number of page views using dogstatsd counters:

![Total Views](http://s14.postimg.org/ct6al1l8h/Screen_Shot_2015_07_23_at_12_05_49_PM.png "Sum of Views")


####•	count the number of page views, split by page (hint: use tags)
####•	visualize the results on a graph


![Views Per Page](http://postimg.org/image/hn7cvqdkh/ "Total Views PP")

####•	Bonus question: do you know why the graphs are very spiky?


##Level 5
####Let's switch to the agent.
####•	Write an agent check that samples a random value. Call this new metric: test.support.random



####•	Visualize this new metric on Datadog, send us the link.