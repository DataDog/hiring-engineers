# Answers for Support Engineer Test
# Done by Mohamed ElNokali

## Level 1: Collecting your Data
-------------------------------
### What is an Agent ?

An agent is a piece of software, a computer program which perform some functions and tasks in the background and allows you to collect metrics and system events from your host machine like CPU, Memory Usage, Disk space and also customs metrics. 

DataDog agent sends metrics to DogStasD which is responsible for collecting and aggregating the Data and send them back to DataDog servers where they can be visualized on the Datadog app for monitoring. 

Here is My Custom Agent [Screenshot](https://www.flickr.com/photos/157378248@N06/36466718365/in/dateposted-public/)


### The Agent is reporting from my machine [moe.dell](https://app.datadoghq.com/dash/host/323828476?live=true&page=0&is_auto=false&from_ts=1502299262684&to_ts=1502302862684&tile_size=m)


### My Custom Agent [screenshot](https://www.flickr.com/photos/157378248@N06/36466718365/in/dateposted-public/)



## Level 2: Visualizing your Data
---------------------------------
### Postrgres Database Dashboard URL with the test.support.random metric reporting graph --> [HERE](https://app.datadoghq.com/dash/334682/postgres---metrics-overview?live=true&page=0&is_auto=false&from_ts=1502287456564&to_ts=1502301856564&tile_size=m)


### What is the difference between a timeboard and a screenboard ?

**A timeboard** 
	-  Used more in troubleshooting. 
	-  Takes you deeper in the graphs for more detailed info about what is really happening.
	-  The graphs can be shared one by one.
	-  All the board is showing graphs for the same timeframe like (The past hour, the past 4 hours ....etc) for the whole board.

**A Screenboard**
	-  Used more for an overall system visual
	-  Can be customized with a wide range of widgets like Images, Event Stream, Status Checks....etc
	-  The whole board is shared at once, not graphs individually
	-  Perfect to be used on TVs for status sharing for the whole Team 


### The snapshot of test.support.random graph passing 0.9 [screenshot](https://www.flickr.com/photos/157378248@N06/36466718245/in/dateposted-public/)

NB: As you can see in the screenshot, I managed to do the snapshot with mentioning my name, mail using @ but I didn't receive any mail in my Inbox
But I well received the monitoring alerts, so my mail is not the culprit, may be I missed something


# Level 3: Alerting your Data
------------------------------

- You can see my monitoring [here](https://app.datadoghq.com/monitors#2611791?group=triggered&live=4h)

- According to the monitoring alert, I got notified by mail, you can see the screenshot [here](https://www.flickr.com/photos/157378248@N06/35659115843/in/dateposted-public/) 

- Scheduled a daily downtime for my alert, You can check the downtime [here](https://app.datadoghq.com/monitors#downtime?id=241415350) and the screenshot of the downtime [here](https://www.flickr.com/photos/157378248@N06/36070316670/in/dateposted-public/) 

