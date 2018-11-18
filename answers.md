1. Tag Assignment

![alt text](https://github.com/cconerby/hiring-engineers/blob/master/1_Assigning_Tags.JPG)

2. MongoDB Integration:

![alt text]https://github.com/cconerby/hiring-engineers/blob/master/2_MongoDB_Instrumented_2.JPG

![alt text](https://github.com/cconerby/hiring-engineers/blob/master/2_MongoDB_Instrumented.JPG)

3. Custom_Agent_Random_Code.py
```
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
  def check(self, instance):

        x = random.randint(1, 1000)

        self.gauge('random.number', x)
```
4. Custom Agent Metrics with 45 Second Interval:

![alt text](https://github.com/cconerby/hiring-engineers/blob/master/3_4_Custom_Agent_My_Metric_45_Seconds.JPG)

5. Bonus Question #1:

  You can change the check collection interval with the agent manager within Windows.(GUI).  Also potentially with API but I have yet to locate the example code for this on the Datadog API site.
  
6. Timeboard Python Code:

```
#!/opt/datadog-agent/embedded/bin/python

import datadog
from datadog import initialize, api

options = {
    'api_key': 'cd02ee5f618e30da34729601c6b4a57f',
    'app_key': 'fe990d6d6fc005c91a4e76a5504dc346175f699a'
}

initialize(**options)

title = "My Metric Timeboard"
description = "My Metric Timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:random.my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.extra_info.heap_usage_bytesps{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "Mongo_Heap_Usage_Anomaly"
},

{
 "definition": {
        "events": [],
        "requests": [
            {"q": "sum:random.my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric_1Hour_Rollup"

}

]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
 ```
 7. 5 Minute Timeboard Screenshots
 
 ![alt text](https://github.com/cconerby/hiring-engineers/blob/master/9_10_5Minute_Timeboard_1.JPG)
 
 ![alt text](https://github.com/cconerby/hiring-engineers/blob/master/9_10_5Minute_Timeboard_2.JPG)
 
 *Note graph is empty because of 5 minute window.  For full timeframe this graph shows ~40,000 for rollup value for past  60 minutes.  This is only taken every 60 minutes and therefore doesn't display on 5 minute window.
 ![alt text](https://github.com/cconerby/hiring-engineers/blob/master/9_10_5Minute_Timeboard_3.JPG)
 
 8. Bonus Question #2
 
 The Anomaly graph is showing the expected range of the Mongo Heap Usage Metric based on historical patterns.  This expected range range is based on our 'basic' algorithm choice.  The 'gray' area shows the expected range while metrics outside of the expected area are represented with 'red'
 
 9. Monitor Warning Email:
 
 ![alt text](https://github.com/cconerby/hiring-engineers/blob/master/11_Monitor_Email.JPG)
 
 10. Monitor Downtime Screenshots

![alt text](https://github.com/cconerby/hiring-engineers/blob/master/12_Monitor_Downtime_email_weeknights.JPG)

![alt text](https://github.com/cconerby/hiring-engineers/blob/master/12_Monitor_Downtime_email_weekends.JPG)


 
 11. APM Dashboard Link and screenshot:
 
Link:  https://app.datadoghq.com/dash/990988/my-metric-timeboard?live=true&page=0&is_auto=false&from_ts=1542570398925&to_ts=1542573998925&tile_size=s

[alt text](https://github.com/cconerby/hiring-engineers/blob/master/13_APM_Dashboard.JPG)

APP Code Instrumented:
```
#!/opt/datadog-agent/embedded/bin/python


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

12. Bonus Question #3:

A service is a set of process that do the same job.
Webapp and database are example services for a web application.

A resource is a particualar action for a service. 
For example a URL for a web application and a SQL query for a database service.

13. Final Question:

It would be great to use newly available smart beacons that can determine the number of people in a space/room to report this information for restaurants/bars.  Datadog could leverage this data and provide a dashboard.  This way customers can know if an establishment is too crowded or not crowded enough before making the trip to the restaurant/bar.


 
 

 

  
