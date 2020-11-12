Your answers to the questions go here.

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

_Setup the environment_

**I spun up a fresh VM via Vagrant per the docs.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/0.1+SetupEnv+-+vagrant.png" width="600">

**Collecting Metrics:**

_Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog._

- **I added tags via the agent config file**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/0.2+SetupEnv-map.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.1+CollectingMetrics+-+AgentConfig+-+tags.png" width="600">

_Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database._

- **Using PostgreSQL I setup a DB and connected it to the DataDog Agent**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.2+CollectingMetrics+-+PostgreSQL.png" width="600">

_Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000._

- **Using the python script provided by the [Docs](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) I slightly modified it and added a variable which generated a random number 0 - 1000**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+mymetric.png" width="600">

_Change your check's collection interval so that it only submits the metric once every 45 seconds_

- **Following the naming convention best practices per the docs, I updated the yaml file for custom_my_metric.yaml to reflect the updated interval.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+AgentCheck+-+check+file+-+interval.png" width="600">

_**Bonus Question** Can you change the collection interval without modifying the Python check file you created?_

- **Per the [docs](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval) the interval is set on the instance level within the check file.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+Interval.png" width="600">

#### Custom_My_Metric script

```
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

import random

class CustomMyMetricCheck(AgentCheck):
    def check(self, instance):
        randomNum = random.randint(0,1000)
        self.gauge('my_metric', randomNum, tags=['RandomKey:RandomValue'])

```

## Visualizing Data:

_Utilize the Datadog API to create a Timeboard that contains:_

- _Your custom metric scoped over your host._
- _Any metric from the Integration on your Database with the anomaly function applied._
- _Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket_

**First I used the Dashboard UI to understand the JSON request to the Timeboard API and read [Using Postman with Datadog APIs Docs](https://docs.datadoghq.com/getting_started/api/)**
**After I understood how the API worked and the shape of the request I wrote a small node.js script to send the request**
**I revisted these dashboards after connecting a new APM app to monitor DB operations**

Postman Request Body

```
<!-- Postman Request -->
{
    "title": "API Timeboard Multiple graphs w/style",
    "widgets": [
        {
            "definition": {
                "type": "query_value",
                "requests": [
                    {
                        "q": "avg:my_metric{*} by {data_cat}.rollup(sum, 3600)"
                    }
                ],
                "title": "My Metric - Roll up 1hr (3600 sec)"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{*}",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    }
                ],
                "title": "My Metric - Instance"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:trace.pg.query.duration.by.service.50p{env:none,service:node-postgres}, 'basic', 2)",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "anomalies(avg:trace.pg.query.duration.by.service.75p{env:none,service:node-postgres}, 'basic', 2)",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "anomalies(avg:trace.pg.query.duration.by.service.90p{env:none,service:node-postgres}, 'basic', 2)",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "anomalies(avg:trace.pg.query.duration.by.service.95p{env:none,service:node-postgres}, 'basic', 2)",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "anomalies(avg:trace.pg.query.duration.by.service.99p{env:none,service:node-postgres}, 'basic', 2)",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    },
                    {
                        "q": "anomalies(avg:trace.pg.query.duration.by.service.100p{env:none,service:node-postgres}.rollup(max), 'basic', 2)",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    }
                ],
                "title": "PostgreSQL DB Latency: Anomaly fn"
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

**API Script Request:**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/2.5+VisualizingData+-+API+Request.png" width="600">

**The script I used to send a request to the Timeboard API using node.js and axios**

```
<!-- timeboard.js  -->

var axios = require('axios');
var data = JSON.stringify({"title":"API Timeboard Multiple graphs w/style","widgets":[{"definition":{"type":"query_value","requests":[{"q":"avg:my_metric{*} by {data_cat}.rollup(sum, 3600)"}],"title":"My Metric - Roll up 1hr (3600 sec)"}},{"definition":{"type":"timeseries","requests":[{"q":"avg:my_metric{*}","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"}}],"title":"My Metric - Instance"}},{"definition":{"type":"timeseries","requests":[{"q":"anomalies(avg:trace.pg.query.duration.by.service.50p{env:none,service:node-postgres}, 'basic', 2)","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"}},{"q":"anomalies(avg:trace.pg.query.duration.by.service.75p{env:none,service:node-postgres}, 'basic', 2)","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"}},{"q":"anomalies(avg:trace.pg.query.duration.by.service.90p{env:none,service:node-postgres}, 'basic', 2)","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"}},{"q":"anomalies(avg:trace.pg.query.duration.by.service.95p{env:none,service:node-postgres}, 'basic', 2)","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"}},{"q":"anomalies(avg:trace.pg.query.duration.by.service.99p{env:none,service:node-postgres}, 'basic', 2)","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"}},{"q":"anomalies(avg:trace.pg.query.duration.by.service.100p{env:none,service:node-postgres}.rollup(max), 'basic', 2)","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"}}],"title":"PostgreSQL DB Latency: Anomaly fn"}}],"layout_type":"ordered","description":"Timeboard API","is_read_only":true,"notify_list":["J.Tustin@gmail.com"],"template_variables":[{"name":"host","prefix":"host","default":"vagrant"}]});

var config = {
  method: 'post',
  url: 'https://api.datadoghq.com/api/v1/dashboard',
  headers: {
    'Content-Type': 'application/json',
    'DD-API-KEY': 'XXXXXX',
    'DD-APPLICATION-KEY': 'XXXXX',
    'Cookie': 'DD-PSHARD=157'
  },
  data : data
};

