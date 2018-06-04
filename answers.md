## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

After signing up on Datadog's website, I installed the Mac OS X Datadog Agent using the one-step install command in the instructions. 

![Install Agent](https://raw.githubusercontent.com/khewonc/Example-Images/master/Install%20First%20Agent.jpg)
*API key removed*

![Agent Installed Terminal](https://raw.githubusercontent.com/khewonc/Example-Images/master/Installed%20Agent.png)

After clicking the 'Finish' button, I was sent to the Homepage and one host was now shown to be sending data to Datadog.

![Home Page](https://raw.githubusercontent.com/khewonc/Example-Images/master/Home%20Page.png)

The System Overview Dashboard gave a summary of various metrics that were being tracked.

![System Overview](https://raw.githubusercontent.com/khewonc/Example-Images/master/System%20Overview.png)

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

From [this webpage on basic agent usage for Mac OS X](https://docs.datadoghq.com/agent/basic_agent_usage/osx/), I found the location of the config file and edited it according to instructions on [assigning tags using the configuration files](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files). I added two tags with key:value pairs `example_first_tag:example_value_1` and `example_second_tag:example_value_2`.

![Added Tags Config](https://raw.githubusercontent.com/khewonc/Example-Images/master/Added%20Tags%20to%20Config%20File.png)

After restarting the Agent, clicking on 'Host Map' from the 'Infrastructure' tab showed the new tags.

![Host Map Tags](https://raw.githubusercontent.com/khewonc/Example-Images/master/Host%20Map%20-%20Tags.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed MongoDB according to the [instructions on the MongoDB website](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/). After searching for MongoDB under the 'Integrations' tab, I used the instructions under 'Configuration' (and 'MongoDB 3.x' since I downloaded version 3.6.4) to install the integration.

![MongoDB Integration](https://raw.githubusercontent.com/khewonc/Example-Images/master/MongoDB%20Integration%20View.png)

I created a new user with administrator privileges as outlined in step 1. For step 2, there was no `mongo.yaml` file in the mongo.d directory so I created one and added the MongoDB instances. After restarting the Agent, I received an `Error: localhost:27016: [Errno 61] Connection refused` message when checking the status of the Agent using `datadog-agent status`. Port 27017 however appeared to be connecting without any problems. According to the [MongoDB documentation](https://docs.mongodb.com/manual/reference/default-mongodb-port/), port 27017 is the default port. Therefore, I commented out the first instance before installing the MongoDB integration.

![mongo.yaml](https://raw.githubusercontent.com/khewonc/Example-Images/master/mongo.yaml%2027016.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Following the example under [Write an Agent Check](https://docs.datadoghq.com/developers/agent_checks/), I created a `my_metric.yaml` file in `conf.d` and a `my_metric.py` file in `checks.d`. Python has a [random module](https://docs.python.org/2/library/random.html) that can be used to generate a random value. In line with the example, `my_metric.py` should send a metric of a random value for my_metric.

my_metric.py

![my_metric.py](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20py%20code.jpg)

my_metric.yaml

![my_metric.yaml](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20yaml%20code.jpg)

When `my_metric` is searched for in the metrics tab, a graph shows the obtained values for my_metric.

![my_metric graph](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

A time delay can be introduced with the [Python time module](https://docs.python.org/2/library/time.html).

![my_metric py time delay](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20py%20time%20delay.png)

Checking the status of the running Agent, the average execution time for my_metric changed from 0ms to 45070ms.

![execution time my_metric](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20time%20delay%20Average%20Execution%20Time.png)

The my_metric graph also shows the difference in collection intervals.

![my_metric time delay graph](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20time%20delay.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

I can modify the YAML conf file instead of the Python check file as shown in the [Write an Agent Check](https://docs.datadoghq.com/developers/agent_checks/#configuration) example. I commented out the time delay in the Python check file and added `min_collection_interval: 45` to the YAML conf file.

my_metric.py

![remove time delay my_metric.py](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20py%20remove%20time%20delay.jpg)

my_metric.yaml

![time delay my_metric.yaml](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20yaml%20time%20delay.jpg)

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

After looking through the [API support section](https://help.datadoghq.com/hc/en-us/sections/201224239-API), I decided to use Postman to make API calls since it had an [in-depth guide](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs).

I downloaded Postman and the [Datadog Postman Collection](https://help.datadoghq.com/hc/article_attachments/360002473992/DataDog.postman_collection_redacted.json). Before importing the collection, I replaced the API key and generated and replaced the APP key as suggested in the guide.  

* Your custom metric scoped over your host.

Under the 'Timeboards' folder within Postman, I created a POST request following the [Datadog API](https://docs.datadoghq.com/api/?lang=python#create-a-timeboard) and using the [Graphing JSON page](https://docs.datadoghq.com/graphing/miscellaneous/graphingjson/) as a guide.

* Any metric from the Integration on your Database with the anomaly function applied.

I used the [Anomaly Monitors via the API section](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-monitors-via-the-api) to write the anomalies function to examine deviations from the total number of commands per second issued to the database.

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

The [rollup to aggregate over time section](https://docs.datadoghq.com/graphing/#rollup-to-aggregate-over-time) was used to write the rollup function. The data were aggregated into a sum.

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

![Postman](https://raw.githubusercontent.com/khewonc/Example-Images/master/Screen%20Shot%202018-06-03%20at%202.32.25%20AM.jpg)
*API key and app key removed*

```
{
      "graphs" : [{
          "title": "my_metric Scoped Over Host",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "my_metric{host:Carolines-MacBook-Pro.local}"}
              ]
          },
          "viz": "timeseries"
      },
      {
      		"title": "Anomalies in Total Number of Commands per Second Issued to MongoDB",
      		"definition": {
      			"events": [],
      			"requests": [
      				{"q": "anomalies(mongodb.opcounters.commandps{host:Carolines-MacBook-Pro.local}, 'basic', 3)"}]
      		},
      		"viz": "timeseries"
      },
      {
      		"title": "my_metric: Sum of All Points For Past Hour in One Bucket with Rollup Function",
      		"definition": {
      			"events": [],
      			"requests": [
      				{"q": "sum:my_metric{host:Carolines-MacBook-Pro.local}.rollup(avg, 3600)"}]
      		}
      }],
      "title" : "My Timeboards",
      "description" : "A dashboard with my_metric info.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
```
I also scoped the 2nd and 3rd graphs over my own host rather than use `{*}`.

Once this is created, access the Dashboard from your Dashboard List in the UI:

[Link to the Timeboard](https://app.datadoghq.com/dash/826132/my-timeboards?live=true&page=0&is_auto=false&from_ts=1528008127439&to_ts=1528011727439&tile_size=m)

* Set the Timeboard's timeframe to the past 5 minutes

I was unable to customise the timeseries' timeframes to only show the past 5 minutes. Based on my understanding of the [timeseries visualization](https://docs.datadoghq.com/graphing/dashboards/widgets/#timeseries), the shortest timeframe that can be chosen is 1 hour. However, by using the cursor, I was able to zoom in on a 5 minute timeframe. In the same article, I saw that a Query Value widget is able to display a value based on the previous 5 minutes. However, it can only display one value unlike a timeseries, which can display many points.

![5 min timeframe](https://raw.githubusercontent.com/khewonc/Example-Images/master/5%20min%20timeframe.png)

*Since only a 5 minute timeframe is shown and the graph with the rollup function uses summed 1 hour buckets, there is no data shown in that graph* 

* Take a snapshot of this graph and use the @ notation to send it to yourself.

Hovering over each graph and clicking on the camera icon allowed me to send snapshots to myself using the @email@address.com notation.

![snapshot1](https://raw.githubusercontent.com/khewonc/Example-Images/master/Snapshot%20my_metric%20scoped%20over%20host.png)

![snapshot2](https://raw.githubusercontent.com/khewonc/Example-Images/master/Snapshot%20anomaly.png)

![snapshot3](https://raw.githubusercontent.com/khewonc/Example-Images/master/Snapshot%20rollup.png)

* **Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph in general detects any unusual fluctuations in a metric based on its historical behaviour. Recent values are used to dictate a statistical range of expected values that a graph may have. The graph above looks at the total number of commands per second sent to the MongoDB database. For anomaly detection, the 'basic' algorithm was used since the data are not seasonal with a tolerance of 3 standard deviations.

Sources: [1](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/) [2](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-monitors-via-the-api)

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

After clicking on the 'New Monitor' link under the 'Monitors' tab, I clicked the 'Metric' option to create a new Metric Monitor.

![metric monitor1](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20monitor%20setup%201.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

The [message template variables page](https://docs.datadoghq.com/monitors/notifications/#message-template-variables) was used to customise the monitor messages. 

![metric monitor2](https://raw.githubusercontent.com/khewonc/Example-Images/master/my_metric%20monitor%20setup%202.png)

```
{{#is_alert}}
Host: {{host.name}}
IP: {{host.ip}}
The value of my_metric has surpassed the alert threshold of {{threshold}}  The average value for the past 5 minutes is {{value}}.
{{/is_alert}}

{{#is_warning}}The value of my_metric has surpassed the warning threshold of {{warn_threshold}}.{{/is_warning}}

{{#is_no_data}}The my_metric value has been in the No Data state for 10 minutes.{{/is_no_data}}

@khewonc@gmail.com
```
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![warning email](https://raw.githubusercontent.com/khewonc/Example-Images/master/Warning%20email%20from%20my_metric.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    * One that silences it from 7pm to 9am daily on M-F,
    
    ![m-f downtime](https://raw.githubusercontent.com/khewonc/Example-Images/master/Weekly%20downtime%20message%20setup.png)
    
    ![m-f downtime email](https://raw.githubusercontent.com/khewonc/Example-Images/master/Weekly%20downtime%20email.png)
    
    * And one that silences it all day on Sat-Sun.
    
    ![weekend downtime](https://raw.githubusercontent.com/khewonc/Example-Images/master/Weekend%20downtime%20setup.png)
    
    ![weekend downtime email](https://raw.githubusercontent.com/khewonc/Example-Images/master/Weekend%20downtime%20email.png)
    
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Clicking on the 'Schedule Downtime' button under the 'Manage Downtime' tab allowed me to customise downtime settings. The @email@address.com notation was used to notify me by email.


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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
    app.run(host='0.0.0.0', port='5050')
```    

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

Using the [APM Setup guide](https://docs.datadoghq.com/tracing/setup/), I tried installing the [Trace Agent](https://github.com/DataDog/datadog-trace-agent#run-on-osx) on my computer. However, following the Mac OS X instructions, I received the reply `-bash: ./datadog-trace-agent-6.2.1: is a directory` when I attempted the 'Run the Trace Agent using the Datadog Agent configuration.' step.

After looking at [an issue](https://github.com/DataDog/datadog-trace-agent/issues/397) for ideas, I decided to follow several suggestions made on that page and download the Trace Agent according to the [Development](https://github.com/DataDog/datadog-trace-agent#development) section. I continued to have problems when trying to run the agent using the listed command, `trace-agent --config /etc/dd-agent/datadog.conf`. After specifying the path of the trace-agent file and substituting the listed configuration with the path of the configuration file from the [Basic Agent Usage page](https://docs.datadoghq.com/agent/basic_agent_usage/osx/#configuration), I was able to get the Trace Agent running in the foreground.

The `datadog.yaml` file was also modified to include the following code according to [this Agent Configuration](https://docs.datadoghq.com/tracing/setup/#agent-configuration):
```
apm_config:
  enabled: true
```

I installed Flask according to these instructions: http://flask.pocoo.org/docs/0.12/installation/#installation. 

Based on the [quickstart Flask guide](http://flask.pocoo.org/docs/0.12/quickstart/), I copied the Flask app code above into a file called `app.py`. Navigating to `0.0.0.0:5050` showed the running Flask code.

![entrypoint](https://raw.githubusercontent.com/khewonc/Example-Images/master/entrypoint.png)

![api/apm](https://raw.githubusercontent.com/khewonc/Example-Images/master/api%3Aapm.png)

![api/trace](https://raw.githubusercontent.com/khewonc/Example-Images/master/api%3Atrace.png)

Following the instructions under the APM tab and Services link, I installed `ddtrace` and ran the `ddtrace-run python app.py` command to instrument the code. Clicking the APM tab and selecting 'flask' showed the traces. For each graph, I clicked the 'Export to Timeboard' icon to add the graph to my timeboard.

![app.py service](https://raw.githubusercontent.com/khewonc/Example-Images/master/app.py%20Service.png)

* **Bonus Question**: What is the difference between a Service and a Resource?

A service is composed of a number of different processes that together carry out the same job. The flask app above is an example of a service although more complex applications may have multiple services. A resource is an action for a service, such as an endpoint or a query. For a SQL database, a SQL query would be a resource.

Sources: [1](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-) [2](https://docs.datadoghq.com/tracing/visualization/)

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

![dashboard](https://raw.githubusercontent.com/khewonc/Example-Images/master/Dashboard%20APM%20my_metric.png)

[Link to Dashboard](https://app.datadoghq.com/dash/826132/my-timeboards?live=true&page=0&is_auto=false&from_ts=1528074027763&to_ts=1528077627763&tile_size=m)

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

I would use Datadog to monitor practice room availability and environmental conditions in the school music building. Since there are no windows and rooms are (somewhat) soundproofed, it can be difficult to determine whether one of the limited number of rooms is open unless the occupant locks the door or is practicing very loudly. This can lead to accidental and awkward disruptions and often, a fruitless trip to the music building in search of a practice space. In addition, instruments are susceptible to changes in temperature and humidity so the ability to monitor these parameters for each room would be useful as not all those rooms were created equal.
