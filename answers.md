Your answers to the questions go here.

**Collecting Metrics:**

Conclusion of DataDog Sign up:
![Sign up Events](https://i.imgur.com/ChFM4WV.jpg)

*Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.*

  Configuration File tags:
  ![Agent Config File Tags](https://i.imgur.com/YeAj6y5.jpg)

  Host and Tags on Host Map
  ![Host and Tags on Host Map](https://i.imgur.com/vix1FPc.jpg)

*Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.*

  PostgreSQL Integration:
  ![PostgreSQL Integration](https://i.imgur.com/ZdhDyuA.jpg)

*Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.*

  Custom Agent Check Configuration File: (located etc/datadog-agent/conf.d)
  ![Agent Check Config File](https://i.imgur.com/QnUbzbJ.jpg)

  Custom Agent Check File: (located etc/datadog-agent/checks.d)
  ![Agent Check py File](https://i.imgur.com/KLSJrTh.jpg)

*Change your check's collection interval so that it only submits the metric once every 45 seconds.*

  Custom Agent Check File with Specified Collection Interval: (located etc/datadog-agent/checks.d)
  ![Agent Check py File](https://i.imgur.com/nq2SqcH.jpg)

*Bonus Question Can you change the collection interval without modifying the Python check file you created?*

  Yes, you can change the collection interval in the check configuration file, even specifying the collection interval for specific instances

  Example: Custom Agent Check Configuration File (Example instances from Documentation): (located etc/datadog-agent/conf.d)
  ![Agent Check Config File with Designated Instance Collection Intervals](https://i.imgur.com/ZYxWmTi.jpg)

**Visualizing Data:**

*Utilize the Datadog API to create a Timeboard that contains:*
  - Your custom metric scoped over your host.
  - Any metric from the Integration on your Database with the anomaly function applied.
  - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

  To create this Timeboard using the API, I utilized [this article](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs) about using Postman and DataDog, importing the DataDog collection JSON file, setting up an environment with variables for the DD agent and application keys that are substituted in for the variables in the API call, POST https://app.datadoghq.com/api/v1/dash?api_key={{dd_api_key}}&application_key={{dd_app_key}}. I created a graph for each of the above bullet points separately and then combined.

  And then using the script in the apibody.json file as the call's JSON body.

  Timeboard with Each Metric Individually Graphed and Combined:
  ![API Created Timeboard](https://i.imgur.com/z8gSZbl.jpg)

  Combined:
  ![API Combined Timeboard](https://i.imgur.com/P0KL7M0.jpg)

*Once this is created, access the Dashboard from your Dashboard List in the UI:*
  - Set the Timeboard's timeframe to the past 5 minutes
  - Take a snapshot of this graph and use the @ notation to send it to yourself

  Timeboard with 5 Minute Timeframe Snapshot:
  ![5 Minute Timeboard Snapshot](https://i.imgur.com/7mhvyBo.jpg)

  Email Notification Screenshot of 5 Minute Timeframe:
  ![Email Notification Screenshot of 5 Minute Timeframe](https://i.imgur.com/EuhVgKw.jpg)

*Bonus Question: What is the Anomaly graph displaying?*

  The anomaly graph is displays in the gray area surrounding the actual metrics, a prediction of the expected behavior based on past events.

**Monitoring Data**

*Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:*
  - Warning threshold of 500
  - Alerting threshold of 800
  - And also ensure that it will notify you if there is No Data for this query over the past 10m.

  Creating the Metric Thresholds:
  ![Creating the Metric Thresholds](https://i.imgur.com/ZrnFoyr.jpg)

*Please configure the monitor’s message so that it will:*
  - Send you an email whenever the monitor triggers.
  - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
  - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
  - When this monitor sends you an email notification, take a screenshot of the email that it sends you.

  Configuring the Message:
  ![Configuring the Message](https://i.imgur.com/XXo7JWp.jpg)

  Email Notification Screenshot:
  ![Email Notification Screenshot](https://i.imgur.com/TvHyNaP.jpg)

*Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*
  - One that silences it from 7pm to 9am daily on M-F,
  - And one that silences it all day on Sat-Sun.
  - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

  Configuring the Downtime During the Week:
  ![Configuring the Downtime During the Week](https://i.imgur.com/09qXmz3.jpg)

  Email Notification Screenshot:
  ![Email Notification Screenshot](https://i.imgur.com/Svqaiay.jpg)

  Configuring the Downtime for the Weekend:
  ![Configuring the Downtime for the Weekend](https://i.imgur.com/EhKD4HP.jpg)

  Email Notification Screenshot:
  ![Email Notification Screenshot](https://i.imgur.com/MUgWzbe.jpg)

**Collecting APM Data**

*Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:*

  Created and ran a Flask virtual environment. Ran the sample Flask app, sampleflaskapp.py, using DDtrace-run to start APM tracing.

  Flask App APM and Infrastructure Screenboard Screenshot:
  ![Flask App APM and Infrastructure Screenboard Screenshot](https://i.imgur.com/j1H2RUG.jpg)

  [Link to Screenboard](https://p.datadoghq.com/sb/df8671eb7-cec14f9fbda39aeaad39bfaa7110b0e6)

*Bonus Question: What is the difference between a Service and a Resource?*

  A service is a set of processes that do the same job while a resource is a particular action for a service

**Final Question**

*Is there anything creative you would use Datadog for?*

  I've always been bothered by the homelessness issue in the United States and perhaps using DataDog to track availability in homeless shelters and similar housing might prevent people from having to sleep out on the street and in uncomfortable conditions. Tracking shelter availability information as well as homeless populations in an area in a database may allow for initiatives to create additional shelters in areas of greater volume and necessity or even just providing transportation of those without shelter to open areas nearby.
