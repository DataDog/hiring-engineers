Your answers to the questions go here.
The excercises were very challanging but a really good learning experience. I did have issues with the last one as I could not get PIP or Flask woring correctly in my Vagrant environment. I believe the issue may have something to do with the Ubuntu version that vagrant uses (12.04) but not 100% sure. 

The URL for my dashboard that has the exmaples in it can be found here: 
https://app.datadoghq.com/dash/840545/my-cool-metrics2?live=true&page=0&is_auto=false&from_ts=1529700828621&to_ts=1529704428621&tile_size=m

While I thought the excercises are a good idea and will show how resourceful a candidate is, I think you could add some stuff that would make it better for SE's. I would ask some questions that also have a sales context. Maybe have them create different dashboards for different audiences (app owner, tech lead, IT executive). I see the power of Datadog in it's flexibility and I can see how it would be appealing to developers but how would you pitch it to IT operators or managers, how would it replace some of the existing products out there? Why is it better?

Here are the answers to the invididual tracks:

**Collecting Metrics:**

Here is the YAML for the MySQL DB I monitored:

    init_config:  
 
      instances: 
      - server: localhost 
      user: datadog 
      pass: datadog  
      tags: 
          - Prod_DB  
          - MySQL_Prod  
      options: 
          replication: 0 
          galera_cluster: 1 


Here is a screenshot if a monitored host with custom tags:
![Tags Image](https://github.com/pazzman99/hiring-engineers/blob/master/Tags.JPG)


This is the code for the "Random Number" metric:

    import random
    from checks import AgentCheck
    class MyRandNum(AgentCheck):
        def check(self, instance): 	
            rand_num = random.randint(1,1000)	
            self.gauge('My_Rand_Num', rand_num)
  
 Here is a link to the file
 [My_Metric.py](https://github.com/pazzman99/hiring-engineers/blob/master/my_metric.py)
 
 Here is the Yaml file code:
        
    init_config:

    instances:  
    [{}]

Here is the link the the Yaml file
[My_Metric.yaml](https://github.com/pazzman99/hiring-engineers/blob/master/my_metric.yaml)

Bonus Question: Can you change the collection interval without modifying the Python check file you created?
- You can do this by going to metrics/summary and clicking on the metadata edit and change the interval

**Visualizing Data:**


Here is the code for the script to create the time board via the API:

    POST 'https://api.datadoghq.com/api/v1/dash'
    from datadog import initialize, api

    options = {
        'api_key': '6dde5873456f6a9b66b98930161cdbd8',
        'app_key': 'b16780246a98509d1ea03c064b1097b5ba5a4cae'
    }

    initialize(**options)

    title = "My_Metric_TimeBoard"
    description = "Really cool Timeboard for Metrics"
    graphs = [{
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:mysql.performance.cpu_time{*}"}
            ],
            "viz": "timeseries"
         },
        "title": "MySQL CPU Performance"
    }
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:My_Rand_Num{*}"}
            ],
            "viz": "timeseries"
        },
        "title": "MyRandom Number"
    }]

    read_only = True
    api.Timeboard.create(title=title,
                         description=description,
                         graphs=graphs,
                         template_variables=template_variables,
                         read_only=read_only)



Here is the link to the code I used to create the timeboard through the API
[TestAPI.py](https://github.com/pazzman99/hiring-engineers/blob/master/testapi.py)

Here is a link to the snapshot of the timeboard:
https://github.com/pazzman99/hiring-engineers/blob/master/Timeboard_API.JPG

Here is the code for the script:




Here is a screenshot of MySQL metric with anomoly detection turned on:
https://github.com/pazzman99/hiring-engineers/blob/master/Metric_with_Anomoly_Detection.JPG


Here is a screenshot of the email that was sent using the @ notation:
https://github.com/pazzman99/hiring-engineers/blob/master/Email_of_Snapshot.JPG


Here is a screenshot of the dashboard with the custom and MySQL metrics over time:
https://github.com/pazzman99/hiring-engineers/blob/master/Dashboard_with_Metric.JPG



Monitoring Data:

Here is a screen shot of the monitor config:
https://github.com/pazzman99/hiring-engineers/blob/master/Monitor_Config.JPG


Here is a screenshot of an email the monitor sent:
https://github.com/pazzman99/hiring-engineers/blob/master/Monitor_Email.JPG
 


Collecting APM Data:

Here is the code for the flask app with the instrumentation configured:

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

traced_app = TraceMiddleware(app, tracer, service="MyWebbApp_V2", distributed_tracing=False)


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
    app.run(host='127.0.0.1', port='4999')
    
    
Here is a link to the file:
https://github.com/pazzman99/hiring-engineers/blob/master/testweb.py


Here is a screenshots of a dashboard with APM and host metrics:
https://github.com/pazzman99/hiring-engineers/blob/master/APM_3.JPG


For the final question, since you can grab metrics from anywhere, it would be really cool to add business metrcis to the technology ones. For example, maybe see $$ of sales aligned with user hits or traffic volumes over time. Maybe even ITOM stuff like ticket or incident volumes graphed with system performance over time. There are a lot of possibilities. 

In closing I want to thank you for your consideration and really look forward to speaking with you.
