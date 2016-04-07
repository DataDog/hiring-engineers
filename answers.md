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


This is a screenshot of the homepage of MyAmazingToolKit.com:

![Alt text](Level 1 -Python Web Application - FlaskApp.jpg?raw=true "Homepage of MyAmazingToolKit.com")

The libraries I used to build my python web application are:

import MySQLdb 
#Create a connection to MySQL

import sys 
#import the system library

import random 
#to sample a random value

from flask import Flask, render_template, request, json, redirect, url_for
#Flask: A python Framework for creating web applications
#render_template : Library used to render the template files
#json: used to return json data
#request: Library used to read the posted values for the logging and signing up
#redirect: redirects to a url
#url_for: generates an endpoint for the provided method

from werkzeug import generate_password_hash, check_password_hash
#To create a hashed password

import os
#To interact with the operating system

from time import time 
#To have the current time

from datadog import statsd
# Use Statsd, a Python client for DogStatsd








We can visualize page views per second metrics on datadog interface, by using web.page_views metrics.

![Alt text](Level2_web.page_views_2.jpg?raw=true "Page Views per second")



You can also see the metrics in the datadog interface following the link below with correct credentials: 
[page views per second] (https://app.datadoghq.com/metric/explorer?live=false&page=0&is_auto=false&from_ts=1457524711086&to_ts=1457534945500&tile_size=m&exp_metric=web.page_views&exp_scope=&exp_agg=avg&exp_row_type=metric)



https://app.datadoghq.com/metric/explorer?live=true&page=0&is_auto=false&from_ts=1457952953446&to_ts=1457956553446&tile_size=l&exp_metric=database.query.time.95percentile%2Cdatabase.query.time.median&exp_scope=&exp_agg=avg&exp_row_type=metric
Also please refer to the screenshot 'Level2_web.page_views.jpg'

I visualize the latency metric using database.querry.time.95percentile to see how long the queries took. We used a database of users subscribed to the website
I can challenge this metric by increasing the size of the database.

See the latency evolution of the queries, depending on the database size:
--for 115 rows in the database, the average latency is 0.06s  (Queries between 7.40am to 7.50am ). Please refer to the screenshot 'Level2_database_query_time_115rows.jpg'
--for 250 rows in the database, the average latency is 0.14 s (Queries between 8.03am to 8.04am ). Please refer to the screenshot 'Level2_database_query_time_250rowsjpg.jpg'
--for 500 rows in the database, the average latency is 0.26 s (Queries between 10.05pm to 10.11pm ). Please refer to the screenshot ' Level2_database_query_time_500rowsjpg.jpg'
I overlapped on the same graph the 95 percentile (blue line)showing the querry longest times, and the median (purple line)showing the query median time, following the example in the datadog tutorial.
This enables to see the average time and detect a peak of latency. The difference between the 95 percentile and the median time would have been more accurante with more query requests. 
https://app.datadoghq.com/dash/106169/database-query-time?live=true&page=0&is_auto=false&from_ts=1457953796671&to_ts=1457957396671&tile_size=m&fullscreen=76417418
Please refer to the screenshot 'Level2_database_query_time_comparaisons.jpg'



##Level3;

I created a Tagged metrics - web.page_views tagged page:home 
Please refer to the screenshot 'Level3_Tagged metrics - web.page_views tagged page home.jpg'


Also, I created a latency metrics tagged for two pages on a same graph: community ( purple ) and friends ( blue)
https://app.datadoghq.com/dash/107211/blank-dashboard?live=false&page=0&is_auto=false&from_ts=1458210156000&to_ts=1458213756000&tile_size=m&fullscreen=76678605

See refer to the screenshot ' Level3_Tagged latency metrics per page.jpg'




##Level4;

I have created different page views metrics for the different pages of the website in the same graph.

Please refer to the screenshot 'Level 4 count per page . jpg'


For a better visibility, I have displayed the single page count metrics in lines, and the total number of page views in column.

The colors are associated to the following pages of my website:

-dark blue : home page
-red: community page
-purple: friends page
-orange: login page
-grey: signup page

Please also refer to the link to the dashboard: https://app.datadoghq.com/dash/107211/blank-dashboard?live=true&page=0&is_auto=false&from_ts=1458213034894&to_ts=1458216634894&tile_size=m&fullscreen=76684262



The graphs are spiky because they are 'counts'.


##Level5

I display the metrics from the agentcheck test.support.random which shows some random values every 15 seconds.

Please refer to the link to the dashboard: https://app.datadoghq.com/dash/113226/level-5---agentcheck?live=true&page=0&is_auto=false&from_ts=1459249191528&to_ts=1459252791528&tile_size=m&fullscreen=77704229


Moreover, please refer to the screenshot: 'Level5 - RandomCheck test.support.random.jpg'

Also, see the file randomCheck.py  ( located in /etc/dd-agent/checks.d/ )
and the file randomCheck.yaml ( located in /etc/dd-agent/conf.d/ )



##Level6 
###(Docker container )

I have created a docker container and integrated it to Datadog.
Please see the integration in the screenshots below:
'Level6_docker_started.png', 'Level6_docker_running.png' and 'Level6_docker.png'
