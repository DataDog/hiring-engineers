# Solutions Engineer - Brendan McIlhenny
## Mac Computer Setup using Vagrant

First things first, let's download Vagrant [here](https://www.vagrantup.com/docs/installation/) and follow the prompts like any other program, which will install a Vagrant Linux Ubuntu virtual machine on my Mac laptop running MacOS Mojave.

What does Vagrant do? When dev teams are working on different operating systems and have different dependencies and you're all working on the same project, collaborating is bound to get annoying really fast. That's where Vagrant comes in. It creates an all encompassing environment using the same configurations regardless of all of these OS/ language/library versions and dependencies. With Vagrant installed I created a new folder that would serve as Root to this project and changed into it:

```
cd Development

mkdir datadog-code-challenge

cd datadog-code-challenge
```

According to the Vagrant docs I  then needed to run the command `vagrant init hashicorp/precise64` then `vagrant up`, which would build a box to hold my environment configurations but `vagrant up` gave me this error:

```
No usable default provider could be found for your system.

Vagrant relies on interactions with 3rd party systems, known as
"providers", to provide Vagrant with resources to run development
environments. Examples are VirtualBox, VMware, Hyper-V.

The easiest solution to this message is to install VirtualBox, which
is available for free on all major platforms.

If you believe you already have a provider available, make sure it
is properly installed and configured. You can see more details about
why a particular provider isn't working by forcing usage with
`vagrant up --provider=PROVIDER`, which should give you a more specific
error message for that particular provider.
```
Hmm, first roadblock but a clue. As the error message reads above, Vagrant did not have a default "provider", which serves programs like Vagrant resources to run development environments. So I went over [here](https://www.virtualbox.org/) to download Virtualbox and followed the prompts to get it up and running.

Let’s try this again.

`vagrant init hashicorp/precise64`then a `vagrant up`. Success! Since Vagrant runs the virtual machine you have to ssh into it with the command `vagrant ssh`.

![vagrant ssh](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/ssh.png)

With the vm all set and ready to go it's now time to install the agent. Head over to the datadog UI (https://app.datadoghq.com/account/settings#agent/ubuntu) for instructions on installing the agent. Since my virtual machine is running Ubuntu I chose the Ubuntu option and ran the commands inside my ssh'ed instance:

```
DD_API_KEY=<MY-API-KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/install_dd_agent.png)

I then got the error:
```the program 'curl' is currently not installed.  You can install it by typing: sudo apt-get install curl
```
So I ran `sudo apt-get install curl` and installed curl in the virtual machine. This took about 10 seconds then I reran the simple one line installation again, then once the agent installed I started the agent up with the command `sudo service datadog-agent start`. And that's it for setup.

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/run_agent.png)


First step of the actual assignment is I needed to add some tags by manipulating the `datadog.yaml` configuration file. according to datadog’s docs, the configuration file is located at /etc/datadog-agent/datadog.yaml file. I'd change the documentation here slightly by explicitly stating to navigate to the file or changing the command box to something more explicit like `sudo nano /etc/datadog-agent/datadog.yaml`. I was not familiar with Linux commands before this exercise and was left scratching my head thinking what the command `/etc/datadog-agent/datadog.yaml` meant. If it's a command I'd expect something to happen when I ran `/etc/datadog-agent/datadog.yaml`.

So I ran `sudo nano /etc/datadog-agent/datadog.yaml` and this opened up a simple text editor in the vm itself so I could change the configuration file to add my host's tags. I ran into some issues here with tags not showing up so I poked around the datadog agent docs (https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6) and found that I could run the command `sudo service datadog-agent status`. I got a helpful message saying my config file could not be parsed properly, meaning the syntax I used to add tags was incorrect.  It took some finagling to get this part to work as I had to add the tags on one line like the image below. I'd make another recommendation here to change the docs to be more explicit about putting tags on one line like this winning combination:

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/tags.png)

Eventually I landed on the right syntax, restarted the agent with the command `sudo service datadog-agent restart` and my tags started showing up in the UI:

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/host_map_tags.png)

Next step was to install a database on my machine and run the corresponding integration for the datadog agent. I decided to use postgresql for Linux Ubuntu, so I ran the command `sudo apt-get install postgresql` courtesy of the postgres docs (http://postgresguide.com/setup/install.html).

According to the docs, this installation procedure created a user account called postgres that is associated with the default Postgres role. In order to use Postgres, we can log into that account. So I switched over to the postgres account on your server by typing `sudo -i -u postgres`, then I navigated over to the datadog integrations tab, found postgres, clicked on it, then clicked on the configuration tab and followed the prompts.

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/postgres_1.png)
![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/postgres_2.png)

Next step was writing a custom agent check that submits a metric named my_metric with a random value between 0 and 1000, then changing the collection interval so that it only submits the metric once every 45 seconds. Using these docs as reference (https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6), I navigated to the `/etc/datadog-agent` directory where the `checks.d` folder was located and created the file `custom_my_metric.py` where I was to define my check, a check that would return a metric named "my_metric" with a random value between 0 and 1000. My file looked like this:

```
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

import random

class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1001))
```

I then navigated to the `/etc/datadog-agent/conf.d` directory where I put my custom check configuration file `custom_my_metric.yaml` with the following code:

```
init_config:

