# Solutions Engineer Answers
`Yoonhye Jung`
`Sydney`
`yoonhyej.jung@gmail.com`



## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

> Answer: Set up `Vagrant Ubuntu 14.04 LTS` for this exercise.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

> Answer: Signed up and Installed "Datadog Agent v6" on Ubuntu
> 
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Setup_01_Agent%20installation.png" />

> 1. Click 'Intergrations-Agent' button on the top drop-down menu  
> 2. Find [Ubuntu](https://app.datadoghq.com/account/settings#agent/ubuntu) on the left-side menu
> 3. Follow the instruction for installing Datadog Agent v6 on Ubuntu
```
DD_API_KEY=5d35ac69e9371611b7100041d2959ee9 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Setup_02_Install%20agent%20on%20Ubuntu.png" />
> Apply 'easy one-step install' in Ubuntu terminal

><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Setup_03_Start%20agent%20on%20Ubuntu.png" />
> Complete installation and start Datadog Agent
```
sudo start datadog-agent
```

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
> Answer: Edited "datadog.yaml" file to add tags `region:ap` `env:production` `role:database:mysql`
> 
> 1. Find "datadog.yaml" for Agent v6 configuration which is located in "/etc/datadog-agent/" for Linux(Ubuntu)
>>```
>>cd /etc/datadog-agent/
>>```
> 2. Use 'emacs' editor to add tags in "datadog.yaml" file
>>```
>>sudo emacs datadog.yaml
>>```
>See the form example for tagging in "datadog.yaml" file and add a line next to it

><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_01_Tagging.png" />
>
> 3. Restart Datadog Agent for the applied changes
>>``` 
>>sudo service datadog-agent restart
>>```

> 4. See the updated tags on the Host Map page in Datadog
>
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_02_Tags%20on%20Hostmap%20page.png" />

> Link: [Host Map page](https://app.datadoghq.com/infrastructure/map?host=581392043&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

>>https://app.datadoghq.com/infrastructure/map?host=581392043&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host



* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
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
