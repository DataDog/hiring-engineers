## Prerequisites - Setup the environment
  I chose to use docker to launch datadog agent and monitor a mongodb instance.

  ### Pull Images Via Docker Hub
  * Mongo: `docker pull mongo`
  * Mongo-express: `docker pull mongo-express`
  * Datadog Agent: `docker pull datadog/agent`

  ### Setup mongo container *note port mapping for all containers*
  `docker run -d --name mongodb mongo -p 27017:27017`

  ### Setup mongo-express container (because web interfaces are prettier!)
  `docker run -it -d --rm -p 8081:8081 --link mongodb:mongo --name mongo-express mongo-express`

  ### Setup datadog agent container
  ```
  docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -e DD_API_KEY= < YOUR API KEY> \
              -e DD_APM_ENABLED=true \
              -e DD_APM_NON_LOCAL_TRAFFIC=true \
              -p 8126:8126/tcp \
              datadog/agent:latest \
  ```
  ### View running containers to verify
  `docker ps -a`  

  ![list docker containers](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/running-docker-containers.png)

## Collecting Metrics:
  **Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**
  ![hostname with tags](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/hostname-with-tags.png)

   * shell into dd-agent container:
   `docker exec -it dd-agent bash`
   * install nano editor:
   `sudo apt-get update`
   `sudo apt-get install nano`
   * open datadog.yaml (/etc/datadog-agent/datadog.yaml) file in nano editor:
   `nano datadog.yaml`
   * change hostname & add tags:
   `hostname: WOPR`
   `tags: project:tictactoe`
   * restart dd-agent:
   `docker restart dd-agent`
   * *note* I added additional tags to the host via the UI

  **Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

   * verify mongodb container is running from preliminary setup
    `docker ps -a`
   * navigate to integrations menu on datadog dashboard and search for "mongodb" and follow configuration instructions
      * create mongo.yaml file on local machine
      *note* follow the guidance [here](https://docs.datadoghq.com/integrations/mongo/)
      * copy mongo.yaml file to dd-agent conf.d directory: \
       `docker cp mongo.yaml dd-agent:conf.d/mongo.yaml`
      * Shell into mongo instance: \
        `docker exec -it mongodb bash`
      * start mongo CLI: \    
         `mongo`
      * add new admin user:    
          ```
            use admin
            db.auth("admin", "admin-password")
            db.createUser({"user":"datadog", "pwd": "<generated pwd", "roles" : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})
           ```
      * verify user was created through mongo-express interface (admin > system users> id = admin.datadog):

        ![mongo-express user check](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/mongo-express-user-check.png)
   * restart the datadog agent
    `docker restart dd-agent`
   * verify host is availabile via mongodb dashboard within datadog
    ![mongodb dashboard](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/mongodb-dashboard.png)

  **Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**
   * write python script for my_metric to generate a random number between 1-1000:
      ```
      try:
          from checks import AgentCheck
      except ImportError:
          from datadog_checks.checks import AgentCheck

      __version__ = "1.0.0"

      class MyMetric(AgentCheck):
          def check(self, instance):
              from random import *
              self.gauge('my_metric', randint(1,1000))
      ```
   * copy python script files to docker agent container \
      `docker cp my_metric.py dd-agent:conf.d/my_metric.py`
   * *note* refer to [Writing a customer Agent check](https://docs.datadoghq.com/developers/write_agent_check) for more details   

  **Change your check's collection interval so that it only submits the metric once every 45 seconds.**
   * write my_metric.yaml file to set collection interval *note:The names of the configuration and check files must match.*
      ```
      init_config:

      instances:
        - min_collection_interval: 45
       ```
   * copy python yaml file to docker agent container conf.d directory \
      `docker cp my_metric.yaml dd-agent:conf.d/my_metric.yaml`
   * restart the agent
      `docker restart dd-agent`
   * Navigate to the metrics explorer dashboard and search for "my_metric" to view a timebased plot
   ![my_metric graph](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/metric-explorer-mt_metric.png)

  **Bonus Question Can you change the collection interval without modifying the Python check file you created?**
   * You can avoid changing the python check file by setting the collection interval via the .yaml configuration file

## Visualizing Data:
**Utilize the Datadog API to create a Timeboard that contains:**
  **Your custom metric scoped over your host.**
    * For API references look [here](https://docs.datadoghq.com/api/?lang=python#timeboards)
    * Create application key via integrations > API's menu
    * Install datadog python libraries locally:
      `pip install datadog`
    * Write python script per datadog API documentation to [create timeboard](https://docs.datadoghq.com/api/?lang=python#create-a-timeboard)
    ```
      from datadog import initialize, api

      options = {
        'api_key': '<YOUR API KEY>',
        'app_key': '<YOUR APP KEY>'
      }

      initialize(**options)

      title = "My Metric Over Host & Mongodb Anomaly"
      description = "timeseries plot for my_metric"
      graphs = [{
          "definition": {
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ],
              "viz": "timeseries"
          },
          "title": "my metric over time"
          },
          {
          "definition": {
              "requests": [
                {
                  "q": "anomalies(avg:mongodb.mem.bits{*}, 'basic', 2)",
                  "style": {
                    "width": "normal",
                    "palette": "dog_classic",
                    "type": "solid"
                  },
                }
              ],
              "viz": "timeseries"
              },
              "title": "Avg of mongodb.mem.bits over *"
          },
          {
            "definition": {
              "viz": "timeseries",
              "requests": [
                {
                  "q": "avg:my_metric{host:WOPR} by {host}.rollup(sum, 60)",
                  "style": {
                    "width": "normal",
                    "palette": "dog_classic",
                    "type": "solid"
                  },
                }
              ]
            },
            "title": "Sum of My_Metric on WOPR"
          }
      ]

      template_variables = [{
          "name": "WOPR",
          "prefix": "host",
           "default": "host:WOPR"
      }]

      read_only = True
      api.Timeboard.create(title=title,
                          description=description,
                          graphs=graphs,
                          template_variables=template_variables,
                          read_only=read_only)
    ```

    ![timeboard created screenshot](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/my_metric-custom-timeline.png)

  **Any metric from the Integration on your Database with the anomaly function applied.**
    * anomaly detection can be called via the datadog API (see complete script above for context):
    ```
    "definition": {
        "requests": [
          {
            "q": "anomalies(avg:mongodb.mem.bits{*}, 'basic', 2)",
            "style": {
              "width": "normal",
              "palette": "dog_classic",
              "type": "solid"
            },
          }
        ],
        "viz": "timeseries"
        },
        "title": "Avg of mongodb.mem.bits over *"
    ```

  **Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket**
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
Once this is created, access the Dashboard from your Dashboard List in the UI:
  * Set the Timeboard's timeframe to the past 5 minutes
    * ![5m view](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/my_metric-5m-view.png)

  * Take a snapshot of this graph and use the @ notation to send it to yourself.
    * highlight notation
    ![tagging graph](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/tagging-graph.png)

    * email notification   
    ![tagging graph](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/%40notification.png)
  * Bonus Question: What is the Anomaly graph displaying?
    * when zoomed in the anomaly graph shows a "shadow" range for abnormal behavior.

## Monitoring Data
**Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.**

**Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:**

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.
![mointor config](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/monitor-dashboard-config.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![email alert](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/monitor-alert-email.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  ![downtime email](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/scheduled-downtime-email.png)

## Collecting APM Data:
**Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:**

```python
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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

  * to run a trace on the flask application above first launch a python container in docker:
    `docker run --name python-dev python -p 5050`
  * shell into container:
    `docker exec -it python-dev bash`
  *  install flask and ddtrace
    `pip install flask`
    `pip install ddtrace`
  * copy python app to docker container:
    `docker cp my_app.py python-dev:home/my_app.py`
  * run ddtrace when in the same local directory as my_app.py:
    `ddtrace-run python my_app.py`
  * hit localhost:5050 through command line or web browser. The trace won't start until the server is pinged.

  * The above app was a simple webserver and was the most easy to understand how & what happens when a trace takes place.  

* **Bonus Question**: What is the difference between a Service and a Resource?
  * A service is a set of processes that do the same job. For example, a database.
  * A resource is a particular action that a service can do. For example, a database resource would be the query itself.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
![trace list](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/flask-app-trace-list.png)

![trace list](https://github.com/polyygon/hiring-engineers/blob/polyygon/images/flask-app-trace-dashboard.png)

Please include your fully instrumented app in your submission, as well.

## Final Question:

**Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?**
  * Outfitting a copper mine and all of its assets - from trucks, cranes, and drills would be a childhood dream. I would first  do a proof of concept on my sons tonka trucks and sandbox. I would mointor the load weight (in lbs) and state (full or empty) at several parts of a mock mining process. Using the desired data could give valuable insight into how to better organize my crew to become more productive. An interesting potential second order effect would be monitoring asset health and deploying predictive maintence on all my gear! 

## References
 * [Guide to the Docker Agent](https://docs.datadoghq.com/agent/docker/)
 * [Datadog Agent Docker Hub Image](https://hub.docker.com/r/datadog/agent)
 * [Mongo-Express Docker Hub Image](https://hub.docker.com/_/mongo-express)
 * [Python Docker Hub Image](https://hub.docker.com/_/python)
