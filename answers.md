Your answers to the questions go here.

<!-- python script to send random number 0-1000 -->

# the following try/except block will make the custom check compatible with any Agent version

try: # first, try to import the base class from new versions of the Agent...
from datadog_checks.base import AgentCheck
except ImportError: # ...if the above failed, the check is running in Agent version < 6.6.0
from checks import AgentCheck

# content of the special variable **version** will be shown in the Agent status page

**version** = "1.0.0"

```
import random

class CustomMyMetricCheck(AgentCheck):
    def check(self, instance):
        randomNum = random.randint(0,1000)
        self.gauge('random.number', randomNum, tags=['RandomKey:RandomValue'])
~
~
~
~
"custom_my_metric.py" 17L, 668C

```

Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

using the DataDog Postman API package I generated the Tiemboard using the Dashboard Post endpoint

```
{
    "title": "API TIMEBOARD SINGLE GRAPH w/style",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{*} by {data_cat}.rollup(sum, 3600)",
                        "style": {
                            "palette": "warm",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "avg:my_metric{*}",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "anomalies(avg:postgresql.db.count{*}, 'basic', 2)",
                        "style": {
                            "palette": "orange",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    }
                ],
                "title": "My Metric - Roll up 1hr (3600 sec), Instance, PostgreSQL DB Size: Anomaly fn"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "Timeboard API",
    "is_read_only": true,
    "notify_list": [
        "J.Tustin@gmail.com"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "vagrant"
        }
    ]
}
```

Bonus Question: What is the Anomaly graph displaying? -

DD_SERVICE="sample-app" DD_ENV="dev" DD_LOGS_INJECTION=true DD_TRACE_SAMPLE_RATE="1" DD_PROFILING_ENABLED=true ddtrace-run python sampleApp.py

start python env
source my_env/bin/activate

https://docs.datadoghq.com/tracing/visualization/
Service Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of building your application.
Resource Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.

APM App

```
const tracer = require('dd-trace').init(DD_ENV="sampleAppNode", DD_LOGS_INJECTION=true, DD_TRACE_SAMPLE_RATE="1")
const http = require('http');

// Create an instance of the http server to handle HTTP requests
let app = http.createServer((req, res) => {
    // Set a response type of plain text for the response
    res.writeHead(200, {'Content-Type': 'text/plain'});

    // Send back a response and end the connection
    res.end('Hello World!\n');
});

// Start the server on port 3000
app.listen(3000, '127.0.0.1');
console.log('Node server running on port 3000');

```
