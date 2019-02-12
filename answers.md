Prerequisites - Setup the environment
I used a Windows Server 2012 R2 with SQL Server and Python installed for the exercise. hostname: PATAM10 tags: #bs:citidirect #database #prod
For the next step ---> "Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine."
I went to the datadoghq.com website and signed up for my own account following the instruction prompts. On the first login I followed the getting started instructions to install the agent. It is very easy to get the agent started as there is a one step install command for Windows.
https://github.com/patam01/hiring-engineers/blob/master/Image001.JPG
In a very short time, the agent started reporting data:
https://github.com/patam01/hiring-engineers/blob/master/Image001-1.jpg
https://github.com/patam01/hiring-engineers/blob/master/Image002.jpg
https://github.com/patam01/hiring-engineers/blob/master/Image004.jpg
________________________________________
Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog. 
I added host tags and users tags as shown in the screenshot:
https://github.com/patam01/hiring-engineers/blob/master/Image005.jpg
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
For SQL Server monitoring, I followed the steps outlined in the documentation: https://docs.datadoghq.com/integrations/sqlserver/
https://github.com/patam01/hiring-engineers/blob/master/Image003.png SQL YAML Config
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. Change your check's collection interval so that it only submits the metric once every 45 seconds.
I created a my_metric check using documentation link: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6
https://github.com/patam01/hiring-engineers/blob/master/Image007.png
Bonus Question Can you change the collection interval without modifying the Python check file you created?
It is possible to change the interval without modifying the .py file, you can change it in the YAML
https://github.com/patam01/hiring-engineers/blob/master/Image008.png
________________________________________
Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:
Your custom metric scoped over your host. Any metric from the Integration on your Database with the anomaly function applied. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
Timeboard script: https://github.com/patam01/hiring-engineers/blob/master/API%20Timeboard.py
Once this is created, access the Dashboard from your Dashboard List in the UI:
https://github.com/patam01/hiring-engineers/blob/master/Image008-2.jpg
I set the Timeboard's timeframe to the past 5 minutes Using "ALT + ]" I zoomed to 5 min interval Take a snapshot of this graph and use the @ notation to send it to yourself.
https://github.com/patam01/hiring-engineers/blob/master/Image008-1.jpg
Bonus Question: What is the Anomaly graph displaying?
The part of the "Anomalies Sql Batch Requests" graph that are shown in RED are showing that for this metric the value is outside of normal. In this case the mathematical formula used ('1e-3', direction='above') for any spikes above the value of 1e-3 will be highlighted as outside of the normal. It uses the history of the metric to predict the future values. If the value is outside of the expected range it will color it red on the graph.
________________________________________
Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
Warning threshold of 500 Alerting threshold of 800 And also ensure that it will notify you if there is No Data for this query over the past 10m.
Screen shot of creating 500 & 800 threshold and No Data alert:
https://github.com/patam01/hiring-engineers/blob/master/Image009.jpg
Please configure the monitor’s message so that it will: Send you an email whenever the monitor triggers.
Screen shot of breached alert email notification
https://github.com/patam01/hiring-engineers/blob/master/Image010.jpg
Create different messages based on whether the monitor is in an Alert, Warning, or No Data staInclude the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
Screen shot of email notification for missing data for 10 mins:
https://github.com/patam01/hiring-engineers/blob/master/Image011.jpg
Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
One that silences it from 7pm to 9am daily on M-F,
Screen shot of scheduled downtime during weekdays:
https://github.com/patam01/hiring-engineers/blob/master/Image012.jpg
And one that silences it all day on Sat-Sun.
Screen shot of scheduled downtime for weekend:
https://github.com/patam01/hiring-engineers/blob/master/Image013.jpg
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
<Add screen shots for scheduled downtime email notification>
https://github.com/patam01/hiring-engineers/blob/master/Image014.jpg https://github.com/patam01/hiring-engineers/blob/master/Image015.jpg
________________________________________
Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
https://p.datadoghq.com/sb/ap338w9s48uq47nq-236d0816d44be41d11be22de7c950d8a
https://github.com/patam01/hiring-engineers/blob/master/Image016.jpg
Bonus Question: What is the difference between a Service and a Resource? From the documentation:
Services: https://docs.datadoghq.com/tracing/visualization/#services
A service is a set of processes that do the same job. For instance, a simple web application may consist of two services:
A single webapp service and a single database service.
While a more complex environment may break it out into 6 services:
3 separate services: webapp, admin, and query. 3 separate external service: master-db, replica-db, and yelp-api.
Resources: https://docs.datadoghq.com/tracing/visualization/#resources
A Resource is a particular action for a service.
For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks). For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.
Resources should be grouped together under a canonical name, like /user/home rather than have /user/home?id=100 and /user/home?id=200 as separate resources. APM automatically assigns names to your resources; however you can also name them explicitly. See instructions for: Go, Java, Python, Ruby.
These resources can be found after clicking on a particular service.
Please include your fully instrumented app in your submission, as well.
Flask File: https://github.com/patam01/hiring-engineers/blob/master/flask_data.py
________________________________________


