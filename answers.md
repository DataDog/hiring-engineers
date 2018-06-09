# My answers 

## Setup the environment

&rarr; I used an Ubuntu 18.04lts desktop version  hosted on a virtual box virtual machine

## Collecting Metrics:

*  Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

&rarr; In order to add tags I added them in the /etc/datadog-agent/datadog.yaml as you can see below  
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot1.PNG)

*  Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

&rarr; I choiced to use PostgreSQL because it is the database i am the most familiar with.  

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

&rarr; Here is the code for my customagent.py  
```
    from checks import AgentCheck  
    import random  
    class HelloCheck(AgentCheck):  
    	def check(self, instance):  
    		self.gauge('my_metric',random.randint(0,1000))
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
* Bonus Question Can you change the collection interval without modifying the Python check file you created?

&rarr; In order to modify the collection interval without modifying the Python check file you have to change the yaml file of the check locate in : /etc/datadog-agent/conf.d/your_check/your_check.yaml  

&rarr; You can see below the Python check file, the yaml file and the check graph which show a new data each 45 sec.  
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot2.PNG)


## Visualizing Data:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

&rarr; You will find below all the three graphs based on my_metric.  
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot3.PNG)
&rarr; Concerning the script used I took screenshots of the differents json configuration of my graphs :  
	- my_metric 
	![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/my_metric_config.png)
	- anomaly of my_metric 
	![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/anomaly_config.PNG)
	- sum_my_metric 
	![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/my_metric_sum_config.PNG)

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

&rarr; On the picture, you will see the timeboard showing the value of my_metric for the last 5 minutes and my snapshot.  

![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot4.PNG)

* **Bonus Question**: What is the Anomaly graph displaying?

&rarr; The anomaly graph is displaying the trend of the metric, hightlighning when the value doesn't match the trend  

## Monitoring Data

&rarr; On the screenshot, you will find the configuration of the monitor :  
	- the alert threshold,  
	- the warning threshold,  
	- the notification in case there is some missing data for more than 10 minutes  

![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot5.PNG)

&rarr; Below you will find my monitor's message:  
```
	{{#is_alert}} This is an alert made by a {{value}} value from {{host.ip}} {{/is_alert}} 
	{{#is_no_data}}There is no data since 10 min{{/is_no_data}} 
	{{#is_warning}}This is a warning{{/is_warning}} 
	@alexandrecorre.1995@gmail.com
```
&rarr; This is the screenshot of the alerting mail that I received.  
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot6.PNG)

* **Bonus Question**:

&rarr; Below is the mail that I received for the week downtime, and the configuration of the downtime.  
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot7.PNG) 
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot7_1.PNG)

&rarr; The is the mail that I received for the weekend downtime, and the configuration of the downtime.  
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot8.PNG)  
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot8_1.PNG) 

## Collecting APM Data:

&rarr; I used the default app for this part as I am not used to the Flask package  

my_app.py:  
```
from flask import Flask
import logging
import sys

#Have flask use stdout as the logger
main_logger = logging.getLogger()  
main_logger.setLevel(logging.DEBUG)  
c = logging.StreamHandler(sys.stdout)  
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
c.setFormatter(formatter)  
main_logger.addHandler(c)  

app = Flask(__name__)  

@app.route('/')  
def api_entry():  
&nbsp;    return 'Entrypoint to the Application'  

@app.route('/api/apm')  
def apm_endpoint():  
	return 'Getting APM Started'  

@app.route('/api/trace')  
def trace_endpoint():  
	return 'Posting Traces'  

if __name__ == '__main__':  
	app.run(host='0.0.0.0', port='5050')  
```


**Bonus Question**: What is the difference between a Service and a Resource?

&rarr; A service is defined by a verb which describes the function it implements, for exemple : validate a token.  
However, a resource refer to some data so it is defined by a noun, for exemple : log files.  

The link to my dashboard is : https://p.datadoghq.com/sb/49ba87d1e-6327d00df9ae6d489a2fbbea92483705 .
However, as my virtual machine isn't working all the time, I think this screenshot will show you the data when the VM was up.
![alt text](https://github.com/Alexandrecorre/hiring-engineers/blob/solutions-engineer/screenshot9.png) 

## Final Question:

* Is there anything creative you would use Datadog for?

&rarr; When I see all the differents features of the Datadog agent, I think it can be used nearly everywhere to improve some old architecture system but that's not really creative.  
A more creative way to use Datadog would be to gather data on online Games and help improve there resiliency.  
Even better, using some iot technologies it could be possible to collect data from camera in museum to have to watchtime of each piece of art to know for example which one is the most watch and then help positionning the masterpiece all over the museum.

### I wanted to thanks you for your time reading me, I really enjoyed this exercice and especialy working with the Datadog technologies.
### Have a nice day.
### Thanks