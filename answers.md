## Hiring Exercise - Solutions Engineer

**Candidate**: Giada Valsecchi

**Date**: March 2022

**Role**: Sales Engineer for the Dublin team

## 0. Prerequisites - Environment

As suggested, I've set up a new linux VM via Vagrant and Oracle Virtual Box on my Windows PC. I've used the an Ubuntu 18.04.3 LTS box for the full exercise.
```
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
end
```
Later in the exercise, I've modified the basic Vagrant configuration file to assign a custom hostname to the guest VM and provided it with a static IP, in order to reach some of the opened ports from the browser of the host machine. In the first screenshots, you'll see the standard hostname `vagrant` instead.
- **VM Hostname:**	`v-giada-host-1`
- **IP:**	`10.0.2.15`
- **Vagrant Static IP:**	`192.168.33.10`

*References*: 

[Vagrant: Setting Hostname](https://www.vagrantup.com/docs/networking/basic_usage#setting-hostname)

[Vagrant: Static IP](https://www.vagrantup.com/docs/networking/private_network#static-ip)

I've signed up for the trial account in the EU region of Datagog, [datadoghq.eu](https://datadoghq.eu/).
![New Account](/images/0_1_DD_account.png)

## 1. Collecting Metrics:

I've followed the QuickStart instruction to install the Datadog Agent v7 on my Ubuntu VM. It was automatically suggesting the correct **DD_SITE** and **DD_API_KEY** for my account.
```
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=XXXXXXXXXXXXXX9bfd0 DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

The installation prompt ended successfully and, in a few minutes, the UI's Infrastructure List and Map were showing the first entry.
![Infrastructure List](/images/1_1_Infrastructure_List.png)
![Host Map](/images/1_2_Host_Map.png)

--------

### Adding tags in the Agent config file

I've followed the Datatog documentation on the configuration file of the Agent. The `datadog.yaml` file is located in the `/etc/datadog-agent/` directory. I modified the `@param tags` paragraph of the configuration file and restarted the agent with the command:
```
sudo service datadog-agent restart
```
Initially, I've added only two custom tags:
- **project:hiring_exercise**
- **owner:giada**

![Tags on yaml](/images/1_3_tags.png)
![Tags on UI](/images/1_4_tags_on_UI.png)

---------

### Installing a MySQL database and the respective Datadog integration for that database.

I've installed a MySQL DB using the following tutorial:
- [How To Install MySQL on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04)

The version installed is: 5.7.37-0ubuntu0.18.04.1 (Ubuntu)

The MySQL integration is already included in the Datadog Agent checks, so I followed the dedicated page on the Datadog docs to setup the DB. First, I had to create a DB user for the DD agent with the proper privileges to collect the metrics.
```
mysql> CREATE USER 'datadog'@'%' IDENTIFIED BY '<UNIQUEPASSWORD>';
```
Checking if it was created properly:
```
mysql> SELECT user,authentication_string,plugin,host FROM mysql.user;
```
![MySQL Datadog user](/images/1_5_mysql.png)

Granting the needed privileges:
```
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'%' WITH MAX_USER_CONNECTIONS 5;
mysql> GRANT PROCESS ON *.* TO 'datadog'@'%';
```
Provided query for checking the privileges:
```
mysql -u datadog --password=<UNIQUEPASSWORD> -e "show slave status" && \
echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
```
![MySQL Datadog user privileges](/images/1_6_mysql.PNG)

Granting privileges on `performance_schema` to collected additional metrics ( for `extra_performance_metrics` that need to be enabled explicitly, see below):
```
mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'%';
```
Then, a few changes on the agent configuration were requested. 

The related yaml file for DD Agent v7 is located in the `/conf.d/mysql.d` directory. I've copied and modified the already existing `conf.yaml.example`, assigning to the new `conf.yaml` file the proper owner and group, `dd-agent:dd-agent`.
I've changed the suggested parameters for the **Metric collection**, as in the guide:
[Metric collection - MySQL on Host](https://docs.datadoghq.com/integrations/mysql/?tab=host#metric-collection).

```
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: '<YOUR_CHOSEN_PASSWORD>' # from the CREATE USER step earlier
	## single quotes needed for the special character
    port: 3306
	## I used the default one, 3306
    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
	  disable_innodb_metrics: false
	  schema_size_metrics: false
      extra_performance_metrics: true
            
```
A few minutes after restarting the agent, the MySQL integration showed up in the UI.

![MySQL Integration UI](/images/1_7_mysql.png)

I used the Agent commands to view the MySQL check:
```
sudo -u dd-agent -- datadog-agent check mysql
```
![MySQL check](/images/1_8_mysql.PNG)
![MySQL issue 0](/images/1_9_mysql.png)
**_Note_**: As you can see from the check and also in the UI, there's an Integration issue:
>Datadog’s **mysql** integration is reporting:
>* Instance #mysql:ae58c35fcae584e7[WARNING]: Failed to fetch records from the perf schema >'events_statements_summary_by_digest' table.

I've checked the existence of the mentioned table in the `performance_schema` and also run without issues a simple SELECT query on it, with the datadog user. 

![MySQL issue 1](/images/1_10_mysql.PNG)
![MySQL issue 2](/images/1_11_mysql.PNG)

I've decided not to carry on further analysis on the issue because it was outside the exercise scope.


For the **Log collection** part, I followed the docs:
[Log collection - MySQL on Host](https://docs.datadoghq.com/integrations/mysql/?tab=host#log-collection).

First of all, I changed the `/etc/alternatives/my.cnf` to enable general, error, and slow query logs, and I restarted the `mysql.service` service. 

I granted the `read` access to other users (including dd-agent) on the `/var/log/mysql` directory and files with `chmod -R 754 mysql`.

Finally,I modified the `conf.yaml` check configuration file in `/conf.d/mysql.d` with the following:

![MySQL logs 1](/images/1_13_mysql.PNG)
![MySQL logs 2](/images/1_14_mysql.PNG)

With the `sudo datadog-agent status`, I noticed an error reading the log files that I solved giving a `chmod 755 mysql` to the directory.

![MySQL logs 3](/images/1_15_mysql.PNG)
![MySQL logs 4](/images/1_16_mysql.PNG)

-----------

### Creating a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I've tried to follow the example given in the docs (Ref:[Custom Agents Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#custom-agent-check) ) but I had a few errors with the code provided. I've then adapted to the case what I found in [Metric Submission: Custom Agent Check](https://docs.datadoghq.com/metrics/agent_metrics_submission/?tab=gauge).

I've used the following names:
- **Custom AgentCheck:**	`custom_giada`
- **my_metric:**	`giada_custom.metric`

I've created the python definition of the AgentCheck in `/etc/datadog-agent/checks.d`, in the file `custom_giada.py`:
```python
## Custom Agent Check for the hiring exercise
#  It submits a metric called "giada_custom.metric"
#  with a random value between 0 and 1000.

import random

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"

class MyClass(AgentCheck):
    def check(self, instance):
        self.gauge(
                "giada_custom.metric",
                random.randint(0, 1000),
                tags=["custom_metric:yes","metric_submission_type:gauge"],
                )
```
Then, I've created a name-matching directory, `/conf.d/custom_giada.d/`, where I created a new configuration file `custom_giada.yaml` that reports a sequence called ` instances ` that contains one empty mapping.
```
instances: 
	-{} 
```
Each of these new files and directories are assigned to `dd-agent:dd-agent` user and group. After the agent reboot, the check was online and the custom metric was visible from the UI.
```
sudo -u dd-agent -- datadog-agent check custom_giada.py
```
![Custom AgentCheck](/images/1_17_custom_check.PNG)
![Custom Metric](/images/1_18_custom_check.PNG)

------------

### Changing the check's collection interval so that it only submits the metric once every 45 seconds.

To change the collection interval, I've modified the `custom_giada.yaml` in `/conf.d/custom_giada.d/`, inserting the parameter in the existing instance: 
```
instances: 
	#-{}
	- min_collection_interval: 45
```
-----------

### **Bonus Question**: Changing the collection interval without modifying the Python check file you created

The most straight-forward way to change the collection interval seems to me the one above, that modifies the yaml file and not the python file. It is also possible to modify the collection interval globally in the `datadog.yaml` configuration file but it affects the collection interval of all the checks.

-----------

## 2. Visualizing Data:

In order to use the Datadog API, I had to install the `python3-pip` libraries on my VM and the `datadog-api-client` component. 

I had some issues with the installation command below, that was constantly stopping with an SSL_ERROR with the certificate provided by [api.datadoghq.eu](https://api.datadoghq.eu/). 
```
pip3 install datadog-api-client
```

The error on the certificate was unexpected, because the root CA list on the VM was already updated. Also, the certificate check from the client was OK.
At last, I've tried to patch the VM instance in general, without success. 

The issue was solved with an upgrade of the `datadog-api-client` component.
```
pip3 install --upgrade datadog-api-client
```

I collected the keys that need to be exported as environment variables from the **Organization Settings** page on the UI, where I also created the Application Key called *Dashboard*:

- **DD_SITE**="datadoghq.eu" 
- **DD_API_KEY**="XXXXXXXXXXXXXXXX9bfd0" 
- **DD_APP_KEY**="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX4d97c" 

![APP Key](/images/2_1_API.PNG)


Then, I've followed the tuturial for creating a new dashboard using the API, using python language. 
[Using API: Create a new dashboard](https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard)

I compared a few examples to find something simple that I could adapt to my scope. I finally found an example that could suit me in the public GitHub repository:

[datadog-api-client-python/examples/v1/dashboards/](https://github.com/DataDog/datadog-api-client-python/tree/master/examples/v1/dashboards).

I've tried to understand the definitions of the widgets here:
[Datadog API Client for Python](https://datadoghq.dev/datadog-api-client-python/datadog_api_client.v1.model.html) .

![API Timeboard](/images/2_2_API.PNG)

The script I produced is the **_Timeboard_API.py_** included in the **code** folder of the repository. I used the following commands to launch it:
```
export DD_SITE="datadoghq.eu" DD_API_KEY="XXXXXXXXXXXXXXXX9bfd0" DD_APP_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX4d97c" 

python3 Timeboard_API.py
```

---------

Once created, I was able to access the Dashboard from the Dashboard List in the UI:

### Set the Timeboard's timeframe to the past 5 minutes

![API Timeboard 5 min](/images/2_3_API.PNG)

### Take a snapshot of this graph and use the @ notation to send it to yourself.

![API Timeboard snapshot](/images/2_4_API.PNG)

![API Timeboard email received](/images/2_5_API.PNG)

### **Bonus Question**: What is the Anomaly graph displaying?

The anomaly function is an algorithmic feature that could be applied to metrics to calculate an estimated expected value, based on the data collected in the past. It's useful to highlight anomalous behaviour of the metric during the collection timeframe taken in exame. 

The function is represented graphically with a grey band around the metric line, that shows at first glance if the new collected value lays within the predicted ones. If the new value is outside the standard deviation calculated by the function, the data is highlighted in a different colour. 

The tolerance of the band is controlled by the parameter `bundle`, that in my example is set to 2. The chosen `algorithm` is *basic*.

Datadog algorithm adapts its prediction to the metric’s baseline. In fact, considering the peaks of the metric used in my Dashboard, the anomaly function graph of my example shows different forecast when the time-frame is changed (in the pictures below: 15 min, 1 hour, 1 day). Collecting metrics from a empty DB, almost all of them were basically flat so I had chosen the only one that was floating.

![Anomaly function 15 min](/images/2_6_API.PNG)

![Anomaly function 1 hour](/images/2_7_API.PNG)

![Anomaly function 1 day](/images/2_8_API.PNG)

---------------

## 3. Monitoring Data

As requested, I've used the Monitor UI to create a monitor that watches the average of `giada_custom.metric` and alerts the team if the value exceedes the indicated threshold for 5 minutes. 

![Monitor creation](/images/3_1_monitor.PNG)

**Alert Conditions:**

* Warning threshold of 500
* Alerting threshold of 800
* Sending a notification if there is No Data for this query over the past 10m.

![Alert conditions](/images/3_2_monitor.PNG)

The customized monitor's message should have the following features:

* Sends an email whenever the monitor triggers.
* Shows different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Includes the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

I've used the condition variables to modulate the message for different triggers: Alert, Warning, No data. 

I've included different texts and recepients (actually, always me...) in the same body. I've also used message variables to generalize the message, such as `{{value}}`, `{{threshold}}`, `{{host.name}}` and `{{host.ip}}` ^[note].

![Monitor message](/images/3_3_monitor.PNG)

*References*: 
[Notifications](https://docs.datadoghq.com/monitors/notify/#message-template-variables) ,
[Conditional Variables](https://docs.datadoghq.com/monitors/notify/variables/?tab=is_alert#conditional-variables).

The message written for the exercise is not taking into consideration any recovery condition. 

The full body is:

```
{{#is_alert}}
{{override_priority 'P1'}}

@giada.valsecchi@live.it

**Avg of giada_custom.metric** on host **{{host.name}}**, IP **{{host.ip}}**, is **over threshold** ( >= {{threshold}})!!!
**Breached value** = {{value}}  at {{last_triggered_at}} 

{{/is_alert}}

<!--EndFragment-->


<!--StartFragment-->

{{#is_warning}}

@giada.valsecchi@live.it 

**Avg of giada_custom.metric** on host **{{host.name}}**  has reached a **warning value** ({{warn_threshold}} <= x <=  {{threshold}})!
**Last value** = {{value}}  at {{last_triggered_at}} 

{{/is_warning}}

<!--EndFragment-->


<!--StartFragment-->

{{#is_no_data}}

@giada.valsecchi@live.it 

Agent on host **{{host.name}}** has not been sending data for **giada_custom.metric** since {{last_triggered_at}} 

{{/is_no_data}} 

<!--EndFragment-->
```
The new monitor in the UI Monitor Page:

![Monitor list](/images/3_4_monitor.PNG)
![Monitor](/images/3_4b_monitor.PNG)

Below, a screenshot of the emails received (The ALERT and the NO DATA images were taken on [TEST] emails. The metric and the value are flat, at 0.0):

![Monitor WARNING email](/images/3_5_monitor.PNG)
![Monitor ALERT email](/images/3_6_monitor.PNG)
![Monitor NO DATA email](/images/3_7_monitor.PNG)

^[note]  The `{{host.ip}}` variable is not providing the expected value. I've researched in the documentation to find the definition of the default `host` tag, in order to check field called `host.ip` and giving it the IP value.

  The entry in the infrastructure list is showing the IP field populated with the same IP that is found with the `ifconfig` command. 
 
  ![Monitor host.ip issue](/images/3_8_monitor.PNG)
 
  I wasn't able to find a solution to the issue above.
 
----------

### **Bonus Question**: Setting up two scheduled downtimes for this monitor:

1. One that silences it from 7pm to 9am daily on M-F,
2. And one that silences it all day on Sat-Sun.
  
I've created two recurring monitor downtimes from the **Manage Downtimes** in Monitor UI list. In order to use only two conditions for the above requests, I've used two recurrence rules (RRULE) that shift a little from the indication, but the outcome should be the same. 

The condition 1.) is scheduled from the following Monday at 07 pm, with a duration of 14 hours, and with the following Recurrence Rule:
```
FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU,WE,TH,FR
```
 ![Monitor downtime M-F](/images/3_9_monitor.png)
 
The condition 2. is scheduled from the following Saturday at 09 am, with a duration of 2 days, and with the following Recurrence Rule:
```
FREQ=WEEKLY;INTERVAL=1
```
 ![Monitor downtime weekends](/images/3_10_monitor.png)
  
I've received an email notification when the downtime was scheduled, as indicated in the *Notify your team* settings.

 ![Email downtime schedlued](/images/3_11_monitor.png)
 
----------
 
