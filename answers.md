# Solution Engineer Technical Exercise Submission - Pabel Martin

Here are my answers for this technical exercise along with all supporting links, screenshots, and color commentary.

What will be fairly obvious is that this exercise was fun to get through, but **very** challenging.  For better or worse, almost all of this was a first for me in many areas:
  * I'd never heard of Vagrant, Flask, YAML, or Markdown until working on this exercise
  * I've heard of Python, Ubuntu, MongoDB, and GitHub prior to this exercise, but have never worked with any directly
  * The only thing I'd done before that was a part of this exercise was google liberally (always) and execute some command line stuff (years since I'd done this) so I was pretty rusty.
  
If I had to characterize what it was like to go through this, I would say that it was just brute force trial and error.  Throughout the whole exercise I was reminded me of the scene in the Matrix where Neo first sees Matrix code 'falling' on the monitor and asks Cypher if he always looks at it encoded. Cypher responds that he has to because of all the information coming through but that he's used to it and now just sees the people in the matrix that the code represents.  In this exercise, it felt like all I ever saw was green falling code.  Eventually after following enough instructions and steps it worked, but I honestly don't fully know how or understand the details of how/why everything worked.

![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/scene1.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/scene2.png)

This submission, for example, is something I've never done before.  I had a developer friend walk me through GitHub and what forks, commits, branches, pull requests, and markdown were and how they were used.  I haven't had experience with any of these to-date so I used [this](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) and [this](https://stackoverflow.com/questions/2822089/how-to-link-to-part-of-the-same-document-in-markdown/16426829#16426829) to create this submission.  It's entirely possible I haven't submitted as expected on the right branch so enjoy a chuckle if I didn't even get this first part right.  :)

You'll also see this in the submission, but two major mistakes for me were not coming back to the main exercise GitHub page.  I missed the update to use Ubuntu 16.04 instead of 12.04 as well as the update to the Flask app for host name.  If I'd seen that, I would have saved myself a ton of grief/time; a mistake I'll strive to only make once.



## Table of Contents

  * [Setup the Environment](#setup-the-environment)
  * [Collecting Metrics](#collecting-metrics)
  * [Visualizing Data](#visualizing-data)
  * [Monitoring Data](#monitoring-data)
  * [Collecting APM Data](#collecting-apm-data)
  * [Final Question](#final-question)
  


## Setup the Environment

I followed the steps outlined in the **Setting Up Vagrant** link from the Reference section and setup Vagrant on my Macbook Pro.  The exercise page as of 5/27/18 when I started referenced setting up a machine with Ubuntu 12.04 so I used the 'precise' argument in the command line referenced in the [Vagrant Getting Started](https://www.vagrantup.com/intro/getting-started/) page.

This caused an issue later on in the exercise when trying to install MongoDB and Flask as it kept hitting issues/errors from dependencies.  I upgraded the box manually to Ubuntu 14 and that helped clear the MongoDB issues.  I still hit issues installing Flask later on that I couldn't get past so I was back on the exercise's GitHub page trying to find a workaround.  That's when I noticed that it was updated to reference Ubuntu 16.04 so I started the exercise from scratch with a new box on that version.

These screenshots will show the details of my Datadog trial account along with the Infrastructure List page showing both boxes I configured.  The configuration files documented below are the same on both boxes for the datadog-agent so I've only included one copy for review.

![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/DDenv.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/infrahostlist.png)


## Collecting Metrics

### Datadog Agent and Tags

I followed the instructions in the datadog docs [page for the agent](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/), as well as the instructions in the datadog app for my trial account.

I navigated to /etc/datadog-agent and used sudo vim datadog.yaml to update the file.  It took some googling and longer than I'd like to admit to remember how to do that and use vim to edit and save the file.  I commented out the dd_url line, api_key, and tags section.  I added three tags to each host for location, environment, and role.  See screenshots and snippet of the datadog.yaml file below.

```
# The host of the Datadog intake server to send Agent data to
dd_url: https://app.datadoghq.com

# The Datadog api key to associate your Agent's data with your organization.
# Can be found here:
# https://app.datadoghq.com/account/settings
api_key: dc32e242694d198af81287e6ee9461b6

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


### MongoDB Installation and Integration Configuration

I followed the instructions on the [Mongo site to install community edition](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).  As previously mentioned I had to do this twice because of the two different hosts I created on different versions of Ubuntu.

I then used the instructions in the [datadog integration page in my trial account](https://app.datadoghq.com/account/settings#integrations/mongodb) and the [Docs section for Mongo](https://docs.datadoghq.com/integrations/mongo/) to configure the agent.  I google'd to find Mongo shell commands for user creation.  I had never worked with YAML before so it was a lot of trial and error using this [YAML interpreter](http://www.yamllint.com/) to get the proper conf.yaml file to recognize my Mongo server and collect metrics.
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

One thing I could never resolve were errors related to Mongo.  It seems as if two configurations are there for mongo on both services.  The host shows 'mongo' and 'mongodb', and while 'mongodb' always had successfull checks and metrics, 'mongo' always has errors associated with it.  Checking the datadog agent status and tailing the logs for the agent always revealed the same 'server is missing' error.  I imagine it's something that's misconfigured, but I could never figure out where the issue was.  That said, the one collector functioned as expected and returned the data needed to complete these steps. See screenshots.
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/mongoerrors1.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/mongoerrors2.png)

### Custom Agent Check

To complete this section I used the [writing agent check section in datadog docs](https://docs.datadoghq.com/developers/agent_checks/), [this page](https://datadog.github.io/summit-training-session/handson/customagentcheck/) for a sample of a check, and [this page](https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/) for how to generate a random number in python.

As mentioned before, I don't have much of this in my background so this was the first python file/script I ever created and run.  I'm not sure, nor would I want to admit, how long it took me to get this part done.
```python
from checks import AgentCheck
import random

class MyCheck(AgentCheck):

    def check(self, instance):

        self.gauge('my_metric', random.randint(-1,1001))
```
I confirmed this was working as expected by using the metrics explorer and searching for my_metric.  I also noticed that it appeared on the hosts under 'no-namespace' as well as in the datadog agent logs under 'mycheck'.

To change the collection interval, I referenced the datadog docs which had a section for configuring a custom written check.  The combination of that, the YAML interpreter, a lot of trial and error, and tailing the agent log led to confirming this worked as expected.  Here's the mycheck.yaml file from /etc/datadog-agent/conf.d:
```
init_config:

instances:
    #[{}]
    [{min_collection_interval: 45}]
```


### Bonus Question
Based on this section from the datadog docs section, I changed the collection interval for my custom check using the YAML config file.  Given that I didn't have to change the Python check file I created, I believe the answer to this bonus question is **Yes**.
>For Agent 5, min_collection_interval can be added to the init_config section to help define how often the check should be run globally, or defined at the instance level. For Agent 6, min_collection_interval must be added at an instance level, and can be configured individually for each instance.


## Visualizing Data
To complete this section, I took the approach detailed below.  I'm not sure if it's 'cheating', but given my lack of development background this was the only path I saw to getting this done.

I created a dashboard in my environment via the UI ([link](https://app.datadoghq.com/dash/822625/ui-created-timeboard?live=true&page=0&is_auto=false&from_ts=1528137594823&to_ts=1528141194823&tile_size=m)) with all the elements called for, plus a few others just to familiarize myself with the functionality.
![alt text]()

Once this was completed and working appropriately, I used to the [API timeboard docs](https://docs.datadoghq.com/api/?lang=python#timeboards) to get sample requests/responses.  I also got the API and APP keys from the API section in the datadog trial account environment.  I created a python script to get all timeboards in order to get the definition I needed.  It didn't bring back all the definitions, but did give me the ID.
```python
from datadog import initialize, api

options = {
    'api_key': 'dc32e242694d198af81287e6ee9461b6',
    'app_key': '9ae728793d0bddbb5effc3768fd58ed459a96a33'
}

initialize(**options)

print api.Timeboard.get_all()
```
Then I used a python script to pull a specific timeboard an entired the ID I got.
```python
from datadog import initialize, api

options = {
    'api_key': 'dc32e242694d198af81287e6ee9461b6',
    'app_key': '9ae728793d0bddbb5effc3768fd58ed459a96a33'
}

initialize(**options)

print api.Timeboard.get(822625)
```
I received the [following output]() which contained all of the definitions of the graphs I successfully created in the UI.

I used that information as a guide to creating a python script to leverage the create a timeboard API.  I used the sample request and made adjustments specific to the exercise requirements and changed titles so it was clear that the dashboard was created via the API.
```python
from datadog import initialize, api

options = {
    'api_key': 'dc32e242694d198af81287e6ee9461b6',
    'app_key': '9ae728793d0bddbb5effc3768fd58ed459a96a33'
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
![alt text]()

Using the keyboard shortcut, I changed the API created timeboard to display the past 5 minutes.
![alt text]()

I used the camera icon on my MongoDB graph to take a snapshot and send the notification to myself via @mention.
![alt text]()

### Bonus Question
The graph with anomaly applied is displaying when any metric is out of range of what's expected based on historical values.  My particular graph is set to show anomalies outside of 3 deviations from norm.  This could potentially help determine if/when there is something wrong as the algorithm accounts for seasonality and historical trends.


## Monitoring Data


## Collecting APM Data


## Final Question




