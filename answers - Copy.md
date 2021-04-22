If you want to apply as a Solutions or Sales Engineer at [Datadog](http://datadog.com) you are in the right spot. Read on, it's fun, I promise.


<a href="https://www.datadoghq.com/careers/" title="Careers at Datadog">
<img src="https://imgix.datadoghq.com/img/careers/careers_photos_overview.jpg" width="1000" height="332"></a>

## The Exercise

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Once this is ready, sign up for a trial Datadog at https://www.datadoghq.com/

**Please make sure to use “Datadog Recruiting Candidate” in [the “Company” field](https://a.cl.ly/wbuPdEBy)**

Then, get the Agent reporting metrics from your local machine and move on to the next section...



I created an ec2 instance in my account, for now I will use a t2.micro, if I find that later steps demand more, I will resize the instance.

I installed the datadog client, and 
![image](images/installed-agent.PNG?raw=true "Installed Agent")

during the startup processs, I saw the filename  "/etc/datadog-agent" so I would assume this is the config file, a quick google search confirmed this.





## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

running a "grep" command, allowed me to find that there was infact a direct mention of "tags" within this file, and as such, I have created 3 tags as follows:


![image](images/tags.PNG?raw=true "Tags")

**one thing to note, I had to stop here for 2 days to move house, I am currently trying to troubleshoot getting the client to publish metrics once again as my instance was stop-started, these steps may give some insight into the troubleshooting steps I have followed**

I checked the outbound SG on my instance, and could see that all outbound traffic was allowed. As SGs are stateful,I do not need to open inbound traffic (unlike ACLs).

I searched online and found the doc:

https://docs.datadoghq.com/agent/troubleshooting/

when first thing to check per the doc was my API-key. When checking the datadog config file, the API key was the same. 

I restarted the datadog client to ensure it was up and sending traffic (should have checked top before hand to confirm if it was running).

this did not work^^ as such, I am trying to find the status of the agent on the instance.

I found the doc here https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7 outlining how to check the status
running the command :

sudo service datadog-agent status

and see the following information:

![image](images/broken.PNG?raw=true "Broken")

My guess is that there is a small difference in the datadog.yaml vs the default (which I found datadog provides here https://raw.githubusercontent.com/DataDog/datadog-agent/master/pkg/config/config_template.yaml)

as such, I will compare the two files to see that is different

Two files look Identical, in almost all parts

![image](images/diff.PNG?raw=true "Diff")

found the agent logs are contained in "/var/log/datadog/agent.log"

66: did not find expected '-' indicator
2021-04-19 22:21:51 UTC | CORE | INFO | (pkg/logs/logs.go:162 in Stop) | Stopping logs-agent
2021-04-19 22:21:51 UTC | CORE | INFO | (pkg/logs/logs.go:174 in Stop) | logs-agent stopped
2021-04-19 22:21:51 UTC | CORE | INFO | (cmd/agent/app/run.go:466 in StopAgent) | See ya!
2021-04-19 22:21:52 UTC | CORE | INFO | (pkg/util/log/log.go:526 in func1) | runtime: final GOMAXPROCS value is: 1
2021-04-19 22:21:52 UTC | CORE | WARN | (pkg/util/log/log.go:541 in func1) | Error loading config: While parsing config: yaml: line 66: did not find expected '-' indicator
2021-04-19 22:21:52 UTC | CORE | ERROR | (cmd/agent/app/run.go:234 in StartAgent) | Failed to setup config unable to load Datadog config file: While parsing config: yaml: line 

is contained in the logs, checking to see what is on line 66

line 66 contains "tags"

checking compared to the github example, I cannot see a "-" in either, perhaps it is a missing space?

Will test and try again

did not work, I changed 

datadog.yaml.example to contain the same information, and a comparison looks as follows:

![image](images/replacing-config.PNG?raw=true "replacing-config")


based on the error changing from:

66: did not find expected '-' indicator

to

65: did not find expected key

my guess is that it is to do with spacing

changed spacing from

```
 tags:
   - environment:dev
   - 12456:23456
```
to 
```
tags:
 - environment:dev
 - 12456:23456
```
and it worked! not sure why this change broke my config if it was set up this way previously

I can now see my tags created correctly within the datadog console:

![image](images/tags2.PNG?raw=true "tags2")





* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.


running the command sudo apt install mysql-server I was able to walk through the steps to create my database, including setting a master password etc.:

![image](images/database.PNG?raw=true "database")

found the steps to integrate mysql here
: https://app.datadoghq.eu/account/settings#integrations/mysql

After following these steps, I ran some basic queries against the database:


![image](images/databaseQueries.PNG?raw=true "databaseQueries")




* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?

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

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

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

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)