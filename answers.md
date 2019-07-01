## Prerequisites - Setup the environment:

---> Used my own Hyper-V ubuntu VM that I normally use for day to day tasks in my current job.

(screenhots/01 Set Up Platform)

## Collecting Metrics:

---> Added tags to agent config file.

(screenhots/02 Add Tags.jpg)

---> Installed MySQL and Datadog MySQL integration.

(screenhots/03 mySQL Integration)

(screenhots/04 Host Mapping and Tags.jpg)

--->  Created custom agent check (my_metric.py) with a random value between 0 and 1000.

(screenhots/05 Custom Agent Check Result.jpg)

(scripts/my_metric.py, scripts/my_metric.yaml)

--->  Changed my_metric metric collection interval to once every 45 seconds.

(scripts/my_metric.yaml)

# Bonus Question:
--->  You can change the collection interval by  setting the min_collection_interval to 45  in /etc/datadog-agent/conf.d/my_metric.yaml file

## Visualising Data:
--->  Utilising Datadog API create a timeboard that contains:
	--->  Create a my_metric data graph.
	--->  MySQL metric with database anomaly function applied.
	--->  My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.
--->  Take a snapshot of the graph and use the notation
--->  Set timeboard timeframe to past 5 minutes.

(scripts/api-timeboard.py)

(screenhots/06 My Dashboard.jpg)

##### Bonus Question:
--->  The anomaly graph displays any deviations of CPU from the MySQL integration utilising historic data collected that is outside its expected behaviour threshold. 
	  The blue line are current metrics, the grey area is the threshold and the red markers are the anomaly detections.

## Monitoring Data:
---> Created a new metric monitor that watches the average of my_metric and alert if it is above the following values:
	---> Warning threshold of 500.
	---> Alerting threshold of 800.
	---> Ensure that it will notify if no data for this query past 10 minutes.
	---> Configure monitor message to:
	---> Email whenever the monitor triggers.
	---> Create different messages based on whether the monitor is in an alert, warning or no data state.
	---> Include the metric value that caused the monitor to trigger and host ip when the monitor triggers an alert state.

(screenhots/07 Configuration Metric Monitoring Pt.1.jpg , 
 screenhots/07 Configuration Metric Monitoring Pt.2.jpg)

---> When this monitor sends an email notification, take a screenshot of the email.

(screenhots/08 Metric Alert.jpg)

##### Bonus Question:
---> Set up two scheduled downtimes for this monitor:
---> One that silences it from 7pm to 9am daily on M-F.

(screenhots/09-A Downtime for Weekdays.jpg)

---> One that silences it all day on Sat-Sun.

(screenhots/09-B Downtime for Weekends.jpg)

---> Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

(screenhots/10 Downtime for Notification.jpg)

## Collecting APM Data:
---> Instrument the Flask app using Datadog’s APM solution.
---> Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
---> Please include your fully instrumented app in your submission.

  - https://p.datadoghq.com/sb/znd1wt2sbu3ntv68-dcb6bcc08663a9100b606ba7bb418931

(screenhots/11 Flask Application.jpg)
(scripts/flask_app_example.py)

(screenhots/12 Dashboard with System and Flask Metrics.jpg)
(screenhots/13 Flask APM Dashboard.jpg)
(screenhots/14 Public Screenboard with Flask and System Metrics.jpg)

##### Bonus Question:
---> A service is a set of processes that do the same job. For instance, a simple web application may consist of two services:
  - A single web application service and a single database service.
  - While a more complex environment may break it out multiple services.


  - For a web application: some examples might be a canonical URLs, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks).
---> A resource is a particular action for a service.
	 More particularly, for a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.

## Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

%%%% IoT Monitoring and Industry 4.0 %%%%

Within the integration of communication services to our day-to-day life, I guess the most exciting results will be seen within the adoptation of Industry 4.0 and particularly Internet of Things.

Indeed both of the concepts are extremely broad and we can dream of implementing them to any aspect of our lives.

What I have felt fascinating completeing the exercise is how much you can improve the efficiency of a production line by using Watchdog on all the components of an automation line. 

You can use parse the overall and individual performance of the automation components in the production chain, estimate the probable issues way in advance (can be monitoring life-cycle of the sensors, to i/o power efficiency of the engine drivers, or the error rates which can be collected from an PLC process), and avoid any down times not only for IT infrastructure, but also any utility device in a Digitalized ecosystem.

On the other hand, Datadog can be an extreme tool to improve the Datacenter utilization. Considering different apps which has different sensitivity on resource (CPU, memory, IO rate) you can automate an entire DC operations, automating the migration of the application blocks to the different cabins or racks even with the input of the temperature of the particular areas of a data center.
