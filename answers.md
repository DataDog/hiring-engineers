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

https://app.datadoghq.com/dashboard/gek-bgr-27h/mymetric?from_ts=1639782997319&to_ts=1639786597319&live=true

<img width="1349" alt="postmanbody" src="https://user-images.githubusercontent.com/32316958/146616850-c1d66751-1c9c-4908-b2f2-fd1d333fee7d.png">

View the dashboards within the Dashboard list in the Datadog user interface.  The sum of my_metric to show within a 5 minute time span.  Snapshot of the graph with hourly anomalies dashboard included. 

https://app.datadoghq.com/dashboard/5aa-992-hs3/postman-test?from_ts=1639786334482&to_ts=1639786634482&live=true

<img width="1277" alt="Timeboard" src="https://user-images.githubusercontent.com/32316958/146616807-8f607ea6-6d7e-49bd-9067-9142a818e05d.png">

<img width="1267" alt="postmantimeboard" src="https://user-images.githubusercontent.com/32316958/146623324-a7d8c465-ca4f-4f8d-85f7-b7c8ca39ed10.png">

**Bonus:** 
The anomaly graph appears blank, but with perspective of the rollup of the hourly sum, I would assume that it would reveal there are more than two standard that change per hour.   

## Monitoring Data

Created a new Metric Monitor that watches the average of my_metric and have it alert the following values over the past 5 minutes.  In the cog menu, edit the monitor to set an alert threshold of 800, a warning threshold of 500, and a no data if the query does not receive data for 10 minutes. 

Configure the message and who it gets sent to in the set up menu

Configured the monitor’s messages in the cog menu to send a email whenever the monitor gets triggered. Configure the settings to send specific messages according to the variables set with reference to the template forms. 

<img width="1281" alt="metricmonitor1" src="https://user-images.githubusercontent.com/32316958/146616727-3d8f41dc-44af-4d52-af8c-c0226dbd54bc.png">
<img width="1243" alt="metricmonitor2" src="https://user-images.githubusercontent.com/32316958/146616752-1761074b-a082-49e7-a453-302ce942abf1.png">
<img width="710" alt="email1" src="https://user-images.githubusercontent.com/32316958/146616776-7f3b524c-b776-4644-801f-e2a0b6d7a5e4.png">
<img width="710" alt="email2" src="https://user-images.githubusercontent.com/32316958/146616778-c829e927-70f4-4ca5-8f34-20b2d117bc49.png">

Uploaded more screenshots of emails for reference. 


**Bonus Question:**
To set downtime for specific days, edit configuration through Manage Downtime within the Monitors menu.  There will be an option to schedule downtime. Use RRule Generator to set more specific options.  

<img width="719" alt="downtime_weekdays" src="https://user-images.githubusercontent.com/32316958/146616821-217268f7-90ad-422d-8254-027677ed590e.png">
<img width="720" alt="downtime_weekends" src="https://user-images.githubusercontent.com/32316958/146616832-eee833e4-c5dc-4ddc-a462-6726b8e00a0b.png">

## Collection APM Data

Created a basic flask app on my vagrant vm using python and Datadog’s APM solution
Dashboard with both APM and Infrastructure Metrics: Issues became present with python 2 installation.  Tried with pip3 and issue was resolved.  

<img width="714" alt="ddtrace_app" src="https://user-images.githubusercontent.com/32316958/146622489-f6b7c8ad-a3d9-4e02-83f2-4d896a7a766c.png">


<img width="519" alt="ddtrace-output" src="https://user-images.githubusercontent.com/32316958/146623170-e554b5bf-935b-4b27-b4fc-cf63c1fcfe99.png">


**Bonus Question:**
Services act as “building blocks” that utilize microservice architectures.  A service can group together endpoints, and is usually named after a specific business action.  A resource is an action given to a service (e.g. query to a database or an endpoint.  

## Final Question 
Datadog can be used in many different ways.  For example, it can be utilized to organize IoT devices within businesses such as a bar.  The devices can collect metrics such as inventory, capacity, sales.  It is even possible to integrate AWS services such as Amazon QuickSight to utilize machine learning and predict future events such as peak sales.  
Datadog can also be used to monitor hardware usage for devices such as CPU and memory.  This would be useful for organizations that rely on devices that need to run constantly.  For example, a company that makes predictions on weather patterns may rely on devices that are outdoors and record specific data.  Datadog can help visualize the system's levels and alert if it goes above/below a specific threshold.  
