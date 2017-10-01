# Stig's answers

Hey Datadogs - my name is Stig and I've had he pleasure of going through your hiring exercise. 
These are my answers, screenshots and links - enjoy :)

## Pre-reqs
FYI - I chose to use my private MacBook. First of all because I was curious about what the agent is able to pull our of it. And secondly I was too lazy to set up the vagrant and virtualbox stuff to get my environment running. 
So - my private Mac is what you'll see. It is rather old as well, so this should be a great challenge :)

## Collecting metrics
I added 2 screenshots here. One is my Hostmap after installing the initial agent, postgres, the integration and adding the tags (agent and user). In the second one (no bonuspoints expected!) I played with the grouping. It doesn't make too much sense when only monitoring one host, but it adds some context to the map (which I like).
Not sure if you can access my Datadog user, but added the links as well (just in case)

![Alt text](screenshots/Stigs-Hostmap.png?raw=true "Hostmap")
[Stig's Hostmap](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false ".. hope it works!")

![Alt text](screenshots/Stigs-grouped-Hostmap.png?raw=true "Hostmap")
[Stig's grouped Hostmap](https://app.datadoghq.com/infrastructure/map?mapid=3556&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=role%2Cenv&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false ".. hope it works!")

And now to the custom check. I started off writing the hello.world check - just to check how things worked. Then I wrote the random_number check. Instead of writing a random number function or using something like randint, I chose to ask for it through a public API I have used in the past, which delivers the random number and additionally a fun fact about that number. Reason for it was that I wanted to test the events as well. To not clog the event list (although the aggregation string works well), I only send an event for numbers < 100.

I used the documented <i>min_collection_interval</i> to set the collection interval to 45 seconds. It doesn't seem to be 100% accurate though, I see the metrics mostly in 1 minute intervals in the metric explorer. I didn't find another way to do it though.

<b>Bonus question:</b> Is there another way to change the collection interval? 
I am really not sure, but my best guess is that it can changed globally in the agent configuration. It could probably be programmed as well (in the .py).

Attached code+config is [random_number.py](src/random_number.py) and [random_number.yaml](src/random_number.yaml).

And here are screenshots of the metric explorer and events:

My Metric
![Alt text](screenshots/Stigs-metric.png?raw=true "Metric")

My event
![Alt text](screenshots/Stigs-event.png?raw=true "Events")

## Visualizing Data
Here I actually experienced some problems using the API. First of all, I didn't get it working with Python. When running my script, it ended with the message that the datadog module can not be found. I'm sure it is my environment, and something isn't set correctly. But I didn't want to spend time troubleshooting, so I tried the Shell approach.
The Shell API worked fine when adding my own metric in host-scope, but when I added the anomaly function I got an error:

`{"errors": ["Error(s) found in query:\nError parsing query: \n unable to parse anomalies(avg:postgresql.max_connections{*}, basic, 6): Rule 'scope_expr' didn't match at ', 6)' (line 1, column 51)."]}`

The rollup function works fine, so in the spirit of "quick and dirty", I just added the anomaly function manually in my timeboard.
I have attached the [not_working](src/create_timeboard_not_working.sh) and [working](src/create_timeboard.sh) script for reference.

Here are the screenshots I saved for this exercise.

My Timeboard (Past day)
![Alt text](screenshots/Stigs-timeboard-1d.png?raw=true "Timeboard (Past day)")

My Timeboard (5 minutes)
![Alt text](screenshots/Stigs-timeboard-5m.png?raw=true "Timeboard (5 minutes)")

Taking a snapshot
![Alt text](screenshots/Stig-takes-snapshot.png?raw=true "Taking snapshot")

Snapshot in Event list
![Alt text](screenshots/Stigs-snapshot-eventlist.png?raw=true "Snapshot in Event list")

I would have expected to receive an email with the snapshot (or a notification) as well, but so far I haven't received one.

<b>Bonus question:</b> What is the Anomaly graph displaying? 
The anomaly graph helps us understand how my metric is behaving, compared to what is "normal". The normal can be calculated in different ways (based on the use case), but it typically has an historical component built into it. For example: understanding how the metric behaved the past few Fridays, helps us predict what we expect this, and future, Fridays. Vendors use different names for this kind of visualization, another commonly used term is Baseline or baselining.
The following screenshot shows how the anomaly algorithm learns normal behavior over time.

![Alt text](screenshots/Stigs-anomaly-graph.png?raw=true "Learning normal behavior")

## Monitoring Data
Here are the screenshots for this part of the exercise:

Monitor definition (step 1 & 2)
![Alt text](screenshots/Stigs-monitor-top.png?raw=true "Monitor definition")

Monitor definition (step 3 & 4)
![Alt text](screenshots/Stigs-monitor-bottom.png?raw=true "Monitor definition")

Notification email - no data (during a break I closed my laptop :))
![Alt text](screenshots/Stigs-notification-no-data.png?raw=true "Notification no data")

Notification email - warning
![Alt text](screenshots/Stigs-notification-warning.png?raw=true "Warning notification")

<b>Bonus exercise:</b> Scheduled downtime.
Since I started this exercise on a weekend and will end it on a weekend, I won't receive an email (until Monday morning). I've added the downtime definitions as screenshots - hope that serves "answer" as well :)

Downtime Mo-Fr 7am-9am
![Alt text](screenshots/Stigs-daily-silencer.png?raw=true "Downtime definition")

Downtime weekend
![Alt text](screenshots/Stigs-weekend-silencer.png?raw=true "Downtime definition")

## APM
Now, this should be my parade discipline since I have some experience in this field - but APM is not APM. I am having trouble getting the ddtrace to report the traces and run into these 2 warnings (app starts up anyway):

If I start the app with ddtrace-run I get the following error:
`ERROR:ddtrace.writer:cannot send services: [Errno 61] Connection refused`

If I just instrument the code (following the flask documentation) I get the following warning:
` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
No handlers could be found for logger "ddtrace.writer"`

I have added the code (basically the code from the exercise + the tracer lines) here. Maybe I did something wrong, wouldn't be the first time ;) Anyway - this task was a fail for me!

<b>Bonus Question:</b> What is the difference between a Service and a Resource?
Without really knowing how Datadogs define these terms, my interpretation would be that a Service is the application (end-to-end) as a whole, and a Resource is a component (backend-DB, web-server, etc.) that is part of the Service.

## The Final Question
I have been thinking about this throughout the exercise, and in the end you can monitor just about anything if you have the right handles and interfaces for it :) That is pretty cool - the framework is flexible. 
As a sales-driven technician, one neat use case could be to monitor the state of an opportunity in whatever opportunity tracking tool you are using. Let's face it - noone looks at that anyway ;) A Slack notification, and the whole team can tale part in celebrating progress and success.
