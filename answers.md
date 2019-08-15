## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise.

DataDog Test Environment (Step By Step) -
I am using an Window 10 Environment for quick deployments of VMs without the complexity of the infrastructure. However, there are many different types of environment like AWS, Rackspace, OnApp, Vmware, Openstack, etc.

1. Installed VirtualBox 6.0
2. Installed Ubuntu 19.04-live ISO to VirtualBox as VM.

<a href='https://photos.google.com/share/AF1QipPSU_on0EF3X7JrG1Zvn8K8Vz8udKpdFRby4moouGLbFZkQ_q4MY25zQ4hDpx_GTw?key=bmliSXlrenIwU2d3UV9UcE1DcWU1cDBub3RnTklR&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/GKuSWBE3xlKgJ1d-xWMlTanFMpKaS8yoV0ygBkRC_Kr-2OCHtdxdSt_MPUAXPwcqwx5lWVcPhf5qupv1t_aGVv_6wEkyc7yhDa4q0L4jdcoCPf0nUhQMaGe05-TqDxSwlahr5yhtyw=w2400' width="500" /></a>

3. Installed the Datadog Agent with the script below.

```
DD_API_KEY=(REMOVED) bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

<a href='https://photos.google.com/share/AF1QipPihy_WRyTybaI12AWNMfmIG4XRhLvMRbQziZ6evcEBdSfgq0OjHXxn9Znib3L5wQ?key=d1ZTMk0wMXFtZF9RMXVJVzZjUEdnaXI5QnlCMkZR&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/408ndZ1PpunAcOoVitoQwx1tu1RnX5ZwxMNB3qUEoxhmh6WWtjaAcE86AkEdS6bpd6oWiP7OWenjKcNsEdiBxWkrncKDcc2dIo6_mXNxvrs4hXOadyTfUg6ymDPfLZJdzcGgSoDdsg=w2400' width="500" /></a>

4. Found Permission errors running the Datadog agent with /etc/datadog-agent/datadog.yaml

<a href='https://photos.google.com/share/AF1QipMM89or3LdOzORcuZkcgn-0Ki4SXzp-oWH1qhlOu-ZttrzQ9f4gm1gXUs1RJoyXlQ?key=MzFMQjJsMkJ6OFFHREhJQ3NyU0VoX1p5bk5KcHNn&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/XK3v9BB5ABnlPuD_ecN3OUDoA3fw6ujJXh_zANcG5CNORTMRDA3IZLWi6XVhePr3YGogqhvt2o6kVHDyrMkiS6NBacAHzxy8YOfNs7HbOFbS41cifQhlpkW9tHzPhD0XlGH94J-9dg=w2400' /></a>

A quick resolution is to chmod 777 /etc/datadog-agent/datadog.yaml for testing purpose.

5. After fixing the permission issue, Datadog Agent will successfully start.
<a href='https://photos.google.com/share/AF1QipPcsCPQ0RmPu9we21bZBaMXoREHS-gJztZlhw5ukr0-6C3b-iLGhBFiiW39gt9ztA?key=dGd4NFFNVXMtMmdGNkFFd0t5b2tWYi1nZjVTS1Fn&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/TKPuiVIi15ynz3ZTUPRtJcXDut3O35KbbnpQurAxRDXMr0_JZSKf2qKlqJlhTuEZ6XVt-66c-Un2mkux9xqrGX5PECYxUwCRbhF-EnJMAI6neb6vsHnI03IiBuAoVB-RlNWAXnzCpQ=w2400' width="500" /></a>

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

<a href='https://photos.google.com/share/AF1QipMJ2HbktIRolA0zwE8rNReQGI3jzTHx4GUOkdD-RXL1veYvCx_IhgmLcUL0A6j8HQ?key=Z0FibmpQWkM1a0JIOXdKWTlIX2pWdlVoeXJneTdB&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/SAwoowjv_esV3z-vmUutliLqzO0UBjvaJKuwmrkk5xrG1q46Bje4_AsMVg8h-6i_JSkXT9RUW2SXChioR71EzxXBUc57CJR4RbxvIJ1v6rJx0Gcnf6pdnudw9x2BL10LpD3yxwRYGg=w2400' width="200" /></a>

## Collecting Metrics:

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Datadog Agent Status with tag settings.

<a href='https://photos.google.com/share/AF1QipNTa_qWEchmAY_spYTKUQtJxvCpCJix_V2PRKI1vOppIK58DdDiBny7XXIWwcBpbQ?key=XzdLLUcwWnotTXVtSGxscmpyMlJBVHpqVlUtSWRn&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/Z-VNr7TLJmsXcTYqOiMrhfV3gYC_eGfNIWOhkST_f79_VOhVMXkonLkN4GaL9IycrdAv-Ex_PbO2x9UvfaxBx7mrLkHnpr0Fa0UIe76WKJi5R6EnbUicdHOQrsKQ4oqtshQknK3thA=w2400' width="400" /></a>

Host Map and Tags are displayed below. [Link Here](https://app.datadoghq.com/infrastructure/map?host=1214193486&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

<a href='https://photos.google.com/share/AF1QipN7BdKk8ntQ1ipBiNtKx-4qoO3egaU1peCv3Jq0IExpE4-WF7kg3YnzLq0NpZbA1A?key=M0NfbGJ2WHQtWjJXQnlEcy1vU0J0Y0FRT1RsU05B&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/eQSnfIhc8TNFmrgbAaScU2mwwJ5dQCDdL1SLtendHAcfhAvb2-Qr9eme9RI-C2rVZ3IwTGVIepPmWSrJdJjbXdLtIBnq1AXR25zCo-YL2f-mJyWl18xZ2eh2HWxCURC5d4OrmBieRg=w2400'/></a>

DataDog Agent configuration file - How to setup tags in datadog.yaml
<a href='https://photos.google.com/share/AF1QipMiy5n7WYaq4SOIYFu57mIX-HrwzE4XWMWFH1ldUMEsNg_BjVMJrDsNFiHPiPZGFQ?key=MUdEVWZ2RUhObU1hMVM3TndQa2ZKQnNXanhTejln&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/xE6-yofYHc7a89yzfq7q0knCqoJQUYSd4l8qUGRW97DhX9ok5ZLL9jh34BCHFySBgkadwQ0osstypXAaZoikewb6X_cFRfgMszNJQwAi8yMd6DOSXh4650aNOc2J9v5-jMkfu_lYqQ=w2400' /></a>

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

1. Install MySQL with the below commands.
```
  1.1 Update the repository with “Sudo apt-get update”
  1.2 Installed mysql with “sudo apt-get install mysql-server”.
  1.3 Installed the policykit with “sudo apt install policykit-1”.
