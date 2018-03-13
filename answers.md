Your answers to the questions go here.

# Collecting Metrics:
 1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

- To add tags, I went into the Datadog.yaml file, and added tags within the tag section.  See below for a screenshot of the yaml file as well as the tags showing up in the UI.

![alt text](/images/tags_in_file.png)
![alt text](/images/tags_in_UI.png)


 2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

- Had some issues with getting the databases to run properly. Could not get PostgreSQL tor umm properly on my machine.  MongoDB ended up running properly.  Was having issues getting metrics to appear on the agent at first.  Followed documentation, but main issue was with the yaml file syntax.  Had to utilize a yam linter to get the correct syntax before the agent would grab metric properly.

![alt text](/images/DB_checks.png)
![alt text](/images/database.png)

 3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.

- Looked through documentation for creating a custom agent check.  Utilized the gauge check.  Created a yaml file called my_metric.yaml in the config.d directory.  Within the my_metric.yaml file, created an init_config and and instance.

````
init_config:
instances:
    [{}]
````

Created a my_metric.py file in the checks.d directory. In this file, I inherited the AgentCheck class from the checks method.  I created a new class called MyMetric which inherited all the methods from the AgentCheck class.  Then created a new check method that takes in the arguments of self and an instance.  Then used the gauge metric and called self on it passing in the name and a random integer method from the python docs.  I needed to import in the random method, which I added to the top of the method , then I set the random integer values to be between 0 and 1000.

````
import random
from checks import AgentCheck
class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
````

![alt text](/images/custom_agent_check.png)
![alt text](/images/my_metric.png)

4. **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

- Yes, you can change the interval without editing the python check file.  You need to add the collection_interval method to the yaml file under init_config.

# Visualizing Data:
1. Utilize the Datadog API to create a Timeboard that contains:
    * Your custom metric scoped over your host.
    * Any metric from the Integration on your Database with the anomaly function applied.
    * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
    * Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.

- Created a new timeboard in the dashboard section.  Chose my_metric as a time series scoped over my local host.  Added my mongodb metric with the anomaly function applied.  Then added my_metric graph with the rollover function set to 3600 seconds.  I then utilized the dog-watcher utility to be able to create logs of any changes to my Datadog agent and upload them as a backup to my GitHub repo.
````
{
	  "dash": {
	    "read_only": false,
	    "graphs": [
	      {
	        "definition": {
	          "viz": "timeseries",
	          "requests": [
	            {
	              "q": "avg:my_metric{host:Shauns-MacBook-Pro.local}",
	              "style": {
	                "width": "normal",
	                "palette": "dog_classic",
	                "type": "solid"
	              },
	              "type": "line",
	              "conditional_formats": []
	            }
	          ],
	          "autoscale": true
	        },
	        "title": "Avg of my_metric over host:Shauns-MacBook-Pro.local"
	      },
	      {
	        "definition": {
	          "viz": "timeseries",
	          "requests": [
	            {
	              "q": "anomalies(avg:mongodb.locks.collection.acquirecount.intent_sharedps{*}, 'basic', 2)",
	              "style": {
	                "width": "normal",
	                "palette": "dog_classic",
	                "type": "solid"
	              },
	              "type": "line",
	              "conditional_formats": []
	            }
	          ],
	          "autoscale": true
	        },
	        "title": "Avg of mongodb.locks.collection.acquirecount.intent_sharedps over *"
	      },
	      {
	        "definition": {
	          "viz": "timeseries",
	          "requests": [
	            {
	              "q": "avg:my_metric{*}.rollup(sum, 3600)",
	              "style": {
	                "width": "normal",
	                "palette": "dog_classic",
	                "type": "solid"
	              },
	              "type": "line",
	              "conditional_formats": []
	            }
	          ],
	          "autoscale": true
	        },
	        "title": "Avg of my_metric over *"
	      }
	    ],
	    "description": "created by shaunwyee@gmail.com",
	    "title": "Shaun's TimeBoard 6 Mar 2018 19:35",
	    "created": "2018-03-07T03:35:36.677800+00:00",
	    "id": 637673,
	    "created_by": {
	      "disabled": false,
	      "handle": "shaunwyee@gmail.com",
	      "name": "Shaun Yee",
	      "is_admin": true,
	      "role": null,
	      "access_role": "adm",
	      "verified": true,
	      "email": "shaunwyee@gmail.com",
	      "icon": "https://secure.gravatar.com/avatar/de86887bb320f0045418ef7ba6aa851a?s=48&d=retro"
	    },
	    "modified": "2018-03-07T03:38:24.737693+00:00"
	  },
	  "url": "/dash/637673/shauns-timeboard-6-mar-2018-1935",
	  "resource": "/api/v1/dash/637673"
	}
