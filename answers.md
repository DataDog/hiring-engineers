
Welcome to my answer page for the Challenge, I really liked doing it and I'm looking forward to hearing from you if you have feedback.
All the best,
Charly

My document is divided in two parts, the first one is a pragmatic text that lists my answers to the challenge step by step.
The second is the V0 of a tutorial, based on my attempt to do the challenge using the collaborative node.js APIs. 
[Link to the answers for the challenge in Python](#challenge)

[Link to the tutorial in Node.js](#tutorial)

----------

##Challenge 
This part is dedicated to the answers of the questions for the coding challenge of [Datadog](datadoghq.com). I chose to do the challenge using python, given the fact that the library for python was really well documented. My knowledge in python is only about signal processing yet. You'll find here, my answers for the different levels, step by step. With my reflexions and the troubleshoot I faced, with the solution I found.
##Level 1
####Installation of the Agent
The Agent can be downloaded on the Free Trial tab on the web site of Datadog. The installation can be done via the terminal. Once all the basics information registered, we can get some insights from our local machine.
![Dashboard of my local machine](https://lh3.googleusercontent.com/mbPLXpy05oTBscUV8xEqFEgvK4R1OnIsrlnmSi6rZrI=s0 "Dashboard_local.png")
-----
####What is the Agent?
The Datadog Agent is piece of software that runs on your hosts. Its job is to faithfully collect events and metrics and bring them to Datadog on the behalf of the.
The Agent has three main parts: the collector, dogstatsd, and the forwarder.
- The collector runs checks on the current machine for whatever integrations and it will capture system metrics like memory and CPU.
- Dogstatsd is a statsd backend server you can send custom metrics to from an application.
- The forwarder retrieves data from both dogstatsd and the collector and then queues it up to be sent to Datadog.
This is all controlled by one supervisor process.
---
####Event via the API
![API_Keys](https://lh3.googleusercontent.com/uvepCImNCyIdrTOHNU7BZZ6_HifK4n-43660FvRuS9I=s0 "API_Keys.png") 

The very first step to submit an event via the API is to create an API key and an Application key. This can be found under the integration/APIs section. By using python we can easily create an event that will be shown on the Event section create those keys. Begin by installing Datadog via your terminal with the command.
![API_Init](https://lh3.googleusercontent.com/126Dn-Vs4W_jsyRohspkWuF656k_wQnLBWefVD_D5hQ=s0 "API_Init.png")
![API_Event](https://lh3.googleusercontent.com/nZTee79Lt0J11w6obfjYMkWOa6ZrzwHijnxtWsOiNYg=s0 "API_Event.png")

First off, you import the libraries and then load your API keys. Finally, create your event with the title, the text etc, you can go to the documentation to see all the option that you can use. Then submit the event, and if you get the good status, you’ll see in your feed of event, what you just submitted.
![Event](https://lh3.googleusercontent.com/Z3nCQnxjYycWHm3DTFoOeXmt3B7QpYL_l2m5RYCVjpM=s0 "Event.png")
---
####Event in the mailbox

You can trigger the evolution of some data, for instance the number of views on a webpage. Then if the number goes beyond a limit that you set, you can chose to be alerted. 

![Event_Mail](https://lh3.googleusercontent.com/ino1Zs-yXH6raQTTvaWOBbDva1WkKO2JSt6Qe2TMQtY=s0 "Event_mail.png")

First, create a monitor and select a metric that you want to supervise. Chose to be alerted by mail if this very metric is higher than a limit. Now, we can simulate an activity and check that the monitoring is working. This short python function will do it:

![Snippet_PageView](https://lh3.googleusercontent.com/enXypuSYl08g2IoUnBcjdR2tlPyucR14njxiVdz3lPs=s0 "Snippet_IncreasePageView.png")

Now we use this function to trigger the alarm, either by calling this function several times or by submitting an event through the API:
>#####api.metric.send(metric='web.page_views', points=1000)

Then, has expected we receive the mail that alerts us :

![Mail](https://lh3.googleusercontent.com/NW7TpOTtsT4icWD5-kOqigYc_FlrSKwI-98VXs-AJ78=s0 "Mail.png")

----------


##Tutorial
In this second part, I'd like to propound a tutorial. At first, I tried to do the challenge with the Node.js APIs but the hard time I had trying to figure out the ways to reach the results, made me thinking that it could be useful to have a tutorial. The basis is still the same, the challenge, yet the reasons why I'm doing it are the following:

 - The documentation for the Node.js API is not sufficient for someone that isn't familiar with it
 - Showing my abilities to convey a clear message, which is one of the most important asset needed in this job.
 

----------

