# Vagrant, Ubuntu and Containers
I decided to use vagrant and Ubuntu 16.04 (Xenial) on my Windows 10 machine. Installed Vagrant 2.1.4

Followed instructions but I could not use their pre-defined commands since I decided to 16.04. I swapped out "hashicorp/precise64" to ubuntu/xenial64" etc. My vagrant config file looks slightly different as well.
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/vagrant_config.jpg?raw=true)

Turned off hyper-v in windows and restarted. 

Got apache to work on my local machine. Not relevant but might become useful at some point. Can see /var/www/html directory by browsing to http://127.0.0.1:5678/

Installed docker on my host with a TAG. Forgot the tag first and had to remove and reinstall container. I can see the tag in the host map. 
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/TAG-in%20docker%20container.jpg?raw=true)

`$ sudo docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=9fb35ec4a2ff537e74f3fd08955ae3be  -e DD_TAGS=farid-test-tag-0 datadog/agent:latest`

Added the option network later to have all my containers on the same network. 

`sudo docker run -d --name dd-agent2 --network='nraboy' -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=9fb35ec4a2ff537e74f3fd08955ae3be  -e DD_TAGS=farid-test-tag datadog/agent:latest`


# MYSQL
First I installed mysql on my ubuntu host and then decided to move over to mysql in a container. 
Uninstalled Mysql from my host and instead went with the containerized mysql image. 
Followed instrustions here <https://www.techrepublic.com/article/how-to-deploy-and-use-a-mysql-docker-container/>

Installed Docker Mysql container.
`sudo docker run -d --name=dd-mysql2 --network='nraboy' -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=9fb35ec4a2ff537e74f3fd08955ae3be  -e DD_TAGS=farid-test-tag mysql/mysql-server:latest`

Followed instructions to install Mysql <https://docs.datadoghq.com/integrations/mysql/>

Created user CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'dataDog1!'; (Had to change this to datadog2 later)

* mysql datadog password: dataDog!1
* mysql root password: Shirvani!1

Changed config file in container to reflect mysql settings. Enabled Performance Scheme

Added user to configuration block in container conf.yaml (Copied the example and started todo modifications to mentioned in documentation)

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/conf-yaml-working.JPG?raw=true)

Granted user datadog everything.  Gave it the password datadog docs creted for me and allowed mysql container to receive from all IPs
`bind=0.0.0.0`


Enabled logs and saw error message from mysql which i resolved

``2018-10-05 06:23:33 UTC | ERROR | (runner.go:289 in work) | Error running check mysql: [{"message": "(1130, u\"Host '172.18.0.3' is not allowed to connect to this MySQL server\")", "traceback": "Traceback (most recent call last):\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/datadog_checks/checks/base.py\", line 352, in run\n    self.check(copy.deepcopy(self.instances[0]))\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/datadog_checks/mysql/mysql.py\", line 304, in check\n    password, defaults_file, ssl, connect_timeout, tags) as db:\n  File \"/opt/datadog-agent/embedded/lib/python2.7/contextlib.py\", line 17, in __enter__\n    return self.gen.next()\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/datadog_checks/mysql/mysql.py\", line 403, in _connect\n    connect_timeout=connect_timeout\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymysql/__init__.py\", line 90, in Connect\n    return Connection(*args, **kwargs)\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymysql/connections.py\", line 699, in __init__\n    self.connect()\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymysql/connections.py\", line 935, in connect\n    self._get_server_information()\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymysql/connections.py\", line 1249, in _get_server_information\n    packet = self._read_packet()\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymysql/connections.py\", line 1018, in _read_packet\n    packet.check_error()\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymysql/connections.py\", line 384, in check_error\n    err.raise_mysql_exception(self._data)\n  File \"/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymysql/err.py\", line 107, in raise_mysql_exception\n    raise errorclass(errno, errval)\nInternalError: (1130, u\"Host '172.18.0.3' is not allowed to connect to this MySQL server\")\n"}]``


Verified containers can communicate

From Datadog container to mysql container

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/curl-from-container.JPG?raw=true)


Tested datadog user

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/tested-user.JPG?raw=true)

After endless hours of troubleshooting and reading online I discovered your example YAML file for mysql inside the container didin’t follow YAML standard. YAML is very sensitive when it comes to formatting , spaces , tabs, etc. As soon as I fixed this and lined up all rows under each other parser could parse and I started to see metrics being collected. 
I have this guy to thank <https://stackoverflow.com/questions/31313452/yaml-mapping-values-are-not-allowed-in-this-context/31335106>

# Custom Metric
Created a custom Agent check that submits a metric named farid.check with a value 47.

Followed <https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6#configuration>

See my metric in Metrics Summary 


![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/Custom_Agent.jpg?raw=true)

Changed reporting interval to every 45 seconds.

`$root@4e12f552273e:/etc/datadog-agent/conf.d# cat > hello.yaml`

```
init_config:

instances:
    [{min_collection_interval: 45}]

```

# Timeboard
Before I started with the Timeboard API I took a snapshot of my VM, just incase

```
C:\HashiCorp\Vagrant\datadog_project>vagrant snapshot save default ubuntu_before_timeboard
==> default: Snapshotting the machine as 'ubuntu_before_timeboard'...
==> default: Snapshot saved! You can restore the snapshot at any time by
==> default: using `vagrant snapshot restore`. You can delete it using
==> default: `vagrant snapshot delete`. 
```

