If you want to apply as a solutions engineer at [Datadog](http://datadog.com) you are in the right spot. Read on, it's fun, I promise.

<a href="http://www.flickr.com/photos/alq666/10125225186/" title="The view from our roofdeck">
<img src="http://farm6.staticflickr.com/5497/10125225186_825bfdb929.jpg" width="500" height="332" alt="_DSC4652"></a>

## The Exercise

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

- [x] You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.

> Being as I was unfamiliar with linux or even using a virtual machine, I read through the [Vagrant documentation] (https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) and after watching some YouTube videos, I attempted to make sense of everything and actually downloaded Vagrant, VirtualBox and Ubuntu 18.04 LTS and followed the [tutorial](https://www.youtube.com/watch?v=3AnlvTgsoYM&t=175s) to start the VM. 

> The first thing was to create a Vagrantfile, which is a config file written in Ruby which configures and provisions the VM.  
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


- [x] Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

> The process for signing up for Datadog is painless and the instructions were very clear. Once I started my 14-day free trial, I was able to choose Ubunutu for my operating system and the command was a simple copy and paste to start downloading the Agent. The script even included my API key

> ```DD_API_KEY=8<API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"```
> 
> ![agent running](https://res.cloudinary.com/themostcommon/image/upload/v1535486511/Screen%20Shots/SS_DD_Agent_running.png)


## Collecting Metrics:

- [x] Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

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
Having only used templates to create YAML files in the past, I referenced this [Github] (https://github.com/Animosity/CraftIRC/wiki/Complete-idiot%27s-introduction-to-yaml) to make sure that I was keeping the correct syntax. A valuable lesson learned was that most of the configuration file is commented out with “#” leading the line so the # needs to be removed for the changes to be read. 

> To save the changes with emacs, (Mac: control = ^) 
> 
> ```^-x, ^-s``` 
> 
> At the bottom of the screen, you will see will see: 
> ```Wrote /etc/datadog-agent/datadog.yaml```
> 
> Then to close the document 
> 
> ```^-x, ^-c```
> 
> 
> At first, I assumed that I could see the tag updates after a browser refresh, but they never appeared. And then I saw this note:
> 
> ![no agent responding](https://res.cloudinary.com/themostcommon/image/upload/v1535486510/Screen%20Shots/SS_No_Agent_Reporting.png)
> 
> After reading the docs some more, I thought I needed to change the process_config so that it would also collect containers and processes.
> 
> ![process config](https://res.cloudinary.com/themostcommon/image/upload/v1535486510/Screen%20Shots/SS_Process_config.png)
> 
> And after updating the config file, I started getting a new error. 
> 
> ![NTP error](https://res.cloudinary.com/themostcommon/image/upload/v1535486510/Screen%20Shots/SS_NTP_Error.png)
> 
> After reading the docs on NTP and how to correct this issue, I finally discovered that I had a syntax error in the yaml config file and after correcting it, the warnings disappeared but I still had no tags. 
> 
> Unsure of what else to do at this point, I stopped Datadog service: 
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




- [x] Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

> As I am most familiar with PostgreSQL, I chose to download it. 
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
> After looking in the `datadog-agent/conf.d` directory and found no file by that name to edit, I looked in the` postgres.d` directory and found the `conf.yaml.example `. After editing the file, I saved it and restarted the Agent and it *did not connect* to Postgres. 
> 
> Looking at the instructions, I realized that the file I was supposed to edit was supposed to be the conf.d directory and not buried further down so I created the file and added the configurations to the `conf.d` directory.
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
> And was happily greeted with success. 
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

- [x] Change your check's collection interval so that it only submits the metric once every 45 seconds.

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
> With my output producing no errors or warnings: 
> 
> ```network (1.6.0)
    	---------------
      Total Runs: 78
      Metric Samples: 26, Total: 2028
      Events: 0, Total: 0
      Service Checks: 0, Total: 0
      Average Execution Time : 0ms* ```
      
**Bonus Question** Can you change the collection interval without modifying the Python check file you created?

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
* [Writing an Agent check](https://docs.datadoghq.com/developers/agent_checks/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)