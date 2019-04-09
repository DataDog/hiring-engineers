# Jim Gallagher Hiring Exercise


Datadog Team,

I want to first thank you for the opportunity to complete the hiring exercise as well as give kudos - out of the myriad of these that I have done over my career this one was actually enjoyable and felt valuable. As I go through and provide answers I'll also attempt to show my thought process, for better or worse. I'll highlight the questions as they come up and answer inline, adding any challenges I encountered along the way.

## Pre-reqs

I took the advice of the guide and went with an Ubuntu 16.04 Vagrant box. Not shown: where I install Vagrant but forget about Virtualbox and wonder why my VM won't boot...! Off to a great start. 

I was glad to see the agent installation steps were broken out as I am always a bit leary of [piping scripts to my shell.](https://www.seancassidy.me/dont-pipe-to-your-shell.html)

![Much appreciated](https://s3.us-east-2.amazonaws.com/jim-dd/install-instructions.png)

## Collecting Metrics

> _Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog._

From my `/etc/datadog-agent/datadog.yaml`
```bash
# Set the host's tags (optional)
tags:
 - jims_rad_tag
 - env:test
 - role:mysql
 ```

![Host Tags](https://s3.us-east-2.amazonaws.com/jim-dd/host-tags.png)

I accidentally left leading spaces when uncommenting out the tags section in the config file and got some parsing errors, which I was able to figure out by using `datadog-agent` and its subcommands.

![Parse Error](https://s3.us-east-2.amazonaws.com/jim-dd/parse-error.png)

> _Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database._

 I went with [MySQL](https://help.ubuntu.com/lts/serverguide/mysql.html.en) (as a fan of the classics). Following the [configuration instructions](https://docs.datadoghq.com/integrations/mysql/) from the documentation was straightforward, although I must have hit a `:q!` in Vim without saving my changes in `/etc/datadog-agent/conf.d/mysql.d/conf.yaml`. Once I went to restart the agent and do a `datadog-agent configcheck` it gave me some missing parameters errors, which made sense since it using the defaults from `conf.yaml.example`. 

![MySQL Error](https://s3.us-east-2.amazonaws.com/jim-dd/mysql-error.png)

> _Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000._

 For a second there I _almost_ just picked a random number myself. Luckily, it's simple to [generate random numbers in python](https://docs.python.org/3/library/random.html). Following good naming hygiene according to the [custom check documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) I named my file `custom_jim.py`: 


 ```python
import random

# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "0.0.1b"


class JimCheck(AgentCheck):
    def check(self, instance):
        self.gauge('custom.my_metric', random.randint(0,1000))
```
At first I could not figure out how to get rid of "no_namespace" for `my_metric` on the Host Map GUI, which didn't look "clean" to me. I realized that I could leverage the pseudo-hierarchical dotted format and settled on `custom.my_metric`, to fit the naming scheme so far.

>_Change your check's collection interval so that it only submits the metric once every 45 seconds._

Using the [custom check documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval), I created `/etc/datadog-agent/conf.d/custom_jim.yaml` with the following: 

```python
init_config:

instances:
  - min_collection_interval: 45
```



>_**Bonus Question:** Can you change the collection interval without modifying the Python check file you created?_

I will admit to being confused by this bonus question because its clear from the docs that to change the collection interval you do it via the YAML configuration file (`custom_jim.yaml`) as shown above, *not* the Python check file (`custom_jim.py`). I wasn't sure how you could change it in the Python check file at all - but I did dig into the source a bit and see that the [collection interval is part of the base AgentCheck class](https://github.com/DataDog/dd-agent/blob/da02e5f01b030d2c1cd6682a37eb4f474d6d003d/checks/__init__.py#L337-L338), so it seems to be possible. 

It also appears that the default collection interval of 15 seconds is [coded into the agent's source](https://github.com/DataDog/datadog-agent/blob/33db6c888082da73e04a7d344b9c78ee3a72371d/pkg/collector/check/check.go), so I suppose one could change the default in the source and compile your own agent as another way of changing the collection interval (and my official answer to the bonus question).

## Visualizing Data

> _Utilize the Datadog API to create a Timeboard that contains:_
> 
> * _Your custom metric scoped over your host._
> *  _Any metric from the Integration on your Database with the anomaly function applied._
> * _Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket_
> 
> _Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard._

Here is the shell script I used to create the Timeboard. I didn't find out about `dogshell` until after I finished the exercise, or else I may have used that!

`$ cat create_timeboard.sh`
```bash
#!/bin/bash

api_key=5efc746f0ec0e3d2a250d0684a4eeb3b
app_key=9ad728e08a2e484825699a7332e7b724563d8ddf


curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "My custom dashboard with LOG y-scale",
      "widgets" : [{
          "definition": {
              "type": "timeseries",
              "requests": [
              {"q": "avg:custom.my_metric{host:jimbuntu}"},
              {"q": "avg:custom.my_metric{*}.rollup(sum, 3600)"},
		      {"q": "anomalies(avg:mysql.performance.user_time{*}, "basic", 2)"}
              ],
              "yaxis": { "scale": "log"}
          }
      }],
      "layout_type": "ordered"
}' \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"
```
> Set the Timeboard's timeframe to the past 5 minutes and take a snapshot of this graph and use the @ notation to send it to yourself.

![5minat](https://s3.us-east-2.amazonaws.com/jim-dd/5mintag.png)

It was really handy to have the JSON output from the GUI to come up with the appropriate API payload. One thing I did was change the y-axis scale to logarithmic in order to have my three metrics show something on the timeboard since they're multiple orders of magnitude apart. 

![Nice](https://s3.us-east-2.amazonaws.com/jim-dd/nice.png)

> _**Bonus Question:** What is the Anomaly graph displaying?_

The anomaly graph uses some clever statistics to highlight any derivations from what it considers normal, given past data. In my case I am highlighting the MySQL performance. To get something interesting on the graph I ran a script to query my DB a bit. 

```bash
for i in {1..100}; do mysql -u root -proot -D mysql -e "SELECT * FROM Users"; done
```
And behold, an anomaly! 
![MySQL blip](https://s3.us-east-2.amazonaws.com/jim-dd/mysql-graph.png)


## Monitoring Data
> _Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes: 800 alert, 500 warn, and 10m of no data._
> _Please configure the monitor’s message so that it will send an email, create different messages based on whether the monitor is in an Alert, Warning, or No Data state, and include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state._

Configuring the monitor:

![Monitor Definition](https://s3.us-east-2.amazonaws.com/jim-dd/monitor-definition.png)


My monitor's message: 
```
{{#is_alert}}ALERT: My metric has averaged {{value}} for the past 5 minutes on {{host.ip}} {{/is_alert}} 
{{#is_warning}}WARNING: My metric has averaged over 500 for the past 5 minutes. {{/is_warning}} 
{{#is_no_data}}No data has been reported by My metric in over 10 minutes. {{/is_no_data}}  
@jim011235813@gmail.com
```

> _When this monitor sends you an email notification, take a screenshot of the email that it sends you._

An example warning message:
![Email from Monitor](https://s3.us-east-2.amazonaws.com/jim-dd/monitor-email.png)

> _**Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor and take a screenshot of that notification email._

An example downtime notification:

![Downtime](https://s3.us-east-2.amazonaws.com/jim-dd/downtime.png)

## Collecting APM data

> _Given the following Flask app, instrument this using Datadog’s APM solution._

Here I took the approach of setting up Flask, and then launching the included app (`flaskapp.py`) from the command line with `ddtrace-run` prepended. I also took the liberty of scripting a few hundred `GET /` requests against the app so APM would have something to trace.

At the shell: 

```bash
$ pip install ddtrace
$ pip install flask
$ export FLASK_APP=flaskapp.py
$ ddtrace-run python -m flask run flaskapp.py &
$ for i in {1..300); do curl -s localhost:5050/; done
```

> _**Bonus Question:** What is the difference between a Service and a Resource?_

A service is a process or collection of processes that do a specific task, such as a frontend, webapp, or database. A resource is a particular action a service is doing. In the case of a webapp it might be an individual endpoint (e.g. /login, /cart/checkout, etc.) or for a database a specific query. In our case the service would be our Flask app, and a resource could be the `/` endpoint.

> _Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics._

Here I created a [Dashboard](https://p.datadoghq.com/sb/nlkqvg6rbbnue0yp-55a032abe2e58fd474b6e29e419be5fd) that shows the total number of hits traced on our Flask app next to the sum of all collections on My Metric. 

![Screenboard](https://s3.us-east-2.amazonaws.com/jim-dd/screenboard.png)

## Final Question
> Is there anything creative you would use Datadog for?

A few ideas that spring to mind: 

One of my passions in life is the guitar, which much to my wife's chagrin has included collecting instruments. One of the greatest stores on earth, the [Chicago Music Exchange](https://www.chicagomusicexchange.com/), had the good sense to create an app named [Reverb](http://reverb.com) that acts as a portal for both stores and individuals to buy/sell musical equipment (and CME being the geniuses they are get a cut of every transaction). As much as I enjoy ~~wasting~~ spending quality time scrolling through my Reverb feed, there is an API. With this API, a simple app could scrape data to feed into Datadog, at which point the possibilities are endless. Anomaly functions here could be very useful for finding both well priced deals or extremely rare pieces. 

For something a little more broadly applicable, governments and research organizations around the world provide a [number of open data sources](https://www.data.gov/open-gov/) for things like weather, seismic activity, sea levels, etc. I could envision a number of useful monitors and alerts based on this data such as warnings around increased seismic activity, changing ocean temperatures, or other anomalous activity. 



## Thank you

Thank you again for the opportunity to complete the exercise, I found it extremely rewarding. 
