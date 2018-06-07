# Solution Engineer Technical Exercise Submission - Pabel Martin

Here are my answers for this technical exercise along with all supporting links, code, screenshots, and color commentary.

What I think will be fairly obvious is that this exercise was **very** challenging for me.  For better or worse, a lot of this was a first for me in many areas:
  * I'd never heard of Vagrant, Flask, YAML, or Markdown until working on this exercise
  * I've heard of Python, Ubuntu, MongoDB, and GitHub prior to this exercise, but hadn't worked with any of them hands-on and directly
  * The only thing I'd done before (that was a part of this exercise) was google liberally (always) and execute some command line stuff (years since I'd done this) so I was pretty rusty.
  
If I had to characterize what it was like to go through this, I would say that it was brute force.  Throughout the whole exercise I was reminded of the scene in the Matrix where Neo first sees Matrix code 'falling' on the monitor and asks Cypher if he always looks at it encoded. In this exercise, it felt like all I ever saw was green falling code.  Eventually after following enough instructions and steps and examples it worked, but I honestly don't know or understand all the details of how/why everything worked.

![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/scene1.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/scene2.png)

This submission, for example, is something I've never done before.  I had a developer friend walk me through GitHub and what forks, commits, branches, pull requests, and markdown were and how they were used.  I haven't had experience with any of these to-date so I used [this](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) and [this](https://stackoverflow.com/questions/2822089/how-to-link-to-part-of-the-same-document-in-markdown/16426829#16426829) to create this submission.  It's entirely possible I haven't submitted as expected on the right branch so enjoy a chuckle if I didn't even get the first part right.  :)

You'll also see this in the submission, but two major mistakes for me were not coming back to the main exercise GitHub page.  I missed the update to use Ubuntu 16.04 instead of 12.04 as well as the update to the Flask app for host name.  If I'd seen that, I would have saved myself a **ton** of grief/time; a mistake I'll strive to only make once.


## Table of Contents

  * [Setup the Environment](#setup-the-environment)
  * [Collecting Metrics](#collecting-metrics)
    * [Datadog Agent and Tags](#datadog-agent-and-tags)
    * [MongoDB Installation and Integration Configuration](#mongodb-installation-and-integration-configuration)
    * [Custom Agent Check](#custom-agent-check)
    * [Bonus Question 1](#bonus-question-1)    
  * [Visualizing Data](#visualizing-data)
    * [Bonus Question 2](#bonus-question-2)
  * [Monitoring Data](#monitoring-data)
    * [Bonus Question 3](#bonus-question-3)
  * [Collecting APM Data](#collecting-apm-data)
    * [Bonus Question 4](#bonus-question-4)
  * [Final Question](#final-question)
  

## Setup the Environment

I followed the steps outlined in the **Setting Up Vagrant** link from the Reference section and setup Vagrant on my Macbook Pro.  The exercise page as of 5/27/18 when I started referenced setting up a machine with Ubuntu 12.04 so I used the 'precise' argument in the command line referenced in the [Vagrant Getting Started](https://www.vagrantup.com/intro/getting-started/) page.

This caused an issue later on in the exercise when trying to install MongoDB and Flask as it kept hitting issues/errors from dependencies.  I upgraded the box manually to Ubuntu 14 and that helped clear the MongoDB issues.  I still hit issues installing Flask later on that I couldn't get past so I went back on this exercise's GitHub page to find a workaround in the reference section.  That's when I noticed that it was updated to reference Ubuntu 16.04 so I started the exercise from scratch with a new box on that version.

These screenshots will show the details of my Datadog trial account along with the Infrastructure List page showing both boxes I ultimately configured as part of this exercise.  The configuration files documented below are the same on both boxes for the datadog-agent and others so I've only included one copy for review.

![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/DDenv.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/infrahostlist.png)

[Back to the top](#table-of-contents)

## Collecting Metrics

### Datadog Agent and Tags

I followed the instructions in the datadog docs [page for the agent install on Ubuntu](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/), as well as the instructions in the datadog dashboard for my trial account.

I navigated to /etc/datadog-agent and used sudo vim datadog.yaml to update the file.  It took some googling and longer than I'd like to admit to remember how to navigate the box and use vim commands to edit and save the file.  I un-commented (is that what you say?) the dd_url line, api_key, and tags section.  I added three tags to each host for location, environment, and role.  See screenshots and snippet of the datadog.yaml file below.

```
# The host of the Datadog intake server to send Agent data to
dd_url: https://app.datadoghq.com

# The Datadog api key to associate your Agent's data with your organization.
# Can be found here:
# https://app.datadoghq.com/account/settings
api_key: REMOVED

# If you need a proxy to connect to the Internet, provide it here (default:
# disabled). You can use the 'no_proxy' list to specify hosts that should bypass the
# proxy. These settings might impact your checks requests, please refer to the
# specific check documentation for more details.
#
# proxy:
#   http: http(s)://user:password@proxy_for_http:port
#   https: http(s)://user:password@proxy_for_https:port
#   no_proxy:
#     - host1
#     - host2

# Setting this option to "yes" will tell the agent to skip validation of SSL/TLS certificates.
# This may be necessary if the agent is running behind a proxy. See this page for details:
# https://github.com/DataDog/dd-agent/wiki/Proxy-Configuration#using-haproxy-as-a-proxy
# skip_ssl_validation: no

# Setting this option to "yes" will force the agent to only use TLS 1.2 when
# pushing data to the url specified in "dd_url".
# force_tls_12: no

# Force the hostname to whatever you want. (default: auto-detected)
# hostname: mymachine.mydomain

# Set the host's tags (optional)
tags:
   - location:DC
   - env:prod
   - role:VM-server
```

![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/precisetags.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/xenialtags.png)

[Back to the top](#table-of-contents)

### MongoDB Installation and Integration Configuration

I followed the instructions on the [Mongo site](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) to install community edition on Ubuntu.  As previously mentioned I had to do this twice because of the two different hosts I created on different versions of Ubuntu.

I then used the instructions on the [integration page of my datadog dashboard](https://app.datadoghq.com/account/settings#integrations/mongodb) and the [Datadog Docs section for Mongo](https://docs.datadoghq.com/integrations/mongo/) to configure the agent.  I google'd to find Mongo shell commands for user creation to complete that step.  I had never worked with YAML before so it was a lot of trial and error using this [YAML interpreter](http://www.yamllint.com/) to get the proper conf.yaml file to recognize my Mongo server and collect metrics.
```
init_config:

instances:
      - server: mongodb://datadog:datadog@127.0.0.1:27017/admin
        tags:
            - location:DC
            - role:database
            - env:prod

      - additional_metrics:
            - collection       # collect metrics for each collection
            - metrics.commands
            - tcmalloc
            - top
```

Here is a screenshot from datadog of MongoDB installed on both of my VMs along with the relevant tags.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/MongoDBinstall.png)

One thing I could never resolve were errors related to Mongo.  It seems as if two configurations are there for mongo on both services.  The host shows 'mongo' and 'mongodb', and while one would always have successfull checks and metrics, the other always had errors associated with it.  Checking the datadog agent status and tailing the logs for the agent always revealed the same 'server is missing' error.  I imagine it's something that's misconfigured, but I could never figure out where the issue was.  That said, the one collector functioned as expected and returned the data needed to complete these steps/exercise. See screenshots.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/mongoerrors1.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/mongoerrors2.png)

[Back to the top](#table-of-contents)

### Custom Agent Check

To complete this section I used the [writing agent check](https://docs.datadoghq.com/developers/agent_checks/) section in datadog docs, [this page](https://datadog.github.io/summit-training-session/handson/customagentcheck/) for a sample of a check, and [this page](https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/) for how to generate a random number in python.

As mentioned before, I don't have much of this in my background so this was the first python file/script I'd ever created and run.  I'm not sure, nor would I want to admit, how long it took me to get this part done.
```python
from checks import AgentCheck
import random

class MyCheck(AgentCheck):

    def check(self, instance):

        self.gauge('my_metric', random.randint(-1,1001))
```
I confirmed this was working as expected by using the metrics explorer and searching for my_metric.  I also noticed that it appeared on the hosts under 'no-namespace' as well as in the datadog agent logs under 'mycheck'.  The 'no-namespace' piece didn't seem like the cleanest way to have this installed/configured, but I couldn't figure out why it was happening and how to fix it.

To change the collection interval, I referenced the datadog docs which had a section for configuring a custom written check.  The combination of that, the YAML interpreter, a lot of trial and error, and tailing the agent log led to confirming this worked as expected.  Here's the mycheck.yaml file from /etc/datadog-agent/conf.d:
```
init_config:

instances:
    #[{}]
    [{min_collection_interval: 45}]
```

[Back to the top](#table-of-contents)

### Bonus Question 1
Based on the datadog docs writing a check section, I changed the collection interval for my custom check using the YAML config file as opposed to the python file.  Given that I didn't have to change the Python check file I created, I believe the answer to this bonus question is **Yes**.
>For Agent 5, min_collection_interval can be added to the init_config section to help define how often the check should be run globally, or defined at the instance level. For Agent 6, min_collection_interval must be added at an instance level, and can be configured individually for each instance.

[Back to the top](#table-of-contents)


## Visualizing Data
To complete this section, I took the approach detailed below.  I'm not sure if it was 'cheating', but given my lack of development background this was the only path I saw to getting this completed.

I created a dashboard in my environment via the UI ([link](https://app.datadoghq.com/dash/822625/ui-created-timeboard?live=true&page=0&is_auto=false&from_ts=1528137594823&to_ts=1528141194823&tile_size=m)) with all the elements called for, plus a few others just to familiarize myself with the functionality.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/tb_UI.png)

[Back to the top](#table-of-contents)

Once this was completed and working appropriately, I used the [API timeboard docs](https://docs.datadoghq.com/api/?lang=python#timeboards) to get sample requests/responses.  I also got the API and APP keys from the API section in the datadog dashboard for my trial account.  

Based on what I saw in the sample request, I installed the [datadog libraries](https://github.com/datadog/datadogpy) via 'sudo pip install datadog'.  Then I created a python script similar to the sample request to get all timeboards.  My aim was to get the definitions of the graphs I needed to submit a create via the API.  It didn't bring back all the definitions, but it did give me the ID.
```python
from datadog import initialize, api

options = {
    'api_key': 'REMOVED',
    'app_key': 'REMOVED'
}

initialize(**options)

print api.Timeboard.get_all()
```
Then I used a python script to pull a specific timeboard via the ID I got.  One piece that tripped me up here that seems obvious now was adding the print command to the last line.  Using the sample in the API docs, it didn't have the print command so I kept getting no response and a command prompt after running the script.  In my head that meant it wasn't working.  Not sure if it was the time of night or what, but it took a minute before I realized I need to add the print command to the script.
```python
from datadog import initialize, api

options = {
    'api_key': 'REMOVED',
    'app_key': 'REMOVED'
}

initialize(**options)

print api.Timeboard.get(822625)
```
I received the [following output](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/Timeboard%20API%20Pull.rtf) which contained all of the definitions of the graphs I successfully created in the UI.

I used that information as a guide to creating a python script to leverage the create a timeboard API.  I used the sample request and made adjustments specific to the exercise requirements and changed titles so it was clear that the dashboard was created via the API and not just a straight copy of the one I'd created first in the UI.
```python
from datadog import initialize, api

options = {
    'api_key': 'REMOVED',
    'app_key': 'REMOVED'
}

initialize(**options)

title = "API Created Timeboard"
description = "A timeboard created via the DD API as part of the SE technical exercise"

graphs = [
   {
    "definition": {
#        "events": [],
        "requests": [
            {
               "q": "avg:my_metric{host:ubuntu-xenial}",
               "style":{
                         "width":"normal",
                         "palette":"dog_classic",
                         "type":"solid"
               },
               "type":"line",
            }
        ],
        "viz": "timeseries",
        "autoscale":True
    },
    "title": "Average of MyMetric on Ubuntu 16.04"
  },

   {
    "definition": {
#        "events": [],
        "requests": [
            {
               "q": "anomalies(avg:mongodb.locks.collection.acquirecount.intent_sharedps{role:database}, 'basic', 3)",
               "aggregator":"avg",
               "style":{
                         "width":"normal",
                         "palette":"dog_classic",
                         "type":"solid"
               },
               "type":"line",
            }
        ],
        "viz": "timeseries",
        "status":"done",
        "autoscale":True
    },
    "title": "Mongo Metric Against DB Role w/ Basic Anomalies"
  },

   {
    "definition": {
#        "events": [],
        "requests": [
            {
               "q": "sum:my_metric{host:ubuntu-xenial}",
               "aggregator":"sum",
               "style":{
                         "width":"normal",
                         "palette":"dog_classic",
                         "type":"solid"
               },
               "type":"line",
            }
        ],
        "viz": "query_value",
        "autoscale":True,
        "precision":"0"
    },
    "title": "Sum of MyMetric on Ubuntu 16.04"
  },


]

read_only = True


api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
```

This script successfully created the following timeboard.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/tb_API.png)

[Back to the top](#table-of-contents)

Using the keyboard shortcut, I changed the API created timeboard to display the past 5 minutes.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/tb_API_5.png)

[Back to the top](#table-of-contents)

I used the camera icon on my MongoDB graph to take a snapshot and send the notification to myself via @mention.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/snapshotsend.png)

[Back to the top](#table-of-contents)

### Bonus Question 2
The graph with anomaly applied is displaying when the specified metric is out of range of what's expected based on historical values.  My particular graph is set to show anomalies outside of 3 deviations from norm.  This could potentially help determine if/when there is something going wrong or about to go wrong since the algorithm accounts for seasonality and historical trends.

[Back to the top](#table-of-contents)

## Monitoring Data

Using the UI, I created a monitor as defined in the exercise requirements.  It warns and alerts on the avg. of 500 and 800 for my_metric in a 5 minute range.  It is also set up to alert if no data is sent over the past 10 minutes.  I've also configured the notifications to show what caused the trigger, the specific host/IP, the alert state, and different text in the notification body based on the Alert, Warning, or No Data state.  See screenshots below for evidence.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/Monitor.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/monitorconfig1.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/monitorconfig2.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/Monitor%20Email.png)

[Back to the top](#table-of-contents)

### Bonus Question 3
I created two scheduled downtimes to mute the alerts during the times listed in the exercise.  See screenshots for configuration and email notifications.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/downtime1.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/downtime2.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/dtemail1.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/dtemail2.png)

[Back to the top](#table-of-contents)

## Collecting APM Data
This was easily the toughest portion of the exercise for me.  I'd never heard of Flask so spent a lot of time reading through the quickstart and installation documentation provided in the reference section.  In working through the Flask install, I hit a lot of errors/dependencies when using the original Ubuntu 12.04 host.  Because of that I manually upgraded it to Ubuntu 14 and then was able to get past those errors and get through the installation (this was on my 'precise' host).  I wasn't able to get an installation done using venv as described in that documenation so just installed everything directly on the machine.

I then copy/pasted the sample application provided in the exercise into a python script and started working through the quickstart instructions to get the flask app running.  I continually hit the following error when trying to get the app to run via the 'flask run' command:
error: socket.error: [Errno 98] Address already in use

I google'd and searched for hours on how to get around this, looking for examples and suggested solutions.  I went back to the exercise's GitHub page to check out the reference section and that's when I noticed that the text was changed and it said that I needed to be using Ubuntu 16.04.  Based on that, I created a new VM on Ubuntu 16.04 and went through all the previous setup again.  It wasn't ideal, but I wanted to start fresh and it helped solidify that I did learn a little something through all the pain and effort because it took much less time to get this new box configured.

At this point I got right back to the same issue/blocker and hit the "Address in Use" error.  I played around with Virtual Box network settings and tried a whole bunch of stuff that didn't work.  Through this research, I came across the following command to help determine what was running on your machine ("sudo netstat --program --listening --numeric --tcp").  Using this I noticed that the datadog agent was running on 5000 and I'd seen in the various pages I was on that 5000 was the same port that Flask ran on.  At this point I went to the datadog.yaml file and did an internal fist pump when I found a configuration line that allowed me to set the ports.  I un-commented the lines and changed them to 6000 and 6001.
```
# Additional path where to search for Python checks
# By default, uses the checks.d folder located in the agent configuration folder.
# additional_checksd:

# The port for the go_expvar server
expvar_port: 6000

# The port on which the IPC api listens
cmd_port: 6001

# The port for the browser GUI to be served
# Setting 'GUI_port: -1' turns off the GUI completely
# Default is '5002' on Windows and macOS ; turned off on Linux
# GUI_port: -1
```

[Back to the top](#table-of-contents)

I now was able to run the sample app via a python command as well as through the 'flask run' command, so felt good about getting passed that issue/blocker.  My issue now however, was that when I tried to hit the localhost/IP address and port from the browser on my MBPro I got a connection refused error.  I fought this error unsuccessfully for a few hours and then broke down and phoned a friend.  Not sure if that's cheating or not allowed, but I was at a loss.  If that's not OK, feel free to ignore the rest of this section.  I spoke with a friend who's a developer and walked him through what I had set up and what I was trying to accomplish.  As expected, it took 10 minutes to explain it to him and maybe 2 minutes for him to walk through what I needed to look at.  He basically said the issue was that my MBPro had no path to access the machine so I was just hitting the MBPro's local loopback address.  He directed me to the Vagrantfile as opposed to the VirtualBox network settings as a way to get that resolved.  That direction was the key to getting through this.

I went to the Vagrantfile and updated the configuration to port forward from the host 5000 to the guest 5000.  I un-commented this line and updated the ports.
```
  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "forwarded_port", guest: 5000, host: 5000
```

From there, I reloaded the VM via this updated Vagrantfile and got the Flask app up and running again.  I still was hitting an error when trying to hit the app via the browser, but the error was different.  Instead of connection refused, I was now getting connection reset which seemed promising.  In reading through the [Flask quickstart](http://flask.pocoo.org/docs/0.12/quickstart/), I noticed the section about making the app/server Externally Visible.  I tried running the flask command with the --host 0.0.0.0 tags as described but was still hitting the issue.  Some more google'ing and clicking through the Flask pages led me [here](http://flask.pocoo.org/snippets/20/) where I found some samples of code where instead of app.run() they actually passed 0.0.0.0 and port name.  I did the same in my sample application configuration and that was the Eureka moment that made it work.  The ultimate irony is that only after figuring that out did I notice that the exercise page was updated to show this change to the sample flask application. I learned a very valuable lesson to always review the page to see any updates/changes made.  :(

So after I confirmed that the app was running and I was getting expected responses, I started following the instructions in the APM section of my datadog trial account.  I installed the ddtrace libraries and then ran the application via ddtrace-run to have the application automatically instrumented.  I got the results below after starting the app and then hitting the URLs to get responses.
```
vagrant@ubuntu-xenial:/etc/python3/ddproject$ sudo ddtrace-run python ddflask.py flask
DEBUG:ddtrace.contrib.flask.middleware:flask: initializing trace middleware
2018-06-04 13:49:06,761 - ddtrace.contrib.flask.middleware - DEBUG - flask: initializing trace middleware
DEBUG:ddtrace.writer:resetting queues. pids(old:None new:4938)
2018-06-04 13:49:06,761 - ddtrace.writer - DEBUG - resetting queues. pids(old:None new:4938)
DEBUG:ddtrace.writer:starting flush thread
2018-06-04 13:49:06,761 - ddtrace.writer - DEBUG - starting flush thread
 * Serving Flask app "ddflask" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
INFO:werkzeug: * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
2018-06-04 13:49:06,764 - werkzeug - INFO -  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
DEBUG:ddtrace.api:reported 1 services
2018-06-04 13:49:06,765 - ddtrace.api - DEBUG - reported 1 services
INFO:werkzeug:10.0.2.2 - - [04/Jun/2018 13:49:14] "GET / HTTP/1.1" 200 -
2018-06-04 13:49:14,952 - werkzeug - INFO - 10.0.2.2 - - [04/Jun/2018 13:49:14] "GET / HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.01681s
2018-06-04 13:49:15,798 - ddtrace.api - DEBUG - reported 1 traces in 0.01681s
INFO:werkzeug:10.0.2.2 - - [04/Jun/2018 13:49:22] "GET /api/apm HTTP/1.1" 200 -
2018-06-04 13:49:22,353 - werkzeug - INFO - 10.0.2.2 - - [04/Jun/2018 13:49:22] "GET /api/apm HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00132s
2018-06-04 13:49:22,814 - ddtrace.api - DEBUG - reported 1 traces in 0.00132s
INFO:werkzeug:10.0.2.2 - - [04/Jun/2018 13:49:29] "GET /api/trace HTTP/1.1" 200 -
2018-06-04 13:49:29,958 - werkzeug - INFO - 10.0.2.2 - - [04/Jun/2018 13:49:29] "GET /api/trace HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00124s
2018-06-04 13:49:30,859 - ddtrace.api - DEBUG - reported 1 traces in 0.00124s
```
[Back to the top](#table-of-contents)

After this, the metrics started showing up in my environment, I did another internal and maybe external fist pump, and then added an APM trace metric to my Timeboard I created via the UI in the exercise above.  Link to the dashboard and screenshot is below.

[UI Created Dashboard w/ APM Data](https://app.datadoghq.com/dash/822625/ui-created-timeboard?live=true&page=0&is_auto=false&from_ts=1528208413485&to_ts=1528212013485&tile_size=m)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/tbwithapm.png)

Here is the application I used to generate the APM data.  It's the sample app provided in the exercise with my changes to the app.run() command.
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
    app.run(host='0.0.0.0',port=5000)
#    app.run()
```

[Back to the top](#table-of-contents)

### Bonus Question 4
Based on my reading of the docs [here](https://docs.datadoghq.com/tracing/visualization/), a service is a collection of resources.  So the service would something like the database, while the queries and stored procedures would be resources.  Or a webapp would be a service, and specific URL's and functions would be the resources.

Or....this Millenium falcon would be the service and each lego would be a resource.

![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/falcon.jpg)

[Back to the top](#table-of-contents)

## Final Question
I don't know if it's terribly creative, but I'm considering upgrading my account to a paid version to help me out with all the IT support I provide my parents, aunts, uncles, in-laws, and siblings.

I'm currently hit with the common questions/complaints most tech employees get:
  * My computer is really slow, what's happening?
  * My internet is really slow, is something wrong?
  * Do I need to get a new computer?
  * My wifi is going in and out, can you fix that?

Today I'm indirectly responsible for 3 Windows desktops, 2 Windows laptops, 4 MacBook Airs, 2 MacBook Pros, 3 Linksys routers, and 4 Netgear routers across 4 states in the US.  My aforementioned family members believe in a heterogenous environment.

I can envision a world where I have a dashboard and monitors set up on each of those devices, everyone's home network, and if possible a speed test on the ISP in everyone's city.  With that, I could either predict when the phone calls were going to start, pre-emptively let them know there's an outage, or proactively alert myself when real issues are going on and get in front of it.  

Not a ton of business value or creativy outside of team Martin and Drenner (in-laws), but a huge time savings that would deliver a great personal ROI.

[Back to the top](#table-of-contents)
