Your answers to the questions go here.
## Setting up environment

Followed steps to set up vagrant environment via Virtual Box.  Had some bugs that related to the updating python to install tracers and flask.  

##Collecting Metrics

Added tags to Agent configuration file

Installed mySQL in Vagrant environment.  Database was already installed for Datadog agent.  Configured file in mysql.d/conf.d to link to agent.  

Created script files in checks.d to check that pushes a custom metric to the Datadog server

Change the collection interval to submit metrics every 45 seconds. 

**Bonus question:**

Yes it is possible to edit the interval by adding min_collection_interval to the yaml in the conf.d/ file.

## Visualizing Data

Created board using PostMan API editor and sent POST API to Datadog using api token.  Included screen shot of API editor with JSON body. 
      
View the dashboards within the Dashboard list in the Datadog user interface.  The sum of my_metric to show within a 5 minute time span.  Snapshot of the graph with hourly anomalies dashboard included. 

**Bonus:** 
The anomaly graph appears blank, but with perspective of the rollup of the hourly sum, I would assume that it would reveal there are more than two standard that change per hour.   

## Monitoring Data

Created a new Metric Monitor that watches the average of my_metric and have it alert the following values over the past 5 minutes.  In the cog menu, edit the monitor to set an alert threshold of 800, a warning threshold of 500, and a no data if the query does not receive data for 10 minutes. 

Configure the message and who it gets sent to in the set up menu

Configured the monitor’s messages in the cog menu to send a email whenever the monitor gets triggered. Configure the settings to send specific messages according to the variables set with reference to the template forms. 


**Bonus Question:**
To set downtime for specific days, edit configuration through Manage Downtime within the Monitors menu.  There will be an option to schedule downtime. Use RRule Generator to set more specific options.  

## Collection APM Data

Created a basic flask app on my vagrant vm using python and Datadog’s APM solution
Dashboard with both APM and Infrastructure Metrics: Issues became present with python 2 installation.  Tried with pip3 and issue was resolved.  

**Bonus Question:**
Services act as “building blocks” that utilize microservice architectures.  A service can group together endpoints, and is usually named after a specific business action.  A resource is an action given to a service (e.g. query to a database or an endpoint.  

## Final Question 
Datadog can be used in many different ways.  For example, it can be utilized to organize IoT devices within businesses such as a bar.  The devices can collect metrics such as inventory, capacity, sales.  It is even possible to integrate AWS services such as Amazon QuickSight to utilize machine learning and predict future events such as peak sales.  
Datadog can also be used to monitor hardware usage for devices such as CPU and memory.  This would be useful for organizations that rely on devices that need to run constantly.  For example, a company that makes predictions on weather patterns may rely on devices that are outdoors and record specific data.  Datadog can help visualize the system's levels and alert if it goes above/below a specific threshold.  
