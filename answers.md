Your answers to the questions go here.

---

Hello DataDog Team,

Thank you for the opportunity! I enjoyed this exercise, learning about the platform, and understanding the experience of DataDog's users. I researched each step of the challenge using the DataDog docs, user-submitted blog posts, product-specific docs, and personal notes. I provided screenshots in this file via an S3 bucket and added code samples where needed.

After spending time in the product, it is clear how powerful the analytic and reporting tools are and a clear focus on creating an easy to use UX. It seems there is an endless combination of metrics to develop but provided in a way that isn't overwhelming. I can understand how impactful this platform could be to members across the organization, regardless of job function or level.

I learned a lot about the technologies used in the exercise and feel I have a deeper understanding of what it would be like being a Sales Engineer at DataDog. I imagine there is an endless stream of new and creative ideas from users using DataDog, which enables the experience of both student and teacher; learning from and teaching customers new ways to gain insights into their business.

Again, thank you for the opportunity, and please let me know if I can provide anything additional. I look forward to speaking with you soon!

Thank you,

Joe Tustin

---

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

_Setup the environment_

**I spun up a fresh VM via Vagrant per the docs.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/0.1+SetupEnv+-+vagrant.png" width="600">

**Collecting Metrics:**

_Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog._

- **I added tags via the agent config file and checked they were reporting correctly via the UI. Hashbrown is the name of my cat, seemed reasonable to add a tag representing him via data_cat**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/0.2+SetupEnv-map.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.1+CollectingMetrics+-+AgentConfig+-+tags.png" width="600">

_Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database._

- **Using PostgreSQL I setup a DB and connected it to the DataDog Agent**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.2+CollectingMetrics+-+PostgreSQL.png" width="600">

_Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000._

- **Using the python script provided by the [docs](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7), I slightly modified it and added a variable which generated a random number 0 - 1000**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+mymetric.png" width="600">

_Change your check's collection interval so that it only submits the metric once every 45 seconds_

- **Following the naming convention best practices per the docs, I updated the yaml file for custom_my_metric.yaml to reflect the updated interval.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+AgentCheck+-+check+file+-+interval.png" width="600">

_**Bonus Question** Can you change the collection interval without modifying the Python check file you created?_

- **Per the [docs](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval) the interval is set on the instance level within the check file. I do not believe there is any other way to change the interval for a specific check outside of this action.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/1.3+CollectingMetrics+-+Interval.png" width="600">

**Custom_My_Metric script**

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

---

**First, I used the Dashboard UI to understand the JSON object needed to send a request to the Timeboard API.**

