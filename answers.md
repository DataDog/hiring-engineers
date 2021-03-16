Exercise completed using a Vagrant Ubuntu Box

## Collecting Metrics:
![My Host](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/host_map_with_tags.png)
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
![Custom Metric Graph](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/my_metric.png) \
This is the custom metric I made that generates a random number between 1 and 1000

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
I had trouble locating where you put the collection interval line (which file that is). From the exercise I gathered that you would just put the line into the custom_metric.py file however I could not get this to work. The docs also were phrased in a way that led me to believe you could configure the agent itself to globably change the interval time but I could not figure this out either. I did however find the change interval option in the DatadogHQ UI

![Changing Metric Interval](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/edit%20metric%20interval.png)

## Visualizing Data:
![My Api Dashboard](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/dashboard_created_with_api.png?raw=true)
 The above dashboard was made with the following JSON body plugged into the Postman Datadog API collection
```
{
   "description":"dashboard made by an API testing Ben",
   "is_read_only":false,
   "layout_type":"ordered",
   "notify_list":[
      
   ],
   "title":"Bens API Dashboard",
   "widgets":[
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
You'll notice that for the anomalies graph I didn't use a Postgresql metric. I made this decision because the only metrics I was consistently seeing were related to the number of tables on the database. I could not get row operation (fetch and return) statistics to populate in the big Postgres Overview Dashboard. So I used disk.io.util instead so grabbing the anomalies was an interesting graph to look at.

Changing the timeframe of a dashboard: \
![Changing timeframe](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/change_timeframe.png?raw=true) \
Grabbing a snapshot of that timeframe and @myself:
![Snapshot](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/snapshot.png?raw=true)

Is this question asking contexually within the metric itself or a broader context as to what the anomolies function actually does? \
Contextually - Seeing spikes of cpu usage at certain times etc \
Broader Context - Able to determine when incoming datapoints are within a certain expectation or not. \

## Monitoring Data:
Setting up a monitor with a warning and alert at the levels of 500 and 800 respecitely. The notifcation text email has options for whether it is a warning or alert:
![Monitor with Options](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/monitor_w_options.png) \
Monitor Notification: \
![Monitor Email Notification](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/alert_email.png) \
Weekday Downtime: \
![Weekday Downtime](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/weekday_downtime.png) \
Monitor Weekend Downtime: \
![Weekend Downtime](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/weekend_downtime.png)

## Collecting APM Data:
![Infrastructure and APM Dashboard](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/dashboard%20with%20flask%20apm%20included.png)
For the APM section I used the Datadog provded Flask app with a change to the port number
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
    app.run(host='0.0.0.0', port='5002')
```

You can visit my API dashboard with Infrastructure and APM here: https://p.datadoghq.com/sb/ee2as39v7pgo65cy-72e87b22b2b989a105269df944cd03cd
I tried to pause it so the APM stats would remain. 

I've always viewed services as the building blocks for the archtiechting of computing infrastructure. That could mean the actual compute instances of a cloud deployment in the terms of a microservices something like a Kubernetes deployment. Whereas resources are the individual actions of the service such as a GET or POST request.


## Final Question:
quantum circuit fidelity - I'm still questioning the actual practicallity of this, but building fault tolerant and effective quantum gates / circuits is a huge problem currently and having a tool that could  monitor when a quantum circuit errors out is crucial to development of that technology. But again, it's more of a pipedream than practical reality that current classically computed SaaS programs could integrate with quantum hardware.

In the high performance computing space, datadog could be vital to being able to identify when a compute resource is overworking based on it's workload so the architect would know they need to instantiate a larger compute instance for the job at hand. 

There's an area of strategy called dynamic work design, one of the key principles of this design is to connect the human chain through a system of checks and triggers. Datadog to me is an computational version of this principle. And in that sense I think datadog could be used in all sorts of large scale systems with lots of components working together whether that's running diagnostics on jet engines to tell when it may need a repair or being able to detect power surges and dips in an electrical grid. 



