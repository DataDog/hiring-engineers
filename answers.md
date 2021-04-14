Your answers to the questions go here.

## Collecting Metrics:

* **Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

* Because I chose to use containers, I decided that the best way to add the tags would be to use the REST API capabilities.  To make this more scalable, there should be a script that allows for host and tags as input, that would iterate over the hosts and add the appropriate tags.  For sake of the excercise, I've just use a curl command to add the tags.

Use this call in script to list hosts:
```
curl -X GET "https://api.datadoghq.com/api/v1/hosts" \
 -H "Content-Type: application/json" \
 -H "DD-API-KEY: $DD_API_KEY" \
 -H "DD-APPLICATION-KEY: $DD_APPLICATION_KEY"
```
Found hostname *docker-desktop*
```
curl -X POST "https://api.datadoghq.com/api/v1/tags/hosts/docker-desktop" \
 -H "Content-Type: application/json" \
 -H "DD-API-KEY: $DD_API_KEY" \
 -H "DD-APPLICATION-KEY: $DD_APPLICATION_KEY" \
 -d '{ "host": "docker-desktop", "tags": ["environment:development", "vmwareebc"] }'
```
![AddTag](https://github.com/scotcurry/hiring-engineers/blob/master/AddTag.png)

* **Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

**Postgres Integration Screenshot**
![PostgresIntegration](https://github.com/scotcurry/hiring-engineers/blob/master/IntegrationsInstalled.png)

**Postgres Overview Screenshot**
![PostgresOverview](https://github.com/scotcurry/hiring-engineers/blob/master/PostgressOverview.png)

* **Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

**Custom Agent Check Screenshot**
![CustomAgentCheck](https://github.com/scotcurry/hiring-engineers/blob/master/AgentCheck.png)

* **Change your check's collection interval so that it only submits the metric once every 45 seconds.**
**Curryware.yaml File**
```
init_config:


instances:
  - min_collection_interval: 45
```

* **Bonus Question Can you change the collection interval without modifying the Python check file you created?**

I'm not sure I understand the question.  I edit the YAML file to set the collection interval, not a Python file.

## Visualizing Data:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please note that the examples below are based on information running in containers that may not always be running.  Please 
contact Scot Curry at 312-489-1056 if the data is not populating.

[Curryware Timeboard](https://p.datadoghq.com/sb/s680qmbidyyypnvm-0d6eef751ed1027ddd547bcdd764d9ea)

![Curryware Timeboard Screenshot](https://github.com/scotcurry/hiring-engineers/blob/master/Timeboard.png)

[Link to Timeboard Creation Python Script](https://github.com/scotcurry/hiring-engineers/blob/master/buildtimeline.py)

**Notes**

*Research* - I wasn't able to get the Python library to work when building the Timeboard.  I ended up just using the REST API call.  I need
to look at the source for what type of input object the library is expecting.

*Question* - I wasn't able to correctly obtain Postgres metrics.  Since I'm using the Datadog container agent, I attempted to use the Docker
labels to pass the configuration information.  I've included it below in the hopes I can get a better understanding of how this should be
implemented.

```
docker run -d --name datadog-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -e DD_API_KEY=<Datadog Key> \
  -l com.datadoghq.ad.check_names='["postgres"]' \
  -l com.datadoghq.ad.init_configs='[{}]' \
  -l com.datadoghq.ad.instances='[{"host":"localhost", "port":5432,"username":"datadog","password":"AirWatch1"}]' \
  gcr.io/datadoghq/agent:7
  ```
  
* **Set the Timeboard's timeframe to the past 5 minutes**
  
This was a simple dropdown.
![Timeboard timeframe dropdown](https://github.com/scotcurry/hiring-engineers/blob/master/TimeDropDown.png)
  
* **Take a snapshot of this graph and use the @ notation to send it to yourself.**

The only way I was able to find to take a snapshot was via API, so based on the instructions that this would be done via the
console, I'm uncertain how to complete this task.

* **What is the Anomaly graph displaying?**

It is showing the actual data within Datadog generated expected ranges.  It would seem to be based on machine learning, as it can
detect exception in "normal" data.  This would include spikes at specific times during a day.

## Monitoring Data:

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

## Collecting APM Data:

For this exercise I went a bit off script.  I got started with the Datadog technology for a real project.  I had created a site to automate some of the processes my company uses for performing Executive Briefings, so I didn't use the sample provided.

APM Screenshot 1:
![APM Screenshot 1](https://github.com/scotcurry/hiring-engineers/blob/master/APMScreenshot.png)

APM Screenshot 2:
![APM Screenshot 2](https://github.com/scotcurry/hiring-engineers/blob/master/APMScreenshot2.png)

Link to the instrumented app.py file:
[Link to app](https://github.com/scotcurry/MobileFlowsCalls/blob/master/app.py)

## Final Question:

* **Is there anything creative you would use Datadog for?**

While I haven't seen this capability, what I have seen a demand for is the ability to injest the kinds of data that Datadog currently obtains for infrastructure from mobile devices.  I currently work with two major grocery chains that have seen a need to understand what is going on with their mobile fleet.  They are in reactive mode ("it's a network issue, no it's an app issue").  They are both looking for a solution where the Ops team would be notified (store 10 is having latency issues, we should give them a call) when thing aren't working as expected.  This is exactly what Datadog does.
