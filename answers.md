<a href="https://www.datadoghq.com/careers/" title="Careers at Datadog">
</a>

## 1. Collecting Metrics:

A. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I created a virtual environment to learn the Datadog agent with Vagrant and Virtual Box, used SSH to reach the machine (through Windows PowerShell, yikes), and configured it as instructed. I added custom tags to demonstrate the flexible tagging in the datadog.yaml file, and located the same tags in the Infrastructure->Host Map section of the dashboard:

<img src="https://i.imgur.com/ZNuBWNt.png" width=50%>

B. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I haven't ever installed a database, so this ended up being an interesting exercise that may have resulted in some mild anxiety! I chose PostgreSQL as I have experience with using it in both my current and my previous company. I found instructions on how to install it via aptget and that went smoothly. At first, Datadog's dashboard did not see it, so I tried out any kind of status check I could find to verify the connection. Eventually the dashboard showed it as an active and installed integration:

<img src="https://i.imgur.com/1bFs8nb.png" width=50%>


C. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. 

D. Change your check's collection interval so that it only submits the metric once every 45 seconds.

E. **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

My python skills are rudimentary, but I looked up examples on the <a href="https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#overview">Datadog page for creating a custom agent check.</a> I imported the Python random and Datadog checks libraries, and wrote a basic script (checks.d/my_metric.py) to report out on this custom metric including a sample tag:value pair for easy identificaiton within Datadog. The collection interval was set at 45 seconds in conf.d/my_metric.yaml, though it looks like it can also be edited on the front-end in the Metrics Summary page.

<img src="https://i.imgur.com/3Jx1CBE.png" width=50%>

## 2. Visualizing Data:

A. Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Using the instructions posted <a href="https://docs.datadoghq.com/getting_started/api/">here</a>, I imported the Datadog collection into Postman and set up the environment with my Datadog API and Application keys. I completed the full dashboard piecemeal by testing each metric visualization first, understanding what it was doing and how, and then combining them together into one <a href="https://p.datadoghq.com/sb/8a8s43cygzstwdcw-59659872326c732ad4eea553f2e4a8b4">dashboard</a> with the below request:

```json
{
    "title": "2 - Visualizing the Data",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric.count{*}"
                    }
                ],
                "title": "Average of My Metrics over host:vagrant"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:postgresql.rows_returned{*}, 'basic', 2)"
                    }
                ],
                "title": "Average PostgreSQL Rows Returned on host:vagrant with anomaly function"
            }
        },
        {
            "definition": {
                "type": "query_value",
                "requests": [
                    {
                        "q": "my_metric.count{*}.rollup(sum,3600)"
                    }
                ],
                "precision": 1,
                "title": "Rollup of My Metric returned on host:vagrant over the past hour"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "My metrics, reported!",
    "is_read_only": true,
    "notify_list": [
        "kevin.gurevich@gmail.com"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "vagrant"
        }
    ],
    "template_variable_presets": [
        {
            "name": "Saved views for hostname 2",
            "template_variables": [
                {
                    "name": "host",
                    "value": "<HOSTNAME_2>"
                }
            ]
        }
    ]
}
```

<a href="https://p.datadoghq.com/sb/8a8s43cygzstwdcw-59659872326c732ad4eea553f2e4a8b4" title="Click to see the dashboard"><img src="https://i.imgur.com/hVzm2jN.png" width=50%></a>

B. Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?

I set the dashboard timeframe to 5 minutes to drill into recent events, allowing me to find and highlight a dip in metrics, snapshot it, and send out an ad hoc notification using the UI's built-in commenting system.

The anomaly graph displays the number of rows returned in the instance of PostgreSQL running on my VM, enriched with basic anomaly detection, highlighting any activity that falls outside of 2 standard deviation levels of the normal threshold of activity.

<img src="https://i.imgur.com/DHvcX53.png" width=50%>

## 3. Monitoring Data

A. Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Now that I'm all setup collecting metrics, I want to make sure my imaginary devops team doesn't need to babysit this dashboard, so I created some alert and warning thresholds of 800 and 500 respectively, while also adding in alerting for whenever the data doesn't populate for more than 10 minutes.

<img src="https://i.imgur.com/LfWHuZs.png" width=50%>

B. Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Monitor notification email message setup including different messages for alerts, warnings, and no data, highlighting the host:

<img src="https://i.imgur.com/RHGG8l8.png" width=50%>

Monitor notification email test:

<img src="https://i.imgur.com/Q2t6SSx.png" width=50%>

C. **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F.

<img src="https://i.imgur.com/1RuSOtU.png" width=50%>

And one that silences it all day on Sat-Sun.

<img src="https://i.imgur.com/tuYEEvx.png" width=50%>

Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

<img src="https://i.imgur.com/mh33DTp.png" width=50%>

In further efforts to help out my imaginary devops team, I want to make sure they can create schedules of when team members receive alerts by adding scheduled downtimes on week nights and weekends, also including a sample of what that downtime notification looks like!


## 4. Collecting APM Data:

A. Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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

I prepared my environment to use the Flask app provided in the example, so I installed PIP, Flask, and ddtrace to my virtual machine. I decided to use ddtrace because it automatically parses and tracks the example Flask app.

```bash
vagrant@vagrant:~$ ddtrace-run python solutions_flaskapp.py
2020-05-10 21:42:15,185 DEBUG [ddtrace.internal.import_hooks] [import_hooks.py:136] - No hooks registered for module 'cli'
2020-05-10 21:42:15,185 - ddtrace.internal.import_hooks - DEBUG - No hooks registered for module 'cli'
 * Serving Flask app "solutions_flaskapp" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2020-05-10 21:42:15,189 INFO [werkzeug] [_internal.py:113] -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2020-05-10 21:42:15,189 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
```

I then used CURL to hit the endpoints several times to generate some sample APM data.

```bash
vagrant@vagrant:~$ curl 127.0.0.1:5050/api/trace
```

Once the data was in, I created a dashboard of some metrics to demonstrate a joint APM/Infrastructure monitoring dashboard. I used Flask's Hit Requests and Request Duration alongside the System CPU Usage and Unused Memory, and charted them over time to help illustrate the effects of higher usage on my system. You can find the dashboard <a href="https://p.datadoghq.com/sb/8a8s43cygzstwdcw-72477159821af6c64d8cba2a91c57c3d">here</a>, and a screenshot of it below. 

<img src="https://i.imgur.com/c6kms54.png" width=50% />


B. **Bonus Question**: What is the difference between a Service and a Resource?

Services are collections of resources for any kind of specific function, and can include endpoints, queries or jobs, for example, a group of URL endpoints can be grouped together under an API service, while a resource can be a specific API endpoint, query or job that make up the service. 

Using the API Endpoint service example, one specific endpoint is a resource, while the group of all related API endpoints would make up an API service.

## 5. Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


Datadog's monitoring capabilities could enable retailers, restaurants, and other publicly accessible spaces to track and enforce social distancing policies. There will likely be regulations on how many visitors can be present in a space at any given time, creating a potential use-case for a monitoring and alerting system that ensures social distancing compliance by tracking the number of visitors entering and exiting a space, and/or the number of visitors present at any given time.

Gathering data around physical traffic can be achieved with hardware solutions that control and monitor the ingress/egress of visitors, detect and measure mobile devices, or potentially use video/machine learning to identify visitors. Thresholds and alerting can be established based on prescribed capacity or population densities in a given space.

Such monitoring could help businesses ensure regulatory compliance and could be made publicly accessible so potential patrons could ascertain how busy a given location is. Businesses could also benefit from metrics around their visitors, such as frequency, duration, wait time, and peak times.
