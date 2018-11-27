Your answers to the questions go here.

##Prerequisites - Setup the environment
[x]- Sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field),
RESOUCES: https://datadog.github.io/summit-training-session/handson/customagentcheck/
[x]- Get the Agent reporting metrics from your local machine.

##Collecting Metrics:
[x]- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
RESOURCES: 
https://docs.datadoghq.com/tagging/
https://docs.datadoghq.com/tagging/assigning_tags/?tab=go#configuration-files
https://docs.datadoghq.com/agent/faq/agent-configuration-files/?tab=agentv6
https://docs.datadoghq.com/agent/faq/agent-commands/?tab=agentv6

[x]- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
RESOURCES:
https://docs.datadoghq.com/integrations/postgres/
https://www.datadoghq.com/blog/collect-postgresql-data-with-datadog/
http://tutorials.jumpstartlab.com/topics/vagrant_setup.html

[x]- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

[x]- Change your check's collection interval so that it only submits the metric once every 45 seconds.
#Bonus Question Can you change the collection interval without modifying the Python check file you created?

##Visualizing Data:
[]-Utilize the Datadog API to create a Timeboard that contains:
RESOURCES:
https://docs.datadoghq.com/api/?lang=ruby#overview
https://docs.datadoghq.com/api/?lang=ruby#create-a-timeboard

1. Your custom metric scoped over your host.
2. Any metric from the Integration on your Database with the anomaly function applied.
3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

NOTE: Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

[]- Once this is created, access the Dashboard from your Dashboard List in the UI:
1. Set the Timeboard's timeframe to the past 5 minutes
2. Take a snapshot of this graph and use the @ notation to send it to yourself.
#Bonus Question: What is the Anomaly graph displaying?

##Monitoring Data
[]-Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
1. Warning threshold of 500
2. Alerting threshold of 800
3. And also ensure that it will notify you if there is No Data for this query over the past 10m.

[]-Please configure the monitor’s message so that it will:
1. Send you an email whenever the monitor triggers.
2. Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
3. Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
4. When this monitor sends you an email notification, take a screenshot of the email that it sends you.
#Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor: One that silences it from 7pm to 9am daily on M-F, And one that silences it all day on Sat-Sun. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

##Collecting APM Data:
[]- Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution. 
RESOURCES:
https://docs.datadoghq.com/tracing/setup/?tab=agent630

1. Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
2. Please include your fully instrumented app in your submission, as well.
#Bonus Question: What is the difference between a Service and a Resource?

##Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?

