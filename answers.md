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
