Your answers to the questions go here.

# Solutions Engineer Hiring Exercise

- [Prerequisites - Setup The Environment](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/answers.md#prerequisites---setup-the-environment)
- [Collecting Metrics](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/answers.md#collecting-metrics)
- [Visualizing Data](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/answers.md#visualizing-data)
- [Monitoring Data](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/answers.md#monitoring-data)
- [Collecting APM Data](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/answers.md#collecting-apm-data)
- [Final Question](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/answers.md#final-question)
- [Feedback](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/answers.md#feedback)
- [Candidate LinkedIn Account](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/answers.md#candidate-linkedin-account)

<hr>

### Prerequisites - Setup The Environment


##### Vagrant

Downloaded and installed [VirtualBox 6.0](https://www.virtualbox.org/wiki/Downloads) for OS X hosts. I then downloaded and installed the [latest version of Vagrant](https://www.vagrantup.com/downloads.html) for 64-bits macOS.  

I initialized, activated and SSHed into the virtual machine using following commands on my terminal:  

```shell
  $ vagrant init ubuntu/xenial64
  $ vagrant up
  $ vagrant ssh
```
Below is a screenshot of my terminal on typing the above commands:

![vagrant set up](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/vagrant.png)


##### Datadog Sign up 

Signed up for [Datadog](https://app.datadoghq.com/signup), using `Datadog Recruiting Candidate` in the Company field.

##### Datadog Agent Installation

Navigated to the `Integrations` tab on the Datadog webapp and selected `Agent` option: 

![integrating_agent](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/installation%20instructions.png)

Chose the correct platform which is `Ubuntu` in my case and followed the 1-step installation instructions:

![ubuntu_agent](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/ubuntu%20agent.png)

The following command was used on terminal to install the datadog-agent:

```shell
$ sudo apt-get install curl
$ DD_API_KEY=f1939bb97730746da2a69d15c07b5901 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

You can see the following success message on the terminal after correct agent installation:

![Agent is running and functioning properly](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Agent%20installation%20success%20message.png)


<hr>



### Collecting Metrics

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Studied [how to assign tags](https://docs.datadoghq.com/tagging/assigning_tags/?) documentation to get a better idea of tags. I referred [configuration file location](https://docs.datadoghq.com/agent/faq/agent-configuration-files/?tab=agentv6) to get the location of my agent configuration file on ubuntu.   

I had to use `sudo` admin privileges to access and make changes to the `datadog.yaml` file. This was done by initially navigating back to the `vagrant root directory` and then accessing `datadog.yaml` file from the `datadog-agent directory`. Here are the commands used for the same:

```shell
  $ cd..
  $ cd /etc/datadog-agent
  $ sudo nano datadog.yaml
```

*`nano` is vagrant's built-in text editor.*

I referred [tags best practices](https://docs.datadoghq.com/getting_started/tagging/#tags-best-practices) while creating my tags. The above command opened `datadog.yaml` file in my terminal. I then added my respective tags to this file using the correct format as seen in the following image:

![datadog.yaml](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/tags%20file.png)

I then closed the file, saving the changes (using Ctrl + X) and restarted the agent:

```shell
  $ sudo service datadog-agent restart
```

These tags could be reflected on the datadog webapp hostmap. To observe these changes, I navigated to `Host Map` under `Infrastructure` tab on the navigation pane of datadog webapp. My Host Map with tags could be seen there as below:


![host map tags](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/tags.png)

.
> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Installed `PostgreSQL` on virtual machine. I used PostgreSQL for this assignment as I’ve used it for a number of projects while pursuing my Masters in CS. I referred the [PostgreSQL installation](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04) document. 

**Step 1**:
Installed postgresql using the following commands on my terminal:

```shell
  $ sudo apt-get update
  $ sudo apt-get install postgresql postgresql-contrib
```
![postgres installation](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/postgres%20install.png)

Navigated to `Integrations` section of the webapp and looked up for PostgreSQL integration there. I then clicked into it and finished installing it. 

I clicked on `Generate Password` button to generate my PostgreSQL password. I referred the [how to use postgres on ubuntu 16.0](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04) document to learn the usage of postgres on ubuntu. The following command switched me to the `postgres` account on ubuntu:

```shell
  $ sudo -i -u postgres
```

The following command was used to access the `postgres` prompt:

```shell
  $ psql
```

I then created a user on postgres and granted permissions to it following the configuration instructions as shown below:

![postgres user](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/switch%20to%20postgres%20%26%20create%20user%20with%20grant.png)

**Step 2**: Configured the agent to connect to the PostgreSQL server. For this step, I accessed the `conf.d/postgres.yaml` file:

```shell
  $ \q
  $ cd /etc/datadog-agent/conf.d
  $ sudo nano postgres.yaml
```

I added some content to the `postgres.yaml` file as shown and saved the changes:

![postgres.yaml file](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/postgres%20yaml%20file.png)

**Step 3**: Restarted the agent:

```shell
  $ sudo service datadog-agent restart
```
**Step 4**: Executed the `Agent status` command and verified that the integration check has passed. Look for `postgres` under the Checks section:

```shell
  $ sudo datadog-agent status
```

![step 4 status](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/postgres%20staus%20check.png)

The terminal status as well as the webapp integration success message proved that the installation was successful.

.
> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Referred the [writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) for this part.

The document asked me to create 2 files named `my_metric.yaml` and `my_metric.py` files such that their names should match. The check file `my_metric.py` should be placed in the `checks.d` folder, while the configuration file named `my_metric.yaml` should be placed in the `conf.d` folder.

I navigated to `/etc/datadog-agent/checks.d` directory and created a file called [my_metric.py](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/files/my_metric.py)

```shell
  $ cd /etc/datadog-agent/checks.d
  $ sudo nano my_metric.py
```
Saved the following code in `my_metric.py`"

```python
from checks import AgentCheck
import random
class MyMetric(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randint(0,1000))
```

![my_metric.py](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my_metric.py.jpeg)

I then navigated to `/etc/datadog-agent/conf.d` and created the `my_metric.yaml` file there:

```shell
  $ cd /etc/datadog-agent/conf.d
  $ sudo nano my_metric.yaml
```
Saved the following code in `my_metric.yaml`:

```python
instances:
  [{}]
```

![my metric.yaml](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my_metric.yaml.jpeg)


Restarted the Agent for the changes to reflect and checked the agent status:

```shell
  $ sudo service datadog-agent restart
  $ sudo service datadog-agent status
```
![my metric status](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my_metric%20status%20check.png)
![my_metric check](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my_metric%20status%20check%20copy.png)


> Change your check's collection interval so that it only submits the metric once every 45 seconds.

I opened the [my_metric.yaml](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/files/my_metric.yaml) file again to make the following changes before saving it again:

```python
instances:
    -   min_collection_interval: 45
```
![my_metric 45 secs interval](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/45%20sec%20interval%20for%20yaml.png)

Restarted the Agent for the changes to reflect:

```shell
  $ sudo service datadog-agent restart
```
To verify if this was successful, I checked `datadog-agent status` a couple of times and verified that the total run count was updating after 45 seconds.

I found the following important point in the agent check documentation -

_The default is 0 which means it’s collected at the same interval as the rest of the integrations on that Agent. If the value is set to 30, it does not mean that the metric is collected every 30 seconds, but rather that it could be collected as often as every 30 seconds._

.
> Bonus Question Can you change the collection interval without modifying the Python check file you created? 

Yes, the collection interval can be changed by directly changing the collection interval in the `/conf.d/my_metric.yaml` configration file, similar to what I did in the above step.

<hr>

### Visualizing Data

> Utilize the Datadog API to create a Timeboard that contains:
> - Your custom metric scoped over your host.
> - Any metric from the Integration on your Database with the anomaly function applied.
> - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
> Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Researched [Timeboards](https://docs.datadoghq.com/api/?lang=python#timeboards) and figured out that I first needed to install Datadog.

I installed pip for this:

```shell
  $ sudo apt-get install python-pip
```

Once pip was installed, I installed Datadog:

```shell
  $ pip install datadog
```

Next we need the `App Key` and `API key`!

API key can be found by navigating to APIs under Integrations option of datadog webapp. There, under API Keys, you can find your unique api key. Timeboard App key needs to be generated. This can be done by navigating to APIs under Integrations on webapp. Navigated to the Application Keys section, added a name for the application key in the input box and clicked Create Application Key button. By doing this, an application key was generated for me.

I then created a python file named `sk_timeboard.py` in the `datadog-agent repository`. This file included the code to create timeboards for my custom metric scoped over the host, any metric from postgreSQL integration with anomaly function applied and my custom metric with roll up function applied. 
For the 2nd question i.e any metric for my selected database, I selected the `percent usage connection` metric which is the number of connections to this database as a fraction of the maximum number of allowed connections.

Referred [anomalies](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) and [anomaly monitors via the API](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-monitors-via-the-api) to create the anomaly function. 
The anomaly function has two parameters:
- The first parameter is for selecting which algorithm is used.
- The second parameter is labeled bounds, tune it to change the width of the gray band. bounds can be interpreted as the standard deviations for your algorithm; a value of 2 or 3 should be large enough to include most “normal” points.

Referred [rollup](https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1) to create the rollup function on my custom metric:
- Appending this function to the end of a query allows you to control the number of raw points rolled up into a single point plotted on the graph. The function takes two parameters, method and time: `.rollup(method,time)`.

![sk_timeboard](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/sk-timeboard.png)

I then saved [sk_timeboard.py](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/sk-timeboard.png) and ran it using the following terminal command:

```shell
  $ python sk_timeboard.py
```
I then navigated to the `Dashboard` List under Dashboards tab on the webapp:

![dashboard list](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/timeboard%20displayed%20in%20list.png)

I could see `My Timeboard` created successfully in the list and clicked into it to see graphs for `My custom metric`, `PostgreSQL integration anomaly` and `My custom metric rollup` as below:

![my_metric](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my%20timeboard.png)

> Once this is created, access the Dashboard from your Dashboard List in the UI:
> - Set the Timeboard's timeframe to the past 5 minutes
> - Take a snapshot of this graph and use the @ notation to send it to yourself.

To set timeboard’s timeframe to past 5 minutes, I manually dragged the graph such that I could see the data for past 5 minutes:  

![5 min](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/5%20min%20timeboard.jpeg)

I then clicked the small camera icon at the top of one of the metric as below, and added my name with @ notation in the comments, to send the snap to my email address:

![send snap](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/timeboard%20snapshot.png)

Here is the email that I received:

![snapshot](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/email%20for%20custom%20metric.png)

.
> - Bonus Question: What is the Anomaly graph displaying?

The anomaly graph is tracking whether the metric is behaving differently than usual within an assigned deviation. My anomaly graph is displaying if there are abnormalities in the number of connections to this database as a fraction of the maximum number of allowed connections. A straight blue line indicates there’s no abnormalities. Red spikes indicate there are some abnormalities. In my case for the past day, there’s a small red spike which indicates that there’s an abnormality in the number of connections to this database as a fraction of the maximum number of allowed connections.
 

<hr>

### Monitoring Data

> Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
> Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
> - Warning threshold of 500
> - Alerting threshold of 800
> - And also ensure that it will notify you if there is No Data for this query over the past 10m.

I researched the [metric monitor](https://docs.datadoghq.com/monitors/) document to understand how to create monitors in order to monitor the dashboard.

I then navigated to `Metric` under `New Monitors` of `Monitor` section on the webapp. I selected `my_metric` from the metric dropdown and selected my `host`. Added `800` to the alert threshold input box and `500` to the warning threshold input box. Selected notify me if `no data`. I the added a title for my monitor and then added alert, warning, no data messages along with my `host ip` and `email address` in the message field. 
Please refer the screenshots below for more clarity:

![create metric monitor1](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Monitor_1.jpeg)

![create metric monitor2](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Monitor_2.jpeg)

Here are the screenshots of the warning and no-data alert emails that I received: 

![warning](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Monitor_3.jpeg)
![no data alert](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/missing%20data%20alert.png)

.
> Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
> - One that silences it from 7pm to 9am daily on M-F,
> - And one that silences it all day on Sat-Sun.
> - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

I navigated to `Manage Monitors` under Monitors on webapp and clicked on the edit sign besides my monitor in the list.
I then navigated to the `Manage Downtime` tab and clicked `Schedule Downtime`. I selected my monitor name and selected the `Recurring Schedule` option. There I added start day as the same day, repeat every 1 week and selected Monday - Friday for the downtime. Set the beginning time to 7 pm and the duration to 14 hours. I then added an appropriate notification message and added my name in the Notify your team field.

![weekday downtime](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Monitor_downtime%201.jpeg)

I then received an email confirmation for the weekday downtime scheduled:

![weekday email](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Monitor_downtime%202.jpeg)

Next, I scheduled the weekends downtime by following the same procedure that I used for setting the weekday downtime. The only difference is that I chose `Saturday, Sunday` for Repeat on field and the `12 am to 12 am` time slot by setting the begining time to 12 am and duration to 12 hours. I again added appropriate message and added my email address. 


![weekend downtime](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Monitor_downtime%203.jpeg)

I then received an email confirmation for the weekend downtime scheduled:

![weekend email](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Monitor_downtime%204.jpeg)

<hr>

### Collecting APM Data

> Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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

I referred [agent tracking python documentation](https://docs.datadoghq.com/tracing/languages/python/) for this task.

I installed flask using the following command:
```shell
$ pip install flask
```
I then installed ddtrace using the following command:
```shell
$ pip install ddtrace
```
I then edited the `datadog.yaml` file in the `datadog-agent directory` to enable to trace collection for the trace agent. 
For this, I opened `datadog.yaml` file using nano and uncommented following 2 lines from the file:
```shell
apm_config:
enabled:true
```
I saved the file and created a new python file called [app.py](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/files/app.py) in the same directory. I added the given flask app code in this file :

![app.py file](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/app.py%20file2.png)

I then restarted the `datadog-agent`:
```shell
sudo service datadog-agent restart
```
I then ran `app.py` file using ddtrace:
```shell
ddtrace-run python app.py
```
The below screenshot proves the successful running of the flask app:

![flask app running](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/app.py%20running.png)

However, the APM section of webapp continued to show me the following screens:

![apm instructions](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/apm%20instructions.png)
![apm python](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/apm%20python%20screen.png)

*Note: I was unable to complete the task inspite of having the APM app run successfully. I couldn't get the apm to connect to my server inspite of doing  extensive research on the issue and trobleshooting for 2 days.*

I researched [APM (tracing)](https://docs.datadoghq.com/tracing/), [APM Setup](https://docs.datadoghq.com/tracing/setup/), specifically [Tracking Python Applications](https://docs.datadoghq.com/tracing/setup/python/), [Flask Setup](http://flask.pocoo.org/docs/0.12/installation/#installation), [Introduction to Flask, (http://flask.pocoo.org/docs/0.12/quickstart/), and [Flask Framework Compatibility](http://pypi.datadoghq.com/trace/docs/#flask).

Here are the things I tired to debug this issue:
1. Edited `datadog.yaml` file to test for different other ports like `2200, 8156`, etc
2. Tried the `Middleware` approach by installing blinker and editing the flask file correctly. However, I got the same result as before
3. Used java approach by following the APM instructions for java
4. Stopped my host firewall and reset chrome settings to get the security clearance
5. Tried all the APM related steps from scratch on Windows OS
6. Went through all the open, closed issues for [python ddtrace Github repository](https://github.com/DataDog/dd-trace-py/issues) as well as [Solutions Engineering Solutions Github repository](https://github.com/DataDog/hiring-engineers/issues?q=is%3Aissue+is%3Aclosed)
7. Since my account had expired, I created a new account, thinking that might resolve the issue, and repeated all the steps from scratch to get the same output
8. Tried to install datadog agent directly on Mac and repeated all relevant steps

Since I'm out of further approaches to make this run, I'd ask for help in this case.

.
> Bonus Question: What is the difference between a Service and a Resource?

Researched [Getting started with APM](https://docs.datadoghq.com/tracing/visualization/).

A service is a set of processes that function together to provide a complete feature. Eg. a web application is made up of many different services like web app service, database service, query service, etc. 

A resource is an action / query for a service. Eg. /home routes or a sql query like 'SELECT users.first_name from users'; 


> Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
> Please include your fully instrumented app in your submission, as well.

My flask app can be found [here](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/files/app.py).
<hr>

### Final Question

> Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
> Is there anything creative you would use Datadog for?


<hr>

### Feedback 

I really enjoyed taking this challenge. Although I got stuck in the installation step due to a permissions issue, I was able to figure out my mistake and finish the assignment. I got a hands-on experience and a thorough understanding of how powerful the Datadog platform is. Thank you for giving me the opportunity to take this challenge!

### Candidate LinkedIn Account

- [LinkedIn](https://www.linkedin.com/in/shruti-kulkarni94/)
