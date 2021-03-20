
## ENV Details:
For this exercise I used a Vagrant Virtual Box with Ubuntu with the following packages/modules installed: 
- Python3
- Pip3
- Flask
- VirtualEnv
- Postgres

All API calls were made using Postman
## Collecting Metrics:
Here is the my datadog.yaml file for configuring my agent. I have setup a few tags as well as enabled its APM configuration,
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
Here is the corresponding screenshot from the Datadog UI showing the host with the tags listed in the prevoius code block. 
![My Host](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/host_map_with_tags.png)

Then I installed a Postgres database system onto the vagrant box, created a database called new_db and configured the following confiuration file and put it into the etc/datadog-agent/conf.d/postgres.d/ directory.
```
init_config:

instances:
  -host: localhost
  port: 5432
  username: datadog
  password: <REDACTED>
```
Also in the postgres configuration located in /etc/postgres/10/main/
````
relations:
  - large_test
````
This tell postgres to grab relational data from the large_test table.

Here is a screenshot of a dashboard pulling in live statistics from our Postgres database.
![Postgres Dashboard](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/dboardpostgres.png)
 
 
 
 The following is the python file named custom_random.py and placed in the /etc/datadog-agent/checks.d/ directory. It imports a simple random module and then ran that module before creating the my_metric gauge with that random value. 
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

Here's an example of a graph for this metric 

![Custom Metric Graph](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/my_metric.png)

There's also a custom_random configuration file with a small block of code:
  `Instances: [{min_collection_interval: 45}] ` in the /datadog-agent/conf.d/ directory.  The min_collection_interval parameter means that the agent's collector will queue this check every 45 seconds. You can also change this interval from the Datadog UI

![Changing Metric Interval](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/edit%20metric%20interval.png)