```

<a href='https://photos.google.com/share/AF1QipOnl9JSOKWM3li0G8ldxA2cxTStdZRZRFQqqvnipxbjq_hkmU_FGb9mh2Zx0kLxrA?key=MWV5dC1jdjVObUg2c0ptMFpjVnBLQjZtZFozSXhn&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/9HLxD2G5X1ypu91mRD4x7XuzVWf4yybTVTR_HTLE3MyjspuFC71PqLiw5ytpOPgXRMRNVrjUpY5-CWj5tmoBEgLOa6pC4iNAVKQyPCGKVC0AVmCVhQSTUi0mzKW-SGOpCt6XdvCGBQ=w2400' width="450" /></a>

2. MySQL Services have installed and started successfully.
    2.1 Update the firewall and rules to allow access to Mysql.
    ```
    sudo ufw allow MySQL
    ```
    2.2 Allow MySQL to launch on reboot of VMs.
    ```
    systemctl enable MySQL
    ```
    2.3 Create Username and password for Datadog in Mysql. Also allowng access to the Datadog agent to use the database.

```
    CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'datadog123';
    GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS;
    GRANT PROCESS ON *.* to 'datadog'@'localhost';
    SHOW databases like 'performance_schema';
    GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
```

<a href='https://photos.google.com/share/AF1QipMg4g2WNEV0uXaRQ4Qlqd8R8-hTCKi1ysQamgDGMcDEceOH1uUx9iIaPA5BnSN_Hw?key=c2FjMS1HOFF4dUFRX2NSanhuenF1ZVgyYThZOVdB&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/XejJ6-92YszvqPf04eWQ05tMC0UNLq2cCJzRuUZvGCgbrA1WpPEcgT-w0347DyWKhLfeij155hA7tUntzDGIdBCV7Mq1RItxarG63kxRj8SQEiYFjZ7lioQgqfupK4ZZ576uoy4hHw=w2400' width="450"  /></a>  

Created the configuration file for Datadog to access MYSQL. Inside the Datadog folder locate /etc/datadog-agent/conf.d/mysql.d and create new file called conf.yaml with correct permissions

```
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: 'datadog123' # from the CREATE USER step earlier
    port: 3306 # e.g. 3306
    options:
        replication: 0
        galera_cluster: true
        extra_status_metrics: true
        extra_innodb_metrics: true
        extra_performance_metrics: true
        schema_size_metrics: false
        disable_innodb_metrics: false
