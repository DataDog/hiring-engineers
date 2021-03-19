Exercise completed using a Vagrant Ubuntu Box 
All API calls were made using Postman

## Collecting Metrics:
Here is the my datadog.yaml file for configuring my agent. I have setup a few tags as well as enabled its APM configuration (more on that later).
```
api_key: <redacted>
site: datadoghq.com

hostname: bens.datadog.application

tags:
  greeting:hello_datadog_team
  message:you_have_built_an_awesome_platform
  conclusion:thanks_for_reviewing_my_work
  
apm_config:
  enabled: true
```
Here is the corresponding screenshot from the Datadog UI showing my host with the tags listed in the prevoius code block. 
![My Host](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/host_map_with_tags.png)

I then installed a Postgres database system onto my vagrant box, created a database called new_db and configured the following confiuration file and put it into the etc/datadog-agent/conf.d/postgres.d/ directory. At this point I also attempted to pull through a custom query however while the Agent status check was not throwing an error  I was unable to see this metric coming through. 
```
init_config:

instances:
  -host: localhost
  port: 5432
  username: datadog
  password: <REDACTED>
  
  custom_queries:
    metric_prefix: postgresql
    query: "SELECT relname, seq_scan from pg_stat_user_tables"
    columns:
      name: relname
      type: tag
      name: seq_scan
      type: tag
      name: sequence_scan_by_table
      type: gauge
```
Here is a quick screenshot of my out of the box PostgreSql dashboard pulling in live statistics from the postgres database. I ran a number of random write and read operations to get some metrics pulled through.

