## Questions

## Prerequisites - Setup the environment

I set up a Vagrant Ubuntu 12.04 VM, I signed up for Datadog as Guillaume Raimbault and I installed the Datadog Agent.
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/Vagrant_ubuntu_with_datadog.jpg">

<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/datadogAgentReporting.jpg" >

## Collecting Metrics:

* I added tags #region:europe, #town:sannois, #special_tag in etc/dd-agent/datadog.conf
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/tagInDatadogConf.jpg">
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/tagsInDatadogMap.jpg">

* I installed MySQL and the respective integration.
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/mysqlInstalled.jpg">
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/mysqlIntegrationWorking.jpg" width="500">
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/mysqlIntegration.png" width="200">
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/mysqlDashboard.jpg">

* I created a custom Agent check by creating /etc/dd-agent/checks.d/my_metric.py and /etc/dd-agent/conf.d/my_metric.yaml. The corresponding files are in folder <a href="https://github.com/gRaimbault/hiring-engineers/tree/solutions-engineer/code">code</a>.
* I changed the collection interval in my_metric.yaml .

* **Bonus Question** The only solution I found to modify the collection interval is by modifying the yaml files.

## Visualizing Data:

* I created the script timeboardCreation.py (in folder <a href="https://github.com/gRaimbault/hiring-engineers/tree/solutions-engineer/code">code</a>) to create the corresponding Timeboard.
<a href="https://app.datadoghq.com/dash/506051/my-timeboard-raimbault2?live=true&page=0&is_auto=false&from_ts=1516743656614&to_ts=1516747256614&tile_size=m">Dashboard link</a>

Once this is created, access the Dashboard from your Dashboard List in the UI:

* The minimum Timeboard's timeframe in the UI seems to be the past hour.
* Snapshot of the graph with the @ notation to sent it to myself:
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/graphSnapshot.jpg" >

* **Bonus Question**: The anomaly graph compare expected values to observed values in order to highlight anomalies.

## Monitoring Data

I created the corresponding metric monitor for my_metric:
<a href="https://app.datadoghq.com/monitors#3963666?group=all&live=4h">My Metric Monitor link</a>

* Warning threshold of 500 done.
* Alerting threshold of 800 done.
* Notification if there is No Data for this query over the past 10m done
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/myMetricMonitor.jpg">

* Send you an email whenever the monitor triggers. Done, see image below.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state. Done, see image below.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state. Done, see image below.
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/monitorMessage.jpg" >

* Email the monitor sent me:
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/monitorTriggered.jpg" >

* **Bonus Question**: 
    * Downtime that silences it from 7pm to 9am daily on M-F,
    <img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/weekDowntime.jpg" >
    
    * Downtime that silences it all day on Sat-Sun.
    <img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/weekEndDowntime.jpg" >
    
    * Email notifications screenshots: 
    <img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/monitorWeekDowntime.jpg" >
    <img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/monitorWeekEndDowntime.jpg" >
    


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
    app.run()
```    

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well. 

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