```

Datadog agent is now collecting data. [link here](https://app.datadoghq.com/infrastructure/map?host=1214193486&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&app=mysql)

<a href='https://photos.google.com/share/AF1QipN4e3qrf7WzLR3Uz8-YYztZnQVCs4Oxugw0fjMJkszzcmFgVebrMGhGV0ayr8rBIw?key=T0lObkhlcmZQVE91WGdEUzhVNVBfT1dxd0l5WVBn&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/rf3wPi-9dDBdKdX6-FwLrwtxDnWC9-Vvfqu61E-81qkK0Mk3I9YaG0UEgRr4vZjyjoCoVMUCimUDwJtlMoALv5f67JlokmQrW_He6fDoc0z5JdBgEIpDDcvpCPv4w4EgGNxRPZZ7Qw=w2400' /></a>

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

1. Create Python script at /etc/datadog-agent/checks.d/custom_rdata.py and restart the Datadog agent.

Download the file [Here](https://drive.google.com/file/d/1w2p2UTm---PQDDCScSF6gXvzH-eVjbDQ/view)
```
from checks import AgentCheck
from random import randint
__version__ = "1.0.0"
class rdata(AgentCheck):
    def check(self, instance):
        self.gauge('rdata.my_metric', randint(0,1000))
```

2. Then stop and restart the Datadog agent to collection data.
```
sudo systemctl stop datadog-agent
sudo systemctl start datadog-agent
```

3. You can check if the script works via the Datadog Metric UI with “rdata.my_metric”. [Link Here](https://app.datadoghq.com/metric/explorer?live=true&page=0&is_auto=false&from_ts=1565009659540&to_ts=1565013259540&tile_size=m&exp_metric=rdata.my_metric&exp_agg=avg&exp_row_type=metric)

<a href='https://photos.google.com/share/AF1QipPtUh7FhLTrT2YinDBhqjgIf3Eg0X4twiylM9S909mlJnWQpGnvmGdaJc4bX2i-1g?key=MGpXSURnRzY4ZHZVbWh2RnVoUXFPUFlGNUNOTEl3&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/6D1xbVy4RMSKX5QsgNpsLY3Tq7by-vWyMLRqL1OjW5TAODhpWXNfvyFznJksAiuot2lHY-oSl1hqEJKR3gXcpBtT1pmq6V7dJzJs01_GN6n_9zuuQ3ttLe7E9nkb-aIU6ONo8qC1aw=w2400' width="600"  /></a>

Change your check's collection interval so that it only submits the metric once every 45 seconds.

1. Create Python script at /etc/datadog-agent/conf.d/rdata.yaml and restart the Datadog agent.

Download the file [here](https://drive.google.com/open?id=1Y2BH1aDV3ZAYob11ZtBFIkZVE0aUs5X8)
```
init_config:

instances:

  - min_collection_interval: 45
```

2. Then Command to stop and restart the Datadog agent, then check data collection on the dash UI.
```
sudo systemctl stop datadog-agent
sudo systemctl start datadog-agent
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes that is possible by modifying the rdata.yaml and changing the “min_collection_interval” with another value to collect data at different intervals.

# Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host. (DONE)
* Any metric from the Integration on your Database with the anomaly function applied. (DONE)
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket (DONE)

