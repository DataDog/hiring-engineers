# Prerequisites - Setup the Environment

I used the **macOS** environment to complete this exercise.

1- I created my account on https://www.datadoghq.com/
2- To install the **Agent** on my machine I chose the **Mac OS X** platform from the menu list because I'm using the macOS environment and copied this installation command (I removed the API KEY value from the command below to make sure that I don't expose it, and hid it using a black banner on the screenshot image below): 


`DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<API KEY> DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"` 
![Agent Installation](/images/img1.png)

3- From here I was able to access the **Datadog Agent Manager** and check the Agent reporting metrics.

![Agent Status](/images/img2.png)

![Agent Logs](/images/img3.png)

# Collecting Metrics
## Adding Tags
I added tags in 2 ways by checking [Getting started with Tags](https://docs.datadoghq.com/getting_started/tagging/):
1- Manually using the configuation file where I search for the **tags** section and added 2 tags there and restarted the agent.

![Tags1](/images/img4.png)


2- Using the UI of the Host Map Page. I added 1 new tag

![Tags1](/images/img5.png)

## Database Installation
1)I decided to install and work with **MongoDB**.
 I followed the [official mongoDB documentation](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/) to install mongoDB community edition on my     local machine. <br>
 - I installed it with **brew** using these 2 commands:
  `brew tap mongodb/brew` <br>
  `brew install mongodb-community@4.4` <br>
  
  I started the MongoDB service using `brew services start mongodb-community@4.4` and to make sure that its running I used this command `brew services list`<br>
  
  ![MongoDB Started](/images/img6.png)
  
## Datadog and Database
Now that I have MongoDB installed on my local machine, I need to install its corresponding Datadog Integration. I followed this [official Datadog document](https://docs.datadoghq.com/integrations/mongo/?tab=standalone) for the MongoDB integration.
I opened the **Mongo Shell** in the terminal using the command `mongo` and created a database with a read-only user.

```
#This creates a database named admin if it doesn't exist and starts using it
use admin 

# On MongoDB 3.x or higher, use the createUser command.
db.createUser({
  "user": "datadog",
  "pwd": "khalil22",
  "roles": [
    { role: "read", db: "admin" },
    { role: "clusterMonitor", db: "admin" },
    { role: "read", db: "local" }
  ]
})
```
![MongoDB Shell](/images/img9.png)


Now I need to configure the **Agent** running on the host. I edited the `mongo.d/conf.yaml` in the `conf.d` folder by adding the coressponding values and restarted the agent.

![MongoDB Config](/images/img7.png)

I was able to see that the mongoDB is succesfully integrated with Datadog. It was added to the Host Map and its status shows **OK**.

![MongoDB Status](/images/img8.png)

I added a **MongoDB Dashboard** by going to the **Dashboard** menu and installing it from there and since it's already integrated I was able to see the mongoDB metrics on the dashboard.
![MongoDB Dashboard](/images/img10.png)

## Cutsom Agent Check

I followed this official Datadog [documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) to create a custom agent check.
I created a file called `my_metric.py` in the `check.d` folder that is inisde `datadog-agent` directory. I took the example code of the documentation and modified it so it can generate a random number between [0,1000]. I used the `randint` function ot generate the random numbers.

```python
import random # to use the randint function

# the following try/except block will make the custom check compatible with any Agent version

try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```  
Next I created `my_metric.yaml` file in the `conf.d` directory. Here we need to make sure that the name of the python file matches exactly the name of the yaml file. So both need to be named `my_metric` in this case. I added the following lines the `my_metric.yaml` file:
```yaml
instances: [{}]
tags:
  - metric:my_metric
  - env:dev
```

Now that both the python file and the yaml configuration file of this custom metric are created, it's time to check if its working. I used this command to validate my custom metric `datadog-agent check my_metric` and it gave a succesful result.

![MongoDB Dashboard](/images/img11.png)

## Changing the Collection Interval
To change the collection interval, I reopened the `my_metric.yaml` configuration file and added a `min_collection_interval` parameter with the value `45` under `instances`.

```yaml
instances:
  - min_collection_interval: 45
tags:
  - metric:my_metric
  - env:dev
```

**Bonus question**: Yes we can change the collection interval without modidying the python file created. Just like I did right now, I changed it directly from the YAML configuration file.







