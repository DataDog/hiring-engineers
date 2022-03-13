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
- **Static IP:**	`192.168.33.10`

*References*: 
[Vagrant: Setting Hostname](https://www.vagrantup.com/docs/networking/basic_usage#setting-hostname)

[Vagrant: Static IP](https://www.vagrantup.com/docs/networking/private_network#static-ip)

I've signed up for the trial account in the EU region of Datagog, [datadoghq.eu](https://datadoghq.eu/).
![New Account](/images/0_1_DD_account.png)

## 1. Collecting Metrics:

I've followed the QuickStart instruction to install the Datadog Agent v7 on my Ubuntu VM. It was automatically suggesting the correct **DD_SITE** and **DD_API_KEY** for my account.
```
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=a37ca623e45fa0c24da7daa976f9bfd0 DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
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

Once created, accessing the Dashboard from the Dashboard List in the UI:

### Set the Timeboard's timeframe to the past 5 minutes

![API Timeboard 5 min](/images/2_3_API.PNG)

### Take a snapshot of this graph and use the @ notation to send it to yourself.

![API Timeboard snapshot](/images/2_4_API.PNG)

![API Timeboard email received](/images/2_5_API.PNG)

### **Bonus Question**: What is the Anomaly graph displaying?

The anomaly function is applied to metrics to calculate an estimated expected value, based on the data collected in the past. It's useful to highlight anomalous behaviour of the metric during the collection interval. The function is represented graphically with a grey bundle on the metric that shows where the predicted sample should be included.
The datadog algorith to calculate