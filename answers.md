## Collecting Metrics:
* Adding Tags: To add tags to my host, I added the following line to my agent's datadog.yaml file.
  ```
  tags: name:vagrant_ubuntu_1, env:dev, role:host
  ```
  My host with tags: 
  <img src="https://s18.postimg.org/y5pf4kah5/image.png">
* Setting up a database integration:  I set up a MongoDB database on my vagrant box and integrated it with my agent.
  * The new datadog user:
  
    <img src="https://s18.postimg.org/fddk10w3d/db_user.png">
  * The code added to conf.d/mongo.yaml:
    <img src="https://s18.postimg.org/jz9o98k5l/mongo_yaml.png">
  * Link to the MongoDB integration dashboard: https://app.datadoghq.com/screen/integration/13/mongodb
* Custom Agent Check at 45 second intervals:  To add my custom agent I used the following python script and yaml:
  * checks.d/metric_check.py:
    ```
    from checks import AgentCheck
    from random import *
    class MetricCheck(AgentCheck):
         def check(self, instance):
           x = randint(0,1000)
           self.gauge('my_metric', x)
    ```
  * conf.d/metric_check.yaml:
    ```
    init_config:
        min_collection_interval: 45

    instances:
        [{}]
    ```
  * **Bonus Question:**  Yes, I was able to modify the collection interval by adding a min_collection_interval value of 45 in the conf.d/metric_check.yaml file.

## Visualizing Data:
* Creating a Timeboard utilizing the Datadog API:
  * Python script used to create the timeboard:
    ```
    #makeTimeboard.py
    from datadog import initialize, api

    api_key = '6a44adbdf2d661542100723e1b79b58a'
    app_key = '5cd019b15629768501a9d58146fe26e3bdea72d7'
    options = {
        'api_key': api_key,
        'app_key': app_key
    }

    initialize(**options)

    title = "My API Created Timeboard"
    description = "A super awesome timeboard!"
    graphs = [{
        "definition": {
            "events": [],
            "requests": [
                {
            "q": "avg:my_metric{host:precise64}",
            "type": "bars",
            "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
            },
            "conditional_formats": [],
            "aggregator": "avg"
          }
            ],
            "viz": "timeseries",
        "status": "done"
        },
        "title": "Value of my_metric from host:precise64"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {
            "q": "anomalies(avg:mongodb.metrics.document.insertedps{server:mongodb://datadog:_localhost:27017}, 'basic', 2)",
            "type": "line",
            "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
            },
            "conditional_formats": [],
            "aggregator": "avg"
          }
            ],
            "viz": "timeseries",
        "status": "done"
        },
        "title": "MongoDB inserts with anomalies highlighted"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {
            "q": "avg:my_metric{*}.rollup(sum, 3600)",
            "type": "line",
            "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
            },
            "conditional_formats": [],
            "aggregator": "last"
          }
            ],
            "viz": "query_value",
        "precision": "0"
        },
        "title": "Sum of my_metric from the past hour"
    }]


    read_only = True
    api.Timeboard.create(title=title,
                         description=description,
                         graphs=graphs,
                         read_only=read_only)
    ```
  * Created Dashboard: https://app.datadoghq.com/dash/755892/my-api-created-timeboard?live=false&page=0&is_auto=false&from_ts=1522713358275&to_ts=1522716958275&tile_size=m
    <img src="https://s18.postimg.org/dpeelu021/API_Timeboard.png">
* Snapshot of a 5 min interval on the anomaly graph:
  <img src="https://s18.postimg.org/n647svrqx/anomaly_snapshot.png">
* Bonus Question: The anomaly graph is highlighting any data points outside of the expected bounds.  The bounds are relative to the actual data observed and can be manipulated with a multiplier (in this case 2).

## Monitoring Data:
* Create a monitor on my_metric:
  * Link to my created monitor: 
    https://app.datadoghq.com/monitors#4549553?group=all&live=4h
  * No Data Email:
    <img src="https://s18.postimg.org/nivlz2hqh/image.png">
  * Warning Email (metric over 500):
    <img src="https://s18.postimg.org/4dscpbii1/image.png">
  * Monitor message text:
    <img src="https://s18.postimg.org/bv1k495dl/monitor_text.png">
  * **Bonus Question:**
    * M-F Scheduled downtime link: https://app.datadoghq.com/monitors#downtime?id=304580441
    * Weekend downtime link: https://app.datadoghq.com/monitors#downtime?id=305135624
    * Email snapshot: 
      <img src="https://s18.postimg.org/q07d6c9cp/image.png">

## Collecting APM Data:
* Dashboard with APM and Infrastructure Metrics: https://app.datadoghq.com/dash/749235/connors-timeboard-30-mar-2018-1655?live=false&page=0&is_auto=false&from_ts=1522709101868&to_ts=1522716335512&tile_size=m
  <img src="https://s18.postimg.org/410yj45d5/image.png">
* Fully instrumented Flask app:
  ```
  from flask import Flask
  import logging
  import sys
  import blinker as _

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

  traced_app = TraceMiddleware(app, tracer, service="flask-apm-intro-app", distributed_tracing=False)

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
* curl used to power the app: curl 127.0.0.1:5000/api/trace
* **Bonus Question:** A service is a set of processes that are designed to carry out a specific task (like a python script).  A resource is an action performed by a service like a function or query.

## Final Question:
I would love to integrate professional sports data (preferably NHL!) into Datadog to create unique visuals and power advanced analytics.  With the ever growing fantasy sports industry you could even build dashboards and monitors to help fantasy players manage their teams.
