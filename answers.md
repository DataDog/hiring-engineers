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
** Bonus Question: What is the difference between a Service and a Resource?

A services is a set of process that do the same thing over and over.  A Resource is an paticular action for a given service.

* Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/dashboard%20with%20apm%20and%20infrastructure%20graphs.png" width="800" height="332" alt="_DSC4652"></a>
<img src="http://480103081bda39217c58-f86642ef36cf4c67ddae8eac86589bac.r68.cf1.rackcdn.com/Running%20flask%20app%20with%20ddtrace-run%20.png" width="800" height="332" alt="_DSC4652"></a>

* Please include your fully instrumented app in your submission, as well.

** Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

* Is there anything creative you would use Datadog for?

Cryptopcurrency's and the blockchain are becoming more and more mainstream and the new buzz words in tech.  It has intrigued me ever since the bitcoin run on December 2017 when it almost hit the $20k price mark. I like to keep track of certain events to make sure that if for some reason I find a way to go back in time I will have a plan.  I think using Datadog to track my favorite crypto exchanges would be really cool. Most major exchanges provide API's into your accounts so having a  Datadog dashboard that could be a single source of truth could give someone the edge needed to stay on top of what's going on in the market.  This market does not sleep and there are huge fluctuations in price at any given moment.  Using features like anomaly monitoring I can see this helping identify changes that may be going on or pointing out things that are starting to happen.  I have found myself prematurely changing my position in certain coins because of events that happen organically, not out of the norm.  I can see using timeboards to correlate social media post and actions taking place on an exchange to possibly help identify more of the shady practices like a pump and dump scenario.  I think the possibilities are endless with what you could track in this wild west crypto market, and who knows maybe it will help someone not miss the bus on the next crypto run to the moon.

Dashboard link: https://app.datadoghq.com/dashboard/nvb-98w-x5v/challange-dashboard?tile_size=s&page=0&is_auto=false&from_ts=1553612940000&to_ts=1553613840000&live=true

** Final Thoughts

What a cool exercise you all came up with,  hands-on experience is the best way to learn and retain information at least in my experience.  Using git for administering and tracking the exercise was a brilliant idea.  It was fun and I learned a lot and I have a feeling it did not scratch the surface on Datadogs capabilities.  Hopefully, I will get to dig deeper into the tech and join this innovate team on their inspiring mission.

Thank you 
Shawn Terrell "Squirrel" 
