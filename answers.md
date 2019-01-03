Your answers to the questions go here.
# Prerequisites - Setup the environment
To get started I installed Vagrant from brew on my laptop and used that to spin up a Centos 7 VM and signed up for my DataDog Trial.


# Collecting Metrics

Setting up the Datadog agent is pretty simple. Since this is Centos I added the Datadog yum repo so I could easily install the agent via a "yum install datadog-agent". Once the agent is installed , Its a simple matter to copy the datadog.yaml.example file to datadog.yaml and add in the necesary lines to get the agent running. Tags are always nice to have so you can differentiate things like test environments from production environments. No one wants to get alerts from a test server in the middle of the night.  

```
dd_url: https://app.datadoghq.com
api_key: $API key
hostname: exercisevm
tags:
  - test
  - role:pgs
  - env:poc
```
Once your yaml is defined you can start/restart the agent by `service datadog_agent restart` and it should start reporting info. If you don't believe its working you can check what it is doing with ` datadog-agent status` . If that tells you that something like "Could not reach agent" you can check /var/log/datadog/ to see what happened. 
Once its started you should see an event in your datadog panel as well as a host in the host map with the tags defined in your yaml file.
![tags](/tags.png) 

 The next step was to install a database. I installed Postgres from yum and started it up. Following the instructions on the integration page , the first step is to create a user to allow datadog to talk to my database. Once the user was setup and tested with the provided command you are ready to let the agent know you want it to monitor Postgres. This is done by creating a yaml file in /etc/datadog-agent/conf.d/postgres.d from the provided example. To get started all you need to add is your login information you created in the previous step.
 ```
 init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: password
       dbname: test
 ```

After a quick restart of the agent , you should start to see information flow on the integration page ! 
Also a `datadog-agent status` will now show a section for postgres

```   postgres (2.3.0)
    ----------------
      Instance ID: postgres:bd965c0face34e4f [OK]
      Total Runs: 1
      Metric Samples: Last Run: 30, Total: 30
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 1, Total: 1
      Average Execution Time : 39ms
```

![Postgres Integration](/pgs_integration.png) 

## Creating a custom metric

Despite all the out of the box funciotnality provided by Datadog, occasionaly you may find the need to create a custom metric to gather data from some proprietary application. This requires two parts. The [actual check](/checks.d/my_metric.py) which would be a python script under checks.d and a [yaml file](/conf.d/my_metric.yaml) under conf.d to tell datadog to look for your check. These two files need to have the same name so the agent knows what to look for. This sample my metric simply picks a random number between 1 and a 1000 and sends it to the agent. 
In the past I have used a custom check to warn us of an impending SSL cert expiration although this is now built into the http check. I found this wonderful check [online](https://github.com/dobber/datadog-ssl-check-expire-days) and its a good example to show that you can add variables in your yaml file to avoid having to change your python check for different sites. 


## Changing the collection time and Bonus Question 

By default datadog will run your check every 15 seconds. If you don't want to spam your monitored application/site you can modify the yaml file to change the collection interval. For instance to have it only look every 45 seconds you can add a - min_collection_interval: 45 to your instance in the check's yaml file. 

```
init_config:

instances:
  - min_collection_interval: 45

```

# Visualizing Data


https://app.datadoghq.com/dash/1033029/api-timeboard
created by apitimeboard.py

![Last 5 Minutes](/last5.png)

Bonus Question

The anomaly graph is showing my metric of postgresql rows returned in blue with the accepted range in grey. Where the line goes red , it shows values outside the accepted range.

# Monitoring Data
```
{{#is_warning}} My metric is currently {{value}} on {{host.ip}} {{/is_warning}}

{{#is_alert}} My Metric is currently {{value}} on {{host.ip}} {{/is_alert}}

{{#is_no_data}} There has been no data from My Metric in the last 10 minutes {{/is_no_data}}
```


![Alert](/alert.png)
Bonus Question: 
![downtime](/downtime.png)
![downtimestartedemail](/downtimestarted.png)

# Collecting APM Data

![apmdashboard](/infaandapm.png)
https://app.datadoghq.com/dash/1033000/infrastructure-and-apm


Bonus Question
A service would be defined for a particular functional piece of your application such as a ui or backend microservices. A resource is a particular action in a service such as a specific endpoint in a service. 

# Final Question:
  I like to play a game with the option to pick servers in different regions. Previously I was able to select Singapore , Europe , or North America and recieve reasonable ping times. Since changing ISPs the ping times are all over the place. Sometimes NA is not even playable but Europe works great. Using the tcp_check module in datadog I can check my approximate ping time to a representative server in EU and NA to decide what is worth playing on. 

```
  [root@localhost tcp_check.d]# cat conf.yaml
instances:
  - name: EU Server
    host: 34.250.157.17
    port: 443
    timeout: 1
    collect_response_time: true
  - name: NA Server
    host: 54.194.95.138
    port: 443
    timeout: 1
    collect_response_time: true
 ```

![wtping](/wtping.png)
