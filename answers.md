## Prerequisites - Setup the environment
After struggling with mystery network connectivity issues when using Vagrant, I decided to spin up my test VM in AWS EC2 as I have experience there and Amazon does make it easy to create mini sandboxes. So, I logged into AWS and spun up a quick t2.micro instance for free. This is really easy once you have your account set up, key pairs set up, users set up, etc. Here's a quick video:

![AWSEC2creation](https://s3.amazonaws.com/datadoganswers/awsec2spinup.gif)

So, I've signed up for Datadog and spun up an Amazon Linux virtual machine in EC2. I'm ready to collect some metrics. 

## Collecting Metrics:
After installing datadog via the one-step shell script with curl command, I started to edit the config files in order to add tags for my host.

![Agentconfigfile](https://s3.amazonaws.com/datadoganswers/tags_datadog.yaml.png)

To confirm this had worked properly, I could log into the Datadog console and view the host map with tags.

![Hostmapwithtags](https://s3.amazonaws.com/datadoganswers/tags_infra_host_map.png)

The next step was to install a database of some sort. At Percona I dealt with MySQL, MongoDB, RDS, and PostgreSQL. I wanted to try something that maybe has not been tried too many times, so I installed Percona Server for MySQL which is a drop-in replacement for MySQL and functions the exact same way as MySQL. 

I added some databases and tables to my database and ran sysbench to get some metrics reporting which were visible from the console.

![MySQLIntegration](https://s3.amazonaws.com/datadoganswers/MySQL_integration.png)

The MySQL yaml file and agent config check are below as confirmation that this integration was configured correctly and reporting.

![MySQLyaml](https://s3.amazonaws.com/datadoganswers/MySQL_conf_yaml.png)
![MySQLagentstatuscheck](https://s3.amazonaws.com/datadoganswers/MySQL_agentstatus_check.png)


After the MySQL integration, I worked on the random metric - "mymetric". Below is the yaml config file for my_metric to run on all hosts.

```yaml

init_config:

instances:
    [{}]

```

The python script to measure my_metric and retrieve a number between 0 and 1000 is below.

```python

import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))

```

Implementing this check took some trial and error, but I eventually got it working. The datadog-agent check was helpful in diagnosing what was wrong. A lot of it boiled down to getting the python randint function performing as expected.

![randomcheckcheck](https://s3.amazonaws.com/datadoganswers/random_check_check.png)

#### Bonus Question

In order to change the custom check to only submit once every 45 seconds, I modified the random_check.yaml file. The collection interval is the variable to tweak for this and avoids having to edit the python script.

![collectioninterval](https://s3.amazonaws.com/datadoganswers/modified_yaml_collection_interval_45.png)


## Visualizing Data:

I created a shell script and used curl to interact with Datadog API to create my custom Timeboard. This involved some trial and error mainly with formatting in the curl command. I can see this being an extremely valuable feature in large organizations and it would interact well with already-used config management solutions such as Ansible. The script that ended up working for me is below.

```bash

api_key=b9b5d69071df017cba71307bd6ba7f9a
app_key=2bca47846c1a5fc9ffaf0f926fce82c2457886ec

curl -X POST -H "Content-type: application/json" \
-d '{"title" : "Average MySQL Connections",
     "description" : "averages",
     "graphs" : [{
         "title" : "Average MySQL Connections",
         "definition": {
  "requests": [
    {
      "q": "avg:mysql.net.connections{*}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    },
    {
      "q": "avg:my_metric{*}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    },
    {
      "q": "avg:my_metric{*}.rollup(sum, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    }
  ],
  "title": "Average MySQL Connections",
  "viz": "timeseries",
  "autoscale": true
}}]}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

```


After successfully running this script, I was able to log into the Datadog console and see my new timeboard. According to the instructions, below is a 5 minute interval with @BarrettChambers to notify me. 

![collectioninterval](https://s3.amazonaws.com/datadoganswers/snapshot.png)

#### Bonus Question

The anomaly graph is showing when a metric measured is outside of an expected average over time.

## Monitoring Data

Configuring an alarm for my_metric in the Datadog console was a painless process. I created a video that walks through each of the requirements for the alarm including both warning and alerting thresholds and messages as well as the metric measured and I chose to use host.name instead of host.ip because I was spinning up and down my EC2 instance constantly and its IP was not static. 

![alert_config](https://s3.amazonaws.com/datadoganswers/alerting_in_datadog.gif)

I set up a monitor for the my_metric metric. Here is the email screenshot:

![alert](https://s3.amazonaws.com/datadoganswers/emailalert.png)


The next step was to schedule downtime for the alerting. Here is a screenshot confirming the downtime windows via emails I received. 

![downtimemaintenancealert](https://s3.amazonaws.com/datadoganswers/datadog_downtime_alert.png)

## Collecting APM Data:

Update datadog.yaml file to allow for APM metrics:

```yaml

apm_config:
  enabled: true
  
  
  ```

I did not complete this exercise. I attempted to use ddtrace with a MySQL python connector, but was unsuccessful. Here is the script I was running that was a simple connect: 

![apm_python](https://s3.amazonaws.com/datadoganswers/APM_python_mysql.png)

I am 100% sure I am missing something here, but I'd need some more time to figure it out.

## Final Question:

As I got hands on with Datadog, I realized why it is such a popular monitoring tool. Many of Percona's customers are using Datadog for internal monitoring. The only negative thing I've ever heard is that it's expensive. :)

I think an interesting use-case for Datadog would be to actively monitor and report location data during events like concerts, festivals, or street fairs. Using a database with geospatial capabilities like MongoDB to plot this out and then using Datadog to tag and identify hotspots would allow organizers to visualize users experiences through data. This would help organizers identify hotspots and organize future events better and also react in real-time to open areas to alleviate crowd traffic. 
