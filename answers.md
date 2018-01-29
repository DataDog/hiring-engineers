## Prerequisites - Setup the environment

Using Vagrant on Windows 10.

*Screenshots*

## Collecting Metrics:

*Screenshots*

## Visualizing Data:

*Screenshots*

**Bonus Question*: What is the Anomaly graph displaying?**
The graph is showing the given metric, and highlighting the outstanding values

## Monitoring Data

*Screenshots*

## Collecting APM Data:

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

**Bonus Question: What is the difference between a Service and a Resource?**
A "Service" is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two services: a single webapp service and a single database service, while a more complex environment may break it out into 6 services: 3 separate webapp, admin, and query services, along with a master-db, a replica-db, and a yelp-api external service.
A "Resource" is a particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like ```web.user.home``` (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like ```select * from users where id = ?```.

[Dashboard link](https://app.datadoghq.com/dash/517523/support-overview-training)

*Screenshots*

## Final Question:

**Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?**
Coming from UGC, I can think of a dashboard getting information from a social network API, retrieving the number of posts with a certain hashtag, but also the number of products from a feed, and the product coverage for a given UGC set.
Then, cross-reference the product pages views with UGC to get the most popular products without UGC coverage, so that the marketing team can ask a content creator for a paid contribution.
