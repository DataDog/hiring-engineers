# Answers

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

**Answer:**

*Tag definition*
![host tags](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/tagging.png)

*Tags on GUI*
![tags](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/server-tagging.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

**Answer:**

![mysql_overview](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/mysql_overview.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

**Answer:**

[the yaml file](https://github.com/dayousong/hiring-engineers/blob/solutions-engineer/uploads/scripts/larry_check.yaml)

[the python check script](https://github.com/dayousong/hiring-engineers/blob/solutions-engineer/uploads/scripts/larry_check.py)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

**Answer:**

This was defined in the same yaml file as above with the line: __- min_collection_interval: 45__

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

**Answer:**

Not sure if I understand the question, is the above answer for this question too?

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.

**Answer:**

![Timeboard created via API/script](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/timeboard%20via%20api.png)

* Any metric from the Integration on your Database with the anomaly function applied.

**Answer:**

![Mysql metric with anomaly function applied](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/mysql%20metric%20anomaly_robust.png)

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

**Answer:**

![Hourly sum up of my_metric definition](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/my_metric%20hourly%20sum%20up.png)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

**Answer:**

[Here is the Python script that calls the API to create the timeboard](https://github.com/dayousong/hiring-engineers/blob/solutions-engineer/uploads/scripts/timeboard_api.py)

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

**Answer:**

![Snapshot email via @ notation](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/dashboard_snapshot.png)

* **Bonus Question**: What is the Anomaly graph displaying?

**Answer:**

Anomaly graph shows the standard deviation of the metrics based on learning on historical data.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

**Answer:**

![Monitor definition](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/monitor%20definition.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.

**Answer:**

Please refer to the previous screen capture.

* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

**Answer:**

Please refer to the previous screen capture. More details on the message definition:
```
High value of my_metric has been received.

{{#is_alert}}
This is an Alert from {{host.name}}/{{host.ip}}!
The current my_metric value is: {{value}}, the current threshold is: {{threshold}}. 
{{/is_alert}} 

{{#is_warning}}
This is a Warning!
The current my_metric value is: {{value}}, the current threshold is: {{warn_threshold}} 
{{/is_warning}} 

{{#is_recovery}}my_metric is back to normal! {{/is_recovery}} @somebody@gmail.com
```

* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

**Answer:**

Please refer to the previous code block.

Snapshot of alert with IP address:
![Alert with IP address](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/alert%20with%20ip%20address.png)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

**Answer:**

Please refer to the previous screen capture.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

**Answer:** I will leave this for the future exercise.

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

**Answer:**

The definition:
![Flask hit definition](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/Flask%20hit%20definition.png)

The timeboard:
![Flask hit timeboard](https://raw.githubusercontent.com/dayousong/hiring-engineers/solutions-engineer/uploads/images/Flask%20hit%20dashboard.png)

Please include your fully instrumented app in your submission, as well.

**Answer:**

![The instrumented Flask app](https://github.com/dayousong/hiring-engineers/blob/solutions-engineer/uploads/scripts/flask_app_instrumentation.py)

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

**Answer:**

I am so impressed by this product! With the richness and ease of use on both frontend and agents, I think Datadog is ready for the age of IoT and 5G. 

Some minor comments:
1. Maybe it's there that I have not noticed.  The action part of the monitor triggering seems to be limited to notification?  Can we trigger some other types of actions once a monitor is triggered?  Things like triggering a script on the agent side?  
2. The GUI seems to be slow from time to time.  
3. The docker container agent doesn't work easily with tags.  Maybe it's my fault but I thought I have followed all the right instructions.

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

**Thanks for the reminding, just realised it's so easy to share a screenboard, here's a dummy one: https://p.datadoghq.com/sb/54e014755-67c664a71a28185a844b21db7a6f1557**

