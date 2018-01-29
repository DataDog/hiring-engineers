## Prerequisites - Setup the environment

**Using Vagrant on Windows 10.**

Setting up Vagrant
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(1).png?raw=true">

Datadog agent installed
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(2).png?raw=true">

Trace in the Datadog interface
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(3).png?raw=true">

## Collecting Metrics:

Changing tags
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(4).png?raw=true">

Setting up the MySQL integration and retrieving the metrics
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(5).png?raw=true">

Random script init
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(6).png?raw=true">

My random check script:
```python
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', random.randint(0, 1000))
```

**Bonus Question Can you change the collection interval without modifying the Python check file you created?**

Yes, by changing a specific setting in the config file:
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(7).png?raw=true">

## Visualizing Data:

Setting up the MySQL anomalies timeseries widget
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(8).png?raw=true">

Setting up the custom metric timeseries widget
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(10).png?raw=true">

Custom metric + MySQL anomalies dashboard
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(9).png?raw=true">

Changing the rollup value in the custom metric JSON 
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(11).png?raw=true">

New dashboard after change
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(12).png?raw=true">

**Bonus Question: What is the Anomaly graph displaying?**

The graph is showing the given metric, and highlighting the outstanding values

## Monitoring Data

Setting up the monitor and its message
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(13).png?raw=true">

Warning email
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(14).png?raw=true">

Alert email
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(16).png?raw=true">

Schedule downtimes daily
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(15).png?raw=true">

Schedule weekend downtime
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(17).png?raw=true">

Downtimes setup notification emails
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(18).png?raw=true">


## Collecting APM Data:

Final dashboard with infrastructure metrics
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(19).png?raw=true">

Flask script setup
<img src="https://github.com/timothe/hiring-engineers/blob/solutions-engineer/Screenshot%20(20).png?raw=true">

My Flask app:

```python
from flask import Flask
import logging
import sys
import blinker as _
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="training-flask-app", distributed_tracing=False)

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)


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

+ [Dashboard link](https://app.datadoghq.com/dash/517523/support-overview-training)


**Bonus Question: What is the difference between a Service and a Resource?**

A "Service" is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two services: a single webapp service and a single database service, while a more complex environment may break it out into 6 services: 3 separate webapp, admin, and query services, along with a master-db, a replica-db, and a yelp-api external service.
A "Resource" is a particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like ```web.user.home``` (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like ```select * from users where id = ?```.


## Final Question:

**Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?**

Coming from UGC, I can think of a dashboard getting information from a social network API, retrieving the number of posts with a certain hashtag, but also the number of products from a feed, and the product coverage for a given UGC set.
Then, cross-reference the product pages views with UGC to get the most popular products without UGC coverage, so that the marketing team can ask a content creator for a paid contribution.