[LINK TO THE TIMEBOARD](https://app.datadoghq.com/dashboard/9mc-7ck-mnr/my-timeboard?from_ts=1565099088591&to_ts=1565102688591&live=true&tile_size=m)

1. Installed with PIP for datadog as it was erroring with missing Python library.

<a href='https://photos.google.com/share/AF1QipPYDdWVN1pGxcQIG_v5onsxuvqlvlaIzeI3dXkfy8uk8yLGQkwPtyR5GfE1ZWXu1g?key=Y1NNOVJjRXVTWm9BNDRHNEhIUmtSMkVlWl8zWF9R&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/NrFsntrDwk-zOXZZ1EstujaN7iI3PLqJLiEaliN00gZreG3QIrYuP69eb5vJippnXtiDNy27ycZnrQ-0AsGbAbIa_kXHQc2HyWWaXHjcqYNSRVAwFePuZslNb9Ypq7BHJNO-DR0kGA=w2400' /></a>

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard. (DONE)

Download the file (removed)
```python
from datadog import initialize, api

options = {
        'api_key': 'REMOVED',
        'app_key': 'removed'
}

initialize(**options)

title = 'My TimeBoard'
widgets = [{
        'definition': {
                'type': 'timeseries',
                'requests': [
                    {'q': 'avg:rdata.my_metric{*}'}
              ],
              'title': 'My Custom Metric Graph'
    }
},
{       'definition': {
                'type': 'timeseries',
                'requests': [
                    {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
              ],
              'title': 'MySQL with Anomalies Graph'
     }
},
{        "definition": {
                "type": "timeseries",
                "requests": [
                     {'q': 'rdata.my_metric{*}.rollup(sum,3600)'}
                ],
                "title": "My Custom Metric Roll-up Graph"
      }
}]
layout_type = 'ordered'
description = 'A dashboard with random data'
is_read_only = True
notify_list = ['xxxx@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'host1'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
```

Set the Timeboard's timeframe to the past 5 minutes (DONE)

<a href='https://photos.google.com/share/AF1QipOVUjjrOQBsg4ezv16AxKS1V0rXPgm1DJPpnqQwSjYk416kQekNxCeCdx9pa-t1Uw?key=Yk9rcEY5eUlxQ21mZGVCYW8xZTV3VS1Ub1JMMmJB&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/_zTRq78PK9QxzCt5ZFDZFwwCGCJcmIDfOPGBY1K2UNXn-TaKEsHrlzYa4qYkqGGxIaXmpWUei8gPyeFx0GlQAqgk7FriSG3TgRBOAuw38TgyTXIKc_glrXWv4oeFq56xGrSbjnGjqA=w2400' width="600" /></a>

Take a snapshot of this graph and use the @ notation to send it to yourself. (DONE)

PHOTO REMOVED

•	Bonus Question: What is the Anomaly graph displaying?

The Anomaly graph is displaying abnormal behaviour by the data, which uses the high and low data value to determine its threshold.

## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500 (DONE)
* Alerting threshold of 800 (DONE)
* And also ensure that it will notify you if there is No Data for this query over the past 10m. (DONE)

[LINK TO THE DATADOG PAGE](https://app.datadoghq.com/monitors#10799322/edit)

PHOTO REMOVED

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers. (DONE)
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state. (DONE)

```
{{#is_alert}} Alert on host {{host.ip}} at {{value}} with custom metric. {{/is_alert}} {{#is_warning}} Warning on host {{host.ip}} at {{value}} with custom metric. {{/is_warning}} {{#is_no_data}} No Data on host {{host.ip}} with custom metric. {{/is_no_data}}
```
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state. (DONE)
* When this monitor sends you an email notification, take a screenshot of the email that it sends you. (DONE)

PHOTO REMOVED

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F, [Link to Datadog](https://app.datadoghq.com/monitors#downtime?id=582265222)

PHOTO REMOVED

And one that silences it all day on Sat-Sun. [Link to Datadog](https://app.datadoghq.com/monitors#downtime?id=582265222)

PHOTO REMOVED

Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

PHOTO REMOVED

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

Code for the APM.py script and Download File [Here](https://drive.google.com/open?id=10u26jL3yKqfs878nfsea30n8EdpcU0bR)

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

1. Installed ddtrace to run the APM.py script.
```
pip install ddtrace
```

<a href='https://photos.google.com/share/AF1QipM5-aMpuRPE_Gmk95SFJY81sxu9d9S-WcJsmx1cC5gzJmn9JODap3n_AhP_ZzAIKw?key=dTFGQU9aYXN4TkpPdGlSRHdRQUZuZjZydTRCYnBR&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/yyIilRoVlQbeDubs30ltNvvC-knmJhrc_omkIyqJOc3ax0nLaleQ1THRcyWEFrqyOjriA0TAHNKBtTGmeMU8sUMVL_dilth_b1ipQDrJI7yP1lqIHqNiNrV_cOM3GLRY5hcn7AmEKQ=w2400' /></a>

```
Ran the script with ddtrace-run python APM.py
```

<a href='https://photos.google.com/share/AF1QipOFmwKjSSPkqSZg5oZGR0lBxweoo5aspdzOb26wlAGWvsC0ymf0WnxNl4iFBcx5Lw?key=YWw4SFNIcnY5QUxRdVp6ekNwZEcyZ2l6c1k5S1dR&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/0pozLS1zNKLQvB9gjbH6MAK7NUMoEii7WjP8jcs-F6mV6jMBm3lTB1zMMxk-YVUVlZifU6dBHNSV-cV2HEmOJERBCPUYDlP5U20Mv4aCsyF1B0fWqqnsNgyRMCsh8c7cqSr6qAarTg=w2400' /></a>

Generate some logs with the below commands via IE or any browser.

```
http://10.174.1.182:5050/api/apm
```

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
[Link to the DataDog page](https://app.datadoghq.com/apm/service/flask/flask.request?end=1564995594417&env=none&maxPercentile=100&paused=false&start=1564991994417)

<a href='https://photos.google.com/share/AF1QipNQa-FZ_ShpfQd7XAvMRVNjSGG-1AamXNBX3Gveb8b95FD7jmnXOEM2LOZYdN5Mrw?key=T3RHQlhGUlJBUGp5UnFDOWE1WkpOVVN0VS12b1BB&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/vmhB6URWzoiccvZVJHEza3tUxHjraXzegbLE-AVq8QphNTKA3dSK3zr64nT_AJZ-lo6RlwyG8l9Bm5vJarDx6SXUN0yoRgez-VNEHzzchV3Yhjwm5sLYN0sf-jCswIS6YiN3OwSWJQ=w2400' width="600"/></a>

Screenshot with APM and other data. [Link to the DataDog page](https://app.datadoghq.com/dashboard/ey3-dqm-p86/my-flask-http-and-other-info?from_ts=1564999539014&to_ts=1565000439014&live=true&tile_size=m)

<a href='https://photos.google.com/share/AF1QipM3emLkSMmbVqSfxmOimlgD-vF0VYryagFLIm53qfPnWy0SrA0jdnmFjp9C886pSQ?key=bGJka3JFZW5jd3RFbjNra3lzS284TGYzZGNKRklR&source=ctrlq.org'><img src='https://lh3.googleusercontent.com/z6o3l5cfH86Huj1sIjcVKVtd6OfOOULSpQ4Ag0SKS6GQ47407DjQj3-exgqN9vpdJ17v75MVysmBe9nwGKxuLDg4gP4tJuGJfT2bLbF8fcOiwUVGzlS10-aXD_-1KUf3MyyiFDK6lg=w2400' width="600" /></a>

* **Bonus Question**: What is the difference between a Service and a Resource?

A service is a set of processes that do the same job for example a single web application or database. The resource are subcomponents that act to serve the actions of the service for example paths for web services or queries for searching databases.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

The future is in Industry 4.0, where everything will be automated and what you see today will be smarter. Datadog is an innovative and open platform that can fit into any industry like banking, big retail, supermarkets, logistic, distribution centres, etc. Some Customer Opportunities that fit here are Coles, Woolworth, Australia Post, Commonwealth Bank, MYER, David Jones, etc.

For example in Banking, Datadog can be customised to monitoring performance and do automated task like health checks to detect issues based on workloads for hybrid cloud to LoT devices. More ATMs, mobile POS and automated services will be deployed in the future, so Datadog will be the heart of the platform that glue all the other solutions together including integration with cyber security (VM or appliances) systems.
