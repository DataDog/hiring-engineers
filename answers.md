# DataDog Solutions Engineer Technical Challenge Answers
The information below summarizes the experience and code written for the technical challenge for the Datadog Solutions Engineer role.
## Prerequisites - Setup the environment
In order to expedite the process, rather than using Vagrant, I opted to use VirtualBox with a fresh install of Ubuntu 18.04.
## Collecting Metrics
### Tasks

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
<img src="https://github.com/alexgabriel-ca/hiring-engineers/blob/master/DatadogMapwithTags.png" />

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
<img src="https://github.com/alexgabriel-ca/hiring-engineers/blob/master/TimeboardScreenshot2.png"/>

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

```python
import random

for x in range(1):
	my_metric = random.randint(1,1001)

# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class MyValueCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric',my_metric)
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

```python
instances: [{}]

init_config:

instances:
  - min_collection_interval: 45
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
## Visualizing Data
Utilize the Datadog API to create a Timeboard that contains:
* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

```bash
#!/bin/sh
# This script is part 1 of the requirements for the Datadog Technical Exercise

api_key=9d6d81e95d0d9417bb7a6d321a517a5a
app_key=f05603588fcbc601e37765a02f03564559863e01

curl -X POST -H "Content-type: application/json" \
-d '{
"title":"Technical Exercise Timeboard v3",
"description":"Created today",
        "graphs":[
{
                "definition":{
                    "viz":"timeseries",
                    "requests":[
                        {
                            "q":"avg:system.cpu.user{*}",
                            "style":{
                                "palette":"dog_classic",
                                "width":"normal",
                                "type":"solid"
                            },
                            "type":"line"
                        }
                    ]
                },
                "title":"System Load Over Time"
            },
            {
                "definition":{
                    "viz":"timeseries",
                    "requests":[
                        {
                            "q":"avg:my_metric{role:database} by {host}.rollup(sum, 60)",
                            "style":{
                                "palette":"dog_classic",
                                "width":"normal",
                                "type":"solid"
                            },
                            "type":"area"
                        }
                    ]
                },
                "title":"My_Metric with Rollup"
            }
        ],
        "template_variables":[
        ]
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"

# Notes: JSON for the third portion does not work when submitted against the API.  The code was taken directly from both the UI and a query to get JSON data.
# The following snippet causes an error when added to the graphs section:
# Error message:
#{"errors": ["Error parsing query: unable to parse anomalies(avg:mysql.net.connections{role:database}, basic, 2): Rule 'scope_expr' didn't match at ', 2)' (line 1, column 58)."]}
#,
#         {
#            "definition":{
#               "viz":"timeseries",
#               "requests":[
#                  {
#                     "q":"anomalies(avg:mysql.net.connections{role:database}, 'basic', 2)",
#                     "style":{
#                        "palette":"dog_classic",
#                        "width":"normal",
#                        "type":"solid"
#                     },
#                     "type":"line"
#                  }
#               ]
#            },
#            "title":"Aborted Database Connections"
#         }
```

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes.
*I was unable to set this using the UI.*
* Take a snapshot of this graph and use the @ notation to send it to yourself.
*I was unable to accomplish this using the UI.*

* **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data
* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

<img src="https://github.com/alexgabriel-ca/hiring-engineers/blob/master/MonitorScreenshot.png" />

## Collecting APM Data
* I was unable to complete this task.  I tried the following code
* Node.js
```node.js
const tracer = require('dd-trace').init()

const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

var StatsD = require('node-dogstatsd').StatsD;
var dogstatsd = new StatsD();


const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

dogstatsd.increment('page.views')

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```
* Node.js with Express

```nodes.js
const express = require('express')
const app = express()
const port = 3000
const tracer = require('dd-trace').init({ plugins: false })
tracer.use('express')

var StatsD = require('node-dogstatsd').StatsD;
var dogstatsd = new StatsD();

app.get('/', (req, res) => res.send('Hello World!'))
app.listen(port, () => console.log(`Example app listening on port ${port}!`))
```
* Python

```python
print('Hello, world!')
```
* Java
```java
import java.io.Console;

public class Datadog {

    public static void main(String[] args) {
        for (int i = 1; i < 1000; i++) {
            System.out.println("Datadog test.");
        }
        Console c = System.console();
        if (c != null) {
            // printf-like arguments
            c.format("\nPress ENTER to proceed.\n");
            c.readLine();
        }
    }
}
```

* In each test of the above code, no APM data was visible in the UI.
* **Bonus question**
A service is a set of processes that run do the same job.  I.e. Apache load balanced across multiple web servers.
A resource is a portion of the service. I.e. /content/application on a Tomcat server.

### Final Question
* Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!  Is there anything creative you would use Datadog for?

I have a significant amount of exposure and experience in the medical field, so I can definitely see value in monitoring many different types of systems in the medical industry.  Immediate applications that come to mind in cardiology or combining Datadog with biometric monitoring applications via wearable technology.
