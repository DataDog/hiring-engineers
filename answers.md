If you want to apply as a solutions engineer at [Datadog](http://datadog.com) you are in the right spot. Read on, it's fun, I promise.

<a href="http://www.flickr.com/photos/alq666/10125225186/" title="The view from our roofdeck">
<img src="http://farm6.staticflickr.com/5497/10125225186_825bfdb929.jpg" width="500" height="332" alt="_DSC4652"></a>

## The Exercise

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

#### - [x] You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.

> Since I was unfamiliar with linux or using a virtual machine, I read through the [Vagrant documentation] (https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) and after watching some YouTube videos, I attempted to make sense of everything and downloaded Vagrant, VirtualBox and Ubuntu 18.04 LTS and followed the [tutorial](https://www.youtube.com/watch?v=3AnlvTgsoYM&t=175s) to start the VM. 

> I created a Vagrantfile, which is a config file written in Ruby, which configures and provisions the VM.  
> 
> ![vagrantfile](http://res.cloudinary.com/themostcommon/image/upload/v1535493899/Screen%20Shots/SS%20vagrantfile.png)
> 
> From the command line within the  folder with the Vagrantfile, I ran 

> ```$ vagrant up```

> This configured the VM with Ubuntu 
> 
![Ubuntu success](https://res.cloudinary.com/themostcommon/image/upload/v1535486511/Screen%20Shots/SS_Ubunut_success_message.png)
> And then to get inside the VM
> 
> ```$ vagrant ssh```


#### - [x] Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

> The process for signing up for Datadog is painless and the instructions were very clear. Once I started my 14-day free trial, I was able to choose Ubunutu for my operating system and the command was a simple copy and paste to start downloading the Agent. The script even included my API key

> ```DD_API_KEY=8<API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"```
> 
> ![agent running](https://res.cloudinary.com/themostcommon/image/upload/v1535486511/Screen%20Shots/SS_DD_Agent_running.png)


## Collecting Metrics:

#### - [x] Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

> To create tags in the Datadog Agent v.6 configuration file, I had to locate the
> 
> ```/etc/datadog-agent/datadog.yaml```
>
> Since I didn’t have a text editor to update the yaml file, I discovered and installed Emacs in Linux. 
>
>```sudo apt-get install emacs```
>
> Once installed, it should be as simple as typing 
>
> ```emacs <file to be edited> ```
>
> And the terminal has become an editor BUT the file was *“not readable”*. In order to edit the file, it has to be closed and reopened with 
>
> ```sudo emacs /etc/datadog-agent/datadog.yaml```
>
> Following the [tagging documentation] (https://docs.datadoghq.com/tagging/assigning_tags/#assigning-tags-using-the-configuration-files), I added these basic tags to the 
> 
> ![host tags](https://res.cloudinary.com/themostcommon/image/upload/v1535486510/Screen%20Shots/SS_Host_Tags_yaml.png)
> 
I have only used templates to create YAML files, so I referenced this [Github] (https://github.com/Animosity/CraftIRC/wiki/Complete-idiot%27s-introduction-to-yaml) to make sure that I was keeping the correct syntax. A valuable lesson I learned was that most of the configuration file is commented out with “#” leading the line so the # needs to be removed for the changes to be read. 

> To save the changes with emacs, (Mac: control = ^) 
> 
> ```^-x, ^-s``` 
> 
> At the bottom of the screen, you will see: 
> ```Wrote /etc/datadog-agent/datadog.yaml```
> 
> Then to close the document 
> 
> ```^-x, ^-c```
> 
> 
> At first, I assumed I could see the tag updates after a browser refresh, but they never appeared. And then I saw this note:
> 
> ![no agent responding](https://res.cloudinary.com/themostcommon/image/upload/v1535486510/Screen%20Shots/SS_No_Agent_Reporting.png)
> 
> After reading the docs some more, I thought I needed to change the process_config so it would also collect containers and processes.
> 
> ![process config](https://res.cloudinary.com/themostcommon/image/upload/v1535486510/Screen%20Shots/SS_Process_config.png)
> 
> And after updating the config file, I got a new error. 
> 
> ![NTP error](https://res.cloudinary.com/themostcommon/image/upload/v1535486510/Screen%20Shots/SS_NTP_Error.png)
> 
> After reading the docs on NTP and how to correct this issue, I discovered I had a syntax error in the yaml config file. And after correcting it, the warnings disappeared but I still had no tags. 
> 
> I was unsure what to do next, so I stopped Datadog service: 
> 
> ```sudo service datadog-agent stop```
> 
> And then restarted it 
> 
> ```sudo service datadog-agent restart```
> 
> On the Datadog UI, I went to Infrastructure > Host Map > jamessmith-solutions-engineer and voila, the tags were there!
> 
> ![host tags](https://res.cloudinary.com/themostcommon/image/upload/v1535498152/Screen%20Shots/SS_Host_with_Tags.png)
> ![host tag closeup](https://res.cloudinary.com/themostcommon/image/upload/v1535497900/Screen%20Shots/SS_Host_tag_closeup.png)




#### - [x] Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

> Since I am most familiar with PostgreSQL, I downloaded it. 
> 
>     sudo apt update
> 
>     sudo apt install postgresql postgresql-contrib
>
> Integrating Postgres [instructions](https://app.datadoghq.com/account/settings) begins by creating a role for Datadog. 
> 
> ![dd role creation](https://res.cloudinary.com/themostcommon/image/upload/v1535542971/Screen%20Shots/SS_postgres_connect_to_DD.png)
> 
> According to the directions, 
> 
>     Configure the Agent to connect to the PostgreSQL server 
>     Edit conf.d/postgres.yaml
>  
> I looked in the `datadog-agent/conf.d` directory but did not find a file by that name to edit, so I looked in the` postgres.d` directory and found the `conf.yaml.example `. After editing the file, I saved it and restarted the Agent and it *did not connect* to Postgres. 
> 
> Looking at the instructions, I realized the file I was supposed to edit was supposed to be the conf.d directory and not buried further down. As such, I created the file and added the configurations to the `conf.d` directory.
> 
> ![postgre yaml](https://res.cloudinary.com/themostcommon/image/upload/v1535542971/Screen%20Shots/SS_postgres_yaml.png)
> 
> I saved and closed the file. 
> 
> ```Wrote /etc/datadog-agent/conf.d/postgres.yaml```
> 
> And ran the `info command` which was confusing but was able to figure out that it was actually the status command 
> 
> ```sudo datadog-agent status```
> 
> I was happily greeted with success. 
> 
> ![postgres success](https://res.cloudinary.com/themostcommon/image/upload/v1535542971/Screen%20Shots/SS_postgres_running.png)
> 
- [x] Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

> The process to create a custom check involves creating 2 files
> 
*   a config yaml file in the `conf.d` directory
*   a python file in the `checks.d` directory

> To create a random value, I referenced this [tutorial](https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/) and created the files. 
> 
> ![randomvalue.py](https://res.cloudinary.com/themostcommon/image/upload/v1535560590/Screen%20Shots/SS_check_random_py.png)
> ![randvalue.yaml](https://res.cloudinary.com/themostcommon/image/upload/v1535560590/Screen%20Shots/SS_check_initial_config.png)

#### - [x] Change your check's collection interval so that it only submits the metric once every 45 seconds.

> To change the collection interval, I needed to update the randomvalue.yaml file with a min_collection_interval within the `instance` section 
> 
> ![checkvalue interval yaml](https://res.cloudinary.com/themostcommon/image/upload/v1535560590/Screen%20Shots/SS_check_interval_config.png)
> 
> Running the run check command 
> ```sudo -u dd-agent -- datadog-agent check <check_name>```
> ![check run](https://res.cloudinary.com/themostcommon/image/upload/v1535560590/Screen%20Shots/SS_check_running.png)
> 
> And according to the [documention](https://docs.datadoghq.com/agent/faq/agent-commands/#agent-information)
> 
> 	"On Agent v6, a properly configured integration will be displayed under “Running Checks” with no warnings or errors, as seen below:"
> 
	Running Checks
	==============
	network (1.6.0)
	---------------
      Total Runs: 5
      Metric Samples: 26, Total: 130
      Events: 0, Total: 0
      Service Checks: 0, Total: 0
      Average Execution Time : 0ms
> 
> My output did not produce errors or warnings: 
> 
>     network (1.6.0)
	---------------
	Total Runs: 78
	Metric Samples: 26, Total: 2028
	Events: 0, Total: 0
	Service Checks: 0, Total: 0
	Average Execution Time : 0ms* 
     

> [View Host Map](https://app.datadoghq.com/infrastructure/map?host=571252200&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)
> 
      
**Bonus Question** Can you change the collection interval without modifying the Python check file you created?

> I actually updated the collection interval in the config file so, yes, you can! 
> 

## Visualizing Data:

#### Utilize the Datadog API to create a Timeboard that contains:

#### - [x] Your custom metric scoped over your host.
#### - [x] Any metric from the Integration on your Database with the anomaly function applied.
#### - [x] Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

> Initially, I used the Ruby integration to write the code for creating the timeboard. Reading through the [Ruby Client for Datadog API](https://github.com/DataDog/dogapi-rb) docs, I installed the gem: 
> 
> ``` # on ubuntu e.g.
$ sudo apt-get install ruby-dev```

> Then created a timeline.rb file in the shared directory. 
> 

![timeline.rb](https://res.cloudinary.com/themostcommon/image/upload/v1536099792/Screen%20Shots/SS_timeline_rb.png)
> Which seemed very straight forward from the [Datadog API](https://docs.datadoghq.com/api/?lang=bash#create-a-timeboard) docs; however, I struggled with getting to a point where the file was being read and implemented. After exhausting my efforts, I took a step back and looked at the curl option. After a successful GET operation with the correct end points, I tried the example in the docs and it worked!
> 
> Using Postman, I was able to set up the POST request and use the clipboard to properly format the call. 
>
```curl -X POST \
  'https://api.datadoghq.com/api/v1/dash?api_key=8ab45aa2722f65a5198cd6abee513541&application_key=c868f13fbcf5c70bbdfcb5aecf98762542dfe2dd' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: a09aa851-2360-4cdb-8ce3-a96cdfe698d7' \
  -d '{
      "graphs" : [{
          "title": "My First Metics",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}"                   
                  }              
                ]
          },
          "viz": "timeseries"
      }, 
      {
          "title": "My First Metics Rollup",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"                   
                  }]
          },
          "viz": "timeseries"
      }],
      "title" : "My Metrics",
      "description" : "A dashboard with my metric info.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:jamessmith-solutions-engineer"
      }],
      "read_only": "True"
}'
```
> And to create the hourly rollup based on the docs [here](https://docs.datadoghq.com/graphing/functions/rollup/) and [here](https://docs.datadoghq.com/graphing/#rollup-to-aggregate-over-time), I could [Update the Timeboard](https://docs.datadoghq.com/api/?lang=bash#update-a-timeboard) with the additional graph.
> 
> PUT for rollup 
>
```curl -X PUT \
  'https://api.datadoghq.com/api/v1/dash/906289?api_key=8ab45aa2722f65a5198cd6abee513541&application_key=c868f13fbcf5c70bbdfcb5aecf98762542dfe2dd' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: f7cd9182-e5ee-497b-8d93-685fba893ea7' \
  -d '{
      "graphs" : [{
          "title": "My First Metics",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}" }
                ]
          },
          "viz": "timeseries"
      }, 
      {
          "title": "My First Metics Rollup",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "My Metrics",
      "description" : "A dashboard with my metric info.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:jamessmith-solutions-engineer"
      }],
      "read_only": "True"
}
```
To add a graph for an anomaly within PostgresQL, based on the [Anomaly Detection](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/) docs, I updated the PUT request with this code: 

>
	"title": "PostgresQL Anomaly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:postgresql.max_connections{host:jamessmith-solutions-engineer},'basic', 2)" }
              ]
          },
          "viz": "timeseries" 
          
> [View Datadog Dashboard](https://app.datadoghq.com/dash/906289/my-metrics?live=true&page=0&is_auto=false&from_ts=1536230377775&to_ts=1536233977775&tile_size=m)          

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

#### - [x] Set the Timeboard's timeframe to the past 5 minutes
#### - [x] Take a snapshot of this graph and use the @ notation to send it to yourself.

![5 min snapshot](https://res.cloudinary.com/themostcommon/image/upload/v1536115704/Screen%20Shots/SS_annotated_snapshot.png) 

* **Bonus Question**: What is the Anomaly graph displaying?

> According to [Introducing Anomaly Detection in Datadog](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/), "By analyzing a metric’s historical behavior, anomaly detection distinguishes between normal and abnormal metric trends." By recognizing where the data is inconsistent, it can help provide a valuable view into what's happening and even better, anomalies are excluded from changing or adjusting historical trends. 

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

#### - [x] Warning threshold of 500
#### - [x] Alerting threshold of 800
#### - [x] And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

#### - [x] Send you an email whenever the monitor triggers.
#### - [x] Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
#### - [x] Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
#### - [x] When this monitor sends you an email notification, take a screenshot of the email that it sends you.

```
curl -X POST \
  'https://api.datadoghq.com/api/v1/monitor?api_key=8ab45aa2722f65a5198cd6abee513541&application_key=c868f13fbcf5c70bbdfcb5aecf98762542dfe2dd' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: e280a582-4bc6-4306-b163-a47edf9aa365' \
  -d '{
	"name": "My_Metric load is high on {{host.name}} : {{value}} ",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_metric{host:jamessmith-solutions-engineer} > 800",
	"message": "{{#is_alert}}. my-metric average is above 800: {{value}} on {{host.ip}} for the previous 5 minutes   {{/is_alert}}\n{{#is_warning}}. my-metric average is above 500 : {{value}} for the previous 5 minutes   {{/is_warning}}\n{{#is_no_data}}. my-metric data is missing for more than 10 minutes  {{/is_no_data}}\n\n@jamesesmith1009@gmail.com ",
	"tags": [],
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": true,
		"notify_no_data": true,
		"renotify_interval": "0",
		"escalation_message": "",
		"no_data_timeframe": 10,
		"include_tags": false,
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}
```

![my_metric warn](https://res.cloudinary.com/themostcommon/image/upload/v1536119734/Screen%20Shots/SS_monitor_warn.png)

- [x] **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![offline weekends](https://res.cloudinary.com/themostcommon/image/upload/v1536120552/Screen%20Shots/SS_offline_weekends.png)

![offline daily](https://res.cloudinary.com/themostcommon/image/upload/v1536120552/Screen%20Shots/SS_offline_daily.png)

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

> Collecting APM data with the Flask app seemed relatively straight forward and after reading through some Python basics tutorials, I felt that I could figure things out. 
> 
> Based on the [ddtrace Flask docs](http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask), the Flask app needed to be modified by adding the Blinker library and Datadog middleware and then create the middleware object. 
> 
> [APP.PY](https://github.com/notthemostcommon/hiring-engineers/blob/JamesSmith_Solutions_Engineer/app.py)
> 
> Next, I installed the Python integration 
> 
> ```sudo pip install datadog```
> 
> Then I installed the Data Tracing library
> 
> ```sudo pip install ddtrace```
> 
> And then I started Flask app 
> 
> ```ddtrace-run python app.py```
> 
> "Once you’ve completed this step, return to [this page](https://app.datadoghq.com/apm/docs#). Your traces should be available shortly."
> 
> And because I'm no stranger to failure, there was no surprise when I returned to find there was no data. 
> 
> I made sure that the Datadog.yaml file was properly configured
> 
>     apm_config:
>       enabled: true
> 
> After restarting the agent, nothing changed so I used Postman to hit the endpoint and found that I wasn't returning any data. I realized that the Flask app host was different than the VM host and after updating them, there was data! 
> 
> ![apm data](https://res.cloudinary.com/themostcommon/image/upload/v1536194680/Screen%20Shots/SS_apm_integration.png)
> 
> ![apm dashboard](https://res.cloudinary.com/themostcommon/image/upload/v1536194680/Screen%20Shots/SS_apm_dashboard.png)
 

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

> Accordiung to the [Getting Started with APM docs](https://docs.datadoghq.com/tracing/visualization/), Services are "a set of processes that do the same job" and Resources are "a particular action for a service". To break it down further, I found this [example](https://dotnetsoul.wordpress.com/2011/08/16/difference-between-services-and-resources-related-to-webservice-and-rest/) which had this approach to defining them. 
> 
	A “Service” is defined by a verb ( For example, “validate customer’s credit score”, which describes the business function it implements.)
	A resource is defined by a noun for example, “doctor’s appointment” that describes the data provided by the resource.
>   

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

#### Is there anything creative you would use Datadog for?

>One of my passion projects that I've been working on since I started learning to be a developer is an app I call "A or Nay" which uses the NYC Open Data from the Health Department and is essentially a Yelp-like app with addition of health grades and violations history. (Since the time I started building this, Yelp has added grades but still not violation history.) I think Datadog could be a valuable tool to get click-through rates for restaurants based on grades. Being able to use the metrics that are gathered, I could market to restaurants depending on their health grade. So we could validate follow through (i.e. reservations, phone calls, mapping) based on the impact of their health grade and for "A" restaurants show how they can better capitalize on their commitment to health and safety and for "B" restaurants, we can identify people who don't seem to be affected by the health grade as much. And if they have a "C" or lower... well, I can recommend a good P.R. company and a cleaning crew! 




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
* [Writing an Agent check](https://docs.datadoghq.com/developers/agent_checks/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)