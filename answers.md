Your answers to the questions go here.


To be prepared for this exercise, the work was divided into two phases: The first phase was exploratory to understand the Datadog interface, the agent deployment options and some basic as agent install, Azure Integration, Synthetics Monitoring and browse functionality. In the second phase it was to explore the deployment and assignment requirements.

# Phase I: The exploratory

Environment that was use for the tests:

On-premise 		 Windows 10 Desktop
On-Premise		  Vagrant Ubuntu Release 18.04  (for the assignment)
On-Premise 		 Vagrant Ubuntu  Release 18.04   
Azure VM 		   Windows Server 2019 
Azure VM		    Windows Server 2012 R2 (no agent)


Screen shot of the Host Map
 

Azure Integration less than 5 minutes
 


 
With DataDog, you don’t need to install any agent to start collecting metrics

As showed below no agent install on this VM and we are able to see some MetaData and Metrics
 



Synthetic Monitoring

During the trial I also wanted to test the Synthetic Monitoring, I was able to configure in some very easy step, please note that this is only an HTTP test. Synthetics test provide END-to-END visibility for validating that end users can perform critical business transactions.

In this test I setup an HTTP test on on www.saq.com (liquor store are manage by the government of Quebec), choose 3 different regions Canada Central – N. California and Oregon
 







Information on the synthetic test
 

From this view here you have some information to fine tune your website*
 
In conclusion, for the first phase I was very satisfied with what I saw! the easiness, the simplicity and integration of DataDog. 





# Phase II: The assignment

Collecting Metrics:
•	Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

 

Config of the datadog.yaml file
 

•	Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

MySQL was chosen for this exercise, we can see the installation from different views:
1.	From the Host Map

 

2.	From the Infrastructure list 

 


3.	Intetagrations
 

MySQL – Overview Dashboard
 


•	Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. I named it testSupportRandom

 

•	Change your check's collection interval so that it only submits the metric once every 45 seconds.
The yaml file was create under /etc/datadog-agent/conf.d$ ls
 

 

Run the command:
sudo -u dd-agent -- datadog-agent status

And I was able to see 
 

From the UI:
 


•	Bonus Question Can you change the collection interval without modifying the Python check file you created?


Visualizing Data:



Monitoring Data
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
•	Warning threshold of 500
•	Alerting threshold of 800
•	And also ensure that it will notify you if there is No Data for this query over the past 10m.
Configuration of the new Monitor Metric “Test Support Random”
 
 

Here are all the email received from the alert:
•	Send you an email whenever the monitor triggers.
•	Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
•	Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
•	When this monitor sends you an email notification, take a screenshot of the email that it sends you.



 

 

 
 

More print screens from the Monitor Message with detail graphics

 

 

 

Example of event sent @user
 



Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

•	One that silences it from 7pm to 9am daily on M-F,
•	And one that silences it all day on Sat-Sun.
•	Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.






•	One that silences it from 7pm to 9am daily on M-F,
 

 

•	And one that silences it all day on Sat-Sun.
 
 

