Your answers to the questions go here.

## Prerequisites - Setup the environment

The environment I initialized was a RedHat 8. The virtual machine is on my local home network on an ESXi Hypervisor.

## Collecting Metrics:

Q. * Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
A. Inside of datadog.yaml file I created the tag "environment:dev". Tags allows us to filter machines in our environment. This allows us to group machines together and to look at any specific set of machines with the same tags. 

[Tags1.png]
[Tags2.png]

Q. * Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
A. I have installed MySql database. The integration for MySQL was also added to the datadog dashboard. Performance Metrics were also enabled and collecting data.
[DatabaseSystemd.png]
[MySQLIntegration.png]

Q. * Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
A. I created a python file called my_metric.py using the reference below. This was then placed inside the checks.d folder. 
I then created a file called my_metrics.yaml inside of the conf.d folder. The below code was used.

my_metric.py:
=============
from random import randint
from checks import AgentCheck
class my_metrics(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
		
my_metric.yaml:
===============
init_config:

instances:
  [{
      min_collection_interval: 45
  }]
  
ref=https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6

Q. * Change your check's collection interval so that it only submits the metric once every 45 seconds.
A. In order to change the metric interval I used the "min_collection_interval: 45" in the my_metric.yaml. 

Q. * **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
A. The collection interval was changed inside the my_metric.yaml as show above.

## Visualizing Data:

Q. Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

A. The Dashboard was created using the below POST Request via Postman.

{ 
   "title":"API Dashboard",
   "description":"",
   "widgets":[ 
      { 
         
         "definition":{ 
            "type":"timeseries",
            "requests":[ 
               { 
                  "q":"sum:my_metric{host:datadog.rhel8}",
                  "display_type":"line",
                  "style":{ 
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "title":"Sum of my_metric over host:datadog.rhel8"
         }
      },
      { 
         
         "definition":{ 
            "type":"timeseries",
            "requests":[ 
               { 
                  "q":"anomalies(avg:mysql.performance.cpu_time{host:datadog.rhel8}, 'basic', 2)",
                  "display_type":"line",
                  "style":{ 
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "title":"Avg of mysql.performance.cpu_time over host:datadog.rhel8"
         }
      },
      { 
         
         "definition":{ 
            "type":"timeseries",
            "requests":[ 
               { 
                  "q":"avg:my_metric{host:datadog.rhel8}.rollup(sum, 3600)",
                  "display_type":"line",
                  "style":{ 
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "title":"Rollup of my_metric - 1 hour"
         }
      }
   ],
   "template_variables":[ 
      { 
         "name":"var",
         "default":"*",
         "prefix":null
      }
   ],
   "layout_type":"ordered",
   "is_read_only":false,
   "notify_list":[ 

   ]
}
[postman.png]
[ApiDashboard.png]

Once this is created, access the Dashboard from your Dashboard List in the UI:

Q. * Set the Timeboard's timeframe to the past 5 minutes
A. I have selected on the Widget the past 5 minutes for my_metric, then selecting Annotate this graph.

[5MinAnnotate.png]

Q.* Take a snapshot of this graph and use the @ notation to send it to yourself.
A. To send the graph using the @ notation the process is as above, by selecting "Annotate this graph". The 5MinAnnotate.png screenshot illustrates how the metric is sent.

* **Bonus Question**: What is the Anomaly graph displaying?
The Anomaly graph will highlight if the current data is behaving differently based on historical trends.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

[ThresholdMonitor.png]

Q. Please configure the monitor’s message so that it will:
A. In order to create the monitoring message, we modify the "Say what's happening" on Step4. This is illustrated in the ThresholdMonitorEmails.png screenshot. 

{{#is_alert}} My Metric is above {{value}} on {{host.ip}} {{/is_alert}}
{{#is_warning}} My Metric is in warning state {{value}} {{/is_warning}}
{{#is_no_data}} My Metric has no data {{value}} {{/is_no_data}}

@philipbrophy@gmail.com

[ThresholdMonitorEmails.png]

Q. * Send you an email whenever the monitor triggers.
A. The email is sent using the @ notation. This is done at Step 5 "Notify your team".

Q. * Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
A. Using the format above, would send an email based on an alert, warning or not data.
[ThresholdMonitorEmails.png]

Q. * Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
A. The metric value is held in the reserve variable {{value}}.
[ThresholdMonitorEmails.png]

Q. * When this monitor sends you an email notification, take a screenshot of the email that it sends you.
A. [AlertInbox.png]

Q. * **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

A. In order to schedule downtimes I clicked into manage Downtime under the monitors. From here I schedule a downtime as seen per the screenshots.
[MonitorScheduleDaily.png]
[MonitorScheduleWeekend.png]

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

A. I started the flask application via "ddtrace-run python3 flask_app.py" command. 
[ddtraceFlask.png]

Q. * **Bonus Question**: What is the difference between a Service and a Resource?
A. A Service is a set of processes that do the same job like a database service. A resource is an action that is taken on a Service. For example a "SELECT * FROM users;" on a database.

Q. Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
A. In this dashboard I just did a simple CPU time vs HTTP 200 requests.
https://p.datadoghq.com/sb/gi624z8qfxllgtyd-86665e10ec28ef4466c49468b918136e

[APMGraph.png]

Please include your fully instrumented app in your submission, as well.
A. App attached. I have changed the host from 0.0.0.0 to my internal ip, to tell it to only listen on that. The graph public IP URL is as per above.

[root@datadog admin]# cat flask_app.py
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
    app.run(host='192.168.1.6', port='5050')
[root@datadog admin]#


## Final Question:

Q. Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?

A. I am very impressed  with the Datadog graphing technology and algorithms. One area that I can see where this could be used is in the analysis of network data trending with Cisco or Juniper devices. For example, when there is a spike in network data on an interface, it is not obvious if this is due to an interface going down and traffic been switched to it, or if it just a normal high load for that time of the day. With Datadog anomaly algorithms you would be able to very quickly see if the spike is a historical trend or if it is a new issue. Layer2/3 monitoring of networking devices.

