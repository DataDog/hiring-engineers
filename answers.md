## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

**Answer:**    
I created a VM on alibaba cloud with CentOS7.6 and signed up a new Datadog account for 15 days trial.
[root@dgtest ~]# uname -a
Linux dgtest 3.10.0-957.1.3.el7.x86_64 #1 SMP Thu Nov 29 14:49:43 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux


## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.  

**Answer:**  
Add hostname tag in /etc/datadog-agent/datadog.yaml like this
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-22%2014.44.16.png)
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/14_59_35__02_22_2019.jpg)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.  
**Answer:**  
Installed MySQL 5.7.25 and installed Datadog integration for this DB
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/15_02_01__02_22_2019.jpg)
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-22%2015.47.44.png)
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-22%2015.34.32.png)
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/15_35_18__02_22_2019.jpg)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.  
**Answer:**  
Created a custom Agent check as below and run it
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-22%2015.32.49.png)
![]()

* Change your check's collection interval so that it only submits the metric once every 45 seconds.  
**Answer:** used "min_collection_interval: 45" options to collect metric once every 45 seconds
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-22%2015.48.59.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?  
**Answer:**   
Use "min_collection_interval: 45" options in conf.d/wangzz_my_metric.yaml. Same as last question

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.  
**Answer:**  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-22%2018.13.47.png)

* Any metric from the Integration on your Database with the anomaly function applied  
**Answer:**  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-22%2018.14.25.png)

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket  
**Answer:**  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-22%2018.14.10.png)  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/18_15_29__02_22_2019.jpg)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes  
**Answer:**  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2013.50.04.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.  
**Answer:**  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2013.50.24.png)

* **Bonus Question**: What is the Anomaly graph displaying?  
**Answer:**  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2013.51.09.png)


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

**Answer:**  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/screencapture-app-datadoghq-monitors-2019-02-25-14_00_01.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.  
**Answer:**  
Alert email:
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2014.03.58.png)

Warning email:
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2014.02.55.png)


* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

**Answer:**  
Monitor downtime configuration
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2014.45.38.png)

![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2014.46.08.png)

![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2014.46.28.png)

Downtime started message:  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2014.53.05.png)

Downtime end message:  
![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202019-02-25%2014.53.14.png)

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
**Answer**  
Service is a set of processes that do the same job. In this sample, webapp is one service.  
Resource is a particular action for a service. In this sample,  
"/","/api/trace","/api/apm" are three resources for the webapp service.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.  
**Answer**  
https://app.datadoghq.com/dashboard/wfb-4us-2e9/apm?tile_size=m&page=0&is_auto=false&from_ts=1551089310000&to_ts=1551090210000&live=true

![](https://github.com/wangzhizheng/hiring-engineers/blob/solutions-engineer/screenshot/screencapture-app-datadoghq-dashboard-wfb-4us-2e9-apm-2019-02-25-19_35_11.png)

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?  
**Answer:**  
I think Datadog can be used in any place with data there.
Maybe I will use Datadog for monitoring stock changing, my game score or some of my sales data.