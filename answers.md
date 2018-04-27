### Charlie Boutier - Solution engineer hiring test - April 26 2018

## 0 - Introduction
Welcome on board, here is my answer to the Solutions Engineering test. I did this test on a Macbook pro mid-2012 - macOS High Sierra 10.13.4. I followed the advice, I ran the Datadog Agent on a fresh ubuntu 12.04 VM via Vagrant. The answer is divided into 6 parts :

* Collectings Metrics
* Vizualizing Data
* Monitoring Data
* Collecting APM Data
* Final Question
* Conclusion

## 1 - Collectings Metrics
### Add tag in the agent config file <br />
Here are the path for the AgentV6 and the tags I put: 
* ``` /etc/datadog-agent/datadog.yaml``` <br />
* tags: country:france, region:brittany, role:test, machine:macbookPro2012 <br />
The first screenshots is the config file and the second one is Host mage page with the tags.

<a title="Config file">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Collecting_Metrics/Tag_config_file.png"></a>

<a title="Host and its tags">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Collecting_Metrics/host_tags.png"></a>

* Then a MySQL databased has been installed on the machine with the integration associated:
<a title="mySQL's database integration">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Testmd/Collecting_Metrics/mySQL_integration.png"></a>

<a title="MySQL's dashBoard">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Collecting_Metrics/mySQL_dashBoard.png"></a>

### Created a custom Agent check that submots a metric named my_metric with a random value between 0 and 1000. <br />
To write an Agent check it is important to do three important things: 
* First, write a python script in the folder ``` /etc/datadog-agent/checks.d ```
* Second, a configuration associated with the script placed in the folder ``` /etc/datadog-agent/conf.d ```
* Third, the python script and the config file must have the same name.
In that case, the python script is ``` sendMyMetric.py ``` and the config file ``` sendMyMetric.yaml ``` <br />

Here is the python script, sendMyMetric.py: <br />

```python
from checks import AgentCheck
from  random import randint
class sendMyMetric(AgentCheck):
	def check(self, instance):
	randomMetric = randint(0,1000)
	self.gauge('AgentCheck.my_metric', randomMetric)
```

The custom metric need to be sent once every 45 seconds. As mentioned in the documentation, we need to change the value of the collection interval by setting the value ``` min_collection_interval ``` in the config file on the ``` instances ``` section (Only for AgentV6). It is noted that the collector runs every 15-20 seconds. For example, if we set the value of ``` min_collection_interval ``` at 40, here is the behavior of the collector:
* First round, the collector value is 15 which is inferior at 40, the collector does not collect. 
* Second round, the collector value is 30 which is inferior at 40, the collector does not collect. 
* Third round, the collector value is 45 which is _bigger_ than 40, the collector will collect at 45 seconds. 

Look like 40 is a good value for our situation, here is the config file sendMyMetric.yaml:

```
init_config:

instances:
	-min_collection_interval: 40

```
<a title="custom metric Timeboard">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Collecting_Metrics/customMetric_Timeboard.png"></a>

### Bonus question 
* Can you change the collection interval without modifying the Python check file you created?

Actually, the usual way to change the collection interval is to edit the config file associated with the python file as demonstrated before. But I think we can do it in a tricky way. In fact, we could directly edit the AgentCheck class and set the default collection interval to the expected value. But that's mean it will be changed for every custom Agent Check we will write. So we need to be sure it will be worth it.

## 2 - Vizualizing Data
Here is the python script ``` createTimeboard.py ``` wrote to create a Timeboard answering those three instructions: 
* Your custom metric scoped over your host.
* Any metric from the Integration of your Database with the anomaly function applied.
* Your custom metric with the roll-up function applied, to sum up all the points for the past hour into one bucket

```python

from datadog import initialize, api
from datadog.dogshell.common import report_errors, report_warnings, print_err

#API and APP Key provided by Datadog's website in the setup section
options= {
	'api_key': 'f9154e2dfe7dca8325eb087ffb878fe3',
	'app_key': '497139b7d0c2dd1e82f55347b7e3cf14a6c1c980' 
}

#Initializing the API with the key
initialize(**options)

#Setting up the Timeboard

title = "API Timeboard !"
description = "Here is the timeboard created with the python API, let's have fun !"

#Preparing three different graphs
	#First graph: The custom metric (my_metric) scoped over the host
	#Second graph: MySQL's metric -> CPU time (per sec) with the anomaly function
	#Third graph: The custom metric with the roll up function (sum all the point for the past hour)
graphs=[
	{
		#Frist graph
		"title": "My custom metric",
		"definition":{
			"requests":[{
				"q": "AgentCheck.my_metric{*}",
				"type": "line",
				"style":{
					"palette": "dog_classic",
					"type": "solid",
					"width": "normal"
				}
			}],
			"viz": "timeseries"
		}
	},
	{
		#Second grqph
		"title": "MySQL CPU time (per sec)",
		"definition":{
			"requests":[{
				"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)",
				"type": "line",
				"style":{
					"palette": "dog_classic",
					"type": "solid",
					"width": "normal"
				}
			}],
			"viz": "timeseries"
		}
	},
	{
		#Third graph
		"title": "Custom Metric Roll Up Summ Past Hour",
			"definition":{
				"requests":[{
					"q": "AgentCheck.my_metric{*}.rollup(sum, 3600)",
					"type": "line",
					"style":{
						"palette": "dog_classic",
						"type": "solid",
						"width": "normal"
					},
					"conditional_formats": [],
					"aggregator": "avg"
				}],
				"viz": "query_value"
			}
	}
]

#Creation of the Timeboard through the API
read_only = True
timeboard = api.Timeboard.create(title=title,
					 	   		 description=description,
					 	   		 graphs=graphs,
					 	   		 read_only=read_only)

#Debug function : Allows to check log in case if anything happened
report_warnings(timeboard)
report_errors(timeboard)
```

