#Datadog hiring engineer challenge
####*By Laurent Tran - tranlaurent@hotmail.fr*

I enjoyed to do this project a lot. Cloud monitoring sounds very interesting to me. Datadog has a bright future and I hope to be part of it with you.

Please see below the 5 levels I have completed, and an additional level 6 I have enjoyed doing to try the datadog - Docker container integration:
- [Level1](#Level1)
- [Level2](#Level2)
- [Level3](#level3)
- [Level4](#level4)
- [Level5](#level5)
- [Level6](#level6)
- [Conclusion](#conclusion)

Level 1 to Level 4 were done on the email id tranlaurent@hotmail.fr

Level 5 and 6 were done on the email id viet-tuan_laurent.tran@telecom-sudparis.eu
The trial version expired when I was doing Level 5 so I had to switch. I also switched the OS from Windows to Ubuntu to make the agentcheck installation easier.

Moreover, I have tried the project in both windows and unix, and found out that it's easier to do it in unix ( Ubuntu 12) because the tutorial is more adapted to Unix, especially for the location of the different check and configuration folders during the level5 for the agentcheck. Moreover, the troubleshooting in windows was painful for the Level5, so I decided to do th level5 in Ubuntu only

##Level1

*1.Signed up for Datadog*

*2.What is Datadog ?*

The **Datadog Agent** is piece of software that runs on the client's hosts. 
Its job is to faithfully **collect events and metrics** and bring them to Datadog on the client's behalf so that the client can do 
something useful with his monitoring and performance data.

The Agent has three main parts: the **collector**, the **dogstatsd**, and the **forwarder**.

The **collector** runs checks on the current machine for whatever integrations the client have and it will capture system metrics like memory and CPU.
**Dogstatsd** is a statsd backend server the client can send custom metrics to from an application.
The **forwarder** retrieves data from both dogstatsd and the collector and then queues it up to be sent to Datadog.
This is all controlled by one supervisor process. This is separate so that the client doesn't need to have the overhead of each application if the client doesn't want to run all parts.

*3. Event submitted via the API*

*4. Event appeared on my email tranlaurent@hotmail.fr*


![Alt text](welcome email .jpg?raw=true "welcome email received on my email tranlaurent@hotmail.fr")


##Level2

I created a simple website using python in backend. 
Please see the code  [In this repository](https://github.com/tranlaurentnyc/hiring-engineers/edit/master/webapp)

*The application is a toolkit in which you can watch videos, listen to your music playlist, locate yourself on a map, and  have access to the CNN's RSS. I have named my web application 'MyAmazingToolKit.com'. The Youtube, Google Maps and CNN APIs are used. You need to register / login to access to your toolkit. You can then also be part of a community of friends. Our metrics are mainly based on the 'Sign up' and 'Toolkit Community' pages. We will see the different characteristics of these pages, including the count of page view, the latency of the 'Toolkit Community' displaying the name of the friends within your community, according to the number of your friends.*


####This is a screenshot of the homepage of MyAmazingToolKit.com:

![Alt text](Level 1 -Python Web Application - FlaskApp.jpg?raw=true "Homepage of MyAmazingToolKit.com")

####The libraries I used to build my python web application are:

import MySQLdb 
*Create a connection to MySQL*

import sys 
*import the system library*

import random 
*to sample a random value*

from flask import Flask, render_template, request, json, redirect, url_for 
*Flask: A python Framework for creating web applications,
render_template : Library used to render the template files,
json: used to return json data,
request: Library used to read the posted values for the logging and signing up,
redirect: redirects to a url,
url_for: generates an endpoint for the provided method*

from werkzeug import generate_password_hash, check_password_hash 
*To create a hashed password*

import os 
*To interact with the operating system*

from time import time 
*To have the current time*

from datadog import statsd 
*Python client for DogStatsd*

You can visualize page views per second metrics on datadog interface, by using web.page_views metrics.

An extract of my code for the page view metrics on the home page looks like:


```
@app.route('/')
def main():

	#metric to count the  web.page_view
	statsd.increment('web.page_views')

	
	"""Render the main page."""
	return render_template('index.html')


```


![Alt text](Level2_web.page_views_2.jpg?raw=true "Page Views per second")

You can also see the metrics in the datadog interface following the link below with correct credentials: 
[page views per second] (https://app.datadoghq.com/metric/explorer?live=false&page=0&is_auto=false&from_ts=1457524711086&to_ts=1457534945500&tile_size=m&exp_metric=web.page_views&exp_scope=&exp_agg=avg&exp_row_type=metric)


Moreover, we can visualize the latency metric using *database.querry.time.95percentile* to see how long the queries took. We used a database of users subscribed to the website to perform querries on that database. Indeed, this way we can challenge this metric by increasing or decreasing the size of the database, to check that the latency increases or decreases.

An extract of my code to see the latency is:

```

@app.route('/showCommunity')
def showCommunity():

	#start timer
	start_time = time()
	print start_time
	#connection to the DB
	connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "cacapipi", db = "bucketlist")
	
	#prepare a cursor object using cursor() method
	cursor = connection.cursor()
	
	#execute the SQL query using execute() method
	cursor.execute("select user_name, user_username, user_password from tbl_user ")
	
	#fetch all the rows from the query
	data = cursor.fetchall()
	
	#print the rows
	
		
	for row in data:	
		print row[0], row[1]
	
	
	cursor.close()
	
	#close the connection
	connection.close()
	
	#return timer
	duration = time() - start_time
	print duration
	statsd.histogram('database.query.time', duration, tags = ["page:community"])
	statsd.gauge('test2',200)
	#exit the program
	sys.exit()
	

```


I overlapped on the same graph the **95 percentile (blue line)** showing the **querry longest times**, and the **median (purple line)** showing the query **median time**, following the example in the datadog tutorial.
This enables to compare the average time and longuest querries to **eventually detect a bug/default in the server** expressed by a **peak of the blue line**. In our example, the difference between the 95 percentile and the median time would have been more accurate and significant with more query requests.


See the latency evolution of the queries, depending on the database size:
For 115 rows in the database, the average latency is 0.06s  (Queries between 7.40am to 7.50am ). 
![Alt text](Level2_database_query_time_115rows.jpg?raw=true "Latency for a SQL querry in a 115 rows database")


For 250 rows in the database, the average latency is 0.14 s (Queries between 8.03am to 8.04am ). 
![Alt text](Level2_database_query_time_250rowsjpg.jpg?raw=true "Latency for a SQL querry in a 250 rows database")
For 500 rows in the database, the average latency is 0.26 s (Queries between 10.05pm to 10.11pm ). 
![Alt text](Level2_database_query_time_500rowsjpg.jpg?raw=true "Latency for a SQL querry in a 500 rows database")


We can summarize this result in the following tab:


| Number of the database rows        | Latency (ms)           | Time when the querry was performed  |
| ---------------------- |:--------------------:| -------------------------------------------------------:|
| 115      | 60 | Queries between 7.40am to 7.50am |
| 250      | 140      |  Queries between 8.03am to 8.04am |
| 500 | 260      |    Queries between 10.05pm to 10.11pm |


We can see the whole graph over the day between 7 am and 11 pm below:


![Alt text](Level2_database_query_time_comparaisons.jpg?raw=true "Latency for the three SQL querries")

*We notice that there is an anormal peak at the very beginning at around 7 am. Let's not take into accunt this peak. This peak may have been cause by a bug in my computer which made the querry time slightly longer that what it was supposed to.*

You can also look at the dashboard directly in the interface [here] (https://app.datadoghq.com/dash/106169/database-query-time?live=true&page=0&is_auto=false&from_ts=1457953796671&to_ts=1457957396671&tile_size=m&fullscreen=76417418)



##Level3

I created a Tagged metrics - web.page_views tagged page:home.

See an extract of the code showing the tag for the web.page_views

```
@app.route('/')
def main():

	#metric to count the  web.page_view
	statsd.increment('web.page_views',tags = ["page:home"])
	
	
	"""Render the main page."""
	return render_template('index.html')
	

```

You can notice that I have added a tag: I have  tagged the metric '**web.page_views**' by '**page:home**'.


![Alt text](Level3_Tagged metrics - web.page_views tagged page home.jpg?raw=true "Tagged web.page_views metric")


Also, I created a **latency metrics tagged for two pages on a same graph**: 'Toolkit community' page ( purple ) and 'Toolkit friend' page ( blue).
![Alt text](Level3_Tagged latency metrics per page.jpg?raw=true "Tagged web.page_views metric")

You can also look at the dashboard directly in the interface [here] (https://app.datadoghq.com/dash/107211/blank-dashboard?live=false&page=0&is_auto=false&from_ts=1458210156000&to_ts=1458213756000&tile_size=m&fullscreen=76678605)

Therefore, you can notice that the querries for the 'Toolkit community' page ( in purple ) take longer that the querries for the 'Toolkit friends' page ( in blue), because the friend list is smaller than the list of all the website's users.



##Level4;

In Level 4, we want to count (web.page_count metric) the different pages individually, and have a total count, which is the sum of the different counts.

To do so, we increment a global total count metric everytime a web.page_count metric is incremented.

For example, for my 'Login' webpage, when we increment '**web.page_views_login**', we also increment '**web.page_views_total**'.

```
@app.route('/login', methods=['GET', 'POST'])
def login():

	#metric to count the web.page_views_login
	statsd.increment('web.page_views_login',tags = ["page:login"])
	
	#metric to count the overall number of page views
	statsd.increment('web.page_views_total')
	
	
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('main'))
	return render_template('login.html', error=error)

```


I have created **different web.page_views metrics** (**in lines**) for the different pages of the website in the **same graph**. I have overlapped with these count metrics the total count metric '**web.page_views_total**' (**in blue column**) for a better visibility.

![Alt text](Level4_ count per page.jpg?raw=true "Count for different pages")



The colors are associated to the following pages of my website:

1. **dark blue**: home page
2. **red**: community page
3. **purple**: friends page
4. **orange**: login page
5. **grey**: signup page

You can also look at the dashboard directly in the interface [here] (https://app.datadoghq.com/dash/107211/blank-dashboard?live=true&page=0&is_auto=false&from_ts=1458213034894&to_ts=1458216634894&tile_size=m&fullscreen=76684262)


The graphs are spiky because they are 'counts'.


##Level5

I display here the metrics from the agentcheck test.support.random which shows some random values every 15 seconds.


![Alt text](Level5 - AgentCheck test.support.random .jpeg?raw=true "Agent check - random")

You can also look at the dashboard directly in the interface [here] (https://app.datadoghq.com/dash/113226/level-5---agentcheck?live=true&page=0&is_auto=false&from_ts=1459249191528&to_ts=1459252791528&tile_size=m&fullscreen=77704229)


Also, see the file randomCheck.py  ( located in /etc/dd-agent/checks.d/ in a Unix OS )

```
from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())

```


and the file randomCheck.yaml ( located in /etc/dd-agent/conf.d/ in a Unix OS )

```
init_config:

instances:
    [{}]

```

These two files are linked and need to have the same name: randomCheck.py, and randomCheck.yaml.
randonCheck.py is the check code. It imports the AgentCheck library and the random library. It will call the randomCheck.yaml to check the configuration and the defined instances. Here we didn't need any init_config and instances. Then the metric 'test.support.random' is defined as a gauge and sent to the agent, displaying a random value. By default, every 15 seconds, the random data will be sent. The random value is a normalized number between 0 and 1.

The following section is only optional. I wanted to try to use the docker container and integrate it with the datadog agent.

##Level6 
###(Docker container )

I have followed the tutorial and created a docker container which was then integrated in Datadog. In the two screenshots below, we can see the successful integration of the docker container with Datadog.


![Alt text](Level6_datadog_docker.png?raw=true "Docker ...")

![Alt text](Level6_docker_running.png?raw=true "Docker ...")


##Conclusion
To conclude, my first experience with Datadog was very interesting and pleasant. I am very motivated to pursue the hiring process. 

Thank you for reading my answers, and please don't hesitate if you have further questions,

Best regards,

Laurent Tran

