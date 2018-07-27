![datadog logo](https://i.imgur.com/4a0vj3W.png)

# Solutions Engineer Hiring Exercise

- [Prerequisites - Setup The Environment](https://github.com/cwithac/hiring-engineers/blob/Cathleen_Wright_Solutions_Engineer/answers.md#prerequisites---setup-the-environment)
- [Collecting Metrics](https://github.com/cwithac/hiring-engineers/blob/Cathleen_Wright_Solutions_Engineer/answers.md#collecting-metrics)
- [Visualizing Data](https://github.com/cwithac/hiring-engineers/blob/Cathleen_Wright_Solutions_Engineer/answers.md#visualizing-data)
- [Monitoring Data](https://github.com/cwithac/hiring-engineers/blob/Cathleen_Wright_Solutions_Engineer/answers.md#monitoring-data)
- [Collecting APM Data](https://github.com/cwithac/hiring-engineers/blob/Cathleen_Wright_Solutions_Engineer/answers.md#collecting-apm-data)
- [Final Question](https://github.com/cwithac/hiring-engineers/blob/Cathleen_Wright_Solutions_Engineer/answers.md#final-question)
- [Candidate Information](https://github.com/cwithac/hiring-engineers/blob/Cathleen_Wright_Solutions_Engineer/answers.md#candidate-information)

<hr>

### Prerequisites - Setup The Environment

##### GitHub
Forked the [repository](https://github.com/DataDog/hiring-engineers/tree/solutions-engineer) and cloned [the fork](https://github.com/cwithac/hiring-engineers/tree/solutions-engineer) into my local environment, checking out _solutions-engineers_ and building branch "Cathleen_Wright_Solutions_Engineer" for unique access to the directory and _answers.md_ in the text editor [Atom](https://atom.io/).  

```shell
  $ git clone git@github.com:cwithac/hiring-engineers.git
  $ cd hiring-engineers
  $ git checkout solutions-engineer
  $ git checkout -b "Cathleen_Wright_Solutions_Engineer"
  $ atom .
```

##### Vagrant

Downloaded and installed [VirtualBox 5.2](https://www.virtualbox.org/), 5.2.16 platform packages for OS X hosts.  Downloaded and installed the [latest version of Vagrant](https://www.vagrantup.com/downloads.html) for macOS, 64-bit.  

Initialize, activate and SSH into the virtual machine:  

```shell
  $ vagrant init hashicorp/precise64
  $ vagrant up
  $ vagrant ssh
```

_Welcome to your Vagrant-built virtual machine._

##### Datadog and Agent Reporting Metrics

Signed up using `Datadog Recruiting Candidate` as Company, following the instructions to `install your first Datadog Agent for Ubuntu`.

![Instructions to install your first Datadog Agent for Ubuntu](https://i.imgur.com/nG4CXDv.png)

```shell
The program 'curl' is currently not installed.  You can install it by typing:
$ sudo apt-get install curl

$ DD_API_KEY=c802ac74556f263f47de0d8cddd8131a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

_Your first Datadog Agent is reporting._

![Agent is running and functioning properly](https://i.imgur.com/9cU6eQg.png)

![Initial Dashboard](https://i.imgur.com/YVjtSIO.png)

<hr>

### Collecting Metrics

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Researched [how to assign tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) in the documentation, specifically [assigning tags using the configuration files](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files), information about the [configuration files and folders for the Agent locations](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/#configuration) and [troubleshooting forums](https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-) for specific file locations.  I referred to [tags best practices](https://docs.datadoghq.com/getting_started/tagging/#tags-best-practices) when creating my tags.  

Modified `/etc/datadog-agent/datadog.yaml` in vi, restarting the service to force/expedite change.

```shell
  $ sudo vi /etc/datadog-agent/datadog.yaml
  $ sudo service datadog-agent restart
```

```
# Set the host's tags (optional)
tags: tagwithoutkeyvalue, tag1:tag_one, tag2:tag_two
```
*For the datadog.yaml init file, only the single line form is valid.*

![host map tags](https://i.imgur.com/d8lls61.png)

> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Installed MongoDB 2.0.4 on virtual machine.  [Followed configuration instructions](https://app.datadoghq.com/account/settings#integrations/mongodb), including insertion of Datadog user.

*Note: File names vary between configuration instructions,  [mongo.d/conf.yaml](https://docs.datadoghq.com/integrations/mongo/#configuration) & [conf.d/mongo.yaml](https://app.datadoghq.com/account/settings#integrations/mongodb).  Used `mongo.d/conf.yaml`.*

**Step 1**:

![mongodb install](https://i.imgur.com/vpuRyud.png)

![mongodb ok](https://i.imgur.com/OFDWUO3.png)

**Step 2**: Edit `/etc/datadog-agent/conf.d/mongo.d/conf.yaml` and added the MongoDB instances:

![edited yaml](https://i.imgur.com/t8migsU.png)

**Step 3**: Restart the agent.

```shell
  $ sudo service datadog-agent restart
```
**Step 4**: Execute the info command and verify that the integration check has passed.

```shell
  $ sudo datadog-agent status
```
![step 4 infocheck](https://i.imgur.com/es3dwJE.png)

![mongodb dashboard](https://i.imgur.com/4AFbmsg.png)

> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Researched [writing an Agent check](https://docs.datadoghq.com/developers/agent_checks/), specifically [your first check](https://docs.datadoghq.com/developers/agent_checks/#your-first-check).

The names of the configuration and check files must match. If your check is called `my_metric.py` your configuration file must be named `my_metric.yaml`.  The entire check would be placed into the `checks.d` folder, the corresponding configuration would be placed into the `conf.d` folder.

```shell
  $ sudo vi /etc/datadog-agent/conf.d/my_metric.yaml
  $ sudo vi /etc/datadog-agent/checks.d/my_metric.py
```

Code adapted from `hello.world` example.  [Resource for import random](https://www.pythonforbeginners.com/random/how-to-use-the-random-module-in-python).

`my_metric.yaml`
```python
init_config:

instances:
  [{}]
```
`my_metric.py`
```python
# from checks import AgentCheck
# class HelloCheck(AgentCheck):
#     def check(self, instance):
#         self.gauge('hello.world', 1)

from checks import AgentCheck
import random

class MyMetric(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randint(0,1000))
```

Restart the Agent for the changes to be enabled.

```shell
  $ sudo service datadog-agent restart
```

![my_metric](https://i.imgur.com/9bSHlb0.png)

> Change your check's collection interval so that it only submits the metric once every 45 seconds.

`my_metric.yaml`
```python
init_config:

instances:
    -   min_collection_interval: 45
```
`my_metric.py`
```python
from checks import AgentCheck
import random

class MyMetric(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randint(0,1000))
```

Restart the Agent for the changes to be enabled.

```shell
  $ sudo service datadog-agent restart
```

_Notes from [documentation](https://docs.datadoghq.com/developers/agent_checks/#configuration): For Agent 6, `min_collection_interval` must be added at an instance level, and can be configured individually for each instance._

_The default is 0 which means it’s collected at the same interval as the rest of the integrations on that Agent. If the value is set to 30, it does not mean that the metric is collected every 30 seconds, but rather that it could be collected as often as every 30 seconds._

_The collector runs every 15-20 seconds depending on how many integrations are enabled. If the interval on this Agent happens to be every 20 seconds, then the Agent collects and includes the Agent check. The next time it collects 20 seconds later, it sees that 20 is less than 30 and doesn’t collect the custom Agent check. The next time it sees that the time since last run was 40 which is greater than 30 and therefore the Agent check is collected._

![my_metric45](https://i.imgur.com/VLaCiuF.png)

> Bonus Question Can you change the collection interval without modifying the Python check file you created?

The change must be made in the `/conf.d/my_metric.yaml` configuration file.

<hr>

### Visualizing Data

*Note: At this stage, Vagrant upgrade needed to continue.*

![uname -a](https://i.imgur.com/Kgr5LdQ.png)
![curl auth fail](https://i.imgur.com/wdj56f1.png)

![curl auth success](https://i.imgur.com/GyQorAR.png)

> Utilize the Datadog API to create a Timeboard that contains:
> - Your custom metric scoped over your host.

Researched [Timeboards](https://docs.datadoghq.com/graphing/dashboards/timeboard/), [API Timeboards](https://docs.datadoghq.com/api/?lang=bash#timeboards) as well as [API Authentication](https://docs.datadoghq.com/api/?lang=bash#authentication), requests that read data require full access and also require an application key.

![Application key](https://i.imgur.com/tVmUFYb.png)  

> - Any metric from the Integration on your Database with the anomaly function applied.

[anomalies()](https://docs.datadoghq.com/graphing/miscellaneous/functions/#anomalies) and [anomaly monitors via the API](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-monitors-via-the-api) - The function has two parameters:

- The first parameter is for selecting which algorithm is used.
- The second parameter is labeled bounds, tune it to change the width of the gray band. bounds can be interpreted as the standard deviations for your algorithm; a value of 2 or 3 should be large enough to include most “normal” points.

> - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

[.rollup()](https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1) - Appending this function to the end of a query allows you to control the number of raw points rolled up into a single point plotted on the graph. The function takes two parameters, method and time: `.rollup(method,time)`.

```shell
$ api_key=c802ac74556f263f47de0d8cddd8131a
$ app_key=7112e60f24aa4e28d5d8f03d51de477e7ac5ccd7
```
```json
$ curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "scoped over host",
          "definition": {
              "events": [],
              "requests": [
                {"q": "avg:my_metric{*}"}
              ]
          },
          "viz": "timeseries"
      },
      {
          "title": "rollup function applied",
          "definition": {
              "events": [],
              "requests": [
                {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "My_Metric Timeboard",
      "description" : "A dashboard with my_metric custom agent.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
```

```shell
RESPONSE:
{"dash":{"read_only":true,"graphs":[{"definition":{"requests":[{"q":"avg:my_metric{*}"}],"events":[]},"title":"scoped over host"},{"definition":{"requests":[{"q":"avg:my_metric{*}.rollup(sum, 3600)"}],"events":[]},"title":"rollup function applied"}],"template_variables":[{"default":"host:my-host","prefix":"host","name":"host1"}],"description":"A dashboard with my_metric custom agent.","title":"My_Metric Timeboard","created":"2018-07-26T21:48:17.439658+00:00","id":872422,"created_by":{"disabled":false,"handle":"cathleenmwright@gmail.com","name":"Cathleen Wright","is_admin":true,"role":null,"access_role":"adm","verified":true,"email":"cathleenmwright@gmail.com","icon":"https://secure.gravatar.com/avatar/127e2966bc2d20469f81fdf522092c56?s=48&d=retro"},"modified":"2018-07-26T21:48:17.462807+00:00"},"url":"/dash/872422/mymetric-timeboard","resource":"/api/v1/dash/872422"}
```

![my_metrics timeboard](https://i.imgur.com/ZLikAYy.png)

_Note: Anomaly graph unable to run, can not find resolution to error, including attempting different metrics and parameters in anomaly function.  Graph created with GUI and JSON manipulation._

```json
ATTEMPTED CODE:
{
    "title": "integration of database with anomaly function applied",
    "definition": {
        "events": [],
        "requests": [
          {"q": "anomalies(avg:mongodb.dbs{*}, 'basic', 2"}
        ]
    },
    "viz": "timeseries"
}
```

```shell
RESPONSE ERROR
{"errors": ["Error parsing query: unable to parse anomalies(mongodb.dbs{*}, basic, 2: Rule 'scope_expr' didn't match at ', 2' (line 1, column 32)."]}
```

![gui anomaly](https://i.imgur.com/FrVzMHE.png)

![gui metric](https://i.imgur.com/ViVKn24.png)

![gui json](https://i.imgur.com/5Nt2tpo.png?1)

> Once this is created, access the Dashboard from your Dashboard List in the UI:
> - Set the Timeboard's timeframe to the past 5 minutes

Modification made by highlighting/click and drag the last five minutes of the graph within the GUI, discovered organically, could not find supporting documentation.  

![5 min](https://i.imgur.com/KRFNKGd.png)

> - Take a snapshot of this graph and use the @ notation to send it to yourself.

![snapshot](https://i.imgur.com/2Im9NyX.png)

> - Bonus Question: What is the Anomaly graph displaying?

An [anomaly](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) graph is tracking whether the metric is behaving differently than it has in the past within an assigned deviation (gray overlay).  

<hr>

### Monitoring Data

*Note: Vagrant upgrade disabled `sudo` access to Datadog Agent, reinstalled per setup and created a new `my_metric` per previous configuration.*

> Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Researched [metric monitor](https://docs.datadoghq.com/monitors/monitor_types/metric/).

![create metric monitor](https://i.imgur.com/XiV3BTH.png)

> Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

> - Warning threshold of 500
> - Alerting threshold of 800
> - And also ensure that it will notify you if there is No Data for this query over the past 10m.

![monitor 1-3](https://i.imgur.com/LUGE4QD.png)

Researched [notification options](https://docs.datadoghq.com/monitors/notifications/#overview0), specifically [templating variables](https://docs.datadoghq.com/monitors/notifications/#say-what-s-happening).

> Please configure the monitor’s message so that it will:
> - Send you an email whenever the monitor triggers.
> - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
> - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![monitor 4-5](https://i.imgur.com/yTe1csw.png)

> - When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![alert](https://i.imgur.com/gRelcdn.png)

![warning](https://i.imgur.com/SsDFpws.png)

![no data](https://i.imgur.com/WK6rTPP.png)

_Note: `{{host.ip}}` does not generate a response, possibly due to virtual machine configuration.  Can not find additional support documentation._

> Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

Researched [downtimes](https://docs.datadoghq.com/monitors/downtimes/).

> - One that silences it from 7pm to 9am daily on M-F,

![mondayfriday monitor](https://i.imgur.com/c8mQ8Pu.png)

> - And one that silences it all day on Sat-Sun.

![satsun monitor](https://i.imgur.com/V1jeXH7.png)

> - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![mondayfriday email 1](https://i.imgur.com/dUjtHeY.png)
![mondayfriday email 2](https://i.imgur.com/tNtgZ8U.png)

![satsun email](https://i.imgur.com/jsQPqfw.png)

*Note: `my_metric monitor` 'muted' after screen shots obtained.*

![muted](https://i.imgur.com/pqn8mPc.png)

<hr>

### Collecting APM Data

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

<details><summary>EXPAND</summary>
<p>

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

</p>

> Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

</details>



*Note: Unable to complete the task due to the below errors, best attempts through research and GUI presented.  Similar errors for both Python and Ruby.  Additional troubleshooting included attempting to download and install `ddtrace` locally through `https://pypi.org/project/ddtrace/`, unable to process due to issues syncing Vagrantfile.  Error is not networking, `ping google.com` returns success response.*

```shell
$ sudo apt-get install python-virtualenv
$ mkdir datadog
$ cd datadog/
$ virtualenv venv
$ . venv/bin/activate

(venv):~/datadog$ pip install ddtrace
Downloading/unpacking ddtrace
  Cannot fetch index base URL http://pypi.python.org/simple/
  Could not find any downloads that satisfy the requirement ddtrace
No distributions at all found for ddtrace
Storing complete log in /home/vagrant/.pip/pip.log

(venv):~/datadog$ pip install flask
Downloading/unpacking flask
  Cannot fetch index base URL http://pypi.python.org/simple/
  Could not find any downloads that satisfy the requirement flask
No distributions at all found for flask
Storing complete log in /home/vagrant/.pip/pip.log

$ deactivate

$ pip --version
pip 1.0 from /usr/lib/python2.7/dist-packages (python 2.7)

```

```shell
$ gem install ddtrace
Fetching: msgpack-1.2.4.gem (100%)
ERROR:  While executing gem ... (Gem::FilePermissionError)
    You don\'t have write permissions into the /opt/vagrant_ruby/lib/ruby/gems/1.8 directory.

$ sudo gem install ddtrace
Fetching: msgpack-1.2.4.gem (100%)
Building native extensions.  This could take a while...
ERROR:  Error installing ddtrace:
	ERROR: Failed to build gem native extension.
```

Researched [APM (tracing)](https://docs.datadoghq.com/tracing/), [APM Setup](https://docs.datadoghq.com/tracing/setup/), specifically [Tracking Python Applications](https://docs.datadoghq.com/tracing/setup/python/).  Also researched [Flask Setup](http://flask.pocoo.org/docs/0.12/installation/#installation), [Introduction to Flask](http://flask.pocoo.org/docs/0.12/quickstart/), and [Flask Framework Compatibility](http://pypi.datadoghq.com/trace/docs/#flask).

![APM setup](https://i.imgur.com/EIMeGBC.png)

![APM python](https://i.imgur.com/MzcPfdH.png)

Based on the [custom getting started](http://pypi.datadoghq.com/trace/docs/#custom) documentation, my understanding would be to wrap a trace code around each of the individual routes in order to track their specific performance.  I am curious to see how the GUI would impact this process, as it appears to be a very comprehensive [dashboard](https://www.datadoghq.com/apm/).   

```python
from ddtrace import tracer

# add the `wrap` decorator to trace an entire function.
@tracer.wrap(service='my-app')
def save_thumbnails(img, sizes):

    thumbnails = [resize_image(img, size) for size in sizes]

    # Or just trace part of a function with the `trace`
    # context manager.
    with tracer.trace("thumbnails.save") as span:
        span.set_meta("thumbnails.sizes", str(sizes))

        image_server.store(thumbnails)
```



> Bonus Question: What is the difference between a Service and a Resource?

Researched [Getting started with APM](https://docs.datadoghq.com/tracing/visualization/).

A [service](https://docs.datadoghq.com/tracing/visualization/#services) is a set of processes that do the same job while a [resource](https://docs.datadoghq.com/tracing/visualization/#resources) is a particular action for a service.

> Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
> Please include your fully instrumented app in your submission, as well.

*Please see note on errors from above.*

<hr>

### Final Question

> Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

> Is there anything creative you would use Datadog for?

In my free time, I like to see Broadway shows, but getting tickets, particularly last minute tickets, can be especially challenging.  There are some resources available [online](http://www.playbill.com/article/broadway-rush-lottery-and-standing-room-only-policies-com-116003) for information about rush and lottery policies, but tickets are primarily based on daily availability.  As most of the major theater houses use providers such as Ticketmaster, it would be beneficial to know when there were a lot of remaining seats at a certain time period prior to the curtain.  

For example, in order to have better luck being able to purchase a last minute ticket, I could set an alert that notified me two hours before curtain if the threshold of available tickets went above 20 for 'Hamilton' on Tuesday nights.

<hr>

### Candidate Information

Cathleen Wright

- [LinkedIn](https://www.linkedin.com/in/cathleenmwright/)
- [GitHub](https://github.com/cwithac)
