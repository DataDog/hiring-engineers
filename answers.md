## Prerequisites - Setup the environment

NOTE: All answers are fully supported inline with images and code. If you need to refer to my dashboard, you can find it here: [Erich Jaeckel's Dashboard](https://app.datadoghq.com/dashboard/kbk-zmi-nr9/timeboard-for-the-solution-engineer-exercise?from_ts=1590126493906&live=true&to_ts=1590731293906) 

For the prerequisites, I decided to utilize a mix of OS/Hosts to install the Datadog agent and integrations on:
* Ubuntu Linux VM via Vagrant
* Local (on-prem) Windows 10 machine
* AWS EC2 Windows Server 2019 running a MongoDB instance

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![image](https://user-images.githubusercontent.com/10134849/83217997-0529f680-a13b-11ea-99bb-2cab4deebbee.png)

**Supporting Work:**

AWS EC2 Windows Instance:

![image](https://user-images.githubusercontent.com/10134849/83218167-7c5f8a80-a13b-11ea-899c-5e2d035203ad.png)

Vagrant Ubuntu Instance:

![image](https://user-images.githubusercontent.com/10134849/83219051-55a25380-a13d-11ea-8990-457899fcae1b.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database. 

_For this exercise I installed MongoDB on the AWS EC2 Windows instance:_

![image](https://user-images.githubusercontent.com/10134849/83219183-b16cdc80-a13d-11ea-9e3f-27e084787c9f.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
![image](https://user-images.githubusercontent.com/10134849/83218571-2c34f800-a13c-11ea-884a-efc568986adc.png)
* Change your check's collection interval so that it only submits the metric once every 45 seconds.

This is done through updating the metrics_example.yaml file:

![image](https://user-images.githubusercontent.com/10134849/83219726-1543d500-a13f-11ea-8dfd-434cdae0c322.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

_(See above for my updates to the metrics_example.yaml file and not the Python file.) It also appears that you may be able to change it in the UI as indicated here:_

![image](https://user-images.githubusercontent.com/10134849/83219826-5e942480-a13f-11ea-9f8e-d1d7f1e1c97f.png)

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

![image](https://user-images.githubusercontent.com/10134849/83220561-5806ac80-a141-11ea-8165-68fe16b54180.png)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

**Timeboard Script:**

```python
from datadog import initialize, api

options = {
    'api_key': 'cb21aceba5e3abc987afc33e8c3205a0',
    'app_key': '80a31b1e4994584160fdfaf5ee46bf9a41aa9853'
}

initialize(**options)

title = 'Timeboard for the Solution Engineer Exercise'
widgets = [{
	'definition':{
		'type':'timeseries',
		'requests':[{
			'q':'avg:my_metric{host:vagrant}',
			'display_type':'bars',
			'style': {'palette': 'purple'}				
		}],
		'title':'My Metric Chart'
	}},	
	{
	'definition':{
		'type':'timeseries',
		'requests':[{
			'q':"anomalies(avg:mongodb.dbs{host:EC2AMAZ-HEJUFBT},'basic', 2)",
			'display_type':'line'			
		 }],
		'title':'AVG # of MongoDB dbs over host:Amazon EC2-Windows'
	}},
	{
	'definition':{
		'type':'query_value',
		'requests':[{
			'q':'avg:my_metric{*}.rollup(sum, 3600)',
			'aggregator':'avg'
		}],
		'title':'Avg of My Metric over the Last Hour',
		'time':{},
		'autoscale':True,
		'precision':2	
	}	
}]
layout_type = 'ordered'
description = 'This Timeboard is an API sourced Timeboard for the Solution Engineering exercise'
is_read_only = False
notify_list = ['erich.jaeckel@gmail.com']
template_variables = []



api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)


```

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

![image](https://user-images.githubusercontent.com/10134849/83220865-23dfbb80-a142-11ea-9ae5-43c33b12f22f.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.

![image](https://user-images.githubusercontent.com/10134849/83220951-67d2c080-a142-11ea-817e-48f54f1a0b05.png)

* **Bonus Question**: What is the Anomaly graph displaying?

This is showing that there has been a disruption to the baseline (# of avg databases in MongoDB) and corresponding chart spike (as indicated in red). The trailing gray field now becomes the new "bounds" upon which future spikes and dips are compared against.

![image](https://user-images.githubusercontent.com/10134849/83220972-8042db00-a142-11ea-89e6-e2443492a70b.png)

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

![image](https://user-images.githubusercontent.com/10134849/83221565-280cd880-a144-11ea-88f8-0aa0830d7dc8.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![image](https://user-images.githubusercontent.com/10134849/83221667-6904ed00-a144-11ea-8e2a-8c7673c3ef6c.png)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![image](https://user-images.githubusercontent.com/10134849/83221723-8fc32380-a144-11ea-85cc-1dea6001277d.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,

![image](https://user-images.githubusercontent.com/10134849/83221831-ea5c7f80-a144-11ea-8b43-204989e59c7a.png)

  * And one that silences it all day on Sat-Sun.
  
![image](https://user-images.githubusercontent.com/10134849/83221796-cb5ded80-a144-11ea-8466-190e4d016b1e.png)
  
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
  ![image](https://user-images.githubusercontent.com/10134849/83222055-68208b00-a145-11ea-8d2c-ae4b62ea5c28.png)

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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
    app.run(host='0.0.0.0', port='5050')
```

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

_Services are what make up modern microservice architectures - services consist of groupings of things like endpoints, database queries, and jobs to help one build an application._

_Resources on the other hand represent a particular domain of an application such as a particular action for a service (like an individual endpoint or specific db query)._

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

![image](https://user-images.githubusercontent.com/10134849/83226272-986d2700-a14f-11ea-9fe4-420d1d754302.png)

Please include your fully instrumented app in your submission, as well.

```ruby
require 'sinatra'
require 'ddtrace'
require 'ddtrace/contrib/sinatra/tracer'

Datadog.configure { |c| c.analytics_enabled = true }

Datadog.tracer.trace('web.request', service: 'myapp', resource:'GET /') do |span|
	get '/' do

		'Hello world!'
	end
end

Datadog.tracer.trace('web.request', service: 'myapp',  resource:'GET /blog') do |span|
	get '/blog' do
		'Retrieving a List of Blog article via API...'
	
		# Adding some APM tags
	    	span.set_tag('http.method', request.request_method)
    		span.set_tag('blogs.count', 44) #hardcoding for example's sake			
	
	end  
end

Datadog.tracer.trace('web.request', service: 'myapp',  resource:'GET /page1') do |span|
	get '/page1' do
		'Do Page2 things'
	end  
end
```

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Great question. I'd love to build out a pretty high-tech "ranch" where I live. Such as setting up multiple IoT devices that monitor things like weather, solar panel output (and battery charge), active electrical livestock fencing (to ensure the fencing is "live"), moisture monitors (to make sure the water bowls and troughs are filled) etc. In addition, my house has a number of IoT devices inside that monitor open (and unlocked doors), lights being on or off, alarm systems etc. 

I'd love to connect these IoT devices to AWS IoT and set up a Datadog integration that tracks the status and unique metrics of those systems, having it all in one place.

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)
