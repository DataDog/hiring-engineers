# Dashboard your Data with Datadog
<div>
	<img height=264px src='https://lh5.googleusercontent.com/JWhnhDyCMMNY9cbyJt-agRa6JVNVCRKsMaeacHjdlMcIJx9FDK6XSlAAv9KUm6EA__DtOXK8VpvrjVspY5ccht-ye-dlDd5INbslH5eer4rhEoINidX9YzbbV1LpL9VSl0hs8atr'>
		<img src='https://lh6.googleusercontent.com/xBtUnzy_F1uEuVSSR9ZglSoaDU2uZocNtTGOPXo19bQeZQ2Ue1KWBWazLG7rc3yPMZiqt_7Y-8umcTwoDlLDDstiDKalDIGnUnm46DRFGbx6IPwXjL94SpCU1q_Y2Iwr0J6TjzEh'>
</div>

## Overview
[Why Datadog?](#why-datadog)

[Prerequisites](#prerequisites)

[Setting up your Environment](#setting-up-your-environment)<br/>
&ensp;&ensp;&ensp;&ensp;[- Getting your API Key](#getting-your-api-key)<br/>
&ensp;&ensp;&ensp;&ensp;[- Setting up the Container](#setting-up-the-container)

[Collecting Metrics](#collecting-metrics)<br/>
&ensp;&ensp;&ensp;&ensp;[- Adding Tags to Hosts](#adding-tags-to-hosts)<br/>
&ensp;&ensp;&ensp;&ensp;[- Installing MySQL](#installing-mysql)<br/>
&ensp;&ensp;&ensp;&ensp;[- Creating a Custom Agent Check](#creating-a-custom-agent-check)<br/>
&ensp;&ensp;&ensp;&ensp;[- Changing an Agent Check's Interval](#changing-an-agent-checks-interval)

[Visualising Data](#visualising-data)<br/>
&ensp;&ensp;&ensp;&ensp;[- Creating a Timeboard](#creating-a-timeboard)

[Monitoring Data](#monitoring-data)<br/>
&ensp;&ensp;&ensp;&ensp;[- Setting up a Monitor with Alerts](#setting-up-a-monitor-with-alerts)

[Collecting APM Data](#collecting-apm-data)<br/>
&ensp;&ensp;&ensp;&ensp;[- Instrumenting a Basic Python App](#instrumenting-a-basic-python-app)

[Final Question](#final-question)
[Bonus Questions](#bonus-questions)


## Why Datadog?
Alright so you’re building a modern web app and your stack has many different layers, all of the layers are generating their own data and interacting with each other in weird and wonderful ways. Traditionally there have been solutions to track and monitor metrics within each layer, but doing it this way requires many separate implementations and lacks a complete overview of what’s happening in your application.

Datadog to the rescue! Datadog will enable you to track, aggregate, and analyse metrics and events across the full devops stack -- and allows you to manage it all with simple dashboards. It also allows you to monitor your applications performance, tracing requests from end to end across distributed systems and ultimately make troubleshooting a breeze.

So now that you’re sold, let’s walk through setting up the Datadog Agent on a simple application and get it monitoring some metrics that we can view on a dashboard!

## Prerequisites

- This guide assumes you have a working knowledge of Docker and Vim, and that you’re working on Windows. If you don’t have Docker installed you can find the installation instructions here:
[https://docs.docker.com/docker-for-windows/install/#start-docker-for-windows](https://docs.docker.com/docker-for-windows/install/#start-docker-for-windows)

- You’ll also need to have an account with Datadog, as we need an API key to work with the service. If you don’t already have an account you can sign up here:
https://app.datadoghq.com/signup

## Setting up your Environment
In this section we’ll run a container in docker with a base linux image that has the latest Datadog agent V6 installed. We’ll then connect a terminal to the container and install a text editor so that we can edit files.

If you’re interested, the image we’ll be using can be found here:
https://hub.docker.com/r/datadog/agent/

### Getting Your API Key
Navigate to the Datadog sign in page and log in to retrieve your API key:
[https://app.datadoghq.com/account/login?redirect=f](https://app.datadoghq.com/account/login?redirect=f)

On the first screen after you’ve logged in, hover your mouse over ‘Integrations’ on the left menu and click on ‘APIs’:

![](https://lh6.googleusercontent.com/J-aNjztxlpEKIC_RwVqMzxcW09utGdvzZ_f2LI09l4_MCH1rXN9aiEizTdZTV9gQE1d3egk_GtI-51S4gBuZSX-DtpU-alpvt87jYc8RQC3DRFJo0-FlDtSvLAen7cXEruI4E1ge)

Copy the API Key to be used in our Docker command:

![](https://lh3.googleusercontent.com/Ht8WqQ1l99JK7rhguBwk45F5RPD_sDXRwyNeMhlyShzI-5Gu5ZUhfJAxt2SBG1eRROlMIADkep6QXBOkqUiKrA7DlIzGDiBQQQIhJBUEoLQxif3ReAZLm1R9lpz5AWWi2UQM3Fq6)  

### Setting up the Container
Complete the following docker command by filling in your API key:
```
docker run \
-d --name dd-agent-v6 \
-p 3000:3000 \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
-v /proc/:/host/proc/:ro \
-v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
-e DD_API_KEY={your_api_key_here} \
-e SD_BACKEND=docker \
-e NON_LOCAL_TRAFFIC=false \
datadog/agent:latest
```
And then run the command in a docker terminal:

![](https://lh4.googleusercontent.com/iKaFOCeo2lw3baShoG2j2kbqgrvnig6jovXPgprMvS07rl2K_p5bE9nVjiPFepp1iQLGPrfNrPfI0qNoP4-foMcQ2A6S7S9XD3D4yLCAKVUEOg_2XhkkeKBcg0YvwtwAKid0n6X4) 
  

Check that the container started successfully by typing:
```
docker container ls
```
![](https://lh6.googleusercontent.com/jagLpXVwxVOIhtvcRv3xv2oRCAlkOPN_e6Bw57tze28ZOr6NHOgTyNmeO39NKE4yfKnTOpF_oND1_9pJw6xuU4RgS95bwPG7itVcAlUzIMe4O2RUS1_NJrRBc88yxV23IzB4pzZB)
Note: if the container status is not ‘Up’ you can check the logs to see what the error is with:
```
docker logs {container_id_here}
```
Now that the container is running, we’ll connect into it to finish setting up our environment. Run the command:
```
docker exec -it {container_id_here} /bin/bash
```
And install vim tiny so that we can edit text files:
```
apt-get update
```
```
apt-get install vim-tiny
```

## Collecting Metrics
In this section we’ll be doing a few things, we’ll:

 - **add tags to our host** so that we can subset and query the machines and metrics that we want to monitor.

 - **install MySQL** and its integration. Integrations are an easy way to get setup monitoring common metrics for common services.

 - **create a custom Agent check**. Custom Agent checks are for monitoring metrics from custom applications or unique systems.

 - **change the Agent check's collection interval**.

### Adding Tags to Hosts
There are several ways to add tags to your hosts, but we’ll do it by editing the main Datadog Agent configuration file. Make sure you are in a terminal connected to the host. If not you can connect with:
```
docker exec -it {container_id_here} /bin/bash
```
Open the main configuration file to edit::
```
vim.tiny /etc/datadog-agent/datadog.yaml
```
Add tags to the bottom of the file and save it. Remember in vim you need to press `i` to start inserting text and when you're finished press `esc` and then `:wq!` to save the file. You can use any key:value pair you like:
```
i
```
```
tags: please:hire-me, i-need:money
```
```
esc
```
```
:wq!
```

The final file should look like this:

![](https://lh5.googleusercontent.com/SUfm3kVrngANJ_kydbfyzST2MEUJA-owtp1f-15nZ2anLnAagAvPVkLIUE2FFHz0CU9SEyOQOfSp5JkWb82Ysv28y-7BKC7kGhPuYTlRNW_oiAW0KNluuxZxNXXjRwTwLiD4HYMv)

Disconnect from the container by holding `ctrl` and then pressing `P + Q`.
Restart the container so that the config changes take effect:
```
docker restart {container_id_here}
```
Check that the tags have been added back in the Datadog web application. Hover over ‘Infrastructure’ in the left navigation bar and then click on ‘Host Map’.
  
![](https://lh5.googleusercontent.com/6yfETCaGPSOz-EjfU7rzxMEiZ1Xoq-fW0SLT9YGzSVEwb82dR_1YVFQuO-cZKzAE1-EGmg_Lu9yPt-mi93Yc1wzzKCxbUIQfbapINfqgIz-tWhbvHRhgPVwIgJ3NnJqU6OPppm8Y)

Click on the orange hexagon that represents our host:

![](https://lh5.googleusercontent.com/e5Gu_H3-67Q-8KsgsG4juD9g8yJBSxexPHAR5rXcA311XYyJ6eDlcwNIUjg4QLVcTLRYSKKwhpeskL2xgy1xNpbWu7EkXpQ4W_HIf26QTmqbkEcPNu2y7OPs19r3HpXAtEaxxq1L)

You should now be able to see the tags on your host.

![](https://lh6.googleusercontent.com/G0tIhSOTbinJozavko05yC8V3f6pMEexpMwmksjSNjUZxxVrS7gUJJ8-jmdYxo_bjr7QfvEPOAAz0BFTU37jwjrgDhWGz9iBU6aoFlB0NOO04nWiixZ55b7eFSwfRdbWRWKL-Am_)

### Installing MySQL
Make sure you are in a terminal connected to our host. If not you can connect with:
```
docker exec -it {container_id_here} /bin/bash
```
To install MySQL run:
```
apt-get install default-mysql-server
```
Start MySQL:
```
service start mysql
```
Install sudo so that we can follow the instructions on the Datadog web application:
```
apt-get install sudo
```
Follow the instructions on how to setup a MySQL integration on the Datadog web application:

![](https://lh6.googleusercontent.com/Pmfnl2WXv125Wmggejn3O2In6TSsTkKn6sJEA_9zXH_FnxQaU-F9agEIVnN_HGWstMJW2a70VVqtnjT9zbG8qtBCG5TGkITMuIxVK3dcyzeNaZuKecb_8_GWkYPYEVKRDBpuDswp)

Search mysql and click on the MySQL tile:

![](https://lh3.googleusercontent.com/ON2CpRlRSzXBe1sqlh47dc8NqG-RtsVHspgINmZVcSO2e4VQT3wqa9hpYt9ZFN1OEocKH5GpXk4F2pVHD0TEHTD0UFV0K2VeDimGJ93WwLI8bq56IwkW7XBrbrg4M7FXgXO2loMw)  

Click on configuration:

![](https://lh5.googleusercontent.com/6mJQXpVws9rq5MFQJ7JsgtFi0kfC52HE7eKze2BhBqKhqvw0u9wXghTnihCVIrhwzeRrFYs4-A0HM_TXmCzko5Fhmd7t8hdiNqg2NTrYGtaEILAoXIDfyABN6WkMtxQHPt5_fjDz)

Follow all of the instructions and click on ‘Install Integration’ at the bottom of the page.
Note: you’ll need to create the configuration file:
```
vim.tiny /etc/datadog-agent/conf.d/mysql.yaml
```
  
![](https://lh5.googleusercontent.com/NTLYC6cNLagZcxXKzERAAJuejJo2HVIpWl3gKd_8MtgG01vdu3CUZAO-qvT97YOIoJBuo-K5W7JqArW-9IUz5GHpQ2JUEJUgglpLB9VtQwR7zB9639b5yFUgsWYw6-5sisKh1eTq)

### Creating a Custom Agent Check
Creating a custom Agent check is easy! All we need to do is create two files (that must both have the same name), the first one will be the Agent check’s python code. Make sure you are in a terminal connected to the host. If not you can connect with:
```
docker exec -it {container_id_here} /bin/bash
```
And then type:
```
vim.tiny /etc/datadog-agent/checks.d/mymetric.py
```
Insert the following text and save the file:
```
from checks import AgentCheck
import random

class MyMetric(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', random.randint(1, 1000))
```
The second file is the configuration for the check:
```
vim.tiny /etc/datadog-agent/conf.d/mymetric.yaml
```
Insert the following text and save the file:
```
init_config:

instances:
  - name: myservice
```

### Changing an Agent Check's Interval
We’ll change the collection interval to be every 45 seconds instead of the default 15 seconds. To do this we’ll need to edit the config file for the check:
```
vim.tiny /etc/datadog-agent/conf.d/mymetric.yaml
```
The new file should read:
```
init_config:

instances:
  - name: myservice
    min_collection_interval: 45
```
## Visualising Data
In this section we’ll create a Timeboard using the Datadog API. To do this we’re going to create a very basic python application and also configure some settings in the Datadog web application.

### Creating a Timeboard
Make sure you are in a terminal connected to our host. If not you can connect with:
```
docker exec -it {container_id_here} /bin/bash
```
Install Datadog’s API client library through with the Agent’s embedded python runtime:
```
pip install datadog
```
Create the python application file, anywhere will do but I’ve chosen root.
```
vim.tiny /createVisualisations.py
```
You can create an App Key on the same page you retrieved your API Key from in the Datadog web application in the 'Getting Your API Key' part of this guide. Fill the createVisualisations.py with the following text:
```
from datadog import initialize, api
options = {
  'api_key': '{your_api_key_here}',
  'App_key': '{your_app_key_here}'
}

initialize(**options)
title = "My Timeboard"
description = "This is totally gonna show off my mad skillz."
graphs = [{
    "definition": {
      "events": [],
      "requests": [
        {"q": "avg:my_metric{i-need:money}"}
      ],
      "viz": "timeseries"
    },
    "title": "Avg of my_metric over i-need:money"
  },
  {
    "definition": {
      "events": [],
      "requests": [
        {"q": "avg:mysql.innodb.data_reads{*}"}
      ],
      "viz": "timeseries"
      },
    "title": "Avg of mysql.innodb.data_reads over all hosts"
  },
  {
    "definition": {
      "events": [],
      "requests": [
        {"q": "avg:my_metric{i-need:money}.rollup(sum, 3600)"}
      ],
      "viz": "timeseries"
      },
    "title": "Sum rollup of last hour of Avg of my_metric over i-need:money"
  }] 
read_only = True
api.Timeboard.create(title=title,
            description=description,
            graphs=graphs,
            read_only=read_only)
# Create a new monitor
monitor_options = {
  "notify_no_data": False,
  "no_data_timeframe": 20
}
tags = ["database"]
api.Monitor.create(
  type="metric alert",
  query="avg(last_1h):anomalies(avg:mysql.innodb.data_reads{*}, 'basic', 3, direction='above', alert_window='last_5m', interval=20, count_default_zero='true') >= 1", name="MySql Reads on the only host we have", message="Just doing this as per instructed.", tags=tags, options=monitor_options
)
```
There’s a lot in this piece of code, but we’re just using it for demonstration. If you’d like to go deeper and pick it apart, you can read up on the python library here:
[https://datadogpy.readthedocs.io/en/latest/](https://datadogpy.readthedocs.io/en/latest/)

And the Datadog API reference here:
[https://docs.datadoghq.com/api/?lang=python#overview](https://docs.datadoghq.com/api/?lang=python#overview)

In a nutshell we’ve created a new Dashboard, with three time series graphs:
-   Our custom metric ‘my_metric’ scoped over our host.
-   A metric from our MySQL integration with the anomaly function applied.
-   Our custom metric ‘my_metric’ with the rollup function applied to sum up all the points for the past hour into one bucket.
    
  Let’s check the new Dashboard back in the Datadog web app:

![](https://lh5.googleusercontent.com/SCxiJ3L_yk4QLxqAutehJ8g34GiN09NXRwpZz0AADkRjZvEZ_fmJXZvFthD9lb9tlQ5ANnoItCkmfiJMwJMgvK-lxnTMmItOhEyVsbhiBf6vV6xoxZQlhhvTFT8FJu34DVBapj-8)

Click on ‘My Timeboard’:

![](https://lh5.googleusercontent.com/A8nB7fh8MQekzW_Hm8USutCMt9GXH_bHVy6d8ztvTWwBYII4wTuheTAGzdiI8ACvjTT7mZxTuF2kOWB-f1oHmx6W3XLVszS3Yk-boZIzHTHWcazFnm6J3zy_UjaJ7nZuDOZvvYBg)

The resulting timeboard as a shareable screenboard looks like this for me (follow this link to view https://p.datadoghq.com/sb/f2d796e7c-2d2719b7cba07a6767f801aaf39a5cd8):

![](https://lh6.googleusercontent.com/utNZUsRIu9qNtpbD5EWqKlbTQw9_3ArsqtvaZn7UGs05wybb7iQEMJ_Di7n_wowE28dCv6i5SwA2IvhgTkr4qrNWClAelSSb2qwHYPIIxIYgO2m_AhgGMuRsqTfWjQx5C4z309DQ)

Here you can have a look at the time series that we created. From this interface we can change the graphs’ timeframe and take snapshots to highlight issues to other team members. To get an idea of how this works let’s change the time frame to the last 5 minutes and send it to ourselves with a message. To do this click and drag over a small section on the right of the ‘Avg of my_metric over i-need:money graph:

![](https://lh4.googleusercontent.com/vMbDgb0Ta2bEH-EyyoByPCqeJk0gRmhce4R3zEtzuOgfiHQmJGmByO09hpd_YHq_ZmUHnlZAsrUR-kJz37txvs1HxPe4JYyVbUkpm95BBdAzIwAoy8w9dVv1RnQjuiPCRCConeJy)

You can then send with an annotation by clicking on the camera icon and writing into the text input box that appears. Use the ‘@’ symbol to choose yourself to be notified and you should receive an email:

![](https://lh4.googleusercontent.com/5NwCqfCt2ZJcG3U4idOcZfQ2Ngbz-euOGId5R-KU_ZgjrYjISeJkYEZh3Me9b4zhRWfW7bk0E0aWZy6OPE0guxzn1Jm1C29paxZ-YvmOpARHwUYJEd_fX6Xj8Ql7d4G44LZhxWKA)



## Monitoring Data
Monitoring data is super simple with Datadog, we’ll set up some threshold monitors for our custom metric ‘my_metric’ that will alert us with different email messages.

### Setting up a Monitor with Alerts
Go to the ‘Manage Monitors’ page in the Datadog web app:

![](https://lh6.googleusercontent.com/_J1Y3u1K_3we_mlFD-qKVy0JsR6b-WmSmItZzBZUMqUBWRM1BpJHaxTFmcPHqcjK_2o9JmHgwLHyHgT40dlRlNePwKziiH6I0ANV2mYqIXI03hXYR_3vc7z4mck-FsrAc3MP1syn)

In the top right corner of the page click on ‘New Monitor +’:

![](https://lh4.googleusercontent.com/m871z-LAYjLV_QQULb53MJw9IzIWiBNl6RTGGp2B_1_pbbnz3lBgDEsYoXqtOJQO3SU5RYtxeAy5vJRpVH1aD4eGLkxp8vM19Mu_O3oj8i6qAY_QhHE_TTm_Zirp8cQdxgFa3OBL)

Fill out the monitor form as shown in the pictures.
Note: you can copy and paste this code for the message:

```
{{#is_alert}}ALERT!{{/is_alert}}{{#is_warning}}Warning!{{/is_warning}}{{^is_no_data}} Because my_metric has a value of {{value}} from the host {{host.name}} which is over {{#is_alert}}{{threshold}}!{{/is_alert}}{{#is_warning}}{{warn_threshold}}!{{/is_warning}} Please not that trying to get the host IP from Docker does not work - there should be a value here: {{host.ip}}.{{/is_no_data}}
{{#is_no_data}}Data has been MISSING for more than 10 minutes :O{{/is_no_data}}
```

Another Note: Notice that the 'host.ip' template variable is available, yet in the notification email it comes up blank.
![](https://lh5.googleusercontent.com/cT4YhPsdHkIxYfCtNJhfhsxtcnE-1lfgDDIqnWI8VS_l85wK6C9sQhEMDipoquE0fWc5J5yPaCFaCw5Riqmgmfu3CYaicKvQLKCPzFKWdyoMhA6TMrS0L0S7l2MDbM_-mCBOyE6O)

![](https://lh6.googleusercontent.com/boub7lC-ANnvHgEN-FtvogjftG_WPidtpEmpD1jEi8PpwB21ZSLzMKRy0XUlOCBCW51_TNfEO8SX0rZjYLpdnIDnd_HxrDPNGvUNvkhBuEpN5KIJ0S4p9P5w1yNsmxANWb7kgbK4)

![](https://lh6.googleusercontent.com/p22LuFbCvve9PseaKWg5P97_I32s6-Bc25J3Yommv_bT5H67tiz3cwOiRLu64BnfauE-tmH1ru_fWV91v7G-wmqreskc8Wp75GFNdIrOvHvqwqWHj-hIwBzuE5Rw2iUifqVZOzmm)

The alerting email:

![](https://lh5.googleusercontent.com/5Xkm9ooZa1_zR_sARTK70gUP12MR_YcAr_Zd93B-FvnbR-Hqfwp8bwX-vwyrtVRkRtuqJOWbxXGvlB4aYH_ey0GhHzVK67ORScNebV83znd6EQ7sRoexNrJwTkL3KvIOMFxtU1pb)

## Collecting APM Data
In this section we’ll instrument a simple python application with Datadog’s Application Performance Monitoring (APM).

### Instrumenting a Basic Python App
Make sure you are in a terminal connected to our host. If not you can connect with:
```
docker exec -it {container_id_here} /bin/bash
```
Install flask:
```
pip install flask
```
Create a file in root to be the app server:
```
vim.tiny /app.py
```
Fill the file with the following text:
```
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
  app.run(host='0.0.0.0', port='3000')
```
Install ddtrace with:
```
pip install ddtrace
```
Edit the datadog.yaml config file to enable trace reporting:
```
vim.tiny /etc/datadog-agent/datadog.yaml
```
Under `apm_config:` change `enabled` from `false` to `true`

Disconnect from the container by holding `ctrl` and then pressing `P + Q`.
Restart the container so that the config changes take effect:
```
docker restart {container_id_here}
```
Connect back to the container again:
```
docker exec -it {container_id_here} /bin/bash
```
Run the python application with:
```
ddtrace-run python app.py
```
Visit the application in your browser by navigating to:
```
192.168.99.100:3000
```
  
The APM traces will now be available in the Datadog web app!

My dashboard with Infrastructure Metrics and APM can be found here:
https://p.datadoghq.com/sb/f2d796e7c-2d2719b7cba07a6767f801aaf39a5cd8

 And looks like this:
![](https://lh4.googleusercontent.com/xen5b5D59fkyHmxMcD-JDnvmWHbZm_hmkKzFsD7w7BkqLfcv-Fvq3Sq4v9RZ8UMQ5adT2e-lvpFeVGyRaolRk8Z-IybTC4hSHqcpItuuKezTKb4x43-CpDwTdwakqCiCrkT8dinN)

## Final Question
I would use Datadog to do a HTTP check on www.isitchristmas.com every day. I would then put an alert when the HTTP check response matches 'YES' and also create a dashboard to display the value.

## Bonus Questions
 1. *Can you change the collection interval without modifying the Python check file you created?*
Yes, you can modify the check’s YAML configuration file as done in this guide.

 2. *What is the Anomaly graph displaying?*
The anomaly graph uses an algorithm and historical data to predict the behaviour of a metric. If the value of a metric becomes anomalous a warning will be displayed. In my particular graph, I’ve used a basic algorithm (not seasonal-data), to alert if the values extend past 3 standard deviations of the norm over the past 5 minutes.

3. *Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*
-   *One that silences it from 7pm to 9am daily on M-F,*
-   *And one that silences it all day on Sat-Sun.*
-   *Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.*
Note: Sydney is not UTC

![](https://lh6.googleusercontent.com/4TvUFN1UNbX2BnAMd93UM_wCHRfRX0PzB14M3-PIVKn0aKg44r3rsO7F3Dadv3-JLQR6AWJ6-pdI8JKkeb05zn8-jWd0DkcVETUQSRg6zqwl51WITXPvM9KzIVblJIt-wHD5cf7o)

  
![](https://lh3.googleusercontent.com/EltjYQAEh9rtuFWa_9sQWkNLh_Lz0JvZZbDqKZkfrdxuiB0afHOeUVz8GsG8W7buh88RF5EiDkMQB3fY6C6CtMH6_Afsay6vuKIkcGUpDMyFLkj_80eAaj3FQvQr3wcThKQZvV6T)

4. *What is the difference between a Service and a Resource?*
A service is the name of a set of processes that work together to provide a feature set (e.g. a web server service and a database service) whereas a resource is just a query to a service (e.g. a URL would be a resource to a web server service and the SQL of a query would be the resource to a database service).

