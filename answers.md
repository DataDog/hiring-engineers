
<h2>Prerequisites - Setup the environment:</h2>

Your answers to the questions go here-


I already had few virtual machines configured and ready to use in VMWare Workstation installed locally. I decided to use Ubuntu VM for this exercise.

Signed up as Datadog Recruiting Candidate to get necessary credentials to install agent.


<h2>Collecting Metrics:</h2>

**•	Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

Added tags in agent config file datadog.yaml

![tags in yaml](https://i.imgur.com/Y7VYyfC.png)

Screenshot of HostMap page in DataDog

![tags in UI](https://i.imgur.com/eIefCI6.png)

**•	Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

Installing MySQL database
$ sudo apt-get install mysql-server-5.6
Creating the user
$ sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'syedghouri68';"

Granting necessary permissions

$ sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
$ sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"

$ sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
Creating mysql.yaml file
$ sudo vi mysql.yaml

![mysql yaml](https://i.imgur.com/qyJYIEH.png)

Verifying the integration

$ sudo datadog-agent status

![verifying integration](https://i.imgur.com/JDkCp4S.png)

**•	Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

This is achieved by creating two files - Check Module file and YAML configuration file. mycheck.yaml file is placed in conf.d directory. Python module file is placed in checks.d directory, Both the files has same name mycheck.

![mycheck python](https://imgur.com/nyE0kdo.png)

**•	Change your check's collection interval so that it only submits the metric once every 45 seconds.**

![collection interval](https://imgur.com/uU3x0PK.png)

**•	Bonus Question Can you change the collection interval without modifying the Python check file you created?**

Collection interval is changed in YAML file for the tag min_collection_interval. 

<h2>Visualizing Data</h2>

**Utilize the Datadog API to create a Timeboard that contains:**

**•	Your custom metric scoped over your host.**

**•	Any metric from the Integration on your Database with the anomaly function applied.**

**•	Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.**

I had few issues setting up datadog API. The issues was regarding SNIMissingWarning. Since im using python 2.7 I had to make use of pyOpenSSL. The following links help is setting up and it finally worked.

https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings

https://cryptography.io/en/latest/installation/#building-cryptography-on-linux

On referring API docs, the dashboard is created using the python API.

•	First an API key is generated

•	In the code python_timeboard.py, 3 graphs are added

•	Query for custom metric scoped over your host.
avg:my_metric{env:my_ubuntu1}

•	Query for anomaly function applied on metric from databae
anomalies(avg:mysql.performance.queries{mytag_hiring_challenge} by {host}, 'basic',2)

•	Query for custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
sum:my_metric{mytag_hiring_challenge}.rollup(sum, 3600)


Once this is created, Dashboard is accessed from Dashboard List in the UI:

•	Set the Timeboard's timeframe to the past 5 minutes

This is completed by clicking and dragging the cursor in the timeseries plot. The windows of 5 min is set by dragging cursor only for small portion

•	snapshot of this graph sent using @ notation.

![fivemin interval](https://imgur.com/pyu6UbB.png)

Dashboard:

![dashboard](https://imgur.com/WrJeYhd.png)

•	Bonus Question: What is the Anomaly graph displaying?

Anomaly graph shows if the metric value is out of range of stipulated upper bound and lower bound. The direction and intensity (deviation number)of bounds, the time period of lookup data can be decided based on query. 


<h2>Monitoring Data</h2>

Setting the thresholds:

![thresholdset](https://imgur.com/syePsge.png)

Monitor message: 

![monitor message](https://imgur.com/qaODQTS.png)

Alert Monitor:

Note: I had to deliberately generate random numbers between 800 and 1000 so that average in in last 10 min would be more than 800 to trigger this alert.

It also includes metric and host ip

![Alert monitor](https://imgur.com/Rncjgy6.png)

Warning monitor:

![Warning monitor](https://imgur.com/7O1WMwK.png)

No data monitor

![No Data Monitor](https://imgur.com/nL5gdnp.png)

**Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:**

One that silences it from 7pm to 9am daily on M-F

Note: The time format in email is changed to UTC

![downtime 1](https://imgur.com/0maZ2ou.png)

Email notification : time in UTC

![Email notification](https://imgur.com/1V4N4F1.png)

One that silences it all day on Sat-Sun.

![downtime 2](https://imgur.com/GPtiklv.png)

Email notification: time in UTC

![email notification](https://imgur.com/yrZnSs5.png)


<h2>Collecting APM Data</h2>

The given app is instrumented. I had few issues in the beginning about connection being refused. I fixed the indentation in yaml file and it worked.

Following links were used as reference

http://pypi.datadoghq.com/trace/docs/#module-ddtrace.contrib.flask

https://docs.datadoghq.com/tracing/setup/python/

Screenshots:

![my-app](https://imgur.com/IWUCsaV.png)

![infrastructure](https://imgur.com/5UsbNZI.png)

Links:

https://app.datadoghq.com/apm/service/my-app/flask.request?start=1533539070348&end=1533625470348&env=hiring_challenge&paused=false

https://app.datadoghq.com/apm/services?start=1533539121190&end=1533625521190&paused=false&env=hiring_challenge

**Bonus Question: What is the difference between a Service and a Resource?**

A service is a set of processes that do the same job. For instance, a simple web application may consist of two services:

A single webapp service and a single database service. A service can be of one of 4 tags - web, database, cache, custom


A Resource is a particular action for a service.

For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks).
For a SQL database service a resource is the query itself.

reference : https://docs.datadoghq.com/tracing/visualization/

**Final Question : Is there anything creative you would use Datadog for?**

I see datadog as a powerful monitoring tool. It is also a platform to understand and act in real time to varying behaviour of resources and applications across large number of hosts. 

In my last assignment, I worked on the anomaly detection for financial domain. Based on the solution we had, I feel datadog would have surely helped us to automate configuration of possible anomalous scenarious and thereby making it easy and simple. Datadog would have served the purpose of acting in real time for a fraudlent transactions efficiently.I think datadog can be used in number of domains - It can be used in transportation industry to monitor the state of vehicles, for example flight times can be monitored based on availability and demand to provide better customer service.(I see Jetstar airways in Australia has horrible time management). It can also be of help in traffic management by appropriately signaling the traffic based on the capacity on road. In ecommerce, datadog can help in dynamic pricing of items based on their demand. In manufacturing industry, datadog can be of help by ensuring the whole process of manufacturing cycle completes successfully by configuring it appropriately to handle faulty situations. 


**Thank you for going through the answers and giving me the opportunity to explore datadog. I look forward to work for datadog as Solutions Engineer.** 


Appropriate files and screenshots are added
















