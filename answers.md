
***Welcome*** to my answer page for the Challenge. 

I really liked doing it and I'm looking forward to hearing from you if you have feedback.

All the best,
*Charly*.

My document is divided in two parts, the first one is a pragmatic text that lists my answers to the challenge step by step.
The second is the V0 of a tutorial, based on my attempt to do the challenge using the collaborative node.js APIs.

[Link to the answers for the challenge in Python](#challenge)

Here is a table to smooth your navigation throughout my report
- [Level1](#level1)
- [Level2](#level2)
- [Level3](#level3)
- [Level4](#level4)
- [Level5](#level5)
- [Troubleshoot](#troubleshoot)

[Link to the tutorial in Node.js](#tutorial) (Coming soon)

----------

##Challenge 
This part contains the answers of the questions for the coding challenge of [Datadog](datadoghq.com). I chose to do the challenge using python, given the fact that the library for python was really well documented. My knowledge in python is only about signal processing yet. You'll find here, my answers for the different levels, step by step. With my reflexions and the troubleshoot I faced, with the solution I found.
##Level1
####Installation of the Agent
The Agent can be downloaded on the Free Trial tab on the web site of Datadog. The installation can be done via the terminal. Once all the basics information registered, we can get some insights from our local machine.
![Dashboard of my local machine](https://lh3.googleusercontent.com/mbPLXpy05oTBscUV8xEqFEgvK4R1OnIsrlnmSi6rZrI=s0 "Dashboard_local.png")
-----
####What is the Agent?
The Datadog Agent is piece of software that runs on your hosts. Its job is to faithfully collect events and metrics and bring them to Datadog on the behalf of the user.
The Agent has three main parts: the collector, dogstatsd, and the forwarder.
- The collector runs checks on the current machine for whatever integrations and it will capture system metrics like memory and CPU.
- Dogstatsd is a statsd backend server you can send custom metrics to from an application.
- The forwarder retrieves data from both dogstatsd and the collector and then queues it up to be sent to Datadog.
This is all controlled by one supervisor process.
---

####Event via the API
![API_Keys](https://lh3.googleusercontent.com/uvepCImNCyIdrTOHNU7BZZ6_HifK4n-43660FvRuS9I=s0 "API_Keys.png") 

The very first step to submit an event via the API is to create an API key and an Application key. This can be found under the integration/APIs section. By using python we can easily create an event that will be shown on the Event section. Begin by setting up Datadog API via your terminal with the command.
<img src="https://lh3.googleusercontent.com/126Dn-Vs4W_jsyRohspkWuF656k_wQnLBWefVD_D5hQ=s0" width="450" height="70" />

<img src="https://lh3.googleusercontent.com/nZTee79Lt0J11w6obfjYMkWOa6ZrzwHijnxtWsOiNYg=s0" width="550" height="120" />

First off, you import the libraries and then load your API keys. Finally, create your event with the title, the text etc, you can go to the [documentation](http://docs.datadoghq.com/api/) to see all the option that you can use. Then submit the event, and if you get the good status, you’ll see in your feed of event, what you just submitted.
![Event](https://lh3.googleusercontent.com/Z3nCQnxjYycWHm3DTFoOeXmt3B7QpYL_l2m5RYCVjpM=s0 "Event.png")
---
####Event in the mailbox

You can trigger the evolution of some data, for instance the number of views on a webpage. Then if the number goes beyond a limit that you set, you can chose to be alerted. 

![Event_Mail](https://lh3.googleusercontent.com/ino1Zs-yXH6raQTTvaWOBbDva1WkKO2JSt6Qe2TMQtY=s0 "Event_mail.png")

First, create a monitor and select a metric that you want to supervise. Chose to be alerted by mail if this very metric is higher than a limit. Now, we can simulate an activity and check that the monitoring is working. This short python function will do it:

<img src="https://lh3.googleusercontent.com/enXypuSYl08g2IoUnBcjdR2tlPyucR14njxiVdz3lPs=s0" width="450" height="70" />

Now we use this function to trigger the alarm, either by calling this function several times or by submitting an event through the API:
>#####api.metric.send(metric='web.page_views', points=1000)

Then, has expected we receive the mail that alerts us :

![Mail](https://lh3.googleusercontent.com/NW7TpOTtsT4icWD5-kOqigYc_FlrSKwI-98VXs-AJ78=s0 "Mail.png")

----------
##Level2
I took a really simple web application in python with which you can vote for different subjects, with an admin page to create questions and change the choices or see the statistics.
The code is available on demand, but here are the way I integrated the code to get insights from my app.

#####The load test & the latency
To compute the latency and the page views, I used the following code, inspired from the documentation for the API in python ([Documentation](http://docs.datadoghq.com/api/)) :
![Code to get the latency and the page view](https://lh3.googleusercontent.com/464foJZMBXAZ7DxojjUtLPQknZia5f_MRDN-buIA89E=s0 "ExtractCode_Latency.png")

Then, to do a load test, after going through the [references](https://httpd.apache.org/docs/2.2/programs/ab.html), I wrote the following command:
> admin$ ab -n 1000 -c 10 -t 180 https://calm-caverns-8773.herokuapp.com/

Troubleshoot : The command didn't work with my local webserver at first, I had to install some addictional lib. cf [Troubleshoot](#troubleshoot).
Which gave me the following result (I throw away some lines to make it clearer)

>This is ApacheBench, Version 2.3
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/
Benchmarking calm-caverns-8773.herokuapp.com (be patient)
Finished 3562 requests
Server Software:        Cowboy
Server Hostname:        calm-caverns-8773.herokuapp.com
Document Path:          /
Concurrency Level:      10
Time taken for tests:   180.002 seconds
Complete requests:      3562
Failed requests:        0
Requests per second:    19.79 [#/sec] (mean)
Time per request:       505.340 [ms] (mean)
Time per request:       50.534 [ms] (mean, across all concurrent requests)

You can see the graph on my Datadog account at the following [link](https://app.datadoghq.com/dash/48571/testpython?from_ts=1430868324514&to_ts=1430868624514&tile_size=m&tile_focus=58807842), and this is a screenshot of it: 
![Link to the load testing graph](https://lh3.googleusercontent.com/iM4ucN8Yc1dUG1HuGczOsY8AgpCimHq6vhl9knMcmb4=s0 "PageView_AveragePerSecond.png")
We can see in this chart that the average number of views is computed as a rate/sec.
NB: I did several simulations, with different parameters to see the behaviour of the load testing tool.

Concerning the latency, on the next chart is displayed the latency for both pages (coming for the Level 3), and the[link](https://app.datadoghq.com/dash/48571/testpython?from_ts=1430868329000&to_ts=1430868629000&tile_size=m&tile_focus=58821836). 
![enter image description here](https://lh3.googleusercontent.com/FV8fuAMyKUdtM4d_g0Dq6BcxeGUgB58PaZ6F7LHfVcw=s0 "Latency_differentTags_Detail.png")
The value seems good according to the documentation of Datadog, that states that a latency lower than 1s is acceptable. 

####The Creative Chart
![Creative Chart](https://lh3.googleusercontent.com/G4NcofrE7os0vYUWlopwydMUtC8OAZ1HXAox_S2Zey4=s0 "OriginalGraph.png")
For this chart I decided to display 3 data streams that are strongly correlated. Indeed, the number of sent packet, the latency and the page views, show the reactivity of the web site to a certain 'stimulation'. Plus, we can identify the pattern of system reactivity with the input (number of packet sent), the behaviour of the system (which is the latency) and the output of the system (which is the page views). I chose to display with 3 different type of representations and color so it is clearer.
PS: I wanted to correlate with my system's data (network IO, CPU...) but the values were too different to be represented together, and I didn't find an easy way (without coding) to compute a log scale.

----------
##Level3

####Latency of each page in a stack
Using the very same web app, I introduce tags in the code (can be seen on the command for the latency of Level2), and I access to the tag filter as in the following image:

![Selection of the tags](https://lh3.googleusercontent.com/fTQOzD8smOYD4v7JP9O7RSdo6gJlbqfmKGfNokRln_o=s0 "TagSelection.png")

After tagging all my pages, I ran 3 threads of load testing, and displayed a stack graph of the latency of each page.

![Latency per page](https://lh3.googleusercontent.com/seIEl7liuRHV6VL9ZK-GNpUCGrCPhMPTZAF_g6gCTeE=s0 "Latency_StackLayer.png")

We can see that the sollicitations are different and more importantly, one sollicitation stopped earlier than the other (page /, tagged as N/A).
 
----------
##Level4
####Counting the pages with Dogstatsd
This graph sums up everything concerning the page views.
![Global Page Views](https://lh3.googleusercontent.com/FwhjJQCvCPzUFtiAvCnhFHDgsMwNSm3ngLfKUiuwC7A=s0 "CountOfPages_StackedLines.png")
Indeed, the dotted lines reprensent each page (only two of them are represented). And the stack graph on the background helps to see the sum of both, as we can see the yellow part stands for the sum, and we can distinguish every contribution by it's position in the stack (i.e. the orange represents the contribution of the detail page).
Additionally, I've been using the dogstatsd since the very beginning to increment my variables.

####Bonus Question:
The graphs are spiky because of the flushing of the data stream. The flow of data goes way faster on one side of the system, so even though the refreshing is fast, the pace cannot be captured at it's finest. Maybe the interpolation between two point is done linearly, in which case it could be improved with a least squares method or a Lagrange polynomial method.

----------
##Level5

 As stated in the [documentation](http://docs.datadoghq.com/guides/agent_checks/), the agent writing is pretty straight forward.
 The very first step is to create a new file which can be called [test.yaml](https://github.com/CharlyF/hiring-engineers/blob/master/Code/test.yaml), it will be responsible for the initialisation. And the script in python [test.py](https://github.com/CharlyF/hiring-engineers/blob/master/Code/test.py) will provide a random value, which will basically prove that the system is up and running and thus we have succeeded to set our own agent check.
Here is the[link](https://app.datadoghq.com/dash/48571/testpython?from_ts=1430877484194&to_ts=1430879289747&tile_size=m&tile_focus=58826549) to my dashboard and a screenshot of the agent writing graph:
 ![Agent wrinting Graph](https://lh3.googleusercontent.com/71d7l2BSawTuaJeMomSB_Z7Xm2lSsIxtyA5BgRFmuak=s0 "AgentWriting_RandomGraph.png")
----------

###Troubleshoot
Here is a non exhaustive list of the issues I faced, and the solution I found:
- Running the ab load testing in local wasn't possible I faced the following status: "apr_pollset_poll: The timeout specified has expired (70007)" I imported other libraries and run a few upgrades such as: pip --upgrade ndg-httpsclient, pip install requests==2.5.3;pip install pyopenssl. Plus, I add the option -s for the timeout. 
My solution was first to deploy my site on a heroku server, and then I figured out that I reached the limit of requests, so I just decreased it and it worked.
- Often, I faced problem with python and the import of the datadog library, I had to move the folders like the datadog folder so it can be imported, another way is to change the path.
- The @statsd query didn't work for some reason that I didnt' understand, but there is another way to do according to the API documentation. 
- I tryed to run my site on a localserver and on my heroku server on the same time, and I didn't succeed to get the insight of the source of the generation of the data on the graph. I assume it can be done if we look at the UUID or the sourcename.
- I had to restart the Agent to be sure that all the changes were taken into account
---------
##Tutorial
In this second part, I'd like to propound a tutorial. At first, I tried to do the challenge with the Node.js APIs but the hard time I had trying to figure out the ways to reach the results, made me thinking that it could be useful to have a tutorial. The basis is still the same, the challenge, yet the reasons why I'm doing it are the following:

 - The documentation for the Node.js API is not sufficient for someone that isn't familiar with it
 - Showing my abilities to convey a clear message, which is one of the most important asset needed in this job.
 

----------

