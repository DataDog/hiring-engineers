Your answers to the questions go here.
Prerequisites - Setting Up The Environment

I began by trying to install VirtualBox & Vagrant. It took me a while to figure out exactly why I wasn’t able to get it working - I’m using a Mac with an M1 chip. A curse of the early adopter.

Image(1) - Mac M1 chip issue

Image(2) - Installation of the agent in Ubuntu VM

I tried to use Docker, but I ran into similar issues. I found articles and videos online with tutorials using Parallels Desktpop to set up Ubuntu, so I decided to go with that. It was pretty easy to see up and I went with the Ubuntu 20.04 version, and installed the Datadog Agent.

Image(3) - Agent Reporting Metrics, Local Machine

I was unsure of the ‘Agent Reporting Metrics’ request, so I ran ‘sudo datadog-agent status’ in the Ubuntu terminal to get the current status of the agent on my machine

Collecting Metrics:

Image(4) - Adding Tags to the Agent config file

I decided on the below tags that were of some relevance to where I was at the time:
-General location
-Version of Ubuntu 
-Type of machine used

Image(5) - View from Host Map

Image(6) - MongoDB setup

Initially I started with a MySql database, but I kept running into errors with the ‘localhost’ vs 127.0.0.1. I tried to change all of the details and permissions for the users, but the problem persisted. Instead of digging down into all the issues and wasting time, obsessing over why it wouldn’t work, set up a MongoDB interface instead. I found it much simpler and quicker to connect to.

Image(7) - Successful MongoDB integration from Datadog UI side

Image(8) - Custom Agent Check for ‘my_metric’ with python class and interval at 45s backend
I had difficulty getting the metric generated at the start, but after combing through the documentation I found an example of ‘randint’ and was able to use it for the custom agent check.

Image(9) -Bonus Q - Updated collection interval via Datadog UI

Visualizing Data

Ran into authorisation issues with the API and I was unable to use Postman to use Get or Push requests.

Image(10) - Forbidden Error

I followed the process to update the API key into the Datadog Authorisation environment and it did not seem to work. 
I tried to validate the authorisation, but every time I received the 403 error. I tried to input the API key into the authorisation for the parent collection as well as child collections, but every time I was met with the 403 error.
I also made sure that the headers were updated to include the datadog.eu path, but this also didn’t work. I am unsure why this issue is persisting and would need to link in with somebody from the Datadog team to resolve.
Ultimately, I made a dashboard using the Datadog UI and was able to create the following snapshot and send it to myself. This is how I generated the JSON file for submission and not through the API

Image(11) - 5 minute interval snapshot sent to my email

Bonus Question: Anomaly graph is displaying a straight line, as I chose the mongoldb.uptime metric to report on, which is a constant and wouldn’t anomaly wouldn’t be expected.
Monitoring Data

Created a metric monitor for ‘my_metric’ using the Datadog UI.

Image (12) - Metric Monitor

I updated the message so that I was notified by email based on the above criteria. 

Image(13) - Customised descriptions for notifications
The messaging was updated so that a customised message was sent, depending on the warning
Image showing the recovered metric

Image(14) - Warning message

Image (15) No Data message

Image (16)  Alert,  along with the value and host IP 

Image (17)  The Recovered Notification

Bonus Question
Image (18) - Datadog UI with downtime scheduled 

Image (19) - Daily downtime from 7PM - 9AM

Image (20) - Weekend Downtime

Collecting APM Data

Link to dashboard - https://p.datadoghq.eu/sb/803nv4zj2tjisyvo-7c9f371357eea1e9f41000a2d2c6c4d9