````

2. Once this is created, access the Dashboard from your Dashboard List in the UI:
    * Set the Timeboard's timeframe to the past 5 minutes
    * Take a snapshot of this graph and use the @ notation to send it to yourself.
 - To set the timeframe to 5 mins, I zoomed into the graph until 5 mins was displayed.  I added an annotation to the graph and tagged myself using the @ notation which sent the graph to my email.

![alt text](/images/viz_data_graphs.png)
![alt text](/images/email.png)

3. **Bonus Question:** What is the Anomaly graph displaying?
 - The anomaly graph is displaying the metric on a trend line.  The algorithm used identifies a basic trend of how the metric has been responding in the past, and predicts how it should respond in the future.  The anomalies are the points in the data that are off of the trend line.  This graph is best used for metrics that have strong recurring patters as opposed to ones that are consistently stable and hard to monitor with thresholds.

# Monitoring Data:
1. Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
    * Warning threshold of 500
    * Alerting threshold of 800
    * And also ensure that it will notify you if there is No Data for this query over the past 10m.

2. Please configure the monitor’s message so that it will:
    * Send you an email whenever the monitor triggers.
    * Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
    * Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
    * When this monitor sends you an email notification, take a screenshot of the email that it sends you.

- Creating a monitor was very straight forward.  Followed the steps in the documentation.  Set the threshold for the warning setting to 500 and the alerting setting to 800.  Finally I added the feature to notify me if there was no activity.  The email feature was also very straight forward, set the variable conditional statement codes for each of the alerts and if there there is no data.  Used the @ notation to email my personal email.

![alt text](/images/monitoring_email.png)

3. **Bonus Question:** Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
    * One that silences it from 7pm to 9am daily on M-F,
    * And one that silences it all day on Sat-Sun.
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
- 	Setting downtime monitor was also vey straight forward, set the times and dates for each of the downtime settings.  Screenshots below.

![alt text](/images/email_scheduled_downtime.png)
![alt text](/images/daily_downtime.png)
![alt text](/images/weekend_downtime.png)

# Collecting APM Data:
1. Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
    * Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
    * Please include your fully instrumented app in your submission, as well.
- The main issue I had was with he setup of the trace agent on OSX.  I followed the documentation on the GitHub page, but the file that I downloaded was not working properly.  Found out that the permissions that were set for the file did not include it to be allowed as an executable.  I used the terminal to change the rights to execute the script with sudo chmod 755 command.  This allowed the file to be executed, but running the file with my datadog agent config file was not functioning properly.  It was not able to get the information from the file, this caused the trace agent to exit due to it not being able to read my API key.  I dug around the filing system in the agent, and found a trace script in the bin directory.  This script worked and ran the trace agent.  I created a rails app and followed the docs to have the app detected by the trace agent.  My rails app is located under the trace-app directory attached to this project.

- Creating a dashboard was very straight forward.  Added the service summary widget and a few systems graphs to create my dashboard.  Link and screenshot to the dash is below.

![alt text](/images/traces_info.png)
![alt text](/images/APM_infrastructure_dash.png)

2. **Bonus Question:** What is the difference between a Service and a Resource?
- A service is a set of processes that an application utilizes together to provide a feature.  There can be many different services within an application that are used together to create the application as a whole.  An example would be the database and API services.

- A resource is a query to a service.  Looking at routes in an application, queries are made from the user to the controllers.  The query would tell the controller which view to display based on what the user has queried.

# Final Question:

1. Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?
- I am very much so into professional sports and I was thinking if was could take metrics on which seats are consistently not being filed at games would be interesting.  There are always specific sections of stadiums that are not filled, and thought there could be a way to take the statics of which seats are consistently not being filled, which may cause them to be sold for cheaper at resale.
- Another idea that is similar to my sporting event idea would be relating this to parking spaces around major cities.  There are always areas of cities that have hidden parking spaces or spaces that are always available.  Wanted to look at the metrics of how often spaces are filled and if there are ones that are more time free than others in a given area.
