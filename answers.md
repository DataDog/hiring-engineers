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

I instrumented the Flask app given with Datadog's APM solution. The corresponding code my_app.py is in the folder <a href="https://github.com/gRaimbault/hiring-engineers/tree/solutions-engineer/code">code</a>.

* **Bonus Question**: What is the difference between a Service and a Resource?

<a href="https://app.datadoghq.com/dash/510818/apm--infrastructure?live=true&page=0&is_auto=false&from_ts=1516801159319&to_ts=1516804759319&tile_size=m">APM and Infrastructure Metrics Dashboard link</a> and screenshot:
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/apmInfrastructureDashboard.jpg" >
 

## Final Question:

Is there anything creative you would use Datadog for?
It could be possible to use Datadog to monitor traffic jam in Paris, or to monitor air pollution in different locations, or to monitor parking places around some location.


