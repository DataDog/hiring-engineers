## Datadog Coding Challenge - Lionel Tesolin

Hello Datadog, all the consolidated answers of the coding challenge is resumed in this livedoc. My approach is to relate each step with in mind an hipotetical customer that might need to replicate the same task.
I'm aware (and you also are) that Github is a public platform and all forks are accessible by everyone so it is useful and interesting to check what have the others candidates answered to the same challenge. 
Let's start!
![alt-text](pictures/troll.gif "Let's start")


# Prerequisites - Setup the Environment

### Installation

Vagrant is a powerful vm orchestrator but I have already in my personal notebook an Ubuntu vm image with Docker. I'm using VirtualBox. I will then install the dockerized version of mongodb and datadog agent:

```shell
sudo docker run --name mongodb \
-e MONGO_INITDB_ROOT_USERNAME=lionh \
-e MONGO_INITDB_ROOT_PASSWORD=******** \
-p 27017 \
-d mongo:latest
```

```shell
sudo docker run -d --name dd-agent \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
-v /proc/:/host/proc/:ro \
-v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
-v /opt/datadog-agent-conf.d:/conf.d:ro \
-v /opt/datadog-agent-checks.d:/checks.d \
-p 8125:8125 \
-p 8126:8126 \
-p 5002:5002 \
--link mongodb:mongodb \
-e DD_TAGS=host:lionh-vm\ availability-zone:eu-west-a1\ region:west \
-e DD_API_KEY=44777b5614adfe98cfc78886cbea1eba datadog/agent:latest
```
The run command allow us to share volume between the docker container and the docker host to persist our file configuration. I also made a linkage with the mongodb container and added some custom tags.

![alt-text](pictures/001%20-%20docker%20run.png "Running the agent")

It's necessary to add a user in mongodb to allow the datadog agent to access in ro the database metrics:

```shell
creating user datadog in mongo:
db.createUser({
... "user":"datadog",
... "pwd": "********",
... "roles" : [
... {role: 'read', db: 'admin'},
... {role: 'clusterMonitor', db: 'admin'},
... {role: 'read', db: 'local' }
... ]
... })
Successfully added user: {
	"user" : "datadog",
	"roles" : [
		{
			"role" : "read",
			"db" : "admin"
		},
		{
			"role" : "clusterMonitor",
			"db" : "admin"
		},
		{
			"role" : "read",
			"db" : "local"
		}
	]
}
```


# Section 1: Collecting Metrics

##### Step: Find Hostmap in Datadog, provide screenshot
Here a screenshot of my host in the Host Map page in Datadog:

![alt-text](pictures/Host%20Map.png "Screenshot of my host in the Host Map page")

## Create an Agent Check
##### Step 1: Create the check and metric, generate a random number
Creating a custom agent check 
 - ![see my_metric.py](datadog-agent/datadog-agent-checks.d/my_metric.py "my_metric.py")
Defining a custom metric
 - ![see my_metric.yaml](datadog-agent/datadog-agent-conf.d/my_metric.yaml "my_metric.yaml")

##### Step 2: Run and verify the check
Stopping and restarting the dd-agent container is easy with Docker

```
sudo docker stop dd-agent
sudo docker start dd-agent
```
---
> *Bonus Question Can you change the collection interval without modifying the Python check file you created?*
---
Modifying the ```.yaml``` file was my first approach. The question asked if it is possible to do it without modifying the ```.py```. The Gauge class exposes a ```flush```method that takes *interval* argument. So in Python, it is possible to set how often a given metric is flushed to Datadog.


# Section 2: Visualizing Data

*Utilize the Datadog API to create a Timeboard...*

---

## Create a Timeboard
##### Step 1: I'm going to use Curl as a simple Rest Client and storing the call in a bash script.
---
> *(Make sure your timeboard contains:*)
> - *Your custom metric scoped over your host.*
> - *Any metric from the Integration on your Database with the anomaly function applied.*
---
 - ![see timeboard.sh](timeboard.sh "timeboard curl call")
##### Step 2: Verify the custom Dashboard
![alt-text](pictures/Dashboard%20screenshot.png "Screenshot of my custom Dashboard")
##### Step 3: Verify the email notification with 5 minutes timeframe
---
>*(Access the Dashboard in the UI:)*
> - *Take a snapshot of this graph and use the @ notation to send it to yourself.*
---
Selecting any graph, using the camera button in the top right, I was able to take a snapshot and share it using @ with a suggestion list of user and use my own email adress. I receive immediately the following email in my inbox:
![alt-text](pictures/Email%20notification.png "Email notification")

## What is the Anomaly graph displaying?
An Anomaly uses algorithmic detection to compare a metric with its historical data highlighting deviations over a specific window time. Different algorithm can be chosen.


# Section 3: Monitoring Data

I created a monitor through UI with the requested conditional messages. The host ip get lost because I'm using Docker container but the {{host.name}} placeholder works.

```
**query** max(last_5m):max:my_metric{host:lionh-vm} > 800

{{#is_alert}} The data is above the threshold. A peak of {{value}} is too high, please review host: {{host.ip}} {{/is_alert}}

{{#is_warning}} The data is below the threshold. A peak of {{value}} is high, please consider review what is going on {{/is_warning}}

{{#is_no_data}} No data coming in 10m, please contact support {{/is_no_data}}
```
![Alert Monitor Notification](pictures/email.png)

---
> ***Bonus Question:*** *Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*
> - *One that silences it from 7pm to 9am daily on M-F,*
> - *And one that silences it all day on Sat-Sun.,*
> - *Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.*
---
I scheduled two recurring Downtime and received the notification by mail. One each working day from 7pm, duration 14h and one on Saturday beginning at 00:00am, duration 2 days.

Here the details:

![Downtime definition](pictures/DowntimeDef.png)

![Downtime notification](pictures/Downtime2.png)

![Downtime started notification](pictures/Downtime started.png)

Please note that the time is scheduled in CET and the notification is given in UTC (1 hour delayed)

