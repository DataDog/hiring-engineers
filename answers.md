Your answers to the questions go here.


To be prepared for this exercise, the work was divided into two phases: The first phase was exploratory to understand the Datadog interface, the agent deployment options and some basic as agent install, Azure Integration, Synthetics Monitoring and browse functionality. In the second phase it was to explore the deployment and assignment requirements.

# Phase I: The exploratory 

Environment that was use for the tests:

- On-premise 		 Windows 10 Desktop (kids gaming PC)
- On-Premise		  Vagrant Ubuntu Release 18.04  (for the assignment)
- On-Premise 		 Vagrant Ubuntu  Release 18.04 (test box)   
- Azure VM 		   Windows Server 2019 (Azure integration with agent) 
- Azure VM		    Windows Server 2012 R2 (Azure integration / no agent)

 Account that was used to signed up to DataDog (patolecanard@gmail.com)
 
 All source codes and Screenshots are in folder:  hiring-engineers/Code/ and in hiring-engineers/Screenshots/




Screen shot of the Host Map
![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic1.png "All Systems")
 

 ## Azure Integration less than 5 minutes ! ##

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic2.png "Azure Integration") 

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic3.png "No agent")
 
With DataDog, you don’t need to install any agent to start collecting metrics

As showed below no agent install on this VM and we are able to see some MetaData and Metrics

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic4.png "MetaData and Metrics")


## Synthetic Monitoring ##

During the trial I also wanted to test the Synthetic Monitoring, I was able to configure in some very easy step, please note that this is only an HTTP test. Synthetics test provide END-to-END visibility for validating that end users can perform critical business transactions.

In this test I setup an HTTP test on on www.saq.com (liquor store are manage by the government of Quebec), choose 3 different regions Canada Central – N. California and Oregon

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic5.png "Robots Location")


Information on the synthetic test

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic6.png "Information Synthetics")
 

From this view here you have some information to fine tune your website*

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic7.png "Information Synthetics")
 
In conclusion, for the first phase, I was very satisfied with what I saw! The easiness, the simplicity and the integration of DataDog with other components, everything worked as expected and was very straight forward. Now let’s start the assigment and I hope everything goes well! 





# Phase II: The assignment

## Collecting Metrics:

•	Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Tags that were added: environment:dev, region: Canada, role:database

 ![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic8.png "Tags")

Config of the datadog.yaml file

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic9.png "Tags DataDog yaml")
 

•	Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

MySQL was chosen for this exercise, we can see the installation from different views:

1.	From the Host Map

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic10_1.png "MySQL Host Map")
 
2.	From the Infrastructure list 

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic11.png "MySQL Infra List")

3.	Intetagrations

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic12.png "Integration")
 

MySQL – Overview Dashboard

This OOB Dashboard offers a quick visibility into MySQL only with a few clicks.

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic13.png "MySQL Overview Dashboard")
 
•	Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. I named it testSupportRandom

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic14.png "Custom Agent Check")
 
•	Change your check's collection interval so that it only submits the metric once every 45 seconds.
The yaml file was create under /etc/datadog-agent/conf.d$ ls

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic15.png "Path")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic16.png "Custom Test")
 
Run the command:
sudo -u dd-agent -- datadog-agent status to validate

And I was able to see 

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic17.png "Status")

From the UI:

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic18.png "From UI")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic18_1.png "From UI")


 
•	Bonus Question Can you change the collection interval without modifying the Python check file you created?


## Visualizing Data:



## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

•	Warning threshold of 500
•	Alerting threshold of 800
•	And also ensure that it will notify you if there is No Data for this query over the past 10m.

Configuration of the new Monitor Metric “Test Support Random”

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic19.png "Monitor Metric") 

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic20.png "Monitor Metric 1") 
 

Here are all the email received from the alert:

•	Send you an email whenever the monitor triggers.
•	Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
•	Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
•	When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic21.png "Email")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic22.png "Email 1")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic23.png "Email 2")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic24.png "Email 3")

 

More print screens from the Monitor Message with detail graphics

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic25.png "More Detail")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic26.png "More Detail 1 ")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic27.png "More Detail 2") 

Example of event sent @user

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic28.png "Example of event")



Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

•	One that silences it from 7pm to 9am daily on M-F,
•	And one that silences it all day on Sat-Sun.
•	Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


•	One that silences it from 7pm to 9am daily on M-F,

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic29.png "Silence M-F")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic30.png "Silence M-F 1")
 
•	And one that silences it all day on Sat-Sun.

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic31.png "Silence S-S ")
![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic32.png "Silence S-S 1")


## Collecting APM Data:


For this exercise I used Flask APP (Python) and it was instrument by Datadog’s APM,  I had to do some research since I had never use FLASK in my carreer !

Print screen of the code

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic33.png "Flask Code")


Before running the application:

•	sudo apt-get install python-pip

•	pip install flask

•	pip install ddtrace

To run the app and instrument the tracing:

- export DD_service=app.py

- ddtrace-run python app.py

But at first try it did not work, I had to update the package installer by  
python3 -m pip install --upgrade pip fallow by pip install ddtrace for the tracing library for Python

Re-run
ddtrace-run python app.py

And application is working

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic34.png "Flask App")

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic35.png "Flask Code 1")

A simple command was create to generate traces

TAG009442361643:flask patricio.martinez$ while True

> do

> curl http://localhost:5050/api/trace

> sleep $(( RANDOM % 15 ))

> done


Traces from the Datadog console

![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic36.png "Traces")


![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic37.png "Traces 1")


 
 Services view
 
 ![alt text](https://github.com/Patolecanard/hiring-engineers/blob/master/Screenshots/pic38.png "Services")
 
 
### Bonus Question: What is the difference between a Service and a Resource?

A resource is a particular action for a given service (typically an individual endpoint or query).

Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of scaling instances. Some examples:

•	A group of URL endpoints may be grouped together under an API service.

•	A group of DB queries that are grouped together within one database service.

•	A group of periodic jobs configured in the crond service.

