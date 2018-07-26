# Environment

![Docker Logo](https://www.vectorlogo.zone/logos/docker/docker-card.png)
This testing was done on a Paperspace VM running Ubuntu 18.04. I had started with Docker on Windows which appeared adequate at first, and then caused me trouble. I learned that composed Docker stacks on a local swarm running on Windows doesn't network the same as Linux environments.

![Ubuntu on Windows](https://www.windowslatest.com/wp-content/uploads/2017/07/Ubuntu-on-Windows-10-696x348.jpg)
I then tried the "Ubuntu" available in the Windows Store. Everything worked until I discovered there is no /proc filesystem since it's not even running the Linux kernel. Not having a /proc filesystem leads to a strange lack of information when using typical Linux tools. Too much wasted time on that system!

![Paperspace Logo](https://odsc.com/wp-content/uploads/2018/01/paperspace-logo-300x168.jpeg)
Frustrated, I installed both Ubuntu locally in a Hyper-V VM and spun up a Paperspace instace. Paperspace encountered errors during provisioning, so I worked on the slow local install for a while. Once Paperspace errors resolved, their VM was significantly faster than my local machine so I stuck that. 

# Test Application

I developed a simple api with 6 resources: 3 evil, 3 nice. Since my app is based on Flask, I used the third-party trace-middleware as desribed in the [docs](https://docs.datadoghq.com/tracing/setup/python/#example-simple-tracing)

### source code in ./api/

I developed methods to post comments and events.

![event posted](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/event.png)

I installed the datadog agent using the preferred Ubuntu install script. I noticed that the provided script is prepopulated with necessary keys and that made installation a breeze.

![agent exiting](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/agent_exit.png)
Something needs fixing, the agent won't stay running. Looks like I need to enable  the agent.

I adjusted the datadog.yaml file to enable the agent and APM and added tags while I was there.
![agent exiting](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/epa.png)

![agent exiting](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/tic.png)

Then I verified that the agent was listening on the expected port:
![verified port](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/confirm_8126.png)

*note: 404 is the expected response.*

And data is coming in!

![new data](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/errors.png)

# Custom Check and Metric

I placed the following code in **/etc/datadog-agent/checks.d/** as

**my_metric.py**


```python
from checks import AgentCheck
import random
class my_metric(AgentCheck):
    def check(self, instance):
        val = random.uniform(0,1000)
        self.gauge('my_metric ', val, tags=[u'ddhee',u'maint:tmayse'])
```

I placed the following configuration in **/etc/datadog-agent/conf.d/my_metric/** as my_metric.yaml and while I was there, I skipped ahead and just configured the check to run **not more often than** every 45 seconds. 

**my_metric.yaml:**


```python
init_config:

instances:
    - host: "psh8wbmgg"
      min_collection_interval: 45
```

Checking the config **sudo service datadog-agent status**

![agent config](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/checks.png)

*pleased to find my_check listed at the top*

Timing confirmed in agent logs:
![agent config](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/45.png)

And then, as configured, the check ran:
![agent config](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/check_ran.png)

# Tags on infrastructure

As show earlier, configured tags:
![tags shown in config file](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/tic.png)

![host tags in UI](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/host_tags.png)

Bonus Question Can you change the collection interval without modifying the Python check file you created? **see config & logs above**

*in addition to the tags I configured, an automatic tag was added identifying the host*

# Database Integration

I installed Postgresql as it's generally trouble-free. One of my endpoints (/tfs) stimulates the DB.

The agent is configured by adding postgres.yaml to /etc/datadog-agent/conf.d/postgres.d/postgres.yaml

**postgres.yaml:**


```python
---
init_config:

instances:
  - host: localhost
    password: CG4W1mPaET70QWl2TrjYeAlN
    port: 5432
    tags:
      - ddhee
      - "role:db"
      - "description:DDHEE db"
    username: datadog
```

![Database Dashboard](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/db_dashboard.png)

[Link to board](https://app.datadoghq.com/screen/integration/235/postgres---overview?page=0&is_auto=false&from_ts=1532551260000&to_ts=1532554860000&live=true)

# Timeboard created by API

I needed 4 tries to get this right. I copied the graph definitions from the UI dasboard's JSON output. I found that the anomolies method requires more arguments in a Timeboard. Once I fixed that, my script worked as-expected.

**Tmeboard Script:** 


```python
#!/bin/bash

curl  -X POST -H "Content-type: application/json" \
-d @graphs.ddhee.json "https://api.datadoghq.com/api/v1/dash?api_key=e1dbdaceaf7516f90ef9e2ad5546072e&application_key=25b8d433ca6e9ca99c1ee791e8ece8c67e6a0ec3"
```

![Dashboard created by API](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/dashboard.png)


[dashboard link](https://app.datadoghq.com/dash/871365/)

# Timeboard with five minute window

This took me a while to figure out. It wasn't immediately obvious to me that a Screenboard fit the bill. When I came upon **[How to Transform a Timeboard to a Screenboard or vice versa ?](https://docs.datadoghq.com/graphing/faq/how-to-transform-a-timeboard-to-a-screenboard-or-vice-versa/)** which links to [this script](https://github.com/DataDog/Miscellany/blob/master/dashconverter.py) Once my timeboard was converted to a Screenboard, I was able to set the time to each chart to five minutes.

**here's the command line util I ran**


```python
python dash --api-key e1dbdaceaf7516f90ef9e2ad5546072e --app-key 25b8d433ca6e9ca99c1ee791e8ece8c67e6a0ec3 --titl
e "From Timeboard" 871365
```

![Screenboard Converted by scipt](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/screenboard.png)

[screenboard link](http://app.datadoghq.com/screen/393468)


**Bonus Question: What is the Anomaly graph displaying?**

It reads "Not enough historical data for this algorithm."

*note: I didn't explore other algorithms' data requirements.*

I didn't figure out how to send a screenshot, so I sent myself a URL:
![at mention for new screenboard](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/atmention.png)

The email I got as a result looked like this:
![email from at mention](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/atmentionemail.png)

# Monitoring Data

This image has all the info necessary to verify notifications: Here's what I did:

![monitor setup](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/monitorpage.png)

This is very noisy, of course. I'm glad configuring downtimes was part of the exercise.
![downtimes scheduled](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/downtime.png)

https://app.datadoghq.com/monitors/5645900

**note: For the weekend downtime, I was frustrated by an error that was telling me my start time was too early any time around midnight. I tried from 11:59PM Fri for two days, but that's clearly not right as it didn't have the desired effect. It only just now ocurred to me that the times are UTC. The email was clear about that, but I didn't read it. A better error message might say "that time is in the past", but ulitmately, this was my bad.**

![downtime](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/schedtime.png)

In addition to an email, I captured this event in the event stream:

![event in stream](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/notif.png)

I also enable suggested monitors for my API and was alerted
![hammer](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/hammer.png)

# Integrated Dashboard

https://app.datadoghq.com/dash/871420
    
Included in this dashboard are process metrics, my_metric chaos, NTP offset, and average Apdex by resource.

![App & Host metrics](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/hostandapp.png)


**Bonus Question: What is the difference between a Service and a Resource?**
A service is a group of resources. Short answer: service is essentially the application and resource is essentially it's endpoints/methods.

Here's my application's resource list:

![resource list](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/resources.png)

and here's the service to which they all belong:

![services](https://raw.githubusercontent.com/tmayse/hiring-engineers/master/images/services.png)

# Last Question

During my call with Fahim, I already volunteered call center/suport desk metrics: call volume, hold time, etc. Anomoly detection would be helpful in addition to developing a more robust view of the enterprise.

Here's a crazy idea that might just work:
All on-call engineers track their location via smartphone or whatever is available. Datadog could alert the manager if too few engineers are within rapid-response range of the office. 
