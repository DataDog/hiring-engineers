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

## Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes, this is possible by ediuting the yaml file in the conf.d directory like in the example above.

<br/>
<br/>

# Visualizing Data

I installed the Datadog Python package which contains the Datadog API:

    sudo apt-get install python
    sudo apt-get install python-pip
    pip install datadog

Then I created a standalone Python script (as below). 

It uses the Datadog API to create the custom dashboard in the Datadog UI. The dashboard contains three time graphs

- my_metric over ubuntu host
- Anomalies of the metric "postgresql.bgwriter.checkpoints_timed"
- my-metric rolled up to single hourly values

I also created a new APP key for this purpose.

Python script:

###
    from datadog import initialize, api

    options = {
            'api_key': '******',
            'app_key': '******'
        }

    initialize(**options)

    title = 'Exercise Timeboard'

    widgets = [{
        'definition': {
            'type': 'timeseries',
            'requests': [
              {'q': 'avg:my_metric{host:ubuntu}'}
            ],
            'title': 'my_metric over host ubuntu'
        }
    },{
        'definition': {
            'type': 'timeseries',
            'requests': [
              {'q': 'anomalies(avg:postgresql.bgwriter.checkpoints_timed{host:ubuntu},"basic",2)'}
            ],
            'title': 'postgres checkpoints anomalies'
        }
    },{
        'definition': {
            'type': 'timeseries',
            'requests': [
              {'q': 'sum:my_metric{host:ubuntu}.rollup(sum,3600)'}
            ],
            'title': 'my_metric rollup over last hour'
        }
    }]

    layout_type = 'ordered'

    description = 'An example timeboard for technical exercise.'

    api.Dashboard.create(title=title,
                         widgets=widgets,
                         layout_type=layout_type,
                         description=description)

###

Screenshot of custom dashboard:
![Custom dashboard](./Custom_dashboard.png)

<br/>

I then set the time interval to 5 minutes and took a snapshot sending it to myself via @ annotation


Screenshot of custom dashboard snapshot with @ annotation:
![Snapshot](./Snapshot.png)


Screenshot of snapshot received via mail:
![Snapshot_mai](./Snapshot_mail.png)

<br/>

## Bonus Question: What is the Anomaly graph displaying?

The anomaly graph displays occurences of the "postgresql.bgwriter.checkpoints_timed" metric values that are 2 standard deviations (configured) above the ordinary value

<br/>
<br/>


# Monitoring Data

I configured a metric monitor for the "my_metric"

- Send Warning if value crosses threshold of 500
- Send Alert f value crosses threshold of 800
- Send notification if there are missing data for the past 10m.

I also configured the contents of the notification mail:

    {{#is_alert}}
    ALERT! The value of my_metric {{value}} is above the alert threshold {{threshold}} on host {{host.name}} ({{host.ip}})
    {{/is_alert}} 

    {{#is_warning}}
    WARNING! The value of my_metric {{value}} is above the warning threshold {{warn_threshold}} on host {{host.name}} ({{host.ip}})
    {{/is_warning}} 

    {{#is_no_data}}
    DATA IS MISSING on {{host.name}} ({{host.ip}}) !
    {{/is_no_data}} 

    @jfrische@gmail.com
    
    
Screenshot of monitor configuration:
![Monitor definition](./Monitor_definition.png)

Screenshot of received notifiction:
![Notification mail](./Notification_mail.png)

I then added scheduled downtimes for this monitor:

![Downtime 1](./Downtime1b.png)
![Downtime 1](./Downtime1b.png)

and I received the email notifications fore these schedules downtimes:

![Downtime 1 Mail](./Downtime1b_mail.png)
![Downtime 1 Mail](./Downtime2b_mail.png)

<br/>
<br/>

# Final Question

## Is there anything creative you would use Datadog for?

I belive that the flexibility of Datadog metric collection and manipulation could be used to create very informative and actionable combined business and IT metrics dashboards. 

For example by collecting:
- number of received purchase orders from CRM system (or any DB)
- monetary value of these purchase orders
- IT perfromance metrics (latency, packet loss, file system, memory etc)

It would be possible to detect:
- if a given IT metric has an impact on the business metric (number of received purchased orders)
- if a given business metric (number of received purchased orders) has an alert (e.g. low amount) is caused by a correlated IT metric (e.g. packet loss, low free memory etc, high garbage collection, latency) and if so call to immediate action



