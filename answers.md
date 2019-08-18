# Prerequisites - Setup the environment

I started a Ubuntu 18.04 server on AWS.

I then installed the Datadog agent on this Ubuntu server with the command:

DD_API_KEY=<MY_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

<br/>
<br/>

# Collecting Metrics

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog

I added some example tags to the /etc/datadog-agernt/datadog.yaml file and restarted agent

Screenshot of agent YAML file and host map on Datadog UI:
![YAML file with tags](./YAML_file_with_tags.png)

Screenshot of host map in Datadog UI:
![Host map with tags](./Host_map_with_tags.png)


<br/>
<br/>

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed postgres on the Ubuntu server.

In Postgres I configured a new user 'datadog' using instructions provided for Postgres.

  - create user datadog with password '<PASSWORD>';
  - grant pg_monitor to datadog;
  
I then configured the '/etc/datadog-agent/conf.d/postgres.d/onf.yaml file with the corresponding connection info

  - host: localhost
  - port: 5432
  - username: datadog
  - password: datadog
  - dbname: postgres

I restarted the datado agent and now webt to Datadog UI to see the metrics

Screenshot of Postgres metrics in Datadog UI Metrics Explorer:
![Postgres metrics](./Postgres_metrics.png)

<br/>
<br/>

## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000

I followed the instructions in "https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6"

First I created a Python script: /etc/datadog-agent/checks.d/my_metric.py

    import random
    from checks import AgentCheck
    class my_metric_class(AgentCheck):
          def check(self, instance):
              self.gauge('my_metric', random.randint(1,1000))
          
          
and a yaml file: /etc/datadog-agent/conf.d/my_metric.yaml

    init_config:

    instances:
      [{}]

Then I restarted the agent.

Screenshot of my_metric in Datadog UI Metrics Explorer: 

![My metric](./My_metric.png)

<br/>
<br/>

## Change your check's collection interval so that it only submits the metric once every 45 seconds

I edited the yaml file: /etc/datadog-agent/conf.d/my_metric.yaml

    init_config:

    instances:
      - min_collection_interval: 45

Then I restarted the agent.

I can now see that the metric interval went to 45 seconds

![My metric 45](./My_metric_45.png)

<br/>
<br/>

## Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes, this is possible by ediuting the yaml file in the conf.d directory like in the example above.


