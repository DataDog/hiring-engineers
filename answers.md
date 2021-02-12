## Tasks - The following are the categories in which the tasks have been allocated. 
----------------
    Environment Set-up
    Collecting Metrics
    Visualizing Data
    Monitoring Data
    Collecting APM Data
    Creative Use of Datadog

Reviewer - I have done my best to try and provide you all the details as possible. 

#### Environment Set-up
- VMWare Fusion as Hypervisor on my Macbook Pro (Personal Laptop)
- Operating System - Ubuntu 18.04 - My favourite OS for any Testing
- Datadog Account - jaydesai83@gmail.com
- Datadog Agent - v7.25.1


#### Collecting Metrics
##### Task: 
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
##### How: 
Installed Agent >> Standard Process from Portal for Ubuntu. Edited “datadog.yaml” file located at “/etc/datadog-agent/datadog.yaml” and inserted a couple of tags.

Host in Datadog Dashboard

<img src="./images/cm_image_1.png" width="650" title="Host in Datadog Dashboard">

Agent Status Output

<img src="./images/cm_image_2.png" width="650" title="Agent Status Output">

##### Task: 
Install a database on our machine and then install the respective datadog integeration for that database. 
##### How: 
Installed Integeration >> Standard Process from Portal for MySQL. Edited “conf.yaml” file located at “/etc/datadog-agent/conf.d/mysql.d/conf.yaml” and made changes according to the provided instructions.

Plugin Installed from Datadog Portal

<img src="./images/db_image_1.png" width="650" title="Plugin Installed from Datadog Portal">

Database Metrics available in Metrics Explorer

<img src="./images/db_image_2.png" width="650" title="Database Metrics available in Metrics Explorer">

##### Task: 
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

##### How: 
Followed guide to create a custom agent check. Created a file called mycheck.py “/etc/datadog-agent/check.d/mycheck.py” 
Additionally, created a mycheck.yaml file “/etc/datadog-agent/conf.d/mycheck.yaml” 

Custom Check from Datadog Agent Status Output

<img src="./images/cc_image_1.png" width="650" title="Custom Check from Datadog Agent Status Output">

Custom Check metrics in Datadog Portal

<img src="./images/cc_image_2.png" width="650" title="Custom Check metrics in Datadog Portal">


##### Task: 
Change your check's collection interval so that it only submits the metric once every 45 seconds.

##### How: 
Edited the .yaml file to include –min_collection_interval value and set it to 45. 

##### Task: Bonus Round
Can you change the collection interval without modifying the Python check file you created?

##### How: 
I think the documentation is now updated showing how to edit the .yaml file to change the collection interval. I used the available documentation. 



#### Visualizing Data
##### Task: 
Utilize the Datadog API to create a Timeboard that contains:
    Your custom metric scoped over your host.
    Any metric from the Integration on your Database with the anomaly function applied.
    Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
##### How: 
Download the Postman Collection for datadog and authenticated via the available API Key.

Datadog Postman Collection - Verfication of the API Key

<img src="./images/vd_image_1.png" width="650" title="Verification of API Key">

Rather than using the provided example, I manually created a Dasboard Graphically, exported the JSON, altered it and used it complete the exercise. 
My JSON payload I used to create the Dashboard is as per the screen below:
( The exercise asks for 1 hour, unfortunately the image below is from my testing, which was set to 300 - That value when changed to 3600 will provide data over the hour )

<img src="./images/vd_image_2.png" width="850" title="JSON Payload for Dashboard Creation">

The snapshot/sceenshot of the Visualization is as below. I have also used the 'Notifications' to send the notifications to myself. 
Additionally, I have also created a Public URL For same: https://p.datadoghq.com/sb/jzdbkkrelppjuizh-56f4d3ba1ad4230e82caec7b18beb827
( Unsure if you will have any data on that URL when you test as it is being generated from a VM running on my machine )

<img src="./images/vd_image_3.png" width="750" title="Visualizing Data - Dashboard">



#### Monitoring Data
##### Task:
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

- Send you an email whenever the monitor triggers.
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
- When this monitor sends you an email notification, take a screenshot of the email that it sends you.

##### How: 

I started off my altering my_metric value to be 600, so that it provides me a value in the required threshold. Created a Monitor whith 'Threshold Alert' as detection method. Metric was set to 'my_metric' from my vm 'jay-test-box'. It was a 'Simple Alert'.

<img src="./images/md_image_1.png" width="750" title="Setting Thresholds in Monitor">


My e-mail is already in the system, so receiving notifications is not a challenge. Received notifications from alert@dtdg.co
The task was to create different messages based on what monitor type/state has been triggered. After a few tries, I was able to create all three custom messages.

````
{{#is_alert}}

This is a custom message based on whether the monitor is an ALERT, WARNING or NO DATA state. 
ALERT ! ALERT ! 
Metric value that caused the trigger is **{{value}}** and the Host IP is :  **{{host}}**

{{/is_alert}}

{{#is_warning}}

This is a custom message based on whether the monitor is an ALERT, WARNING or NO DATA state. 
WARNING ! WARNING ! 
Metric value that caused the trigger is **{{value}}** and the Host IP is :  **{{host.ip}}**

{{/is_warning}}

{{#is_no_data}}

This is a custom message based on whether the monitor is an ALERT, WARNING or NO DATA state. 
NO DATA ! NO DATA ! 
Metric value that caused the trigger is **{{value}}** and the Host IP is :  **{{host.ip}}**

{{/is_no_data}}


 @jaydesai83@gmail.com
````

##### Task: Bonus Round
Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F

<img src="./images/md_image_3.png" width="650" title="Downtime 7pm to 9am">

And one that silences it all day on Sat-Sun.

<img src="./images/md_image_4.png" width="650" title="Downtime on Saturday and Sunday">

(Please Note: The calendar dates are not accurate for the screenshot as I was in test mode)

Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

<img src="./images/md_image_5.png" width="650" title="Email notification screenshot">


Challenges:
Had to restart the datadog agent for the new custom metric to be sent out. 

#### Collect APM Data
##### Task: 
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution

##### How: 
I used the provided .py code and ran Flask on the VM and generated some APM Metrics. 

Transaction Trace view in Datadog Portal

<img src="./images/apm_image_1.png" width="850" title="Transaction Trace in Datadog">

Flask Code for the provided Application.

<img src="./images/apm_image_2.png" width="650" title="Flask_Code">

Datadog Agent Status showing APM Metrics summary

<img src="./images/apm_image_3.png" width="550" title="Datadog Agent Status">


##### Task: Bonus Round
What is the difference between Service and Resource?


##### How: 
Service: Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of building your application.
Resource: Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.
My two cents: In most cases, a resource is a subset of service.


 
#### Final Question: Creative Use of Datadog
##### Response: 
I am an IoT nerd and I love beer.  I have a few IoT sensors around the house. I will like to use datadog to create a visualization for me which tells me;

- How many times do I leave the house via my front door ?
- How may times do I enter my garage ? (my beer fridge is located in the garage)
- How many times do I open the fridge ?
- What times have these events occurred at ?
Ideally to understand my drinking habits. ;)


