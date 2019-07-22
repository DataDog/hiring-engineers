Prerequisites
==

Setup the environment

Set-up multiples environments

- Vagrant with Virtual box running Ubuntu/xenial64
- Windows 10 Box
- datadog docker

1. Install Datadog Agent and confirm status on host

![Agent Status](https://i.imgur.com/3VGA69k.png)

Collecting Metrics
==

1. Add tags in the Agent config file and show us a screen-shot of your host and its tags on the Host Map page in Datadog.

![Host Metrics](https://i.imgur.com/yjqOHaV.png)


2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

- installed mysql and you can see the integration in hostmap page
![MySQL Status](https://i.imgur.com/bVNTWSn.png)

![MySQL Integration Installed](https://i.imgur.com/YwrGSOQ.png)

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

- python script custom_firstcheck.py
![Python Script](https://i.imgur.com/Inzymim.png)

I ran in to quite a few issues with creating a custom agent check and began trouble shooting my environment as I thought I may of missed a dependency. Check my installs folder for the files and everything seems to be in order. Tried restarting the agent and the machine and still nothing appearing in my Datadog UI.


Decided to move on with the technical exam as best I could and come back to this with a fresh mind.


4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

- File I would of used
![Yaml Config](https://i.imgur.com/F9oEj96.png)

5. Bonus Question Can you change the collection interval without modifying the Python check file you created?

I would just edit the config file in sublime/notepadd++


Visualizing Data
==

Utilize the Datadog API to create a Time-board that contains:

- As I didn't create my_metric and was running in to environment issue, I have chosen to use system metrics already included in Datadog. The dependencies issues weren't allowing me to utilize the API either so I used the Datadog front end UI and created all of the below using Datadog instead.

1. Your custom metric scoped over your host.

2. Any metric from the Integration on your Database with the anomaly function applied.

3. Your custom metric with the roll-up function applied to sum up all the points for the past hour into one bucket

![My Time-board](https://i.imgur.com/ofCNBZl.png)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Time-board.

Script I would of used: custom_timeboard.py

Accessing the Dashboard
==

Once this is created, access the Dashboard from your Dashboard List in the UI: https://docs.datadoghq.com/api/?lang=python#dashboards

1. Set the Time-board's time-frame to the past 5 minutes

You can see this is set to 5 minutes. I did this by zooming over the time-board.

![My Time-board](https://i.imgur.com/ofCNBZl.png)

2. Take a snapshot of this graph and use the @ notation to send it to yourself.

Snapshot of Graph using @ notation to send to myself

![Notation Sent to myself](https://i.imgur.com/D7FQmlz.png)

3. Bonus Question: What is the Anomaly graph displaying?

The anomaly is displaying anything that is a deviation from the normal average.

Monitoring 
==

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

1. Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- Warning threshold of 500

- Alerting threshold of 800

- Notify you if there is No Data for this query over the past 10m.


2. Please configure the monitor’s message so that it will:

3. Send you an email whenever the monitor triggers.

4. Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

5. Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![Alert Configuration](https://i.imgur.com/FL6yTfe.png)

6. When this monitor sends you an email notification, take a screen-shot of the email that it sends you.

![Alert Email](https://i.imgur.com/Sf2oaD0.png)

7. Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.

Make sure that your email is notified when you schedule the downtime and take a screen-shot of that notification.

![Downtime Email](https://i.imgur.com/yzqPydH.png)

I noticed a timezone issues here even though I set them in Sydney Time.

![Downtime Email](https://i.imgur.com/6urZNr8.png)

Collecting APM Data
==

1. Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

- installed python-pip
- installed ddtrace
- enabled settings for APM=true in yaml
- added app key
- add my_app.py to my repository anyway for your reference.

I ran in to dependency issues again here so was unable to complete the APM install.

2. Bonus Question: What is the difference between a Service and a Resource?

Services are defined to run and complete defined tasks. Services have dependencies which are resources required for the Service to complete that task.

Resources are made up of elements required for that Service to complete it's task/run.

For example DataDog Agent is a Service that is dependent on the resource datadog.yaml


3. Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

After I spent the last few days building out my environments and getting under the hood of Datadog which has been extremely fun, A use case that I could see Datadog really helping the world achieve something ground breaking would be monitoring all hospital equipment availability, Hospital ward/bed availability and much more.

The data can be consumed by dispatchers for ambulance drivers or even publicly available to the consumer to pick which hospital to go as that emergency department may not be as congested. The use cases are endless which is what really excites me about Datadog.

This would result in people gaining faster care in times of need and could potentially result in Datadog saving peoples lives.


