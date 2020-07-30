# Solutions Engineer - Candidate Exercise

- Name: Adilson Somensari
- Email: somensari@gmail.com
- Datadog account: tomaso@italymail.com
- Linkedin: https://ca.linkedin.com/in/adilsonsomensari


## Environment
- For the exercise, I started with a Raspberry Pi, then moved to a VM on Vagrant... Later I moved to a simple VM on Virtualbox as the other hosts I had were quite old and underpowered.

- I also deployed the dockerized agent in a local docker setup as well as the Kubernetes agent on a free cluster on IBM Cloud

- I am re-submitting the exercise after conversations with Matthew Stines. I will add notes to the end of the answer file.
---

# Collecting Metrics

## Tags
I created an Ubuntu VM and added tags to the config file /etc/datadog/datadog.yml

```yaml
tags:
  - "environment:dev"
  - "mytag:myvalue"
  - "country:canada"
``` 

![dashboard](/host_tags_view.png)

## Database 
I configured a mysql instance on my box and configured the database monitoring by cloning the conf.yml file under conf.d/mysql.d directory and changing the database credentials

Created the file: /etc/datadog-agent/conf.d/mysql.d/conf.yaml with the MySQL connection options

Here's the MySQL Dashboard: ![dashboard](/mysql_dashboard.png)

## Custom Agent
- Custom Agent Check: I created the file /etc/datadog/checks.d/exercise.py with the following content
```python
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

from random import randrange

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class ExerciseCheck(AgentCheck):
    def check(self, instance):
        self.gauge('exercise.my_metric', randrange(0,1000), tags=['exercise:random'])
        
```

And I also created the exercise.yml file on the conf.d

``` yml
init_config:

instances:
  - min_collection_interval: 45            	
```

And configured the collection interval to 45 seconds as requested. 

From the docs:
> The collector will try to run the check every X seconds but the check might need to wait in line, depending on how many integrations are enabled on the same Agent. Also if the check method takes more than X seconds to finish, the Agent will notice the check is still running and will skip its execution until the next interval.

### Bonus Question
- Can you change the collection interval without modifying the Python check file you created?

The answer is yes (see item above). By changing the check's yml file you can change the default polling interval (15sec) to a different interval


# Visualizing Data

- Name of the Timeboard: Exercise Timeboard

- Script: I did the most basic thing using bash. I downloaded the timeboard using a simple curl command, edited the title of the timeboard and uploaded it again using the script below (using curl again)

``` bash
curl -X POST -H "Content-Type: application/json" -H "DD-API-KEY: ae9774213091cc6286446962c9de0fa6" -H "DD-APPLICATION-KEY: XXXXXXXXXXXXX" -d @dashboard.json "https://api.datadoghq.com/api/v1/dashboard"
```

- Added a widget with the custom metric
- Added a widget with MySQL Integration and anomaly function
- Added a widget with the rollup function applied

I also did:
- Set the timeboard timeframe to past 5 min (and that was odd... I had to manually set the time by selecting a window in a widget, I was not able just to write 5min on the time picker)
- I took a snapshot and sent it to myself (pretty cool feature I might add)
(SCREENSHOT SNAPSHOT)

### Bonus Question
What is the anomaly graph displaying: My chart is not that interesting since the metric I selected does not vary that much. When I created a chart with my custom metric, things changed. The chart displays the selected metric and the expected range of values based on the algorithm that looks at past performance, previous performance at a particular time of the day, trends, etc. The expected performance range is then represented by the gray area. The metric timeseries will also change its color from blue to red if the value is considered anomalous (i.e. above or beyond the expected range)

![dashboard](/custom_metric_anomaly.png)

# Monitoring Data
I did create the monitor asrequested:
- Monitor Name: My_Metric Value Too High
- Configured the thresholds
- Configured No Data option
- Created the alert message with different content depending on the type of notification
- Added the host and metric value in the message

Here's the threshold configuration
SCREENSHOT XXXXXXXXXXXXXXXXXXXXXXXXXXX

Here are the different messages according to severity and the host/ip/metric values
SCREENSHOT XXXXXXXXXXXXXXXXXXXXXXXXXXX


## Bonus Question
2 Downtime Configurations
  - 1 Silence alerts from 7pm to 9am, M-F
  - 1 Silence alerts on Saturdays and Sundays
  - Screenshot 
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


# APM

I instrumented two apps:
Spring Pet Clinic (no code change, just using regular auto instrumentation)
Sample Flask App

Here’s the code for Flask App:

