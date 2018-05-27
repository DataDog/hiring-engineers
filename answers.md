## Prerequisites - Setup the environment

On my first attempt, I chose to use Vagrant to configure an Ubuntu 12.04 LTS VM.  While the initial set up was straightforward I ran into issues when attempting to use the Datadog API.  This was before I began tracking issues, therefore I don't have detailed logs.  

Essentially, I had problems when attempting to download the datadogpy library via pip.  The error was that pip could not find any library named datadog, even though I verifed the package at pypi.org.

I wanted to use an an official Datadog library, however after being unable to proceed, I decided to try the third party node-dogapi library.  Unfortunately I was running into issues again, this time with installing node and npm.

Ultimately I suspected the problem might be due to the older version of Ubuntu and decided to try a more recent version.

[I chose Ubuntu 16.04 LTS as my host running on VM Virtual Box](https://p.datadoghq.com/sb/7af5f9814-243e179005f19f7df668a6d7dad75b3c)

I already had Virtual Box with Ubuntu instlled my local machine.  There are many [tutorials online](https://linus.nci.nih.gov/bdge/installUbuntu.html) on how to get this up and running.

![alt text](https://github.com/mjmanney/hiring-engineers/blob/solutions-engineer/images/vbox.PNG "Virtual Box")

Next, I installed CURL by opening a terminal and entering the command:

```sh
sudo apt-get install curl
```
which allowed to install the Datadog agent with:

```sh
DD_API_KEY=<MY_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

At the datadog agent root directory edit the config file datadog.yaml.  Note that the Datadog docs recommend to use the yaml list syntax as below:

``` yaml
# Set the host's tags (optional)
tags: mytag:newhost, env:prod, role:database
```

My custom newhost tag appears in the Hostmap, alongside the automatically generated tags.

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/solutions-engineer/images/hostmap.PNG "Host Map with custom tags")

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose to integrate MongoDB with my Datadog agent.  [Instructions can be found on mongodb's documentation.](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/solutions-engineer/images/mongo.png "MongoDB")

After mongodb was installed on the machine I began the integration with datadog.

In terminal run the command `mongo` to access the mongo shell.

Once inside the mongo shell create a read-only user adminstrator for data dog:
```sh
# MongoDB 3.x

# use the admin db
use admin

db.createUser({
  "user":"datadog",
  "pwd": "<CREATE-MY-PASSWORD>",
  "roles" : [
    {role: 'read', db: 'admin' },
    {role: 'clusterMonitor', db: 'admin'},
    {role: 'read', db: 'local' }
  ]
})
```

Verify the user you created with: 

```sh
echo "db.auth('datadog', '<PASSWORD>')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" &&
echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"
```

If everything works properly the terminal will echo the message `datadog user - OK`

Lastly, configure the Datadog Agent to connect to connect to the mongodb instance. 

Edit the config file at datadog-agent/conf.d/mongo.d/mongo.yaml (Agent v6)
I also added some custom tags.

``` yaml
init_config:

  instances:
    - server: mongodb://datadog:<PASSWORD>@localhost:27017/admin
      additional_metrics:
        - collection       # collect metrics for each collection
        - metrics.commands
        - tcmalloc
        - top
      tags:
        - myMongoDB
        - metricsDB
```

Restart the datadog agent with:

```sh
sudo service datadog-agent restart
```

and get the status of the integration with (Agent v6):

```sh
sudo datadog-agent status
```

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/dd_status_mongo-metric.png "Mongo integration status")


## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Custom checks should be placed in the checks.d directory at the datadog-agent root.

datadog-agent/checks.d/my_metric.py

``` python
#import dd AgentCheck
from checks import AgentCheck

#import randit
from random import randint

class myCheck(AgentCheck):
    def check(self, instance):
        x = randint(0, 1000)
        self.gauge('my_metric', x)
```

## Change your check's collection interval so that it only submits the metric once every 45 seconds.

## Bonus Question Can you change the collection interval without modifying the Python check file you created?
This can be done by altering
datadog-agent/conf.d/my_metric.yaml
``` yaml
init_config:

instances:
    -    host: localhost
         min_collection_interval: 45
         name: my_metric
```
