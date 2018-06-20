# Logan Morales - Technical Exercise

## Prerequisites - Setup the environment

To set up my environment, I chose to utulize Virtualbox to spin up an Ubuntu Virtual Machine. The benefit of using a virtual machine over a native system, in my opinion, is the convenience of what I like to call... 'Nuking it'. 

![alt text](https://media.giphy.com/media/YA6dmVW0gfIw8/giphy.gif "Logo Title Text 1")

If something goes wrong, or I make a few config changes that don't play nice with other services, I have the luxury of nuking it and starting fresh within just a few moments. While working with new technologies (and even with familiar ones) it is very comforting to have this fail safe in place - it makes me feel safe to know nothing I do is affecting my core machine and I am working in a complete sandbox. 

After getting my VM up and running, I created a trial account with Datadog and started sniffing around. I added my Ubuntu integration, used the install script to get my system connected and within a few moments, began to see metrics from my VM coming in.
![alt text](https://i.imgur.com/FEdqXWr.png "Logo Title Text 1")

## Collecting Metrics

### Tags... Oh tags.
![alt text](https://media.giphy.com/media/3o6Ei0fWOw1iQ79d0A/giphy.gif)

Following alongside the [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) I was able to locate the `datadog.yaml` config file inside of `/etc/datadog-agent` and make a few changes:

- `sudo nano datadog.yaml`
- Uncomment out the 'tags' section
- Change to:
```
tags:
	- name:logan
	- applying_for:solutions_engineer
```

My configuration file looks like this:

![alt text](https://i.imgur.com/2im4SJj.png "Logo Title Text 1")

I restarted the datadog- agent using 
`sudo service datadog-agent restart` 
so that the agent would read the updated config file and my tags populated inside of Datadog's interface within a few minutes:

![alt text](https://i.imgur.com/XqA2WIu.png)

### Lets get that database going!

I was first introduced into databases during my time at General Assembly where we learned PostgreSQL. Recently, I have been working with MySQL quite a lot and I'm going to use this for my database integration. 

I took the following steps to get this going:
	
1. `sudo apt-get update` to update the package index
2. `sudo apt-get install mysql-server` to install MySQL
3. Follow the [Datadog documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) for installing the MySQL integration:
	- I created a user for the datadog agent with rights to the MySQL Server using the commands:

	```
	sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '$password'
	sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
	```

	- I also opted to receive full metrics catalog by using the following command provided in the docs:

	```
	sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
	sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
	```

	- Moving on! Next I edited the MySQL config file for datadog inside of `/etc/datadog-agent/conf.d/mysql.d/` to connect MySQL to my agent. I created a working copy of the example file 
	(`conf.yaml.example`) using `cp conf.yaml.example ./conf.yaml` and un-commented out the lines corresponding to the documentation provided by Datadog:

	```
	init_config:

	instances:
	  	server: localhost
    	user: datadog
    	pass: $password 
    	tags:
        	optional_tag1
        	optional_tag2
    	options:
        	replication: 0
        	galera_cluster: 1
	```

   Here is a screenshot of my configuration file (`/etc/datadog-agent/conf.d/mysql.d/conf.yaml`):
	
   ![alt text](https://i.imgur.com/ViXlih0.png)

   - I then restarted my agent - `sudo service datadog-agent restart` and ran a check command `sudo datadog-agent check mysql | more` . I appended `| more` so that I could scroll through the results. 

   Here is a screenshot of the check command results:

   ![alt text](https://i.imgur.com/gLBcC2A.png)

   And here is Datadog web interface reporting the metrics from my MySQL integration:

   ![alt text](https://i.imgur.com/AsY1xUt.png)

### Custom Agent reporting metrics with random integer between 1 and 1000.

To understand the process of doing this, I spent a lot of time reading over the [documentation](https://docs.datadoghq.com/developers/agent_checks/) provided by Datadog. Following along with the documentation, here are the steps that I took:

1. `cd /etc/datadog-agent/conf.d/` getting into the directory for the .yaml file.
2. `sudo touch my_metric.yaml` creating a new config file, sudo rights required.
3. `sudo nano my_metric.yaml` to edit the file and filled with:

	```
	# barebones configuration boilerplate
	
	init_config: 	

	instances:
    	[{}]
	```

   Here is a screenshot of my configuration file:

   ![alt text](https://i.imgur.com/FIiMzNX.png)

4. `cd /etc/datadog-agent/checks.d/` getting into the directory for the python script.
5. `sudo touch my_metric.py` must be the same name as the .yaml created in step 2, sudo rights required.
6. `sudo nano my_metric.py` to edit the file and filled with:
	
	```
	from checks import AgentCheck	# Required, inherits from AgentCheck
	import random					# import random number package

	class CustomCheck(AgentCheck):  # define class CustomCheck
		def check(self, instance):
			self.gauge('my_metric', random.randint(0,1000))
	```

   Here is a screenshot of my python file:

   ![alt text](https://i.imgur.com/MDVntv8.png)

7. my_metric Inbound!

   ![alt text](https://media.giphy.com/media/tG6ZDOfW5Xeo/giphy.gif)

   Screenshot of my_metric on Datadog

   ![alt text](https://i.imgur.com/DvsDEob.png)

### 45 Second Collection Interval

To change the collection interval of my_metric, I simply followed the same documentation mentioned above. I modified the file 'my_metric.yaml' to add `min_collection_interval: 45` under `init_config`. The file contents looks like this:

```
init_config: 	
	
instances:
    - username: <$username>
    - password: <$password>
    - min_collection_interval: 45
```

And here is a screenshot my of 'my_metric.yaml' file:

![alt_text](https://i.imgur.com/Dp4HJcG.png?1)

Here is a screenshot of the metric on a 45 second interval from Datadog:

![alt_text](https://i.imgur.com/1E4KIro.png)

### BONUS!!

Changing the collection interval seems to be a key feature of adding a custom metric. I changed the interval using the 'my_metric.yaml' file and did not need to touch my python file

## Visualizing Data

To accomplish this task, I carefully ready the [documentation](https://docs.datadoghq.com/api/?lang=python#create-a-timeboard) on using the API to create a new Timeboard. 

Lets begin!

![alt_text](https://media.giphy.com/media/WZ4M8M2VbauEo/giphy.gif)

1. Get the API and Application Key - It's easy to do:
	- Hover over 'Integrations' from the sidebar and select 'APIs'.
	- An API key is generated by default and resides at the top of the page under the section 'API Keys'.
	- Generate an Application Key - Just below the API Key section - and give it a name.

2.  Test out the API using Postman!
	- Before getting to the final product, I generated some test timeboards using Postman to iron out the bugs that were sure to come 👀
	- I made a test timeboard called 'Hi there' that I pulled from a file on Datadogs [documentation](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs) on using Postman with Datadog. Below is a screenshot of the timeboard in Datadog:

	![alt_text](https://i.imgur.com/bxLPTZI.png)

	- Next, I created a timeboard with my custom metric scoped over my host. Here is my script and a screenshot of the timeboard in Datadog:

	![alt_text](https://i.imgur.com/TLee4CM.png)

	```
	{
      "graphs" : [{
          "title": "Metric over Host",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Logan's timeboard1",
      "description" : "Made by Logan Morales",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
	```

	- Moving on! Then, I made a another timeboard with anomaly information on my MySQL database integration. This was a bit more difficult because I didnt initially know how to connect the MySQL integration. After navigating to the 'Integrations' page and Selected 'MySQL', I navigated right to 'Metrics' and found some usuful information I can look for. I combined this with the anomaly function found in Datadogs [documentation](https://docs.datadoghq.com/graphing/miscellaneous/functions/#anomalies) Below is my script and a screenshot of the timeboard in Datadog.

	![alt_text](https://i.imgur.com/rhhTRL6.png)

	```
	{
      "graphs" : [{
          "title": "MySQL Anomoly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mysql.net.connections{*}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Logan's timeboard2-1",
      "description" : "Made by Logan Morales",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
	```

	- Next! To make the 'custom metric with the rollup function applied to sum up all the points for the past hour into one bucket'... I used the [rollup function in Datadog docs](https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup) to assist me on this one. Below is my script and a screenshot of the timeboard in Datadog.

	![alt_text](https://i.imgur.com/fP0ygb5.png)

	```
	{
      "graphs" : [{
          "title": "Fruit Rollups 🍭",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Logan's timeboard3",
      "description" : "Made by Logan Morales",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
	```

3. After getting all of my individual timeboards together I put them together into one... GIANT... TIMEBOARD! Script and Datadog screenshot below:

![alt_text](https://i.imgur.com/0PRUgce.png)

```
{
      "graphs" : [{
          "title": "Fruit Rollups 🍭",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      },{
          "title": "MySQL Anomoly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mysql.net.connections{*}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      },{
          "title": "Custom Metric over Host",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Logan's Custom Ultimate Timeboard",
      "description" : "Made by Logan Morales",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
```

4. I set the timeboard to 5 minutes by using my mouse to click and drag over a 5 minute window. There is no data for the rollup sum because there was no data yet for the past hour since restarting my system. Below is a screenshot of the 5 minute timeboard:

![alt_text](https://i.imgur.com/Jihtpt8.png)

5. Next! I followed this [blog post](https://www.datadoghq.com/blog/real-time-graph-annotations/) by Isaac Sadaqah to help me with the snapshot of the graph. I cliked on the camera icon next to my graph and left a comment '@loganjmorales@gmail.com ANOMALIES INBOUND~'. There is a screenshot of my action, as well as the graph in my inbox below:

![alt_text](https://i.imgur.com/PorCDKo.png)

![alt_text](https://i.imgur.com/gOOdhmB.png)

6. BONUS!

During my internship at [Comodo](www.comodo.com), we spent a great deal of time performing tasks of an everyday data analyst. One of the biggest tasks was understanding and implementing anomaly detection algorithms on big data. Applying that knowledge to the metric caught by Datadog, the anomaly graph is displaying events that don't quite align with the 'normal' behavior. Anomaly algorithms function to detect what that normal behavior is and uses it as a baseline for detecting behavior that is not normal. In my graph, the red lines are used to identify and bound a particular moment where the points are not behaving like 'normal'. There is a also a grayed out line that signifies where the datapoints should be and where they're deviating from. Anomaly detection is extremely important for analyzing any dataset. In my scenario, it is useful to have the anomaly graph beside the others because I can look at other useful information that may be contributing to the metric behaving abnormally. 

## Monitoring Data

Next we want to create a new metric monitor that will alert me if the average of my custom metric is above the following values over the course of five minutes:
	- Warning threshold of 500
	- Alerting threshold of 800
	- Notify if there is No Data for this query over the past 10 minutes

Here are my steps!

1. Hover over the 'Monitors' section in the navigation and select 'New Monitor'. I want to monitor my custom metric (my_metric), so I selected 'Metric' as my monitor type.

2. I left the detection method at it's default (threshold alert) and defined the metric as 'my_metric'. Setting up the alert conditions, I filled in 800 next to 'Alert Threshold' and 500 next to 'Warning Threshold'. I also changed the notify if data is missing field from 'Do not notify' to 'Notify if data is missing for more than 10 minutes'. In the 'Say whats Happening' section, I filled it in with the following:

```
@loganjmorales@gmail.com HEY! YOU!! THERE'S A PROBLEM WITH {{host.name}}

{{#is_alert}}
![alt_text](https://media.giphy.com/media/3o6Zt3qAcq9gq4wkWA/giphy.gif)
ALErt! ALERTTT!

Host: {{status.hostIP}}

Current metric value: {{value}} 
{{/is_alert}} 

{{#is_warning}}
Keep it cool, this is just a warning

Current metric value: {{value}}
{{/is_warning}} 

{{#is_no_data}}
Nothing has happened in the past 10 minutes.

Current metric value: {{value}}
{{/is_no_data}}
```

WE'VE GOT MAIL!

![alt_text](https://media.giphy.com/media/xT5LMQCHxHbsuqDl28/giphy.gif)

Email of No Data State:

![alt_text](https://i.imgur.com/Y9yAyYF.png)

Email of Warning: 

![alt_text](https://i.imgur.com/bJv7xr0.png)

I was wondering why I wasn't getting any Alert emails... And then I thought 'OHHHHHH I forgot the metric is submitting RANDOM values'. The metric was programed to send a random value between 0 and 1000 so it makes sense that the average for all metrics over a 5 minute window was in the 500 range. I studied the metric and it was submitting values over 800, but not frequent enough for the average to be pulled up that high. So, in order to get this email, I kind of... changed... the metric 🤭

I changed the metric for the purposes of this particular challenge to submit random values between 800 and 1000 and sure enough...

![alt_text](https://i.imgur.com/1vzo51s.png)

![alt_text](https://media.giphy.com/media/LRVnPYqM8DLag/giphy.gif)

3. BONUS!

In order to set up the schedule downtimes, I noticed a tab at the top of the Monitors pages 'Manage Downtime'. I navigated to that page and selected the yellow 'Schedule Downtime' button. 
	
   Mon-Fri
   - I selected my new monitor for the downtime and switched the mode to recurring. Here are the settings I gave to the Scheduled Downtime and a screenshot of the email notifying my of the downtime::

   ![alt_text](https://i.imgur.com/j1qlIPb.png)

   ![alt_text](https://i.imgur.com/1YftPO3.png)

   Weekends!
   - I followed the same steps mentioned above but with the following settings, along with a screenshot of the email notification:

   ![alt_text](https://i.imgur.com/756YVoW.png)

   ![alt_text](https://i.imgur.com/NVOiCFY.png)

![alt_text](https://media.giphy.com/media/l4pTsh45Dg7jnDM6Q/giphy.gif)

## Collecting APM Data

Documentation used:

- [Flask docs for creating env](http://flask.pocoo.org/-ocs/1.0/installation/#install-create-env)
- [Datadog docs for tracing setup](https://docs.datadoghq.com/tracing/setup/)
- [Datadog docs for tracing setup env](https://docs.datadoghq.com/tracing/setup/environment/)
- [Datadog docs for tracing setup python](https://docs.datadoghq.com/tracing/setup/python/)
- [Datadog docs for Flask](http://pypi.datadoghq.com/trace/docs/#flask)

Before getting started, the first thing I did was install pip using `sudo apt-get install python-pip`.

After this, I took these steps:

1. `pip install ddtrace` to install Datadog's python tracing client. 

2. Navigate over the 'datadog.yaml' to enable apm.

```
apm_config:
  enabled: true
```

3. Navigate back to my root directory (`cd ~`) and install the flask environment. 
	- First I had to run `sudo apt-get install python3-venv`
	- Next, create my environment:
	```
	mkdir flaskapp && cd flaskapp
	python3 -m venv venv
	```
	-- Install flask on virtual environment with `pip install Flask`

4. I made my python file 'flaskapp.py' and filled with the provided python application:

```
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

I started the app with `ddtrace-run python flaskapp.py`

So the app started running, but it was not showing up in my infreastructure list on Datadog... 

Time to investigate.

![alt_text](https://media.giphy.com/media/ntxLxpZ0xW1kA/giphy.gif)

I tried going to the Datadog APM UI page to add the app into my system. I selected 'Python' for my language and ran the app - it still wasnt showing up in my interface.

Next, I tried putting in my old middleware by adding

```
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

```

to the Flask app. To run this time, I just used `python flaskapp.py` since I'm not pulling the middleware from `ddtrace-run python`. The app successfully ran again (screenshot below), but still nothing in the APM dashboard.

![alt_text](https://i.imgur.com/6X2GsOa.png)

Next I tried modifying the 'datadog.yaml' config file to see if I missed anything there. One thing I noticed was that `enabled: true` was not indented properly (I know that sounds silly but you never know...) so I fixed that up and restarted the agent. Unfortunately, this did not work either. 

![alt_text](https://media.giphy.com/media/l46CxmW82zcQiRghG/giphy.gif)

I am sad about not getting the Flask app to show in my Datadog dashboard, but I am proud of myself for getting the app to run. 

If selected to advance in the hiring process, I would like the opportunity to walk through the APM solution with a Datadog Guru and understand where I went wrong. I know I am close!

## FINAL QUESTION!!!

I have had a blast learning about Datadog and the many use cases for such robust monitoring system. Something I would like to see... Datadog for DOGS!! Seriously.

I have a few young pups and home and they are extremely active. They have a lot of space to run around and be dogs all over: In the house, in the yard, in my room... Any place they have the opportunity to be silly dogs they take full advantage. 

My family installed a wireless fence around the house and yard to make for a safe and easy border for the dogs. There is a small collar to enforce this. I like it. It's simple and makes a lot of sense. I think it would be a cool idea to take this a step further.

It would be WAY more interesting if the collar could, in addition to enforcing borders, collect metrics about the dog about their activity, whereabouts and their health. The data could be sent to an app on the owner's phone where they could see this data. The application could also implement monitoring technologies offered by Datadog to really understand the data that is coming back about the pup. Maybe Snowball isn't as active on a particular day, we could use anomaly detection to understand when that is happening and correspond it to other collected metrics about the dog's health during that instance. ENDLESS POSSIBILITIES! Please, PLEASE, let's not forget about the pups. 

![alt_text](https://media.giphy.com/media/4XSc0NkhKJQhW/giphy.gif)

Thank you for giving me the opportunity to undergo this challenge. It was so much fun and I hope to have more challenges like this in my future. <3


