Your answers to the questions go here.

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

Setup the environment

![vagrant](https://datadog-examples.s3.us-east-2.amazonaws.com/0.1+SetupEnv+-+vagrant.png)

<!-- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/0.1+SetupEnv+-+vagrant.png" width="1000" height="332"> -->

## Collecting Metrics:

- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![tags](https://datadog-examples.s3.us-east-2.amazonaws.com/1.1+CollectingMetrics+-+AgentConfig+-+tags.png)

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

![psql](https://datadog-examples.s3.us-east-2.amazonaws.com/1.2+CollectingMetrics+-+PostgreSQL.png)

- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

![my_metric](https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+AgentCheck+-+code+sample.png)

- Change your check's collection interval so that it only submits the metric once every 45 seconds.

![Interval](https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+AgentCheck+-+check+file+-+interval.png)

- **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

  Per the [docs](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval) the interval is set on the instance level within the check file.

![docs](https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+Interval.png)

```

# the following try/except block will make the custom check compatible with any Agent version

try: # first, try to import the base class from new versions of the Agent...
from datadog_checks.base import AgentCheck
except ImportError: # ...if the above failed, the check is running in Agent version < 6.6.0
from checks import AgentCheck

# content of the special variable **version** will be shown in the Agent status page

**version** = "1.0.0"

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

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

- Your custom metric scoped over your host.
- Any metric from the Integration on your Database with the anomaly function applied.
- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

I used Postman to send a request to the timeboard api using the Postman Datadog collection.
[Using Postman with Datadog APIs](https://docs.datadoghq.com/getting_started/api/)

![Postman](https://datadog-examples.s3.us-east-2.amazonaws.com/2.1+VisualizingData+-+Postman+request.png)

![Timeboard](https://datadog-examples.s3.us-east-2.amazonaws.com/2.2+VisualizingData+-+metrics.png)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

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

Once this is created, access the Dashboard from your Dashboard List in the UI:

- Set the Timeboard's timeframe to the past 5 minutes

![Timeframe](https://datadog-examples.s3.us-east-2.amazonaws.com/2.3+MonitoringData+-+graph.png)

- Take a snapshot of this graph and use the @ notation to send it to yourself.

![Snapshot](https://datadog-examples.s3.us-east-2.amazonaws.com/2.2+VisualizingData+-+graph.png)

- **Bonus Question**: What is the Anomaly graph displaying?

  The Anomaly graph Identifies strange behavior in a single metric based on the metrics past performance.

  Used for metrics that by nature have natural peaks and valleys.

  It is very hard to set sensible thresholds for these alerts. DataDog provides four algorithms to help identify strange behavior.

  [Anomaly Detection](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/)

## Monitoring Data

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

![Alert Logic](https://datadog-examples.s3.us-east-2.amazonaws.com/3.1+MonitoringData+-+Alert+logic.png)

Please configure the monitor’s message so that it will:

- Send you an email whenever the monitor triggers.
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
- When this monitor sends you an email notification, take a screenshot of the email that it sends you.

  - ![Alert Message](https://datadog-examples.s3.us-east-2.amazonaws.com/3.2+VisualizingData+-+Email+template.png)
  - ![Alert Email](https://datadog-examples.s3.us-east-2.amazonaws.com/3.3+VisualizingData+-+Email+Example.png)

- **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  - One that silences it from 7pm to 9am daily on M-F,
    - ![Custom Alert1](https://datadog-examples.s3.us-east-2.amazonaws.com/3.4+VisualizingData+-+Alert+Settings.png)
  - And one that silences it all day on Sat-Sun.
    - ![SatSun](https://datadog-examples.s3.us-east-2.amazonaws.com/3.4+VisializingData+-+SatSun.png)
  - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
    - ![Email Alert](https://datadog-examples.s3.us-east-2.amazonaws.com/3.5+VisualizingData+-+Alert+Setting+Confirmation.png)

## Collecting APM Data:

- **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

[Public Dashboard URL](https://p.datadoghq.com/sb/bhyiy9gxxdsm6lqv-f0b825c240327f6a2ed765e673e75275)

- ![SampleApp](https://datadog-examples.s3.us-east-2.amazonaws.com/4.1+CollectingAPMData+-+sampleApp.png)
- ![APM Dashboard](https://datadog-examples.s3.us-east-2.amazonaws.com/4.3+CollectingAPMData+-+Dashboard.png)
- ![APM](https://datadog-examples.s3.us-east-2.amazonaws.com/4.2+CollectingAPMData+-+Services.png)

Please include your fully instrumented app in your submission, as well.

```
<!-- DataDog config variables -->
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

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