```python

from flask import Flask
import logging
import sys
from ddtrace import tracer

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@tracer.wrap()
@app.route('/')
def api_entry():
	return 'Entrypoint to the Application'

@tracer.wrap("apm",service="exercise-svc")
@app.route('/api/apm')
def apm_endpoint():
	return 'Getting APM Started'

@app.route('/error')
def errpr_endpoint():
	span = tracer.trace('operation')
	span.error = 1
	span.finish()
	return 'ERROR'

@app.route('/api/trace')
def trace_endpoint():
	return 'Posting Traces'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5555')

```

Here's the dashboard:
![dashboard](/apm_infra.png)

The Spring Pet Clinic app monitoring was a breeze. Just configured the -javaagent option (and the service name) and I was quickly able to see traces, metrics, maps, etc.

In a nutshell, a service defines an “ application” as it groups assets related to the application (db queries, endpoints, etc) and a resource is one of the “ components”  of a service (maybe a query, an instrumented endpoint, etc)

# Final Question
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Well, Datadog offers all the alternatives of a modern observability platform, with metric timeseries, logs and traces... there's a multitude of options here. In the past, I created little projects that consumed data from Weather websites and saved in a timeseries database. I also collected temperature and humidity from sensors (using a raspberry pi) to plot the variations in temperature inside my house. I had a fun project with a friend where we collected information from a car ECU via OBD2... Datadog could be the recipient of the data I collected via sensors and APIs
Possibilities are limitless! :D

---

### Comentary

I decided to experiment with the Datadog platform and tried different components and things that were not in the scope of the exercise. I will add my comments and notes here:

#### Free Tier vs Paid Account
My trial expired and my account was converted into a free account - I expected to lose access to APM. Turns out, your free tier is more flexible than what expected. The free tier docs point to an Infra only solution, but I was able to use a lot more stuff.

Free tiers are an interesting proposition, I see the newer/smaller vendors offering somewhat generous free tiers with full access to a lot of functionality... and some won't even set a temporary deadline for the free tier. The more established players tend to give temporary access to features and then a pay wall or a "talk to the Commercial Sales Rep" to continue. Later Matt re-enabled my account and I was able to continue with my exercise.

#### APM 
I started the exercise picking up the simple and traditional "spring-petclinic" to understand how the datadog agent works and what metrics it offers out of the box. The setup is pretty simple, using the standard -javaagent tag and the information just showed up in the UI as expected. Comments:

- It is interesting to see how opened the agent is. And that includes the instrumentation technology (ByteBuddy), that is not proprietary... in fact, it seems to be supported and sponsored by other vendors. Having a proprietary instrumentation engine can be a differentiator (if you do it right), but it can also demand a lot of engineering resources... a common engine has its cost of development/maintenance shared among its users.

- The profiling options are pretty neat, I like the amount of data that was captured and, more importantly, how it was displayed and the tooling to slice/dice the data. The Java Flight Recorder spec opened the door to some interesting functionality
- JVM metrics (via JMX) seem to report fine, no surprises there
- The Service Map populated well. I was curious on how I could add extra instrumentation to add a service that is not supported to the map... for the cases where the instrumentation was not added (or did not exist). I was not able to find the proper API or library to do so... unless the expectation is to use the distributed tracing for that.
	- This is not the most common use case, I am just used to doing it and the instrumentation APIs from vendors I am familiar with give a lot of leeway. Maybe I just did not find the right way. Are the regular metrics generated based on traces?

	- The metric count seemed small. Discounting the supportability metrics, I expected to see more metrics... but again, this might just be my bias to previous products I used in the past
	- I liked that one of the services (H2 database) was treated like a first class citizen and got his own page with a breakdown of recent queries
- I then tried to repeat the exercise using an "agentless" approach (manual instrumentation/micrometer)
	- I had mixed results (or maybe I had a biased expectation)
	- I was able to manually instrument the application using micrometer to send metrics to Datadog (app.hitcount, app.mygauge - APM and Infra Timeboard)
	- I was not able to get the traces reported without using the datadog agent. In fact, it is not clear to me that this is even an option (was not able to find details on doc)
	- While this is not a big deal, I've worked with a lot of customers that don't want add the agent (for risk, support, performance) and agentless option seems to be getting traction.
		- Again, the new vendors are pushing customers hard on the "self instrument" (open tracing, open instrumentation) so they don't have to build agents... that seems to be an interesting trend and debate
		- Manual instrumentation gives you full control of what is reported and that is great. Turns out, you have to really instrument your code... it is a lot of work and there's no guarantee that your developer will do it right. 
		- Auto instrumentation is fantastic, but you tie you telemetry to a vendor... and there's the agent overhead discussion that always follow an agent deployment on new customers
	- Once I added the javaagent tag, everything reported as expected.

