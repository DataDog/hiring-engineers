## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
<img src=screenshots/screenshot1.png>

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database. 
  * Installed MariaDB (MySQL) on the RHEL box.
  * Create the datadog database user and granted the correct permissions
  * Added the following stanza to conf.d/mysql.d/conf.yaml
```
  instances:
  - server: 127.0.0.1
    user: datadog
    pass: 'password' # from the CREATE USER step earlier
    port: 3306
    options:
       replication: 0
       galera_cluster: 1
       extra_status_metrics: true
       extra_innodb_metrics: true
       extra_performance_metrics: true
       schema_size_metrics: false
       disable_innodb_metrics: false
```
  * Restarted Agent
  * Screenshot:
    <img src=screenshots/screenshot2.png>
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
  The customer agent check file is included in this git repo.  The python script is located at checks.d/mymetric.py 
  Screenshot of the my_metric collection:
  <img src=screenshots/screenshot3.png>
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
  The updated configuration file for the custom check is located at conf.d/mymetrics.yaml 
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
  You don't modify the python script.  The check configuration yaml file has to be updated to update the check interval.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.


* The script has been completed and it is under the scripts directory.  The file is called 'api-timeboard.py'

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
  * Created the Timeboard and set the timeframe to the past 5 minutes.  I am only able to share a snapshot of a single graph in this timeboard.   The Datadog documention confirms you are not able to share/snapshot the whole timeboard (screenshot of the info I found).   Also included is a screenshot of the shared 5 minute snapshot anomaly graph.   
#### Data on Timeboard Functionality
<img src=screenshots/timeboarddata.png>

#### The graph snapshot that was sent to myself
<img src=screenshots/last5minutes.png>
* **Bonus Question**: What is the Anomaly graph displaying?
The graph highlights the times where the metric (in this case the MySQL instance user time CPU cycles) was more or less than the average consumption.

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
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* Created the monitor as asked.  I have inclued exported monitor definition at monitors/my-metric-monitor.json.   Also below is a screen shot of the email alert.
<img src=emailalert.png>


* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

* Downtime created and the screen shot of the email notification is:
<img src=emailnotificaiton.png>


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