Needed a new key

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/created_application_key.jpg?raw=true)

I used Postman to experiment and expand my script.

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/Postman.JPG?raw=true)

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/new_timeboard_created.JPG?raw=true)

Below is my Script for timeboard. I was experimenting a lot as you can see in the dashboard. 

````

api_key=9fb35ec4a2ff537e74f3fd08955ae3be
app_key=11f82e6aea98388f363b67ab629a6a4ebb3b3fbe

curl  -X POST -H "Content-type: application/json" \
-d '{
{
      "graphs" : [{
          "title": "Farids Postman Average Memory Free",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:system.mem.free{*}"}
              ]
          },
          "viz": "timeseries"
      },       
	  {
          "title": "Rate of Queries",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "mysql.performance.queries{*}"}
              ]
          },
          "viz": "timeseries"
      },
	  {
          "title": "Data Reads",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "mysql.innodb.data_reads{*}"}
              ]
          },
          "viz": "timeseries"
      },
	              {
          "title": "Docker containers running",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "docker.containers.running{*}"}
              ]
          },
          "viz": "timeseries"
      }        
      ],
      "title" : "Farids Postman Timeboard",
      "description" : "Farids informative timeboard",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
}}' \
https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}

````

# Anomaly and Monitors
Experimented in the UI first and then alot in postman to get an understanding of this. 

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/anomaly-postman.JPG?raw=true)
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/db_abnomaly_monitor.JPG?raw=true)

Created another one for my own API Timeboard that reports memory status since I could see some activity here. I wanted it to intentionally alert just to see how that looks. 
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/memory_Alert.JPG?raw=true)

Anomaly script . Followed https://docs.datadoghq.com/monitors/monitor_types/anomaly/
````
{
      "type": "metric alert",
      "query": "avg(last_5m):sum:system.net.bytes_rcvd{host:host0} > 100",
      "name": "Bytes received on farid-host0",
      "message": "We may need to add web hosts if this is consistently high.",
      "tags": ["app:webserver", "frontend"],
      "options": {
      "notify_no_data": true,
      "no_data_timeframe": 20
      }
	}
"https://api.datadoghq.com/api/v1/monitor?api_key=9fb35ec4a2ff537e74f3fd08955ae3be&application_key=11f82e6aea98388f363b67ab629a6a4ebb3b3fbe"

````

Experimented by creating a few different monitors. 
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/manage-monitors.JPG?raw=true)


Changed my Timeboard to reflect the last 5min and took a snapshot. 

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/reflecting-last-5min.JPG?raw=true)


# Monitoring Data
Configured the monitor
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/monitoring-configuration.JPG?raw=true)

Changed my check to report 801 and waited 5 min
```
from checks import AgentCheck
   class HelloCheck(AgentCheck):
      def check(self, instance):
      self.gauge('farid.check', 900)
```

After I changed my check I saw the monitor alerting in the dashboard 
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/monitoring1.JPG?raw=true)

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/Monitoring2.JPG?raw=true)

Receive first alert email after 5min.

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/monitoring3-email.JPG?raw=true)

And second follow up email 5 min after the first one.

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/monitoring3-2nd-email.JPG?raw=true)

I turned off my docker container to not send any data and below is the NO-DATA alert I received in my mail. 

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/monitoring-no-data.JPG?raw=true)


# Collecting APM Data (FlaskApp):
To be honest I wasn't sure where to run my flask app host/container. Started to experiment. 

What I think I should do is to run the flask app which reports to the agent in container which reports back to the Dashboard but I might be totally wrong.

I started by installing some packages to be able to run "$pip install ddtrace$ on my host. Helpful instructions <https://www.fullstackpython.com/blog/python-3-flask-green-unicorn-ubuntu-1604-xenial-xerus.html>

Created a file server.py and put my flask app in here.
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/flaskapp_code_dashbaord.JPG?raw=true)

I had to open a port 5050 in vagrant to run this in my browser. 
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/port-added.JPG?raw=true)

Verified if it's working in a browser 

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/server-py-running.JPG?raw=true)
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/entrypoint.jpg?raw=true)
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/getting-apm-started.jpg?raw=true)
![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/posting-traces.JPG?raw=true)

Changed conf.yaml to enable apm. 

Installed blinker 

`#pip install blinker`

I ran curl localhost:5050/api/trace (curling flask)

Flask responds and trace reports back to the agent in container. 

Agent reports back to datadog dashboard. 

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/flaskapp1.JPG?raw=true)

Flask Total Request , Latecy distribution and  Resource

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/flask-resource.JPG?raw=true)

Flask Service

![](https://github.com/datadogchallenge/hiring-engineers/blob/solutions-engineer/flash-service.JPG?raw=true)

Other sources I used for the flaskApp

<https://docs.datadoghq.com/tracing/setup>

<https://docs.datadoghq.com/tracing/setup/#agent-configuration>

<https://docs.datadoghq.com/api/?lang=bash#send-traces>

<https://flask-user.readthedocs.io/en/latest/signals.html>


Bonus Question Service vs Resource:
* FlaskApp is considered a service while the “URL paths” are considered the resources. 



Final Question:
* Datadog can be used to monitor all currect inbound/outbound integrations at Boingo Wireless. Currently all monitoring are done manually in splunk. Some custom made dashboards are made in splunk but they don't have capabilities datadog has. 


