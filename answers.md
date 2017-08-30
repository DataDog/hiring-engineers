Your answers to the questions go here.


--== LEVEL 1 : Collecting your Data ==--

-- Agent Installation --

![Agent Install](./screenshots/Install-Agent.png)



-- Bonus Question --

The Datadog Agent is a program running on the background of a host autonomously.
His job is to collect informations about the host and to send them to the DataDog Cloud where they can be see with the web platform.


-- Tag Addition --

![New Tag](./screenshots/Tags.png)



-- Database Installation --

A Mysql base has been installed and the Datadog integration for it has been successfully configured.

![MySQL Integration](./screenshots/Mysql-Integrate.png)

![MySQL Metrics](./screenshots/Mysql-Metrics.png)


-- Random Agent Check --

The files doing the check are in the directory code-files, and are named randomCheck.py and randomCheck.yaml

Here are the checks visible on the platform.

![Random Check](./screenshots/randomCheck.png)



--== Level 2 - Visualizing your Data ==--


-- Database dashboard --

As seen above, the MySQL dashboard has been cloned and the graph representing the custom Agent Check metrics over time.

![Cloned Dashboard](./screenshots/MySQLDashboard.png)



-- Bonus Question --

A timeboard is used to compare informations over time, it's composed of different graph, having all the same X axis of a selected lenght. A timeboard is thus used to put in parallel different metrics and to help define if there is some correlation between them.

The purpose of a screenboard is to get in one sight different informations, not necessarily connected and time-related.
It can be for instance a current value of a metric or a picture.
This kind of board is more used to share information as well, that's why it's layout can be customise.


-- Snapshot and notifications --

On the screenshots below, we can see the snapshot being taken and then, the notification recieved on my Event page.

![Snapshot](./screenshots/annotationGraph.png)


![Notification](./screenshots/notifProblem.png)


--== Level 3 - Alerting on your Data ==--


-- Monitor Setup --

A monitor has been created in order to notify me whenever the random metric goes above 0.90 in the past 5 minutes.

![Create Monitor](./screenshots/monitorCreated.png)


-- Multi-alert by host --

By changing an option in the monitor's definition, we can make it a multi-alert monitor for each host.

![Multi Alert](./screenshots/multiAlert.png)



-- Email Notification --

As seen in the screenshots below, the notification of an incident send an email automaticaly, another one is sent for the recovery of the issue (in this case, no metric above 0.90 in the last 5 minutes).

![Monitor Alert](./screenshots/alertRandom.png)

![Alert Email](./screenshots/emailAlerte.png)

![Recovery Email](./screenshots/emailRecovered.png)



-- Downtime --

The downtime scheduling can be defined in order to stop the Email notifications outside the office hours.

![Downtime notification](./screenshots/notifDowntime.png)

As we can see, the downtime schedule has been configured to be repeated everyday.

![Downtime Repeated](./screenshots/repeatDowntime.png)





I thank your for the interest that you show for my application.
 















