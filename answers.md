# Set Up
  I am using a linux (Ubuntu 18.04) VM for this project. I registered for DataDog as suggested using Datadog Recruiting Candidate in the Company field and installed the agent.

# Collecting Metrics

#### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  To add tags in the agent config file, I had to first navigate to the file located in V6 at /etc/datadog-agent/datadog.yaml and open it with the text editor as admin. And assigned tags per the documentation

  Assigning agent tags using the config file:
  - ![Agent Config File Tags](https://i.imgur.com/YeAj6y5.jpg?1)

  Host map display of host infrastructure and tags using the DataDog UI:
  - ![Host and Tags on Host Map](https://i.imgur.com/vix1FPc.jpg)

#### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
  I'd already installed PostgreSQL for use in personal projects, and I installed the corresponding integration using the integrations section of the UI

  Screenshot of the completed integrations (including Postgres):
  - ![PostgreSQL Integration](https://i.imgur.com/ZdhDyuA.jpg?1)

#### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
  In order to create a custom agent check, I had to create both a configuration (yaml) file and the actual check py file. Using help from the documentation examples, I created the configuration file at etc/datadog-agent/conf.d/mymetric.yaml and the check file at etc/datadog-agent/checks.d/mymetric.py. The configuration file was simple as there were no explicit check configurations or instances for which I needed to add specifications.

  Configuration File:
  ![Agent Check Config File](https://i.imgur.com/QnUbzbJ.jpg?1)

  Again using the 'hello world' example from the documentation, I created the check. First importing checks from the Agent, defining the custom check class and importing the AgentCheck. Then defining the check function and sending a gauge with the value of a random integer between 0 and 1000 for the 'my_metric' named metric. I imported Python's randint function to use for the random integer generation.

  Check File:
  ![Agent Check py File](https://i.imgur.com/KLSJrTh.jpg?1)

#### Change your check's collection interval so that it only submits the metric once every 45 seconds.
  To only submit the metric once every 45 seconds, I modified the check py file. I defined a default minimum collection interval constant of 45 seconds and then set the agent's min collection interval for an instance to be either first the interval set specifically for that instance in the configuration file or second the value of the constant.

  Check file with specified collection interval:
  ![Agent Check py File](https://i.imgur.com/nq2SqcH.jpg?1)

#### Bonus Question: Can you change the collection interval without modifying the Python check file you created?
  Yes, instead of modifying the collection interval in the check file you can change the collection interval in the check configuration file. Where you can even define specific collection intervals for different instances.

  Here is an example of that using example instances from the [documentation](https://docs.datadoghq.com/developers/agent_checks/#configuration):
  ![Agent Check Config File with Designated Instance Collection Intervals](https://i.imgur.com/ZYxWmTi.jpg?1)

# Visualizing Data:

#### Utilize the Datadog API to create a Timeboard that contains:
  - Your custom metric scoped over your host.
  - Any metric from the Integration on your Database with the anomaly function applied.
  - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

  To create this Timeboard using the API, I utilized [this article](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs) about using Postman and DataDog, importing the DataDog collection JSON file, setting up an environment with variables for the DD agent and application keys that are substituted in for the variables in the API call, POST https://app.datadoghq.com/api/v1/dash?api_key={{dd_api_key}}&application_key={{dd_app_key}}. I created a graph for each of the above bullet points separately and then combined. Lastly, to complete the request I used the script in the apibody.json file as the call's JSON body.

  Here is a screenshot of the entire timeboard containing the four timeseries graphs. One for my_metric scoped over the host, one for free memory on the DB over the host with the anomaly function applied, one for my_metric with the rollup function applied, and the last one with all three combined on one graph:
  ![API Created Complete Timeboard](https://i.imgur.com/j66iy1H.jpg?1)

  Here is a full-screen view of the three combined:
  ![API Combined Timeboard](https://i.imgur.com/P0KL7M0.jpg?1)

#### Once this is created, access the Dashboard from your Dashboard List in the UI:
  - Set the Timeboard's timeframe to the past 5 minutes
  - Take a snapshot of this graph and use the @ notation to send it to yourself

  After trying to scope the timeframe to 5 minutes using the show tab at the top of the graph, I realized to do this you had to click and drag the 5 minute period I wanted to select and view it. Here is a snapshot of the graph as well as a comment using @ notation to email it to myself:
  ![5 Minute Timeboard Snapshot](https://i.imgur.com/7mhvyBo.jpg?1)

  And the email notification:
  ![Email Notification Screenshot of 5 Minute Timeframe](https://i.imgur.com/EuhVgKw.jpg?1)

#### Bonus Question: What is the Anomaly graph displaying?
  The anomaly graph displays a prediction of the expected behavior based on past events, which is depicted in the gray area surrounding the actual metrics.

# Monitoring Data

#### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
  - Warning threshold of 500
  - Alerting threshold of 800
  - And also ensure that it will notify you if there is No Data for this query over the past 10m.

  In order to create a new metric monitor, I had to navigate to the monitors tab and select new monitor. Then choose metric monitor and go through the specifications. First selecting threshold alert, then specifying the monitor is for the custom my_metric metric. Next, I set the alert conditions to trigger when the threshold average of the last 5 minutes was above 500 for a warning and 800 for an alert. As well as a notification if there was no data over a 10 minute period. That procedure is shown in the screenshot below:
  ![Creating the Metric Thresholds](https://i.imgur.com/ZrnFoyr.jpg?1)

  And what the alert and warning look like on the graph:
  ![Metric Thresholds Visualized on the Graph](https://i.imgur.com/AqL9cyk.jpg?1)

#### Please configure the monitor’s message so that it will:
  - Send you an email whenever the monitor triggers.
  - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
  - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
  - When this monitor sends you an email notification, take a screenshot of the email that it sends you.

  To configure the message, I had to first name it and then define what the message would say. In order to differentiate messages between an alert and a warning, I used the {{#is_alert}}, {{#is_warning}}, and {{#is_no_data}} conditional variables and defined custom messages for each inside the respective closing tag. Finally in order to display the host ip and metric value that triggered the alert, I used the {{host.ip}} and {{value}} variables and @ notation at the end to send out an email notifcation to myself. This procedure is shown in the screenshot below:
  ![Configuring the Message](https://i.imgur.com/XXo7JWp.jpg?2)

  And a screenshot of the email from the notification:
  ![Email Notification Screenshot](https://i.imgur.com/TvHyNaP.jpg?1)

#### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
  - One that silences it from 7pm to 9am daily on M-F,
  - And one that silences it all day on Sat-Sun.
  - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

  To configure the downtime during the week, I navigated to monitors and then to manage downtime with the DataDog UI. From there I selected schedule downtime and choose the monitor that I had just created. To define the content of the monitor, I had to say that it was recurring, I had to choose a start date of Monday 8/21/18 and to repeat every 1 week. This brought up the days of the week that I wanted to set the downtime for, and I checked Monday-Friday. I set the start time at 7 PM with a duration of 14 hours that would take it to 9 AM the following day. Lastly I set no end date and used @ notation in the message in order to be notified of the scheduled downtime. The result of this configuration can be seen in the following screenshot:
  ![Configuring the Downtime During the Week](https://i.imgur.com/09qXmz3.jpg?1)

  The following is a screenshot of the resulting email notifcation. I noticed the time displayed in the email was UTC instead of EST and that the timeframe displayed in the email was a notifcation for an hour before the downtime started:
  ![Email Notification Screenshot](https://i.imgur.com/Svqaiay.jpg?1)

  I did the same procedure to configure the downtime for the weekend. Except this time I choose a start date of Saturday 8/25/18, I checked only Saturday and Sunday, and set the duration as 1 day. And again I set no end date and used @ notation in the message in order to be notified of the scheduled downtime. The result of this configuration can be seen in the following screenshot:
  ![Configuring the Downtime for the Weekend](https://i.imgur.com/EhKD4HP.jpg?1)

  This screenshot of the email notification for the weekend downtime also had the time differences:
  ![Email Notification Screenshot](https://i.imgur.com/MUgWzbe.jpg?1)

# Collecting APM Data

#### Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
  In order to instrument the given flask app, I created and ran a Flask virtual environment. I then installed ddtrace and ran the sample Flask app, in sampleflaskapp.py modified to support tracing, using DDtrace-run to start the APM tracing. To set up tracing for the app, I imported ddtrace from tracer and wrapped the application file using "\@tracer.wrap('sampleflaskapp.fetch')". Then when I navigated to the flask app, I started getting trace data for the app. I created a screenboard to display this data. I added a service summary board and a host map board to the screenboard. To set up the service summary board to display the APM trace data, I had to choose the production environment, since that was where the application was running, and to display all the data. To set up the host map I had to choose to filter by the production environment.

  The resulting screenboard featuring the Flask app APM and infrastructure data can be seen in the following screenshot:
  ![Flask App APM and Infrastructure Screenboard Screenshot](https://i.imgur.com/j1H2RUG.jpg?1)

  As well as a [link to the screenboard](https://p.datadoghq.com/sb/df8671eb7-cec14f9fbda39aeaad39bfaa7110b0e6).

#### Bonus Question: What is the difference between a Service and a Resource?
  Straight from the documentation, a service is a set of processes that do the same job while a resource is a particular action for a service.

# Final Question

#### Is there anything creative you would use Datadog for?
  I've always been bothered by the homelessness issue in the United States and perhaps using DataDog to track availability in homeless shelters and similar housing might prevent people from having to sleep out on the street and in uncomfortable conditions. Tracking shelter availability information as well as homeless populations in an area in a database may allow for initiatives to create additional shelters in areas of greater volume and necessity or even just providing transportation of those without shelter to open areas nearby.
