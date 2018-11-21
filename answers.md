Enterprise Sales Engineer
Sid Narang

Introduction: 
My intial step was to make sure the whole project was to watch some getting-started DataDog videos and make sure I understood exactly the types of problems DataDog was solving. This gave me a quick and simple understanding on some of the use cases that are supported by customers and how the product itself could expand.

Prerequisites - Setup the environment
I am using macOS High Sierra Version 10.13.5

Vagrant is fast and simple and *most* of the time has low dependency issues if done right.
As DataDog instructed, I went with Ubunutu 16.04

Next, following the instructions here: https://www.vagrantup.com/intro/getting-started/ and downloading the packager for mac.

To ensure 16.04 version, I ran these commands in my terminal once the installation was done
$ vagrant init ubuntu/xenial64
$ vagrant up

This was a simple process, with SSH being next. ![alt text](https://www.dropbox.com/s/v6ve8efnfv35r2b/VagrantSSH.png?dl=0)

Collecting Metrics:

- Install Agent - 
Going to datadoghq.com and signing up for an account gave me the ability to walk through the product quickly.

The first task was to download the agent, hopping into the Installation Instructions - I was able to get the commands for Ubuntu and run it locally on my machine. 

Script: DD_API_KEY="apikey" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

https://www.dropbox.com/s/hr2rwbtgglurjc9/Installationinstructionsagent.png?dl=0

In the DataDog dashboard, metrics started to appear and were default metrics such as system disk, cpu, etc.

- Add Tags - 
Adding a tag was simple, and is modified in the yaml file located at /etc/datadog-agent/datadog.yaml. This is the config file that DataDog leverages and holds key paramaters and settings when starting up.

My tags were set, as you can see here: https://www.dropbox.com/s/sm0kuqpya7e2j93/tags.png?dl=0

Once tags were set, since this is a config file, the agent has to be restarted, or stopped, and started again. All relevant agent commands can be found here, and were used extensively when I made any changes. https://docs.datadoghq.com/agent/faq/agent-commands/


In order to view my tags, I hopped to the Infrastructure tab, and was able to see them on my dashboard. https://www.dropbox.com/s/mvuvr6cdksycw0q/projse.png?dl=0

- Installing Database - 

The next step was to install a database (MongoDB, MySQL, or PostgreSQL). I picked mongo since I use it quite a bit. I ran these commands to get it installed

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

sudo apt-get update

sudo apt-get install -y mongodb-org

All which can be found here: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

I had to prepare mongo, and DataDog's own guide helped in setting up a user:
https://docs.datadoghq.com/integrations/mongo/#prepare-mongodb

I followed the command below.

# On MongoDB 3.x or higher, use the createUser command.
db.createUser({
  "user":"datadog",
  "pwd": "<UNIQUEPASSWORD>",
  "roles" : [
    {role: 'read', db: 'admin' },
    {role: 'clusterMonitor', db: 'admin'},
    {role: 'read', db: 'local' }
  ]
}) 

- my_metric

This next step required a py and yaml file, with the py file holding the logic and yaml for any neccesary config modifications.

The script is randomvalue.py and randomvalue.yaml; both which will be uploaded here.

Bonus: Since the yaml is also included, I can modify that file only and keep the py file as is.

Visualizing Data:

The API explorer from DataDog was simple to understand, and once I started testing a couple of them, it was easy to implement. I used postman to execute the API. 

Since this was a timeboard, I managed to focus most of my time on that API section: https://docs.datadoghq.com/api/?lang=python#timeboards

The postman script can be found here: https://www.dropbox.com/s/63z0cbf9146egzx/Postman3API?dl=0

Once I ran my script, going into my dashboards, I could see the "My 3 APIs Timeboard" which was configured as expected.

This is the dashboard since the last 1d: https://www.dropbox.com/s/338b8p2nx8wbinw/3APIs.png?dl=0
This is the dashboard for a 5m timeframe:https://www.dropbox.com/s/uurla29t4janyh5/Screenshot%202018-11-20%2017.22.40.png?dl=0

The dashboard is composed of 3 main graphs, (ignore the 4th), one which is my_metric scoped over my host, second is my mongoDB with the anomaly function, and the last one is the rollup function my_metric 

Snapshot image: https://www.dropbox.com/s/bmscnmwjj6shf1e/mymetricsnapshot.png?dl=0

Bonus: The anomaly graph will show when a specific metric is beyond the expected avg over time.

Monitoring Data:

Modifying the alert was easy, and can be found here:

Under the Monitor Tab, just simply create a Monitor and follow the conditions from the screenshot.

https://www.dropbox.com/s/nytqk1n3alglkpu/800500.png?dl=0
https://www.dropbox.com/s/rpf2w2i3kmus0qv/monitoralert.png?dl=0

Email notification:
https://www.dropbox.com/s/9s27bmlka58aqpf/emailalert.png?dl=0

This was a warn signal which meant it was > 500 at least once.

Now to keep the sanity, DataDog allows downtimes for these alerts. 

Mon-Fri Downtime:
Scheduled to start Nov 20, 2018 19:00 PST and repeats weekly from 7:00pm to 9:00am tomorrow on Monday, Tuesday, Wednesday, Thursday, and Friday

Sat-Sun Downtime:
Scheduled to start Nov 23, 2018 0:00 PST and repeats weekly from 12:00am to 12:00am in 2 days on Sunday and Saturday


Collecting APM Data:

In order to set this up, we need an app to start testing against.

I leverged the flask app that was already included but modified it so we could enable trace.

Since I did not go via the ddtrace-run route, I had to change couple of things manually first.

Going into the /etc/datadog-agent/datadog.yaml file, I made the neccesary changes below:

# Trace Agent Specific Settings
#
apm_config:
#   Whether or not the APM Agent should run
   enabled: true
   env: test_sn
#   The environment tag that Traces should be tagged with
#   Will inherit from "env" tag if none is applied here
#   env: none
#   The port that the Receiver should listen on
   receiver_port: 8126

This allowed me to enable the trace agent manually, and next I needed to make sure my flask app could actually use this.


Below is my code for the Flask App, which has import tracer and import TraceMiddleware as well, to enable it.

from flask import Flask
import logging
import sys
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

 # Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)

main_logger.addHandler(c)
app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

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


After restaring the agent, all I really had to do was run the following commands:

python flaskapp.py bash

And from another terminal, just start using curl
url http://127.0.0.1:5050/api/trace
url http://127.0.0.1:5050/api/apm
url http://127.0.0.1:5050

Once this was done, the DataDog dashboard starting picking up metrics as seen here:

https://www.dropbox.com/s/7ade3kyhbbqcfgy/apmmetrics.png?dl=0

Lastly, in order for me to have APM and Infra metrics, all I had to do was modify the dashboard that I already had, and add the trace metric to enable APM metrics to be visualized.

Combined Dashboard: https://www.dropbox.com/s/ff7mej87d97oteb/apmvinfra.png?dl=0

Link: https://app.datadoghq.com/dash/993992/my-3-apis-timeboard

The flaskapp.py will be attached as well.

Bonus Question: What is the difference between a Service and a Resource?

A "Service" is the name of a set of processes that work together to provide a feature set.
	Example: webservice to call something

Resource: A particular query to a service.
	Example: The underlying result 

Final Question:

DataDog possesess the relevant tech to helo solve many common-day problems.

Once of the major issues we will see with population growth, and the influx of cars(self-driving and normal), we will need to understand how traffic can be solved. This is an issue in every country and with the amount of residents within downtown and major hubs, having the ability to understand a common output will be important. The ability to analyze places that can generate quick crowds is also relevant.