#### Logs
- I also tested the APM-Log-Trace integration
- I made the changes to the app (they were minimal) and was able to see the ids being added to my local files. I decided to go the easy way and just added properties to my logback file... the manual log/trace injection can represent a lot of work
- Other vendors actually instrument the log packages, and with a tweak of the pom/maven you get the integration running
- I pointed the agent to tail the app log and got the logs reported and correlated with the application and traces
- The whole process was painless and relatively simple
- I have some opinions about APM and logs. I think logs are not the most effective way to get application telemetry reported... I understand why customers want it and love it, but in an ideal world we should not log everything...we should just plan and implement the instrumentation to report the errors in a more effective and useful way. Logs on APM are probably more useful for legacy apps or apps where the customer doesn't own or doesn't have access to the code... logging them becomes an invaluable tool. If you are building your cloud native app from the scratch and you think about observability, then logs should play a smaller role. (IMHO, of course :D )

#### RUM
- I used the same petclinic application for the RUM evaluation
- The RUM agent setup is quite simple and straightforward, I used the bundle option
- I was not able to find (and I assume it is not an option) an "auto-instrumentation" option where the APM agent injects the Js into the pages being served
	- Auto instrumentation for browsers is tricky, a lot can go wrong when the APM agent injects the JS snippet.
	- When it works though, it is pretty cool and seamless
	- I did not find hooks on APM to have the agent deploying injecting the JS snipped, it does not seem to be an option
- The application was quite simple and was not a "SPA" (Single Page App) with a lot of Ajax calls... I think I was not able to see some of the ajax metrics, but I assume they are tracked just fine
- Most of the RUM/Browser monitoring tools leverage the same W3C WebTiming APIs and the metrics will not vary too much
- I did like the session traces and the visualization options


#### Synthetics
- I did setup a simple test on cbc.ca just to look at the setup process.
- Again, pretty simple and straightforward
- I am quite impressed with the Browser Test (Web Page)  recording capabilities. The Chrome Extension is a great addition and makes the whole test creation/recording a breeze. Manually creating scripts for UI test is a time-consuming (and mind-numbing) process
- On the other hand though, the API test seemed too simple. A basic URL check with basic assertions is a bit limiting to my taste. For API checks, having access to a scripting language is extremely powerful
- In a way, it seems like the Synthetics solution hides the complexity of creating synthetic monitors. It can be a good or bad thing, it just depends on the use case you are trying to cover.

#### Integrations
- I want to look at some of the basic integrations and decided to deploy a NGINX server in front of the petclinic app
- The integration setup was straightforward, and I like how most of the integrations are prepackaged on the agent... you just need to copy a file, change it a bit and you are up for business
- I did configure the log forwarding option, but my account has no log at this point, not sure if everything is working fine
- I also installed the MySQL integration as requested by the exercise. Again, pretty straightforward
Docker
- I deployed the docker agent into my local workstation just for a quick test. All good there, nice and easy.

#### Kubernetes
- I had access to an IBM Cloud account where I configured a small K8 cluster.
- I  did  set up the agent there... Setup was clean and well documented.
- I had only one small cluster, but I was wondering how easy it is to manage large clusters with hundreds of pods. I think this is where tagging/labeling and that honeycomb UI become handy

#### Alerts (or Monitors) and Automation
- I think Monitors (Alerts) is the part of the product that impressed me the most
- The sheer number of different options of monitor types, added to the configuration.
- Even simple things like the notification messages with templating and a few logic operators... it is simple yet very powerful
	- Even the most basic monitors can have functions applied to them, pretty cool

- As part of my Monitor test, I decided to spend some time looking into the APIs and the "Monitoring as Code" options
	- I created a simple Terraform configuration to create a monitor...
	- Creating alerts/monitors is a tedious and labour intensive process, automating the creation/maintenance as much as possible enforces uniformity and tends to decrease the headaches.

#### Infrastructure (or core datadog-agent)
- I started the test using my raspberry pi. I have an old version and ran into some issues... decided to move tests to a regular VM
- Install is a breeze
- I like how the agent is "modular", and pretty much all the optional functionality is right there... it is just one yaml file (or python script) away from delivering value
- The statsd options make the agent super flexible and allows for dozens (if not hundreds) of integrations to be created quite easily... It is pretty neat the way it was built
- As I mentioned in the kubernetes entry, the impression I got is that the core agent and the infra product really shines in large infrastructures. I like how everything on Datadog can easily have a tag applied to it and the tag can be used to slice/dice/group/arrange the data.



---
