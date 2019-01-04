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
Once your yaml is defined you can start/restart the agent by `service datadog_agent restart` and it should start reporting info. If you don't believe its working you can check what it is doing with ` datadog-agent status` . If that tells you that something like "Could not reach agent" you can check /`var/log/datadog/agent.log` to see what happened. 
Once its started you should see an event in your datadog panel as well as a host in the host map with the tags defined in your yaml file.
![tags](/tags.png) 

 The next step was to install a database. I installed Postgres from yum and started it up. Following the instructions on the integration page , the first step is to create a user to allow datadog to talk to my database. Once the user was setup and tested with the provided command you are ready to let the agent know you want it to monitor Postgres. This is done by creating a yaml file in `/etc/datadog-agent/conf.d/postgres.d`from the provided example. To get started all you need to add is your login information you created in the previous step.
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

Despite all the out of the box funcionality provided by Datadog, occasionaly you may find the need to create a custom metric to gather data from some proprietary application. This requires two parts. The [actual check](/checks.d/my_metric.py) which would be a python script under checks.d and a [yaml file](/conf.d/my_metric.yaml) under conf.d to tell datadog to look for your check. These two files need to have the same name so the agent knows what to look for. This sample my metric simply picks a random number between 1 and a 1000 and sends it to the agent. 
In the past I have used a custom check to warn us of an impending SSL cert expiration although this is now built into the http check. I found this wonderful check [online](https://github.com/dobber/datadog-ssl-check-expire-days) and its a good example to show that you can add variables in your yaml file to avoid having to change your python check for different sites. 


## Changing the collection time and Bonus Question 

By default datadog will run your check every 15 seconds. If you don't want to spam your monitored application/site you can modify the yaml file to change the collection interval. For instance to have it only look every 45 seconds you can add a - min_collection_interval: 45 to your instance in the check's yaml file. 

```
init_config:

instances:
  - min_collection_interval: 45

```

If you had no issues with yaml symtax running `datadog-agent status` should show that your custom check is running only about a third as many times as the default checks.

```
    
    memory
    ------
      Instance ID: memory [OK]
      Total Runs: 107
      Metric Samples: Last Run: 17, Total: 1,819
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
      
    
    my_check (unversioned)
    ----------------------
      Instance ID: my_check:5ba864f3937b5bad [OK]
      Total Runs: 36
      Metric Samples: Last Run: 1, Total: 36
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s

 ```

# Visualizing Data

Geting data into Datadog is only the first step! Building a timeboard so you can see what is happening or how various things interact at any given point of time is a very powerful way to get insight into your system. You can create a timeboard via the easy to use datadog GUI or once you realize the instructions for this exercise call for you to use the API you can follow the [great documentation](https://docs.datadoghq.com/api/?lang=python#overview) available. 

In just a few minutes, even as a non developer I was able to create a python script to call the API and create my timeboard. To start off I created a new API key and an APP key from the Integrations/API menu in the datadog UI. With these keys you can start off your script following the [authentication section of the documentation](https://docs.datadoghq.com/api/?lang=python#authentication).

With the goal of createing a timeboard I skipped down to the [timeboard section of the docs](https://docs.datadoghq.com/api/?lang=python#timeboards) 
After adding the timeboard section to the auth section from the previous step , I modified the title and started building out the graphs. The only parts that needed changeing from the example were the title of my graph and the data I actually wanted displayed. Building out the requests section of the graphs dict can be a bit daunting but there is an easy way to cheat. If you build your graph in the UI , you can select JSON in the timeserieres editor window and it will give you everything you need to create that graph via api.

![graph definition](/json.png)

The only other change from the examples was I saved the request to a variable and printed it so I could see whether my script succeeded or failed.

```
response = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     )
print response
```

After pasting together the two sections from the examples and modifying them with my graphs I came up with [this script](apitimeboard.py). When ran I got back a handy chunk of JSON letting me know it succeded!

```
python apitimeboard.py 
{'dash': {'read_only': False, 'description': 'An informative timeboard.', 'created': '2019-01-02T02:11:30.400016+00:00', 'title': 'API Timeboard', 'modified': '2019-01-02T02:11:30.400016+00:00', 'created_by': {'handle': 'mbattaglia@gmail.com', 'name': 'Michael Battaglia', 'access_role': 'adm', 'verified': True, 'disabled': False, 'is_admin': True, 'role': None, 'email': 'mbattaglia@gmail.com', 'icon': 'https://secure.gravatar.com/avatar/32aa83522024c737ebea50bcd564b552?s=48&d=retro'}, 'graphs': [{'definition': {'viz': 'timeseries', 'requests': [{'q': 'avg:my_metric{host:exercisevm}'}], 'events': []}, 'title': 'My Metric on exercisvm'}, {'definition': {'viz': 'timeseries', 'requests': [{'q': "anomalies(avg:postgresql.rows_returned{host:exercisevm}, 'basic', 2)"}], 'events': []}, 'title': 'Integration with anomaly'}, {'definition': {'viz': 'timeseries', 'requests': [{'q': 'avg:my_metric{host:exercisevm}.rollup(sum, 3600)'}], 'events': []}, 'title': 'My metric rolled up to an hour'}], 'template_variables': None, 'id': 1033029}, 'url': '/dash/1033029/api-timeboard', 'resource': '/api/v1/dash/1033029'}
```
I was then able to browse over to my timeboard at https://app.datadoghq.com/dash/1033029/api-timeboard and see what I created.

Next I wanted to be able to show someone what was happening in the last 5 minutes with my postgres integration I graphed. This was as simple as clicking on the graph and selecting the time period I wanted to view. This allows you to set the timeboard to virtually any time period. After that you can click the annotate button which opens up a window where you can put in comments and @a coworker, yourself or datadog support. 
![annotate](/annotate.png)
Here is a graph showing the last 5 minutes of Rows Returned from the Postgres Integration. It is showing the metric itself in blue with the accepted range in grey. Where the line goes red , it shows values outside the accepted range.
![Last 5 Minutes](/last5.png)

# Monitoring Data

Since you can't stare at graphs 24 hours a day , you can let datadog monitor your data and let you know when something is not quite right. In this case I am monitoring the custom metric my_metric. To do this you would click on Monitors and then New Monitor on the left side of the datadog UI. Choose your metric and define when you want it to alert.
![Monitor](/monitor.png)
This will warn me if my_metric goes above 500 and then go to alert status at 800. I also told it to notify no data is recieved for more than 10 minutes which would also indicate a problem.

After defining what I want the monitor to watch , I can now define who and how I want to be notified. In this case I want my email notified on warning, alert, and no data. The syntax for this is very easy to learn with autocomplete in the UI. Here I was able to setup a notification with the same @User used when sending annotations.  It also tells me the ip of the host that is alerting and what the value is. 


```
@mbattaglia@gmail.com

{{#is_warning}}
My metric is currently {{value}} on {{host.ip}}
{{/is_warning}} 

{{#is_alert}}
My Metric is currently {{value}} on {{host.ip}}
{{/is_alert}} 

{{#is_no_data}}
There has been no data from My Metric in the last 10 minutes
{{/is_no_data}}
```
Of course since my metric is all over the place , I quickly got an email letting me know that on 10.0.2.15 my metric is at a warning state with a value of 799 (just below the alert threshold!)
![Alert](/alert.png)



You could also have seperate notifications for warning and alerts , say you wanted the warning to show up in slack but if it hits alert to send to pagerduty by moving the @ into the appropriate section

```
{{#is_warning}}
@myslack
My metric is currently {{value}} on {{host.ip}}
{{/is_warning}} 

{{#is_alert}}
@mypagerduty
My Metric is currently {{value}} on {{host.ip}}
{{/is_alert}} 

{{#is_no_data}}
@mypagerduty
There has been no data from My Metric in the last 10 minutes
{{/is_no_data}}
```

You can also schedule downtimes to silence the Monitor when its not needed. In this case, I only wanted notifications during office hours.
This can be used to silence alerts during non critical times so your team can get a decent night's sleep or a 1 time downtime during a maintenance window so you can focus on your maintenance and not checking on alerts.  
To do this , go to Monitors and manage downtime on the left. On the manage downtime page you can select "Schedule Downtime".
From there simply select monitor you wish to schedule downtime for and the times you want your monitor to be quiet. 
I have one downtime for the weekends:
![noweekend](/noweekend.png)
and one for weekday evenings and nights:
![nonight](/nonight.png)


You can get an email when the downtime is scheduled:
![downtime](/downtime.png)
You can also set it to send an email when the actual downtime starts :
![downtimestartedemail](/downtimestarted.png)

# Collecting APM Data
 Being an Infrastructure person by trade , I used the [sample flask application](/sample.py) for the APM task. I started by adding the following lines to the datadog.yaml and restarting the agent. 
 ```
 apm_config:
  enabled: true
 ```

 The next step was to tell the application to send data to the agent. I first attempted that by adding a few lines to the begining of my sample app. 
```
from ddtrace import patch_all
patch_all()
```
Unfortunatly flask was complaining about ports being in use already even though according to netstat they were not. Luckily there is another way to instrument the application and it doesn't involve modifiying the code nor did it complain about the port being used. 

I commented out the above lines and simply started my application through ddtrace with the following command:

`ddtrace-run python sample.py`
Once the app was up and running , I was able to spam  a couple hundred `curl localhost:5051/api/trace ` and `curl localhost:5050/api/apm' to get some data generated.
The Apm data in of itself can be pretty useful , but it gets even more powerful when combined with infrastructure metrics to see a correlation between the application layer and infrastrucure layer.
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