![Postgres Dashboard](http://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/postgres_dashboard.png)
 
 The following is the python file I named custom_random.py and placed in the /etc/datadog-agent/checks.d/ directory. It imports a simple random module and then ran that module before creating the my_metric gauge with that random value. 
 ```
import random
try:
    from datadog_checks.base import AgentCheck
   except ImportError:
    from checks import AgentCheck
  __version__ = "1.0.0"
  
class RandomCheck(AgentCheck):
  def check(self, instance):
    random_number = random.randint(1,1000)
    self.gauge('my_metric', random_number, tags=['type:custom'] + self.instance.get('tags', []))
``` 

Here is the corresponding graph for my_metric mapped over my tagged host
![Custom Metric Graph](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/my_metric.png)

There's also a custom_random configuration file with a small block of code:
  `Instances: [{min_collection_interval: 45}] ` in the /datadog-agent/conf.d/ directory.  The min_collection_interval parameter means that the agent's collector will queue this check every 45 seconds. You can also change this interval from the Datadog UI
![Changing Metric Interval](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/edit%20metric%20interval.png)

## Visualizing Data:
I've broken up the JSON body from my Dashboad API request into 4 parts. This first block is mainly configuration of the dashboard itself whereas the other 3 pieces are individual widgets or graphs for the dashboard. I've set `layout_type` to "ordered" so this dashboard will be a timeboard rather than a free-form screenboard.
```
{
   "description":"dashboard made by an API",
   "is_read_only":false,
   "layout_type":"ordered",
   "notify_list":[
      
   ],
   "title":"Bens API Dashboard",
   "widgets":[
```
This first widget definition is graphing the custom my_metric over the scope of my tagged host. We can see this in the "q" line - representing the widget's query. We take the max value from my_metric and only pull it only from the host inside of the curly braces. We then graph these values on a timeseries - a specific Datadog widget. 
```
      {
         "definition":{
            "requests":[
               {
                 "q": "max:my_metric{host:bens.datadog.application}"
               }
            ],
            "title":"Custom Metric Over Host",
            "type":"timeseries",
            "yaxis":{
               "include_zero":true,
               "max":"auto",
               "min":"auto",
               "scale":"linear"
            }
         }
      },
  ```
  The second widget is taking a metric from our integrated postgres database and applying the anomalies function. This function is basically going to take my incoming stream of data from my database and tell me when if those incoming datapoints fall within an expected range of values. These values are calculated using the basic algorithim with a bounds of 2. The bounds meaning basically how wide a berth the anomaly algorithm gives before saying a specific point is an outlier.
   ```
      {
         "definition":{
            "requests":[
               {
                 "q": "anomalies(max:system.io.util{host:bens.datadog.application}, 'basic', 2)"
               }
            ],
            "title":"Database System Anomolies",
            "type":"timeseries",
            "yaxis":{
               "include_zero":true,
               "max":"auto",
               "min":"auto",
               "scale":"linear"
            }
         }
      },
 ```
 The third widget represents a rollup function of the custom my_metric over the course of an hour. This basically amounts to an aggregation function that runs every 1800 / 3600 seconds. 
 ```
      {
         "definition":{
            "requests":[
               {
                 "q": "max:my_metric{host:bens.datadog.application}.rollup(sum, 1800)"
               }
            ],
            "title":"My Metric Rollups",
            "type":"timeseries",
            "yaxis":{
               "include_zero":true,
               "max":"auto",
               "min":"auto",
               "scale":"linear"
            }
         }
      }
   ]
}
```
Once we execute our POST API call with this JSON we get the following dashboard on our Datadog UI
  
![My Api Dashboard](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/dashboard_created_with_api.png?raw=true)

To change the timeframe of our dashboard we go to the top right and can either select from some of the dropdown options or just type `5 min` into it and we can set our dashboard timeframe to 5 minute

![Changing timeframe](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/change_timeframe.png?raw=true)
So it looks like we've got an interesting point on one of our graphs, if we click into the graph and select `Send Snapshot` we can send this snapshot to a teammate with the @notation. Below is a screenshot of the email notification for the snapshot. 
![Snapshot](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/snapshot.png?raw=true)

## Monitoring Data:
You can make monitors from both the Datadog UI as well as the API. Below the JSON body, broken into 3 parts, used to create my monitor for the exercise.
This first block contains the title, which contains the host that the monitor is watching as well as the type of monitor this is a metric alert, as opposed to any of the other datadog objects.
```
{
	"name": "Host {{host.name}} is running high",
	"type": "metric alert",
```
Now comes the main elements of our monitor, the query itself -  what the monitor is actually going to be watching and the message - what the monitor is going to say when later defined thresholds are hit. The query is looking to see if the custom metric created earlier is above 800. The next element is the message the monitor is going to send when we've triggered it. We can define different messages depending on what our monitor wants to tell us using curly brack notation `{{#is_threshold}}`. I've set up a message for when the alert activates as well as a message for when a warning is activated and one for if there's no data coming through from the host. We will define both of those thresholds in the 3rd block of code. Lastly in the message I've included @notation and the email address of the teammated (me) I want to notify when this monitor goes off.
```
	"query": "max(last_5m):max:my_metric{host:bens.datadog.application} > 800",
	"message": "{{#is_alert}}\nALERT -- My_metric on host {{host.name}} is running above the approved alert threshold of 800. Latest metric is {{value}}\n{{/is_alert}} \n\n{{#is_warning}}\nWARNING -- My_metric on host {{host.name}} is running above the approved warning threshold of 500\n{{/is_warning}} \n\n {{#is_no_data}}\nUH-OH! There's no data from {{host.name}} {{/is_no_data}}  @bbehrman10@gmail.com",
	"tags": [],
```
This last block is a few configuration options for the monitor, a few key ones to point out are `require_full_window: true` which says to wait for a full window of data before triggering the monitor, `no_data_timeframe: 10` which tells the monitor to alert us after 10 minutes of no data coming through the metric, and finally the `"thresholds": {"critical": 800, "warning": 500}` block defines our two threshold points 800 for a critical alert and a 500 warning alert. 
```
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": true,
		"notify_no_data": true,
		"renotify_interval": "0",
		"escalation_message": "",
		"no_data_timeframe": 10,
		"include_tags": true,
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}
```
You can also create this monitor from the Datadog UI:
Defining the metrics and thresholds
![Monitor Threshold UI](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/monitor_ui1.png)

Message and Configuration
![Monitor Message UI](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/monitor_ui2.png)

When our monitor activates it sends us an email
![Monitor Email Notification](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/alert_email.png)
 
Now let's quickly setup some downtime so we don't get notified by our monitors when we are off the clock.
 
Scheduling downtime for the week after each day and before the next one starts
![Weekday Downtime](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/ScheduleDtimeWeek.png)
 
Scheduling downtime for the weekend
![Weekend Downtime](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/ScheduleDtimeWeekend.png)

Once we schedule we get emailed notifications for our downtime
![Week Notification](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/DtimeNotifWeek.png)
![Weekend Notification](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/DtimeNotifWeekend.png) 

## Collecting APM Data:
![Infrastructure and APM Dashboard](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/dashboard%20with%20flask%20apm%20included.png)
For the APM section I used the Datadog provided Flask app with a change to the port number as well as added a span tag to each of the endpoints.  
```
from flask import Flask
import logging
import sys
from ddtrace import tracer

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
	current_span = tracer.current_space()
	if current_span():
		current_span.set_tag('from_entry_route', 'true')
	    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
	current_span = tracer.current_space()
	if current_space():
		current_span.set_tag('from_apm_route', 'true')
	    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
	current_span = tracer.current_space()
	if current_space():
		current_span.set_tag('from_trace_route', 'true')
	    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')
```
To get this application running and connected with our Datadog instance we have to do a few things. First, back to the datadog.yaml file mentioned earlier and make sure that we write in `apm_config: enabled: true` and restart our agent. This tells datadog to pull in APM metrics. Second, rather than run our flask app normally like `python3 <app_name>.py` we prepend a couple datadog declarations onto that command so it looks like `DD_SERVICE="<SERVICE>" DD_ENV="<ENV>" DD_LOGS_INJECTION=true ddtrace-run python3 <app_name>`

This instruments our application to send statistics to our datadog agent.
Now we can go back into the datadog UI and check out our Flask service.
![APM Service](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/flaskserviceapm.png)
![APM Details](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/flaskdetails.png) 
And we can even click into specific API calls and trace them
![APM Trace](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/flasktrace.png)

The following is a link to a public dashboard with metrics from the custom host, the flask applicaiton, and the Postgres database.
https://p.datadoghq.com/sb/ee2as39v7pgo65cy-72e87b22b2b989a105269df944cd03cd
For some interesting graphs, type this query into the timebar `query goes here`

Services are logical groupings that make up an application. Such as a group of URL endpoints that come together that make an API service, or a group of database queries that act as one's database service. 
Resources on the other hand are those individual elements that come together to make a service like an individual query or webservice call.

## Final Question:
quantum circuit fidelity - I'm still questioning the actual practicallity of this, but building fault tolerant and effective quantum gates / circuits is a huge problem currently and having a tool that could  monitor when a quantum circuit errors out is crucial to development of that technology. But again, it's more of a pipedream than practical reality that current classically computed SaaS programs could integrate with quantum hardware.

In the high performance computing space, datadog could be vital to being able to identify for example when a compute resource is working inefficiently so the architect would know they need to instantiate a larger compute instance for the job at hand. 

There's an area of strategy called dynamic work design, one of the key principles of this design is to connect the human chain through a system of checks and triggers. Datadog to me is an computational versiqon of this principle. And in that sense I think datadog could be used in all sorts of large scale systems with lots of components working together whether that's running diagnostics on jet engines to tell when it may need a repair or being able to detect power surges and dips in an electrical grid. 

## Feedback
I had a lot of fun doing this exercise. And I think it falls in that perfect sweet spot in terms of getting familiar with your platform. In my experience I notice that too often the instructions for technical exercises are either so broad it's hard to pick your spot and go or far too regimented which can put one into "task completion mode" rather than "learning mode." I felt like not only was I putting puzzle pieces together but also I was learning how each of the puzzle pieces work together. Thank you for the opportunity.  -Ben Behrman


