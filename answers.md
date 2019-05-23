## Start your monitoring with DataDog

The Porpuse of this document is to give the reader an introductory guide of DataDog and the different features.

Requirements:
* Ubuntu 16.04 (Minimum)
* Any Database Management System (We are going to use MySQL)
* When signing up for Datadog, use “Datadog Recruiting Candidate” in the “Company” field



## Collecting Metrics:

The first task will be collect metrics, for this we need to intall the Agent in your Ubuntu machine.
Log into your https://www.datadoghq.com/ with your information and navigate to the little puzzle piece title "Integrations" and Select "Agents", then click over Ubuntu and copy and paste the easy one-step install similar to the example below.

```
DD_API_KEY=b2a249da9744daa8e0eceaXXXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
For this we could use different methods, however in this exercise we will use the configuration file to add tags.

Navigate to the directory where datadog-agent was installed and modify the file datadog.yaml as show in the pictures below.

![](images/Tags.PNG)

Check the Tags have been applied as configured.

![](images/Tags4.PNG)

For more methods to assign tags, please follow the documentation linked here https://docs.datadoghq.com/tagging/#assigning-tags

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Intall any Database Management System, for example MySQL following this guideline https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

```
from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.uniform(0, 1000))
```


* Change your check's collection interval so that it only submits the metric once every 45 seconds.

![](images/45seconds.PNG)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
Yes, by modifying the .yaml file

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

```
curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "My Custom Metric",
      "widgets" : [{
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "my_metric{*}"}
              ],
              "title": "Hello World?"
          }
      }],
      "layout_type": "ordered",
      "description" : "A dashboard with memory info.",
      "is_read_only": true,
      "notify_list": ["user@domain.com"],
      "template_variables": [{
          "name": "alphadog",
          "prefix": "host",
          "default": "my-host"
      }]
}' \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"
```

```
curl  -X PUT -H "Content-type: application/json" \
-d '{
      "title" : "My Custom Metricv2",
      "widgets" : [{
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "my_metric{*}"}
              ],
              "title": "Hello World?"
          }
      },
      	{
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "sum:mysql.performance.queries{*}"}
              ],
              "title": "Mysql"
          }
      }],
      "layout_type": "ordered",
      "description" : "An updated dashboard with more info.",
      "is_read_only": true,
      "notify_list": ["moises.zannoni@gmail.com"],
      "template_variables": [{
          "name": "alphadog",
          "prefix": "host",
          "default": "my-host"
      }]
}' \
"https://api.datadoghq.com/api/v1/dashboard/${dashboard_id}?api_key=${api_key}&application_key=${app_key}"
```

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

![](images/5minutes.PNG)

* Take a snapshot of this graph and use the @ notation to send it to yourself.

![](images/emailsendPNG.PNG)

* **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![](images/Monitor01.PNG)
![](images/Monitor02.PNG)
![](images/Monitor03.PNG)
![](images/Monitor04.PNG)
![](images/Monitor05.PNG)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

**No Data**
![](images/AlertNoData.PNG)

**Warning**
![](images/AlertWanringPNG.PNG)

**Alert**
![](images/Alert.PNG)


* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  
  ![](images/Silenceweek.PNG)
  
  * And one that silences it all day on Sat-Sun.
  
   ![](images/Silenceweekend.PNG)
  
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
   ![](images/notifications.PNG)

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

**No Changes**

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

Tried to run ddtrace-run with the following command
```
ddtrace-run python3 ./dogapp.py > nohup.out 2> nohup.err < /dev/null &
```

But I didn't managed to make it work, even when I activated the APM in datadog.yaml

![](images/apmon.PNG)

Couldn't figure out why it wasn't working.

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Anything really, could setup an small IOT in my Door with a contact, setup 0 as a value when the circuit is close and 1 when the circuit is open, so I can monitor when someone goes into my room.

In more useful escenarios, you could setup software with a cognotive services such as Microsoft Vision to identify Weapons in Public Places, if possitive send alerts to the respectives police enforcements.
IoT devices could monitor residential metrics, such as water, electricity, high impacts near areas that are promtept to people falling and monitor elderly houses to alert different departments such as firefighters, ambulences and such.
