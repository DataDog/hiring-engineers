Your answers to the questions go here.

## Collecting Metrics:



* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

<a href="https://www.flickr.com/photos/147840972@N03/46831112674/in/dateposted-public/" title="host map with tag">
<img src="https://live.staticflickr.com/7915/46831112674_d15050149d_b.jpg" width="500" height="332" alt="_DSC4652"></a>


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Installed postgresql and created postgress.yaml integration file:
```
instances:
  - host: localhost
    port: 5432
    username: datadog
    password: kmEcy8FcXk6sOpZRDF2HeDxK
    tags:
      - jaime_sql
      - demo_sql
```
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
`my_metric.py`:
```
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class HelloCheck(AgentCheck):
    def check(self, instance):
        var = random.randint(1, 1000)
        self.gauge('my_metric', var)

```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
Use customer configuration file to submit the interval:

`/etc/datadog-agent/conf.d/my_metric.yaml`
```
root@precise64:/etc/datadog-agent/conf.d# more my_metric.yaml
init_config:

instances:
  - min_collection_interval: 45
```
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Using the min_collection_interval in the configuration file

