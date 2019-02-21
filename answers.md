        Name: Sanjana Raj; Datadog: Solutions Engineer-San Francisco- Hiring Challenge.
I used Vagrant on my Mac OS, as I felt using a VM is much better for resolving bugs and it is faster.

Prerequisites - Setup the environment
1.	I downloaded Vagrant from the official website, along with the VirtualBox by Oracle for hypervisor.
2.	Then, instead of using just vagrant init, I found it better and more efficient to install it with the required OS (in this case-Ubuntu 16.04). 
3.	I used ‘vagrant init bento/ubuntu-16.04’ on the terminal to start my vagrant.
4.	Then I used the command ‘vagrant up’ which installed the vagrant file in my local directory. I then ssh’ed into the VM using ‘vagrant ssh’.

  ![image](https://user-images.githubusercontent.com/32622982/53146155-ff1c9180-3557-11e9-8898-7a3f97a5afb6.png)

5.	I signed up for Datadog as recruiting candidate with my gmail address and the required fields.
6.	As a next step, I installed the datadog-agent for Ubuntu by following the steps in the UI. I used the command given by datadog in my terminal.

  ![image](https://user-images.githubusercontent.com/32622982/53146105-d1374d00-3557-11e9-914c-4bc473ae03a1.png)
	
7.	The above screenshot shows that the agent was successfully installed and running. 
8.	To confirm if the agent was running, I used ‘sudo service datadog-agent status’ command

  ![image](https://user-images.githubusercontent.com/32622982/53146062-a947e980-3557-11e9-8e6a-345744ee0cfc.png)

Collecting Metrics:
1.	Adding tags to the agent makes it easier to monitor an agent when the server and infrastructure become more complex. Ex: region, role, environment, name, field, etc. usually in the key-value pair. 
2.	I added tags by navigating to the directory which has the datadog-yaml file. It is in /etc/datadog-agent/datadog.yaml.

  ![image](https://user-images.githubusercontent.com/32622982/53146208-30955d00-3558-11e9-8434-fe20662ed81b.png)

3.	Any editor can be used to change the tags in the file, I used the nano editor. 
4.	In the file, I looked for the tags section, uncommented it and added ‘region: west’ tag.

  ![image](https://user-images.githubusercontent.com/32622982/53146247-5c184780-3558-11e9-9b9b-8aa9f1660a80.png)

5.	I viewed my host on the datadog UI as soon as it started reporting along with the tags.

  ![image](https://user-images.githubusercontent.com/32622982/53146315-9b469880-3558-11e9-8c25-19677a486b0b.png)
 
6.	I navigated to the Host Map page to view my host and also see the tags that I added earlier. The results can also be filtered out based on the tags. Here, I have used ‘region – west’ tag.

  ![image](https://user-images.githubusercontent.com/32622982/53147000-0c874b00-355b-11e9-93e3-a477b846136f.png)

7.	I Installed PostgreSQL on my vagrant machine from the official website

  ![image](https://user-images.githubusercontent.com/32622982/53147029-21fc7500-355b-11e9-85ab-46d0e7aeb5b5.png)

8.	Then, I installed and configured the appropriate PostgreSQL integration in the datadog UI, the screenshot below elaborates the configuration.
9.	I created a postgres.yaml file in the datadog-agent/conf.d/postgres.d directory to configure the integration with PostgreSQL on my local machine.
10.	I restarted the agent from terminal and verified that the file exists in checks.d directory in etc/datadog-agent.

  ![image](https://user-images.githubusercontent.com/32622982/53147186-9d5e2680-355b-11e9-8caf-2eb244b16f99.png)
	
Custom Agent Check.

1.	To create a custom agent check, I created two files in two different directories. The first file I created is a yaml file for configuration in etc/datadog-agent/conf.d directory.
2.	I named the file mymetric.yaml in which I wrote the following script.

  ![image](https://user-images.githubusercontent.com/32622982/53147068-47897e80-355b-11e9-861b-4ed898efdb04.png) 
	
3.	The second file is a python script in the etc/datadog-agent/checks.d directory. The python script and the yaml file should always have the same filename. 
4.	In mymetric.py file, I wrote a simple function to create a metric called hello world and used a rand() function to generate a value between 0 and 1000.
        *The mymetric.py script is attached in the scripts folder*
5.	To change the interval, I modified the mymetric.yaml file by changing the instances object to 45 seconds. The above screenshot shows the changes to the interval.

Visualizing Data:
1.	Datadog has its own API to create features in any language of your choice. I used the API in python to create a Timeboard which will display 3 different graphs.

     *The custom_timeboard.py script is attached in the scripts folder* 

2.	The script has three functions:
•	To show the metrics over the custom-metric I created in the previous step called ‘hello.world’.
•	To show the anomaly for the postgres-bgwriter-write-time metric from the PostgreSQL integration installed earlier.
•	To show the metrics for the rollup to sum all points. 

  ![image](https://user-images.githubusercontent.com/32622982/53147294-fcbc3680-355b-11e9-95d1-67aca3af1216.png)

3.	The timeboard generated was displayed on the Dashboard list menu in the datadog UI. 

  ![image](https://user-images.githubusercontent.com/32622982/53147330-21b0a980-355c-11e9-9984-7f41cdb482ec.png)

What is the anomaly graph displaying?
Answer: When the PSQL makes commits, the graph shows the activity.

3. Monitoring Data
1.	To avoid monitoring the data constantly, I set up alerts for warning threshold, alerting threshold and also for alerts for no data reported.
2.	I used the monitor menu in the UI and set up alerts and wrote custom alert messages to get notifications on my email address when the alerts are triggered.

  ![image](https://user-images.githubusercontent.com/32622982/53147364-3e4ce180-355c-11e9-931f-26d807eb1fd6.png)
	
	![image](https://user-images.githubusercontent.com/32622982/53147397-56246580-355c-11e9-84b6-80c91af50bb7.png)

3.	The screenshot below shows the alert notification.

  ![image](https://user-images.githubusercontent.com/32622982/53147468-81a75000-355c-11e9-8f99-389e97c98b3c.png)
	
  ![image](https://user-images.githubusercontent.com/32622982/53147512-9edc1e80-355c-11e9-84e3-aa013730da24.png)
	

Bonus Question: Scheduled downtime for after work-hours from 7 PM to 9PM M-F.

  ![image](https://user-images.githubusercontent.com/32622982/53147559-bd421a00-355c-11e9-9746-0a415cea7771.png)
	
Scheduled downtime for weekends all day - Saturday and Sunday.

	![image](https://user-images.githubusercontent.com/32622982/53147580-cb903600-355c-11e9-93be-0d598c48ac33.png)
	
Collecting APM Data:
1.	Datadog lets you use APM data to monitor your application and collect metrics.
2.	I used the given Flask application in a new file called app.py in a new datadog directory. 
3.	I installed Flask on my machine using ‘pip install flask’. To run the flask app, I could either use virtualenv or ‘flask run’ with the host ip or port number.
4.	The mandatory step before running the application is to set an environment variable to the config file for which I used ‘export FLASK_APP=config.cfg” to set my env variable.
5.	To collect the APM data, I modified my app.py file to install the datadog tracer to trace my functions.
6.	I could either use ddtrace-run or tracer middleware. I tried both but I faced challenges in ddtrace-run as no metrics were reported back. 
7.	I tried troubleshooting by reinstalling and modifying my program and verified for any bugs in the app but there were no metrics reported.
8.	Then, I chose to use another custom tracer which is the middleware. The tracer started running on the host, reporting APM services and collecting metrics.

  ![image](https://user-images.githubusercontent.com/32622982/53147657-0d20e100-355d-11e9-981e-66cca5132693.png)

9.	The application’s infrastructure metrics are shown in the graph and below is the screenshot

  ![image](https://user-images.githubusercontent.com/32622982/53147689-29bd1900-355d-11e9-9c1b-e6fb9e56ec09.png)
	
Question: What is the difference between a Service and a Resource?
Answer: A service can be defined as a function that does a task. It can be a unit of design and implementation. It can be a database, interceptor, API endpoint etc. A resource describes the implementation or action of a service like a query to a database. We can think of service as a verb and resource as a noun.
Final Question:
Is there anything creative you would use Datadog for?

1.	Stock Market Prediction - Based on daily highs and lows of the stock price.
2.	Personal Health Tracking 
                - Sleep Monitoring and PSQI Sleep score computation.
                - Weight loss and gain based on calorie intake and diet.
3.	Traffic Monitoring based on your saved routes on freeways – Can monitor traffic on your routes and alert you/notify you about the optimal time to avoid traffic.


Bonus application – Minitwit

I wanted to try collecting metrics via APM with a custom application I wrote in python flask. It is a clone of Twitter and it uses sqlite3 as the database.

Challenges faced during APM for this custom application – I could install the required dependencies and run the application perfectly. I used ddtrace for this and it was showing one service reporting and it was collecting metrics. The only problem was with the UI, when I navigate to APM services, there was no metrics shown. My application was sending data, but it was not shown in the UI. 

I have attached a few screenshots to show a glimpse of my application, while I ran it locally on port 5000 from my Mac.

Log in Page.

		![image](https://user-images.githubusercontent.com/32622982/53147793-802a5780-355d-11e9-8bc0-4359affac270.png)
		
Sending a tweet and glimpse of your timeline.

		![image](https://user-images.githubusercontent.com/32622982/53147821-933d2780-355d-11e9-8ba1-ac5bbd8ccc39.png)

Public Timeline- shows tweets from all followers.

		![image](https://user-images.githubusercontent.com/32622982/53147858-abad4200-355d-11e9-9dbb-586842d73e37.png)