**Second, with the [DataDog Postman collection's assistance](https://docs.datadoghq.com/getting_started/api/), I understood precisely how the Timeboard API worked and what the endpoint expected.**

**Last, after testing using Postman, I understood how the API worked and the expected request's shape; I wrote a small node.js script to send the request. After connecting the new APM app, I revisited these dashboards to monitor DB operations triggered via the APM app.**

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

**Timeboard API Script Response:**

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

---

**First, I used the 'Query Value' graph to represent the roll-up sum of My_Metric. I felt this represented the information best for this specific metric.**

**Second I used a 'Timeseries' graph to chart the change in My_Metric over time.**

**Third, I used a 'Timeseries' graph with the anomaly function applied to my database's latency metrics.**

- **FYI: I connected the PostgreSQL DB to my APM app and fired off a group of requests to create new rows within the DB. This graph charts the changes in latency for those requests.**

[DashboardURL](https://p.datadoghq.com/sb/bhyiy9gxxdsm6lqv-dd81669030a2ebedf65ca4358517d8fd)

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/2.5+VisualizingData+-+5minGraph.png" width="600">

_Take a snapshot of this graph and use the @ notation to send it to yourself._

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/2.5+VisualizingData+-+Snapshot.png" width="600">

- **Bonus Question**: What is the Anomaly graph displaying?

  The Anomaly graph Identifies strange behavior in a single metric based on the metrics past performance.
  Used for metrics that by nature have natural peaks and valleys.
  It is very hard to set sensible thresholds for these alerts. DataDog provides four algorithms to help identify strange behavior and does so using historical data.

[DataDog Anomaly Detection Docs](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/)

## Monitoring Data

- _Warning threshold of 500_
- _Alerting threshold of 800_
- _And also ensure that it will notify you if there is No Data for this query over the past 10m._

---

**I used the UI to create a new metric which tracked my_metric and triggered alerts per the threshold.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.1+MonitoringData+-+Alert+logic.png" width="600">

_Please configure the monitor’s message so that it will:_

- _Send you an email whenever the monitor triggers._
- _Create different messages based on whether the monitor is in an Alert, Warning, or No Data state._
- _Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state._
- _When this monitor sends you an email notification, take a screenshot of the email that it sends you._

**The monitor message using the message template variables to send relevant information per the alert**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.2+VisualizingData+-+Email+template.png" width="600">

**Email message example of a warning**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.3+VisualizingData+-+Email+Example.png" width="600">

- **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  - _One that silences it from 7pm to 9am daily on M-F,_

---

**Using Monitors > Manage Downtime > New Monitor. Here I was able to programatically set the downtime for the team members to respect their off hours and weekends.**

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.4+VisualizingData+-+Alert+Settings.png" width="600">

  - _And one that silences it all day on Sat-Sun._

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.4+VisializingData+-+SatSun.png" width="600">

  - _Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification._

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/3.5+VisualizingData+-+Alert+Setting+Confirmation.png" width="600">

## Collecting APM Data:

**I created a small node.js app which used the local server of the vagrant machine. Within the postgreSQL database there is a table called 'pets' which stores a pet's name and type. While the script is running, each request generates a 'newPet' which consists of a random name and selects an animal type. The 'newPet' item is then inserted into the 'pets' table.**

**One aspect that took a bit of thought was troubleshooting how to connect to the app. Since it was running locally on the VM, I needed to send requests to the localhost via the VM, which I did through a curl call to the port identified - `curl 127.0.0.1:3000`**

**Once the app is connected to the postgreSQL db it is able to send back metrics on the data operations per the APM integration.**

_Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics._

[Public Dashboard URL](https://p.datadoghq.com/sb/bhyiy9gxxdsm6lqv-dd81669030a2ebedf65ca4358517d8fd)

- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.4+CollectingAPMData+-+Commands+to+interact+with+DB.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.1+CollectingAPMData+-+ConnectedApp.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.2+CollectingAPMData+-+Service+List.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.2+CollectingAPMData+-+Service+Map.png" width="600">
- <img src="https://datadog-examples.s3.us-east-2.amazonaws.com/UpdatedFiles/4.2+CollectingAPMData+-+Dashboard.png" width="600">

---

_Please include your fully instrumented app in your submission, as well._

```
<!-- DataDog config Variables -->
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
  return type[Math.floor(Math.random() * (4 - 0 + 1) + 0)];
}

// connect to the DB
client.connect();

// Create an instance of the http server to handle HTTP requests
let app = http.createServer((req, res) => {
  // Set a response type of plain text for the response
  res.writeHead(200, { "Content-Type": "text/plain" });

  const newPet = `
  INSERT INTO pets (name, type)
  VALUES ('${random_name({ first: true })}', '${randomPetType()}')
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
  In reading the docs I came across [APM Glossary & Walkthrough](https://docs.datadoghq.com/tracing/visualization/) which allowed me to dig into the differences

  - **[Service](https://docs.datadoghq.com/tracing/visualization/#services) Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of building your application.**
  - **[Resource](https://docs.datadoghq.com/tracing/visualization/#resources) Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.**

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

**I think a project with many individual components that come together to create something impactful -a 'hive' of sorts- would be a great use of DataDog—enabling insights into behavior that would be too complicated to view individually or manually.**

**At burning man in 2019, I saw Paul Stamets speak about his [BeeMushroomed Feeder](https://fungi.com/pages/bees). Paul is very passionate about solving colony collapse impacting our bee populations and had created a prototype to help bee populations stay healthy. Part of the design was an IoT component that helped keep metrics around the feeders use. I think it would be fascinating to monitor the digital aspects of the product and the physical part of the conditions in which it is placed. For example, it would be interesting to see if the anomaly detection tools would pick up on a die off event based on a dip in network traffic sent from the feeder.**

## Extra Credit: GitGuardian

I also learned about GitGuardian monitoring after accidentally committing my API key in my code sample. I was notified by GitGuardian and by Skylar in Datadog Support within ~30 mins of _committing_ my mistake.

<img src="https://i.imgur.com/UIWXBQU.gif" width="300">