instances:
    -   min_collection_interval: 45
```

As the instructions said and as the documentations reads, you can change the minimum collection interval by specifying a number of seconds (45). In this case the my_metric metric could be collected every 45 seconds. I ran into some issues finding the checks.d folder as well as the conf.d folder and I'd recommend putting a corresponding file structure map on these parts of the docs that rely on the datadog-agent file structure that shows the user where all of these important folders are located.



Next up was creating a time board via the API. Navigate to the datadog ui, click on the integrations tab then the API link under that.

anomaly detection  look for strange behavior in a given metric given the metrics past performance. i used the basic version of the anomaly algorithm given i don’t have much historical data for my database:
* Basic uses a simple lagging rolling quantile computation to determine the range of expected values. It adjusts quickly to changing conditions but has no knowledge of seasonality or long-term trends.
* more info on anomaly here: https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/


next monitoring

setting up monitor i had them all set up but then noticed that the alert was a) not triggering even though the directions say wait for avg i changed it to at least once so i could at least get the picture of the email for the hiring challenge but more importantly b) the template variable {{host.ip}} wasn’t returning anything in the email, it came back blank. So I added host:precise64 to the `define the metric` section and then it starting to work.

setting up downtimes: first i was confused that there was no option to set a weekly recurring downtime where i could check physical days, then i changed the

i copied and pasted the flask app from the code challenge,

set up apm with the apm installation docs here: https://docs.datadoghq.com/agent/apm/?tab=agent630#agent-configuration

found a raspberry pi forum where someone wasn’t able to download anything using pip:
Found some entries for "pip-cannot-install-anything" indicating it could be a ssl-problem, so be sure your system is on current level ("sudo apt-get update" and then "sudo apt-get upgrade"). so tried it

installed the python client as per the documentation (https://app.datadoghq.com/apm/install#) with the command
- pip install ddtrace
but was running into a consistent issue:

vagrant@precise64:~$ pip install ddtrace
Downloading/unpacking ddtrace
  Cannot fetch index base URL http://pypi.python.org/simple/
  Could not find any downloads that satisfy the requirement ddtrace
No distributions at all found for ddtrace
Storing complete log in /home/vagrant/.pip/pip.log
vagrant@precise64:~$

stack overflow said something about http being automatically blocked by pip so to specify https: but that didn’t work
pip install -v ddtrace -i https://pypi.python.org/simple/

it seemed to be an SSL 403 error. googled that with pip. stumbled upon this

https://github.com/pypa/pip/issues/4817

sudo pip install -v ddtrace -i https://pypi.python.org/simple/

ran ddtrace-run python my_app.py according to api install datadog docs (https://app.datadoghq.com/apm/install#)



got error: Flask ImportError: No Module Named Flask

installed Flask

sudo pip install -v flask -i https://pypi.python.org/simple/

then ran the command:
- ddtrace-run python app.py cause my file was called app.py

image

still nothing, command ran fine, flask app was running on 0.0.0.0:5050 but nothing chasing on datadog ui.

so i found the logs for the tracer-agent

/var/log/datadog/trace-agent.log

screenshot of logs

a combination of no data received from the api as well as parsing errors in the yams file.

losing hope, i started curling into the flask app supposedly instrumented using ddtrace to send logs and requests to datadog. I saw I was getting errors!

2019-02-21 20:58:34,602 - werkzeug - INFO - 127.0.0.1 - - [21/Feb/2019 20:58:34] "GET /api/apm HTTP/1.1" 200 -
2019-02-21 20:58:35,294 ERROR [ddtrace.writer] [writer.py:138] - cannot send spans to localhost:8126: [Errno 111] Connection refused
2019-02-21 20:58:35,294 - ddtrace.writer - ERROR - cannot send spans to localhost:8126: [Errno 111] Connection refused

so my flask app wasn’t able to talk to my vagrant I’ve sshed into running the datadog agent. so i looked back at the /var/log/datadog/trace-agent.log logs:

2019-02-21 20:24:53 INFO (main.go:160) - trace-agent running on host precise64
2019-02-21 20:24:53 INFO (api.go:140) - listening for traces at http://localhost:8126
2019-02-21 20:25:03 INFO (api.go:324) - no data received
2019-02-21 20:25:53 INFO (service_mapper.go:59) - total number of tracked services: 0
2019-02-21 20:26:03 INFO (api.go:324) - no data received

no data being received. my hypothesis is that theres a mismatch here, listening for traces at port 8126 but the app being traced was run on a different port and somehow i haven’t configured the two to know that. Back to google. Someone also had this error on Stackoverflow (https://stackoverflow.com/questions/49699969/datadog-errorddtrace-writercannot-send-services-to-localhost8126-errno-111)

from stackoverflow:

There are two ways to access dd-trace agent on host from a container:
1. Only on <HOST_IP>:8126, if docker container is started in a bridge network:
docker run -d <image_name>
dd-trace agent should be bound to <HOST_IP> or 0.0.0.0 (which includes <HOST_IP>).
2. On <HOST_IP>:8126 (if dd-trace agent is bound to <HOST_IP> or 0.0.0.0) and localhost:8126, if docker container is started in the host network:
docker run --network host -d <image_name>
As you already try to reach dd-trace agent on localhost:8126, so the second way is the best solution.

so i tried using the middleware this time instead like this person did: https://stackoverflow.com/questions/52390804/datadog-how-to-implement-ddtrace-on-flask-application


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

traced_app = TraceMiddleware(app, tracer)

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


restarted datadog agent, sent a few curls and BOOM, it started working.

SCREENSHOT

had to google the difference between infrastructure and app, here’s what i got:

The APM language agents monitor your applications at the code level: which transactions, database queries, and external services are taking the most time, what runtime errors are occurring, etc. Infrastructure monitors your hosts at the operating system level: how much CPU, memory, etc. are being used on each server, which processes are running, etc.

a service is a piece of software that is self contained, such as a flask app. your flask app could be one service that makes up your online business, perhaps you have a shopify app that handles payments for your business, that is another service. a resource is a particular component of an individual service responsible for a task. for the instrumented flask app, the endpoints for the web app correspond to a specific function that has one goal: log something.

##LAST QUESTION

######I think it would be cool to use Datadog to monitor your music listening habits and build out a profile/DNA.

I’m really interested in the types of music people listen to and the patterns you can infer from them. I grew up in Southern New Jersey so Bruce Springsteen is in my blood, but I attended high school in Philly and started really getting into r&b/hip hop and The Roots. Then I moved to New Orleans and got really into the Meters and the New Orleans funk movement. Geography plays a huge role in the types of music you’re exposed to, but it’s certainly not the only one. It would be super interesting to see how different factors like time, geography, seasonality, mood, weather, relationships piece together your music DNA and how you can use a combination of monitors, dashboards and algorithms to predict where you fit on the music spectrum, learn to predict what type of music you’d like, or maybe even find an ideal boyfriend/girlfriend.

You could use the Spotify API to record the music you and your friends/family listen to, the time they listened, the location they listened to it, and the weather at the time you listened and get data from an API that records when new music gets released. With a bigger picture of your listening context, you can use Datadog dashboards to see your personal distribution of music listens based on genre and learn to predict what types of music you gravitate towards. Do you listen to more depressing music in the winter methods like Radiohead? If so, are there outliers in the winter months that you can catch with monitors? Sounds like a good use for the the anomaly datadog algorithms. Are there certain relationships you can map out between people and the types of music they listen to?

Can you build out dashboards that prove that your friend’s music tastes rubbed off on you, which in turn you shared with your other friends who have now shared it with their friends? You could use monitors for health reasons. For instance set up a monitor to alert you when you’re listening to too uplifting music at night so that you won’t be too amped to fall asleep at night.