## Visualizing Data:
I've broken up the JSON body from my Dashboad API request into 5 parts. This first block is mainly configuration of the dashboard itself whereas the other 4 pieces are individual widgets or graphs for the dashboard. I've set `layout_type` to "ordered" so this dashboard will be a timeboard rather than a free-form screenboard.
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
  The second widget is taking the heap blocks read metric from our integrated postgres database and applying the anomalies function. This function is basically going to take my incoming stream of database data and tell me when there's an unusual amount of activity on the database specific to the blocks heap read metric. These values are calculated using the basic algorithim with a bounds of 2. The bounds meaning basically how wide a berth the anomaly algorithm gives before saying a specific point is an outlier.
   ```
      {
         "definition":{
            "requests":[
               {
                 "q": "anomalies(max:postgresql.heap_blocks_read{host:bens.datadog.application}, 'basic', 2)"
               }
            ],
            "title":"Postgres Rows Fetched Anomolies",
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
 The third widget represents a rollup function of the custom my_metric over the course of an hour. This basically amounts to an aggregation function that runs every 3600 seconds or 1 hour. We put that value into a bar chart.
 ```
      {
         "definition":{
            "requests":[
               {
                 "q": "max:my_metric{host:bens.datadog.application}.rollup(sum, 3600)",
                 "type": bars
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
      },
```
This last widget is just a query for the number of tables within the database using the metric `table.count`
```
      {
         "definition":{
            "requests":[
               {
                 "q": "max:postgresql.table.count{db:postgres}",
                 "aggregator": last
               }
            ],
            "title":"Database Table Count",
            "type":"query_value"
         }
      }
   ]
}
```
Once we execute our POST API call with this JSON we get the following dashboard on our Datadog UI
  
![My Api Dashboard](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/dashboard_from_api.png)

To change the timeframe of our dashboard we go to the top right and can either select from some of the dropdown options or just type `5 min` into it and we can set our dashboard timeframe to 5 minute

![Changing timeframe](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/change_timeframe.png)

So it looks like we've got an interesting point on one of our graphs, if we click into the graph and select `Send Snapshot` we can send this snapshot to a teammate with the @notation.
![Snapshot1](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/snapshot1.png)
![Snapshot2](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/snapshot2.png)

Our teammate will be sent a notification once we submit this.

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

Here is a dashboard that grabs a number of pieces of information including:
 - Postgres - Live Rows 
 - Postgres - Dead Rows
 - Postgres - Table Count
 - Postgres - Block Heaps Read/Hit Per Second
 - Postgres - Rows Inserted and Deleted
 - Infrastructure - Our Custom Metric and Rollup
 - Infrastructure - CPU Usage
 - APM - Number of Incomimg Flask API Calls
 - APM - Latency on Flask API Calls

Public APM and Infrastructure Dashboard:
![APM Infrastructure Dboard](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/apminfra.png)

You can also visit this public dashboard here:
- https://p.datadoghq.com/sb/ee2as39v7pgo65cy-028c1a051d6b16001f7818a721f61672

Going back to the following time will show you some incoming metrics:
`Mar 19, 9:30 pm – Mar 19, 11:15 pm`
 ##### ** the data represented in this dashboard was generated using the following code blocks:
 ### Curling Flask:
Flask statistics were generated by copy and pasting the following lines approximately 60 at a time after SSHing into the vagrant box.
 ````
curl 127.0.0.1:5002/
curl 127.0.0.1:5002/api/trace
curl 127.0.0.1:5002/api/apm
````

 ### Postgres:
 Postgres statistics were generated by a couple of different blocks. This first one creates a table large_test
````
create table large_test (num1 bigint, num2 double precision, num3 double precision);
````
To insert rows into the database, I ran variations of the following block changing that final value to different integers
````
insert into large_test (num1, num2, num3)
  select round(random()*10), random(), random()* 142
  from generate_series(1,<VALUE>), s(i);
````
Because of the nature of the random data deletes were made basically by guessing a digit for the num1 value. 
````
delete from large_test where num1=<DIGIT>
````
Select queries were operated the same way, by changing the DIGIT for the num1 value
````
select * from large_test where num1=<DIGIT>
````
Services are logical groupings that make up an application. Such as a group of URL endpoints that come together that make an API service, or a group of database queries that act as one's database service. 
Resources on the other hand are those individual elements that come together to make a service like an individual query or webservice call.

## Final Question:
NFL "Virtual Referee" - 
Every season NFL players, coaches, and fans find themselves yelling and screaming over the officiating of football games. And they're asking themselves the same questions: how do we hold these refs more accountable? And while that's an understable question it doesn't really strike at the heart of the problem. The real question they should be asking is how have we not, with all of the technology available, given referees more tools to make the best decisions possible? This is by no means a substitution for referees but I believe gives the crew a virtual member to help them determine a call. Now imagine for a moment, an NFL coach throws their challenge flag and tells the refs he wants to challenge the call. While the refs go to the sideline to determine the call, the virtual ref is executing it's multiple parts:

An AI trained watching footage of games visually determining if certain events have happened and then flagging when they do. This could apply to anything a referee looks for although I suppose for the most accurate version you would separate each specific thing the AI would be looking for and break them into modules. This information would be sent to a determination logic.

IOT devices embedded into a number of on field elements:
 - Helmets to determine illegal head to head hits
 - The ball itself to determine spot of the ball for first downs / touchdowns
 - Cleats to determine if a player steps out of bounds
 - Knee pads to determine if a runner is down

This IOT data would then also be sent to the determination logic.

Determination Logic:
Once receiving all the inputs from the AI and IOT devices, a program would determine what occured on the play in question and submit that and the proving statistics and metrics to what I'm dubbing the "Ref Board." 

The Ref Board is basically a Datadog dashboard that is sent the final determination from the logic step as well as the supporting evidence that proved to the determination algorithim what happened. 

Our refs have reached the sideline and look at their ref board, which helps them validate and make the correct call. The idea here isn't that the virtual ref overturns the human refs, but helps them see information they may have missed. 

A principle in designing really anything whether it's a large distributed system or even one's job tasks is finding ways to connect the chain through triggers and checks so having a platform like Datadog can really enable one to have real visibility into processes.
