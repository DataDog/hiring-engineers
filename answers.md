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
![Custom Metric Graph](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/my_metric.png)
```
##This is the custom metric I made that generates a random number between 1 and 1000

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
![Changing timeframe](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/change_timeframe.png?raw=true)
![Snapshot](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/snapshot.png?raw=true)

Is this question asking contexually within the metric itself or a broader context as to what the anomolies function actually does? \
Contextually - Seeing spikes of cpu usage at certain times etc \
Broader Context - Able to determine when incoming datapoints are within a certain expectation or not. \

## Monitoring Data:
![Monitor with Options](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/monitor_with_options.png)
![Monitor Email Notification](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/Monitor%20Notification.png)
![Weekday Downtime](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/weekday_downtime.png)
![Weekend Downtime](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/weekend_downtime.png)

## Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution: \
![Infrastructure and APM Dashboard](https://github.com/bbehrman10/hiring-engineers/blob/solutions-engineer/supporting_images/dashboard%20with%20flask%20apm%20included.png)

Services are the blocks that come together in an architecture at broader scale whereas resources are more the individual pieces of those larger blocks. \
YUCK WORK ON THAT \

Screenshot of Dashboard with Infrastructure and APM Metric \
Please include your fully instrumented app in your submission, as well. \

Final Question: \
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! \
Is there anything creative you would use Datadog for? \
quantum circuit fidelity /
traffic light / pedestrian traffic /
any sort of large scale system that has multiple pieces working together would benefit absolutely. I think about monitoring flight data from a jet engines to tell when an airline may need to do service on a plane. or even electrical data coming from power grids to help protect against surges and dips. /


