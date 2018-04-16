## Collecting Metrics:
* To add tags, I added the following tagsto my /etc/datadog-agent/datadog.yaml file in my Vagrant Ubuntu
    ```
    tags:
      - name:vagrant_ubuntu
      - role:hire_excercise
      - env:test
    ```
    Here is the Host Map screenshot of my host with tags
    <img src="https://s7.postimg.cc/v1midqior/Screen_Shot_2018-04-15_at_12.52.56_PM.png">
https://app.datadoghq.com/infrastructure/map?host=452467528&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=host&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&node_type=host

* For the database integration, I used MongoDB.
  * To install the MongoDB integration, I created a new datadog user
      ```
      db.createUser({
      "user":"datadog",
      "pwd": "dyFgwvp4o9yDPAR3drclqPeU",
      "roles" : [
        {role: 'read', db: 'admin' },
        {role: 'clusterMonitor', db: 'admin'},
        {role: 'read', db: 'local' }
      ]
      })
      ```

       <img src="https://s7.postimg.cc/hshs4jnyz/Screen_Shot_2018-04-15_at_1.18.12_PM.png">

  * I then added the conf.d/mongodb.yaml file
    <img src="https://s7.postimg.cc/p773xgs0b/Screen_Shot_2018-04-15_at_1.18.42_PM.png">

  * Here is a view of the status check on my mongodb integration from my Host Map
    <img src="https://s7.postimg.cc/m1mi6x1kr/Screen_Shot_2018-04-15_at_1.23.33_PM.png">
    The MongoDB dashboard: https://app.datadoghq.com/screen/integration/13/MongoDB?tpl_var_scope=host%3Aprecise64

* Custom Agent Check
  * To create the custom agent check that submits 'my_metric', I first created a python script to generate the random number 'n' between 0 and 1000 using randint, and used self.gauge to send a gauge of n to 'my_metric'.

    checks.d/my_metric_check.py:
      ```
       from checks import AgentCheck
       from random import *
       class MetricCheck(AgentCheck):
            def check(self, instance):
               n = randint(0,1000)
               self.gauge('my_metric', n)
      ```

  * I then added the conf.d/my_metric_check.yaml file with the following
      ```
      init_config:
          min_collection_interval: 45

      instances:
          [{}]
      ```
* **Bonus Question**:  I added the min_collection_interval:45 to conf.d/my_metric_check.yaml to modify the collection interval without modifying the Python check.