axios(config)
    .then(function (response) {
        console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
        console.log(error);
    });
```

_Once this is created, access the Dashboard from your Dashboard List in the UI:_

**First, I used the 'Query Value' graph to represent the roll-up sum of My_Metric. I felt this represented the information best for the metric.**
**Second I used a 'Timeseries' graph to chart the change in My_Metric over time.**
**Third, I used a 'Timeseries' graph with the anomaly function applied to my database's latency metrics. FYI: I connected the PostgreSQL DB to my APM app and fired off a group of requests to create new rows within the DB. This graph charts the changes in latency for those requests.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/2.5+VisualizingData+-+5minGraph.png" width="600">

_Take a snapshot of this graph and use the @ notation to send it to yourself._

[DashboardURL](https://p.datadoghq.com/sb/bhyiy9gxxdsm6lqv-dd81669030a2ebedf65ca4358517d8fd)

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/2.5+VisualizingData+-+Snapshot.png" width="600">

- **Bonus Question**: What is the Anomaly graph displaying?

  The Anomaly graph Identifies strange behavior in a single metric based on the metrics past performance.
  Used for metrics that by nature have natural peaks and valleys.
  It is very hard to set sensible thresholds for these alerts. DataDog provides four algorithms to help identify strange behavior.

[DataDog Anomaly Detection Docs](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/)

## Monitoring Data

- _Warning threshold of 500_
- _Alerting threshold of 800_
- _And also ensure that it will notify you if there is No Data for this query over the past 10m._

**I used the UI to create a new metric which tracked my_metric and triggered alerts per the threshold.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.1+MonitoringData+-+Alert+logic.png" width="600">

_Please configure the monitor’s message so that it will:_

- _Send you an email whenever the monitor triggers._
- _Create different messages based on whether the monitor is in an Alert, Warning, or No Data state._
- _Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state._
- _When this monitor sends you an email notification, take a screenshot of the email that it sends you._

**The monitor message template using the message template variables to send relevant messages per the alert**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.2+VisualizingData+-+Email+template.png" width="600">

**Email message example of a warning**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.3+VisualizingData+-+Email+Example.png" width="600">

- **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  - _One that silences it from 7pm to 9am daily on M-F,_

  **Using Monitors > Manage Downtime > New Monitor. Here I was able to programatically set the downtime for the team members to respect their off hours and weekends.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.4+VisualizingData+-+Alert+Settings.png" width="600">

  - _And one that silences it all day on Sat-Sun._

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.4+VisializingData+-+SatSun.png" width="600">

  - _Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification._

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.5+VisualizingData+-+Alert+Setting+Confirmation.png" width="600">

## Collecting APM Data:

**I created a small node.js app which used the local server of the vagrant machine. Within the postgreSQL database there is a table called 'pets' which stores a pet's name and type. While the script is running, each request generates a 'newPet' which consists of a random name and selects an animal type. The 'newPet' item is then inserted into the 'pets' table.**

**One aspect that took a bit of thought was troubleshooting how to connect to the app. Since it was running locally on the VM, I needed to send requests to the localhost via the VM, which I did through a curl call to the port identified - curl 127.0.0.1:3000**

**Once the app is connected to the postgreSQL db it is able to send back metrics on the data operations per the APM integration.**

_Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics._

[Public Dashboard URL](https://p.datadoghq.com/sb/bhyiy9gxxdsm6lqv-dd81669030a2ebedf65ca4358517d8fd)

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.1+CollectingAPMData+-+ConnectedApp.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.2+CollectingAPMData+-+Service+List.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.2+CollectingAPMData+-+Service+Map.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.2+CollectingAPMData+-+Dashboard.png" width="600">

---

_Please include your fully instrumented app in your submission, as well._

```
<!-- DataDog config variables -->
const tracer = require("dd-trace").init(
  (DD_ENV = "sampleAppNode"),
  (DD_LOGS_INJECTION = true),
  (DD_TRACE_SAMPLE_RATE = "1")
);
const http = require("http");
const { Client } = require("pg");
var random_name = require("node-random-name");

// Simple app that generates a random pet name and type :: Example - 'Anthony the Cow'
// Each time the application is pinged, a random pet is generated and added to the pets table

// postgreSQL db connection information
const client = new Client({
  user: "datadog2",
  host: "localhost",
  database: "vagrant",
  password: "22",
  post: 5432,
});

// Array of pet types
const type = ["Cat", "Dog", "Cow", "Lizard", "Fish"];

// Function to generate a random number between 0 - 4
// Used for index position for pet type
function randomPetType() {
  return Math.floor(Math.random() * (4 - 0 + 1) + 0);
}

// connect to the DB
client.connect();

// Create an instance of the http server to handle HTTP requests
let app = http.createServer((req, res) => {
  // Set a response type of plain text for the response
  res.writeHead(200, { "Content-Type": "text/plain" });

  const newPet = `
  INSERT INTO pets (name, type)
  VALUES ('${random_name({ first: true })}', '${type[randomPetType()]}')
  `;

  client.query(newPet, (err, psqlRes) => {
    if (err) {
      console.error(err);
      res.end(`Error with DB: ${err}`);
      return;
    }
    console.log("Data insert successful", newPet);
    res.end("Data insert successful", newPet);
  });
});

// Start the server on port 3000
app.listen(3000, "127.0.0.1");
console.log("Node server running on port 3000");

```

- **Bonus Question**: What is the difference between a Service and a Resource?

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
