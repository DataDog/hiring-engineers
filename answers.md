Your answers to the questions go here.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/config%20file%20tag%20add.png" width="800" height="332" alt="_DSC4652"></a>
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Answer%201.png" width="800" height="332" alt="_DSC4652"></a>
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/installing%20mysql%20history.png" width="800" height="332" alt="_DSC4652"></a>
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/mysql%20integratin%20installed.png" width="800" height="332" alt="_DSC4652"></a>
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Metric%20Name%20my_metric.png" width="800" height="332" alt="_DSC4652"></a>
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Change%20collection%20time%20to%2045.png" width="800" height="332" alt="_DSC4652"></a>
**  Bonus Question Can you change the collection interval without modifying the Python check file you created?
Looks like you can change from portal.
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Bonus%20Answer%20question%201.png" width="800" height="332" alt="_DSC4652"></a>
* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Rollup%20sum-custom%20metric-anom.png" width="800" height="332" alt="_DSC4652"></a>
Python code to create and answer timeboard question.
from datadog import initialize, api

options = {
    'api_key': '0cd542dc44bea92cdd5cd0a6ceb535b7',
    'app_key': 'd8b672bec1750306941687fab943563f4443d0f0'
}

initialize(**options)

title = 'Challange Dashboard'
widgets = [
    {"definition": {
      "type": "timeseries",
      "requests": [
        {"q": "avg:my_metric{host:data-dog-test}"}
      ],
      "title": "My_Metric Info"
    }},
    {"definition": {
      "type": "timeseries",
      "requests": [
        {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
      ],
      "title": "Anomaly graph for mysql performance cpu"
    }},
    {"definition": {
      "type": "timeseries",
      "requests": [
        {"q": "avg:my_metric{host:data-dog-test}.rollup(sum, 3600)"}
      ],
      "title": "My_Metric rollup sum Info"
    }}
   ]
layout_type = 'ordered'
description = '.'
is_read_only = True
notify_list = ['shterrel@gmail.com']
template_variables = [{
    'name': 'datadog-test',
    'prefix': 'host',
    'default': 'data-dog-test'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
                    
* Set the Timeboard's timeframe to the past 5 minutes
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/timebord%205min%20screen%20interval.png" width="800" height="332" alt="_DSC4652"></a>

* Take a snapshot of this graph and use the @ notation to send it to yourself. 
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/snapshot%20taken%20and%20sent.png" width="800" height="332" alt="_DSC4652"></a>

** Bonus Question: What is the Anomaly graph displaying?

Its using data to keep track of whats normal in its opinion bassed off the prior data.  The more data the better the algorithm can identify things that are not normal.  This specif graph is looking at mysql cpu performance and bassed off of how its has been running in the past it can identify things out of the ordinary.  
Send you an email whenever the monitor triggers.

* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Warning%20email.png" width="800" height="332" alt="_DSC4652"></a>
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Triggered%20email.png" width="800" height="332" alt="_DSC4652"></a>
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/No%20data%20email.png" width="800" height="332" alt="_DSC4652"></a>

** Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

* One that silences it from 7pm to 9am daily on M-F,
* And one that silences it all day on Sat-Sun.
* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Saturday%20and%20Sunday%20downtime%20schedule.png" width="800" height="332" alt="_DSC4652"></a>
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/scheduled%20downtime%20%20mon%20-%20friday%20evening.png" width="800" height="332" alt="_DSC4652"></a>