## Visualizing Data:
* Python script for creating the Timeboard

      
        from datadog import initialize, api

        options = {
            'api_key': 'ce52b8e3d888e80875032bff5bcd71cb',
            'app_key': '38840cbb77d9c7031c15ff63343b7e7afae7015d'
          }

        initialize(**options)

        title = "My Timeboard"
        description = "my_metric scoped over the host, number of mongodb databases , my_metric sum"
        graphs = [{
            "definition": {
                "events": [],
                "requests": [
                    {
                "q": "avg:my_metric{host:precise64}",
                "type": "bars",
                "style": {
                "palette": "cool",
                "type": "solid",
                "width": "thin"
                },
                "conditional_formats": [],
                "aggregator": "avg"
              }
                ],
                "viz": "timeseries",
            "status": "done"
            },
            "title": "Value of my_metric returned"
        },
        {
            "definition": {
                "events": [],
                "requests": [
                    {
                "q": "anomalies(avg:mongodb.dbs{server:mongodb://datadog:_localhost:27017}, 'basic', 2)",
                "type": "line",
                "style": {
                "palette": "cool",
                "type": "thin",
                "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "avg"
              }
                ],
                "viz": "timeseries",
            "status": "done"
            },
            "title": "Anomalies: Number of MongoDB Existing Databases"
        },
        {
            "definition": {
                "events": [],
                "requests": [
                    {
                "q": "avg:my_metric{*}.rollup(sum, 3600)",
                "type": "line",
                "style": {
                "palette": "cool",
                "type": "thing",
                "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "last"
              }
                ],
                "viz": "query_value",
            "precision": "0"
            },
            "title": "Sum of my_metric the past hour"
        }]


        read_only = True
        api.Timeboard.create(title=title,
                             description=description,
                             graphs=graphs,
                             read_only=read_only)
     
     
    <img src="https://s7.postimg.cc/je23tnjzv/Screen_Shot_2018-04-15_at_3.48.16_PM.png">
    
     https://app.datadoghq.com/dash/786403/my-timeboard?live=true&page=0&is_auto=false&from_ts=1523842111428&to_ts=1523845711428&tile_size=m

* API timeboard image
  * Focusing in on the last 5 minutes can be done by dragging the time period within the graphs. After zooming in, and clicking the snapshot button, I sent this picture to myself with a note
    <img src="https://s7.postimg.cc/lvdv16jej/Screen_Shot_2018-04-15_at_3.51.52_PM.png">


* **Bonus Question**: This graph is showing the amount of databases that exist within MongoDB. The Anomalies graph provides insight into the data's expected bounds relative to the historical data observed. Anomalies will be highlighted with a different color when falling outside of a defined standard deviation, which I set to 2.

## Monitoring Data:
* I created a monitor on my_metric to notify when certain thresholds are crossed:
<img src="https://s7.postimg.cc/oupd1q5bf/Screen_Shot_2018-04-15_at_4.19.15_PM.png">

* Specific messages are sent based on the different monitor states:

      ```
      {{#is_alert}}

      Alert

      my_metric was {{value}} on avg the last 5m

      {{/is_alert}}

      {{#is_warning}}

      Warning

      my_metric was > 500 on avg the last 5m

      {{/is_warning}}

      {{#is_no_data}}

      No Data

      my_metric is missing data for the last 10 mins

      {{/is_no_data}}

      @michaelalaning@gmail.com

      ```
* Screenshot of the email that was sent from a Warning:
    <img src="https://s7.postimg.cc/obtgk8ih7/Screen_Shot_2018-04-15_at_10.25.35_PM.png">

* **Bonus Question**:
  * I scheduled downtime directly from the GUI.

    Monday-Friday downtime  7pm - 9am

    <img src="https://s7.postimg.cc/xpusq799n/Screen_Shot_2018-04-15_at_5.44.37_PM.png">

   Weekends starting Saturday at 9am - Monday at 9am

   <img src="https://s7.postimg.cc/3romlmsej/Screen_Shot_2018-04-15_at_10.23.04_PM.png">

   Here is an example email from the scheduled downtime notification
   <img src="https://s7.postimg.cc/pfdkvv30r/Screen_Shot_2018-04-15_at_10.31.45_PM.png">

## Collecting APM Data:
 * I used the following Flask app provided in the exercise

       ```
       from flask import Flask
       import logging
       import sys

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
           app.run()
       ```
 * the following terminal command was used:
     ```
     $ ddtrace-run python flask_app.py
     ```

 * I also added to my datadog.yaml file:
     ```
     apm_enabled:True
     ```

    Here is a view of a dashboard containing APM and Infrastructure metrics:
    <img src="https://s7.postimg.cc/6x98bs5uz/Screen_Shot_2018-04-15_at_9.42.29_PM.png">


* **Bonus Question**: Services act as a set of processes that make up the necessary components to fulfill specific tasks. Resources are the particular actions that are used within the services, such as a query or function.


## Final Question:
I think looking outside of the IT teams within enterprises could have a lot of impact. Specifically, within database companies, sales organizations could better understand their user community, and Product teams could focus on what features or queries are being most used. On the Sales side, having detailed insights on what the users are doing would help identify potential sales and upgrade opportunities. On the Product side, the roadmap could be more strategically developed around the most heavily used features, with visibility into how new releases affect usage. In general, at an enterprise level, Datadog seems to target IT teams most effectively, but opening the door to other sides within the business could increase overall enterprise strategy.

For a day to day consumer use case, I would love to implement Datadog w to understand what Wifi networks will have the best network speed. Understanding where the different deadzones are in the office, and the optimal time to be on each network would help my coworkers and I understand what we should be connected to during client meetings or product demonstrations. 

