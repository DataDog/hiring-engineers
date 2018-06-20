## Collecting Metrics 


## Adding tags

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I followed along the [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) I was able to find the datadog.yaml file and make the necessary changes:

- take the comments out the 'tags' section
- change to: 
		tags: project:test,laptop:koshap,role:database

![Custom Tags](https://imgur.com/a/xx5xpqs)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose to use PostgreSQL as I was am pretty comfortable with it.  I already have PostgreSQL installed on my machine. 

I used  https://docs.datadoghq.com/integrations/postgres/ to follow to integrate PostgreSQL

1.	Created a read-only Datadog user using the following command line:

```
create user datadog with password '<PASSWORD>';
grant SELECT ON pg_stat_database to datadog;
```

2.	Checked the correct permissions running the following command line:

```
psql -h localhost -U datadog postgres -c \
    "select * from pg_stat_database LIMIT(1);"
    && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
    || echo -e "\e[0;31mCannot connect to Postgres\e[0m"
And entered our ‘<PASSWORD>’.
```

3.	Then, we edited the conf.d/postgres.yaml file (using this https://github.com/DataDog/integrations-core/blob/master/postgres/conf.yaml.example) and added a few tags to configure the agent and to connect it to our PostgreSQL server. 

```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: <YOUR_PASSWORD>
       tags:
            - laptop:margot
            - project:postgres
```

4.	We restarted the agent.

```
launchctl stop com.datadoghq.agent
launchctl start com.datadoghq.agent
```

5.	We ran the `datadog-agent status` command line to make sure the PostgreSQL integration has been successfully completed.



![PostgreSQL Integration Validation](https://imgur.com/a/epPq5a3)


* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Datadog custom agent checks are a way for you to get the Agent to collect metrics from your custom applications or unique systems.

Different types of check can be sent (metric, event, service), however we will here focus on implementing a gauge metric.

To get an Agent check to submit a brand-new metric, I had to create two distinct files: 

* mymetric.yaml that needs to go in `datadog-agent/conf.d`:

```yaml
init_config:

instances:
    [{}]
```

* mymetric.py that has to go in `datadog-agent/checks.d`: 

```python
from random import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', 1000 * random())
```

After that, I restarted the Datadog Agent and executed the `datadog-agent status` command line to make sure the check had successfully been implemented.

![Custom Agent Check Validation](https://imgur.com/a/317okAN)


* Change your check's collection interval so that it only submits the metric once every 45 seconds.


This can be changed by modifying the check’s yaml file: you simply need to add the `min_collection_interval: nb_of_seconds` parameter at the init_config or at the instance level.

To change our check’s collection interval, I therefore slightly modified the `datadog-agent/conf.d/mymetric.yaml` file, and simply added the parameter `min_collection_interval: 45` to the configuration file.

```yaml
init_config:
  min_collection_interval: 45

instances:
    [{}]
```

After that, I restarted again the Datadog agent, and went back to the graph to make sure that the collection interval had, indeed, gone from 15-20 to 45 seconds.

![Change of Collection Interval 47sec](https://imgur.com/a/KDvTJbL)

* Bonus: I changed the interval using the 'my_metric.yaml' file therefore the python file was not touched. 


##Visualizing Data:


__Utilize the Datadog API to create a Timeboard that contains:__
* __Your custom metric scoped over your host.__
* __Any metric from the Integration on your Database with the anomaly function applied.__
* __Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.__

> Datadog allows you to create dashboards so you can quickly visualize the data you’re interested in. The application features two different types of dashboards: timeboards and screenboards. Timeboards are always scoped to the same time and have a predefined grid-like layout whereas screenboards are more flexible and customizable.

We will here focus on creating a timeboard through Datadog API.

To start using Datadog API, you first need to install Datadog. Therefore, go to your python environment and run the `pip install datadog` command line as indicated here: https://github.com/DataDog/datadogpy. 

![Datadog Installation](/screenshots/pipinstalldd.png)

You then need to look for your API key and to create your application key. To do so, just go to Datadog application, go to the “Integrations” section in the side bar menu, and pick the APIs tab. Just hit the button “Create Application Key” and there you go, your brand-new application key!


You then need to adapt a code snippet from here: https://docs.datadoghq.com/api/#timeboards. 
Here is what mine looks like :

```python
from datadog import initialize, api

options = {
    'api_key': <YOUR_API_KEY>,
    'app_key': <YOUR_APP_KEY>
}

initialize(**options)

{
      "graphs" : [{
          "title": "rollup",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      },{
          "title": "Postgres Anomoly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:postgresql.max_connections{*}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      },{
          "title": "Custom Metric",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Timeboard test",
      "description" : "kp",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
```

Then, save and run the python script you just created on your terminal. It should output something like this:

```
{
    "dash": {
        "read_only": true,
        "graphs": [
            {
                "definition": {
                    "requests": [
                        {
                            "q": "avg:my_metric{*}.rollup(sum, 3600)"
                        }
                    ],
                    "events": []
                },
                "title": "rollup"
            },
            {
                "definition": {
                    "requests": [
                        {
                            "q": "anomalies(avg:postgresql.max_connections{*}, 'basic', 2)"
                        }
                    ],
                    "events": []
                },
                "title": "Postgres Anomoly"
            },
            {
                "definition": {
                    "requests": [
                        {
                            "q": "avg:my_metric{*}"
                        }
                    ],
                    "events": []
                },
                "title": "Custom Metric"
            }
        ],
        "template_variables": [
            {
                "default": "host:my-host",
                "prefix": "host",
                "name": "host1"
            }
        ],
        "description": "kp",
        "title": "Timeboard test",
        "created": "2018-06-20T21:45:48.692781+00:00",
        "id": 840679,
        "created_by": {
            "disabled": false,
            "handle": "koshapatel2@gmail.com",
            "name": "kosha patel",
            "is_admin": true,
            "role": null,
            "access_role": "adm",
            "verified": true,
            "email": "koshapatel2@gmail.com",
            "icon": "https://secure.gravatar.com/avatar/db384cd23cd26a724460808376224054?s=48&d=retro"
        },
        "modified": "2018-06-20T21:45:48.723983+00:00"
    },
    "url": "/dash/840679/timeboard-test",
    "resource": "/api/v1/dash/840679"
}
```

![Timeboard with rollup and anomoly](https://imgur.com/a/QRrr8db)

* Set the Timeboard's timeframe to the past 5 minutes

![5min timeframe](https://imgur.com/a/zfknK5r)



* Take a snapshot of this graph and use the @ notation to send it to yourself.

![Email 5min interval](https://imgur.com/a/Ux96Gkx)


* **Bonus Question**: What is the Anomaly graph displaying?

Anomaly detection is a feature allowing you to identify metrics behaving differently than they have in the past. The anomaly graph should therefore highlight unusual data so you can quickly react if you need to.

It is not obvious in the previous graph as it displayed a constant figure (maximum number of connections to PostgreSQL), however when applied to a metric such as my_metric, we can see that the graph\ features a grey area with a blue curve, which is made up of the normal data; and a white area with red values, which is the unexpected data. 



##Monitoring Data


