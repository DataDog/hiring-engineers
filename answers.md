First off I'd like to say I really enjoyed working through this exercise and learned alot along the way about the Datadog suite.



** Setting up the environment**

1. Choosing which environment I would use for the excercise was a learning experience. I had never heard of Vagrant or Virtual box and decided to ahead and use this so I don't run to dependency issues. After reading the documentation I realized that Virtual box can not be ran on the M1 chip. I ended up using an old laptop with intel chip. I installed Vagrant and Virtual box.

2. I initialized Vagrant

```
vagrant init hashicorp/bionic64
```

3. Then started the VM
```
vagrant up
```

4. SSH to box with
```
vagrant ssh
```

## I then installed the DataDog Agent to environment 

It is important to choose the correct Agent for environment. For Ubuntu, I ran the easy one step install command

```
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=c98147090f0162434a358063a74de3a9 DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

To stop agent you can run:

```
sudo systemctl stop datadog-agent
```
To run agent:

```
sudo systemctl start datadog-agent
```

## Collecting Metrics:

#### Environment Tags

In order to add tags you can modify the /etc/datadog-agent/datadog.yaml. I ran into permission issues trying to modify the yaml file. I used documentation regarding permission issues and followed the steps.

I first ran:

```
ls -l /var/log/datadog/
```
I saw that dd-agent did not own files so I ran:

```
sudo chown -R dd-agent:dd-agent /var/log/datadog/
```
I then proceeded to restart the agent and tried to reopen the file and still ran into permission issues. I found this "https://stackoverflow.com/questions/17535428/how-to-edit-save-a-file-through-ubuntu-terminal" and realized I had to run this command to edit file:

```
sudo vi etc/datadog-agent/datadog.yaml
```
what this does is vi enters into another terminal to edit the file. I could then open the file and change the hostname and insert tags by removing the comment #.

I then used the command:
```
:wq
```
to save changes.

## Installing PostGres
I decided to install PostGres since I am familiar with PostGres from my bootcamp. 

to install:
```
sudo apt-get install postgressql
```
I then integrated with Datadog following the steps at "https://www.datadoghq.com/blog/collect-postgresql-data-with-datadog/"

I needed to create the datadog user so I ran these commands:

```
-create user datadog with password 'Camila1234$';
-grant pg_monitor to datadog;
-grant SELECT ON pq_stat_database to datadog;
```
to check if user was created and granted access run command:

```
\du
```

I then logged onto Datadog account and installed the PostGres integration.

## Create custom check
I created custom metric named my_metric.yaml/py

I used the example that was used at "https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7"

I moved to the correct directory with command:
```
cd /etc/datdog-agent/checks.d

then I used this command to create file:
```
sudo vim my_metric.py
```
I confirmed it was present.

I then changed directory to conf.d to create the yaml file. I then ran this command:

```
sudo vim my_metric.yaml
```
I then edited the file to have an instance that uses 45 seconds.

I confirmed that the my_metric.yaml file was present.

I verified by running:
```
sudo -u dd-agent -- datadog-agent check my_metric
```

## Bonus Question
The min_collection_interval is set to a number for example in our case 45, which means that it could collected every 45 seconds and not that it will be collected every 45 seconds. If the collector runs the check at the 45 second interval and there is another task/check that is being performed it could be late. If the check takes longer than time allotted then the Agent will skip until the next interval.

## Visualizing data 

To create dashboards via API I tried using Postman as I wanted to learn more on how to use this service. I followed the steps here "https://docs.datadoghq.com/getting_started/api/".

I obtained the API needed for Postman.

I then installed the integration on Datadog. And followed the steps to proceed in Postman.
In Postman I expanded the Data Api Collection and selected Post a new Dashboard under Dashboards.

I entered api keys into the query params fields.

I then proceeded to enter this code into the body field.

Unfortunately I kept getting an forbiden response and I could not get the dashboards to be created. Due to the time constraint I was not able to figure the solution to my issue. I did want to discuss what I was looking to add. The first dashboard was to scope my_metric I had created. The second dashboard I was looking to create was a dashboard that used the anomaly function using this documentation "https://docs.datadoghq.com/monitors/create/types/anomaly/". The third dashboard I was looking to create was a dashboard with the rollup function using this documentation "https://docs.datadoghq.com/dashboards/functions/rollup/".

{
  "title": "<Luis Dashboard>",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:my_metric{host:LuisDatadog}"
          }
        ],
        "title": "My metric scoped on myhost"
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "anomalies( avg:postgresql.connections{*}, 'basic', 2 )"
          }
        ],
        "title": "Postgres Connection with anomalies factor"
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:my_metric{*}.rollup(sum,3600)"
          }
        ],
        "title": "My metric  Rollup Function Applied"
      }
    }
  ],
  "layout_type": "ordered",
  "description": "<Luis Visualizing Data Dashbaord >",
  "is_read_only": true,
  "notify_list": [
    "test@datadoghq.com"
  ],
  "template_variables": [
    {
      "name": "host",
      "prefix": "host",
      "default": "<HOSTNAME_1>"
    }
  ],
  "template_variable_presets": [
    {
      "name": "Saved views for hostname 2",
      "template_variables": [
        {
          "name": "host",
          "value": "<HOSTNAME_2>"
        }
      ]
    }
  ]
}

I used another dashboard in the Datadog gui to set timeboards timeframe to the past 5 minutes.

I was also able to use the snapshot feature, which is great to illustrate a potential issue and can be reviewed by the team.

## Bonus question

An anomaly function detects abnormal behavior which takes into account the history of the metric,trends, and seasonality.
It is displayed as overlaying grey band on graph for potential results.

### Monitoring Data 

I created a new monitor by logging into Datadog and clicking the new monitor option. The screenshot below shows the thresholds set for Alert > 800, Warning > 500,  and data missing for more than 10 minutes.

I used the template variables to write the monitoring message.
{{#is_warning}}
average value of `system.cpu.user` has been **slightly high** over the past **5 minutes**.
{{/is_warning}} 

{{#is_alert}}
average value of `system.cpu.user` has been **high** over the past **5 minutes**.
{{/is_alert}}

{{#is_no_data}}
There has been **no** data for the  average value of `system.cpu.user` over the past **10 minutes**.
{{/is_no_data}}

## Bonus Schedule downtime
I created a downtime schedule by going to Monitors and click on the yellow schedule downtime icon. When I clicked the icon it prompted me to specify times and days, and to option for message to notify team. Below are the email notifications I received to my email.

## Collecting APM data

I ran into issues trying to install ddtrace on the VM. I went to flask docs and ran:

```
pip install flask
```
```
pip install ddtrace
```
I tried reading the docs on the Datadog site "https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers" but had no success. However doing some reading what needs to be done is setting apm_non_local_traffic: true which is in the apm_config

##Bonus Question

A service groups together endpoints, queries, or jobs for scaling. Example would be a group of URL endpoints grouped under an API service. A resource is a particular action for service. The resource represents a specific domain of your application which allows services to do their job.


##Final Question
The amazing thing regarding Datadog is that it is very dynamic and its application is limitless. Where I can see Datadog used is in peoples fitbits or applewatches that track biostats. It can check what time of the day your heart rate is elevated or not? Also what days of the weeks do you walk more or burn more calories? Monitor when your blood pressure is elevated at what times of the day? With this information the individual can make adjusstments to their daily routine in order to lower these levels, or to be aware what triggers these abnormalities. 