Here is the Timeboard created by this script: 

<a title="API Timeboard">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Vizualizing_Data/past_hour.png"></a>

This is the snapshot of the past 5 min for the Anomaly graph. <br />

<a title="5 min snapshot">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Vizualizing_Data/past_5min_snapshot.png"></a>

## Bonus Question: What is the Anomaly graph displaying

The Anomaly graph is displaying three different things that are:
* Gray band: represent the area where the metric should stay
* Blue line: The metric is in the area represented by the gray band
* Red line: The metric is out of limit

Actually, the gray band has a coherent behavior only after 30 min. In fact, the input of the Anomaly's algorithm is too poor of data to give a correct answer before this period. It also depends if the metric is currently used or not.

## 3 - Monitoring Data
A monitor watches the value of one or several metrics and can notify the different users associate in the parameter. In this case, the main is to create a monitor that watches the average of the custom metric (my_metric). 

Here is the step to configure this monitor:

* Select the threshold Alert and choose the metric to watch.
<a title="1_2">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/1_2_steps.png"></a>

* Red square: Alert the user if the average of the custom metric is above 800 and warn him if it is above 500 over the 5 past minutes.
* Green square: Notify  if there is no data over the past 10 minutes.
<a title="3">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/3_step.png"></a>

* Write a custom message when we the monitor will alert or warn the users and print the host ip and host name as well in the red square. Inside the green square it's the user you want to notify.
<a title="4_5">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/4_5_steps.png"></a>

* Here are the graph's details with the warn and alert's conditions
<a title="Gaph">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/graph.png"></a>

* When there is an alert, warn or any notifications we programmed on the monitor, an email is sent like this one: 
<a title="Mail notification">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/mail_notifications.png"></a>

### Bonus Question
* Schedule two downtimes for this monitor
	* One from 7pm to 9am daily on M-F
<a title="Mail notification">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/Bonus/mail_weekly.png"></a>

<a title="Monitor">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/Bonus/weekly_MF.png"></a>
	* One that silences it all day on Sat-Sun
<a title="Mail notification">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/Bonus/mail_weekend.png"></a>

<a title="Monitor">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/Monitoring_Data/Bonus/weekend.png"></a>


## 4 - Collecting APM Data
* Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
```python
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
    app.run()
```
First, install the python client: <br />
 ``` pip install ddtrace ``` <br />
 
Then the python script has been change a bit. The ddagent is listening on the port:5000 and the default flask's configuraton is to run the server on the port 5000 as well, its has been changed to 5050.<br />
``` flaskData.py ```

```python
   from flask import Flask
   import blinker as _
   import logging
   import sys
  
   from ddtrace import tracer
   from ddtrace.contrib.flask import TraceMiddleware
  
  # Have flask use stdout as the logger
  main_logger = logging.getLogger()
  main_logger.setLevel(logging.DEBUG)
  c = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  c.setFormatter(formatter)
  main_logger.addHandler(c)
 
  app = Flask(__name__)
  traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
 
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
          app.run(port=5050)
```
Then strike the following command line to run the tracer: <br />
``` (flask)vagrant@precise64:~/flask$ ddtrace-run python flaskData.py ```
Here is the result of this command:
<a title="APM">
<img src="https://github.com/SilverGeekPanda/Datadog_Screenshots/blob/Pictures/APM/APM_Failed.png"></a>

But at this step, no traces have been sent to the APM dashboard has not been created. I am still looking why it is stuck on this. It will be great if we can exchange about that. I did not post an issue because this is my last day and my last hours.  

### Bonus Question
* What is the difference between a Service and a Resource? <br/>
According to the documentation, a Service is a set of processes that do the same job. While a Resource is particular for a service. 

## 5 - Final Question
### Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

### Is there anything creative you would use Datadog for?
The first thing that occurred to me  was to combine my electronic background with my sea lover’s side. It could be really fun to build a device with an embedded camera and wireless communication, as Lora or Sigfox for really long distance coverage. Then I will place this device in front of the sea, and with a bit of Image processing collect the data of the swell, wind, temperature and any weather information. Then thanks to Datadog, it could be easier to find the best time to pull out the surfboard from the garage and take an amazing ride!
