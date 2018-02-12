# Datadog Solutions Engineer Technical Exercise for Henry Doan

# What is Datadog?

Your servers, your clouds, your metrics, your apps, your team. Together.

- With turn-key integrations, seamlessly aggregate metrics and events 
across the full devops stack 
- Monitor, troubleshoot, and optimize application performance
- Build real-time interactive dashboards
- Give visibility to system events and metrics across teams	
- Get alerted on critical issues
- Instrument your apps with performance monitoring, write new integrations
	
Learn More: [https://www.datadoghq.com/](https://www.datadoghq.com/) 

# Create a Virtual Machine

You can utilize any OS/host that you would like. Click [here](https://www.vagrantup.com/intro/getting-started/) 
for instructions to create an Ubuntu 12.04 VM using Vagrant with VirtualBox. 

- To connect to the VM from your local machine, type `vagrant ssh`
- To exit the VM, type `exit`

Optionally, you can change the hostname within the VM from the default 
`precise64`. This can be useful in distinguishing your VMs in Datadog if you 
create more than one for testing.  Be sure to run `vagrant init hashicorp/precise64` 
from different directories on your local machine for each VM so you can 
confidently `vagrant destroy` individual VMs without impacting the others.

To change the hostname with the VM:

- Run `sudo hostname <new_hostname>`.  
- Change hostname values found in `/etc/hosts/` and `/etc/hostname`

# Collecting Data

### Installing the Datadog Agent

From the Datadog UI, navigate to Integrations > Agent 
- or go here: https://app.datadoghq.com/account/settings#agent

![integrations_agent](images/integrations_agent.png)

Select your operating system and Agent installation instructions will be provided:

![ubuntu_agent_install_instructions](images/ubuntu_agent_install_instructions.png)

### Adding Tags for a Host

To add tags for a host, update the Agent config file `/etc/dd-agent/datadog.conf`:

```
### Set the host's tags (optional)
tags: env:prd, category:tech, owner:hvd
```

*Tags for example host #1:*
![tags-host1](images/host_map_tags_1.png)
<br><br>
*Different tags for example host #2* 
![tags-host2](images/host_map_tags_2.png)


### Setup Datadog Integration for MySQL

Follow instructions [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-14-04)
to install MySQL on Ubuntu.  Afterwards, confirm MySQL instance is running:

```
$ service mysql status
mysql start/running, process 809
$
```

In Datadog UI, navigate to [Integrations](https://app.datadoghq.com/account/settings#integrations)
and search for "MySQL".  Click "Install", then follow instructions under
"Configuration" tab.  

Once complete, MySQL metrics will be available in Datadog.  Navigate to
[Metrics Summary](https://app.datadoghq.com/metric/summary) and search 
for "mysql" to see newly available metrics:

![mysql_metrics](images/mysql_metrics.png)


### Configure a Custom Agent Check

Follow instructions [here](https://docs.datadoghq.com/agent/agent_checks/) 
to create a custom Agent check.

Here's an example of a custom Agent check (`/etc/dd-agent/checks.d/my_check.py`)
that submits a metric named `hvd.my_metric` with a random value between 
0 and 1000:

```python
from random import *
from checks import AgentCheck

class RandomNum(AgentCheck):
    def check(self, instance):
        random_num = randint(1, 1000)    # Pick a random number between 1 and 1000.
        self.gauge('hvd.my_metric', random_num, tags=['my_metric'])

if __name__ == '__main__':
    check, instances = HTTPCheck.from_yaml('/etc/dd-agent/conf.d/my_check.yaml')
    check.check(instance)
    print 'Metrics: %s' % (check.get_metrics())
```
Here's the corresponding yaml file (`/etc/dd-agent/conf.d/my_check.yaml`):

```yaml
init_config:
      min_collection_interval: 45
instances:
      [{}]
```


### Bonus Question

> Can you change the collection interval without modifying 
the Python check file you created?

> **Answer:** Yes, simply set a `min_collection_interval` value in the associated 
yaml file for your check file.

```yaml
init_config:
      min_collection_interval: 45
...
```

# Visualizing Data

### TimeBoards

Here's a TimeBoard that displays the custom metric from above scoped 
over the host it's configured on, that metric with the rollup function 
applied, and the MySQL Performance Queries metric (anomaly function 
applied): 


Link [here](https://app.datadoghq.com/dash/560047/specialty-dashboard?live=true&page=0&is_auto=false&from_ts=1518372516895&to_ts=1518386916895&tile_size=m)

Screenshot:

![specialty_timeboard](images/specialty_timeboard.png)

### On-Demand Time Range Selection and Snapshots/Annotations

To specify a time range you're interested in, simply click-and-drag
that section of the graph:

![click_n_drag_1](images/click_n_drag.png)

The TimeBoard's time range will automatically update with the custom 
time range:  

![click_n_drag_2](images/click_n_drag_2.png)

To create an annotation, click the "Snapshot" icon...

![snapshot_icon](images/snapshot.png)

...then annotate away:

![annotation](images/annotation.png)

Here's the email notification the user would receive:

![annotation_email](images/annotation_email.png)

### Bonus Question

> What is the Anomaly graph displaying?

> **Answer:** The current metric value with the highlighted area 
indicating "normal" range. Outside of the grey area would be considered 
an anomaly. 


# Monitoring Data

### Metric Monitor

In this example, we create a new Metric Monitor that watches the average 
of the custom metric `hvd.my_metric` that will alert if it's above the 
following values over the past 5 minutes: 

- Warning threshold of 500
- Alerting threshold of 800

![metric_monitor_1](images/metric_monitor_1.png)

Configure the monitor to notify if there is No Data for this query over 
the past 10 minutes: 

![metric_monitor_2](images/metric_monitor_2.png)


### Metric Monitor's Notification Message:

Let's configure the monitor's message to:

- <span style="color:green">Send email</span> whenever the monitor triggers.
- <span style="color:blue">Create different messages</span> based on whether 
the monitor is in an Alert, Warning, or No Data state. 
- <span style="color:orange">Include the metric</span> that caused the monitor 
to trigger <span style="color:orange">and host ip</span> when the monitor 
triggers an Alert state. 

![metric_monitor_3](images/metric_monitor_3.png)

Here's an email notification from the metric monitor:

![metric_monitor_4](images/metric_monitor_4.png)

### Bonus Question

> Since this monitor is going to alert pretty often, you don't want to 
be alerted when you are out of the office. Set up two scheduled 
downtimes for this monitor. 

- One that silences it from 7pm to 9am daily on M-F:
- And one that silences it all day on Sat-Sun.

To create new downtime schedules, navigate to Monitors > Manage Downtime:
- or go here: https://app.datadoghq.com/monitors#/downtime

![manage_downtime](images/manage_downtime.png)

Click "Schedule Downtime", then configure downtime as desired:

![schedule_downtime](images/schedule_downtime.png)


Downtime schedule #1:

![downtime_schedule_1](images/downtime_schedule_1.png)

Downtime schedule #2:

![downtime_schedule_2](images/downtime_schedule_2.png)

- Make sure that your email is notified when you schedule the downtime 
and take a screenshot of that notification. 

Downtime schedule email notifications:

![downtime_schedule_email_1](images/downtime_schedule_email_1.png)
![downtime_schedule_email_2](images/downtime_schedule_email_2.png)


# Collecting APM Data

Datadog’s integrated APM tool eliminates the traditional separation 
between infrastructure and application performance monitoring. This not 
only provides greater visibility, but also allows you to see the 
relationship between application code and the underlying infrastructure. 

Curious? Follow instructions [here](http://pypi.datadoghq.com/trace/docs/#module-ddtrace.contrib.flask)
to instrument a Flask application with trace middleware.

Here's the end result, in a sample Flask app:

```python
from flask import Flask
import logging
import sys

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# instrumenting DD APM for Flask
traced_app = TraceMiddleware(app, tracer, service="testFlaskApp", distributed_tracing=False)

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
    app.run()
```

Here's a dashboard with both APM and Infrastructure metrics (link [here](https://app.datadoghq.com/dash/563672/testflaskapp-dashboard?live=false&page=0&is_auto=false&from_ts=1518132562248&to_ts=1518133561609&tile_size=m&tv_mode=true)):

![testFlaskApp_dashboard](images/testFlaskApp_dashboard.png)

### Bonus Question

> What is the difference between a Service and a Resource?

> **Answer:** A "Service" is the name of a set of processes that work 
together to provide a feature set. A "Resource" is a particular query to 
a service. 


# Final Question

> Datadog has been used in a lot of creative ways in the past. We’ve 
written some blog posts about using Datadog to monitor the NYC Subway 
System, Pokemon Go, and even office restroom availability! 

> Is there anything creative you would use Datadog for?

I'm a devoted record collector/vinyl junkie and my favorite activity is 
listening to music. 

![dancing_to_records](images/dancing_to_records.gif)

For my creative project, I created custom Datadog metrics that represent 
my favorite artists' global popularity. Using the web API from 
[last.fm](https://www.last.fm/api), I retreive each artist's "listeners" 
and "playcount" data, sending them in as custom metrics.

The script executes from a cron job that runs every 5 minutes:

```
$ crontab -l
*/5 * * * * /usr/local/bin/python3 /home/vagrant/artistPopularityMetricLastFM.py >/dev/null 2>&1
$
```

Here's the code (see [artistPopularityMetricLastFM.py](https://github.com/henrydoan/hiring-engineers/blob/master/artistPopularityMetricLastFM.py)):

```python
import json 
import requests

from datetime import datetime,timedelta
from datadog import initialize, api

# initialize datadog api connection parameters
options = {
    'api_key' : 'd81b4c03c052be98c0b368cf8606ba68',
    'app_key' : '122313caaf83fb325fa1aa0482f2ab9d9d3e6125'
}
initialize(**options)

# send metrics to Datadog
def ddPost(mymetric,myvalue,mytags,ts):
    api.Metric.send(metric=mymetric, points=(ts/1000, myvalue), tags=mytags)

# get current epoch timestamp
def getEpoch():
    end_time = datetime.now()
    end_time = end_time - timedelta(seconds=end_time.second,microseconds=end_time.microsecond)
    tdelta = timedelta(seconds=60)
    start_time = end_time - tdelta
    start_epoch = int(start_time.strftime('%s')) * 1000
    end_epoch = int(end_time.strftime('%s')) * 1000
    return(start_epoch, end_epoch)

# Datadog API key
API_KEY = "0108d1afcd40db5dbe8e71f528c18c58"

# last.fm API 
api_root = "http://ws.audioscrobbler.com/2.0/"
api_artist_getInfo = "?method=artist.getinfo"
api_format = "&format=json"
api_key = "&api_key=" + API_KEY

artists = [
	'Anderson%20.Paak',
	'Bill%20Evans',
	'Bruno%20Mars',
	'Cyhi%20the%20Prynce',
	'Jay-Z',
	'John%20Coltrane',
	'Kanye%20West',
	'Kendrick%20Lamar',
	'Miles%20Davis',
	'Nina%20Simone',
	'Thelonious%20Monk'
]

# loop through list of artists
for a in artists:
	# build web API URL per artist
	url = api_root + api_artist_getInfo + api_key + api_format + '&artist=' + a
	#print (url)

	r = requests.get(url) 
	try:
		r.raise_for_status()
	except requests.exceptions.HTTPError as e:
		# status was non-200
		print ("Error: " + str(e))
		break

	data = json.loads(r.content)

	if data is not None and 'artist' in data:

		# get artist's name
		artist_name = data['artist']['name']
		print ("artist name: " + artist_name)

		# get artist's playcount
		artist_playcount = data['artist']['stats']['playcount']
		print ("playcount: " + artist_playcount)

		# get artist's listeners count:
		artist_listeners = data['artist']['stats']['listeners']
		print ("listeners: " + artist_listeners)

		# send data to Datadog

		# get current epoch timestamp
		interval = getEpoch()
		start_time = interval[0]
		end_time = interval[1]

		# tag metric with artist's name 
		ddtags = "artist:" + artist_name

		ddmetric="hvd.listeners"
		ddPost(ddmetric, artist_listeners, ddtags, start_time)

		ddmetric="hvd.playcount"
		ddPost(ddmetric, artist_playcount, ddtags, start_time)
	else:
		print ("Warning: data object is empty, not sending metrics to Datadog")
```

I was then able to create a TimeBoard that shows each artists' 
current popularity data as well as change over time (link [here](https://app.datadoghq.com/dash/564940/lastfm-artist-popularity-dashboard?live=true&page=0&is_auto=false&from_ts=1518453184243&to_ts=1518467584243&tile_size=m&tv_mode=true)):

![lastfm_timeboard](images/lastfm_timeboard.png)


Highlights of this project specific to Datadog features include:
- Utilizing Datadog API instead of custom Agent check to send metrics to 
Datadog (https://docs.datadoghq.com/api/?lang=python#post-time-series-points)
- Utilizing a Top List visualization
- Allowing Datadog to automatically set tag names for tag values that include 
spaces (i.e. artist name) 
- Using Timeshift function in combination with metric formula to graph 
the difference in popularity metric values over time.   

![metric_formula](images/metric_formula.png)
 