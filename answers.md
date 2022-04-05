## Environment setup

Using Vagrant and VirtualBox, I setup a fresh Linux (Ubuntu) VM on my macOS 12.2 laptop. The setup was pretty straighforward; thanks to documentation from Hashicorp - https://learn.hashicorp.com/collections/vagrant/getting-started

Thanks to Vagrant, I don't have to worry about authentication credentials or SSH keys. This makes it perfect for anyone wanting to run quick tests or applications on VMs before tearing it down. 

Verifying Ubuntu version on my VM -->

```
vagrant@vagrant:~$ cat /etc/os-release
NAME="Ubuntu"
VERSION="18.04.3 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.3 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic
```

Installed the DataDog agent for Ubuntu and within a minute, my Vagrant instance was reported in the Infrastructure list UI along with base metrics. A solid out of the box experience.

<img src="https://shivatk.s3.amazonaws.com/Infra-List.png" width="799" height="190">

Verifying Agent version -->

```
vagrant@vagrant:~$ sudo datadog-agent version
Agent 7.34.0 - Commit: 7861858 - Serialization version: v5.0.9 - Go version: go1.16.12
```

I then signed up for a 14 day trial at Datadog.

-------------------------------------------------------------------------------------------------------------------

## Collecting metrics

### Adding Tags

Configured tags for my host by editing the `datadog.yaml` in `/etc/datadog-agent` and adding the following entries 

```
tags:
  - team:solutions-engineering
  - infra:macos
  - webserver:flask
```

Restarted the Agent using `sudo service datadog-agent restart` and checked the status (`datadog-agent status`) to ensure the tags were configured correctly.

```
vagrant@vagrant:/etc/datadog-agent$ sudo datadog-agent status | grep 'host tags' -A 3
    host tags:
      infra:macos
      team:solutions-engineering
      webserver:flask
```

Within a few minutes, I could see these tags being reported in the UI.

<img src="https://shivatk.s3.amazonaws.com/HostMap-tags.png" width="914" height="266">

-------------------------------------------------------------------------------------------------------------------

### Database monitoring

I decided to go with mySQL for this part. Since the MySQL check was already included in the Datadog Agent package, no additional installation outside of just mySQL was necessary. 

Installing MySQL on my Vagrant instance was a single `apt install` command.

`sudo apt install mysql-server`

Once the database installation was complete, I created the datadog user with sufficient privileges for the Datadog agent to collect data from the DB using the instructions laid out in this Datadog document - https://docs.datadoghq.com/integrations/mysql

Checking MySQL version -->

```
vagrant@vagrant:/$ mysql -V
mysql  Ver 14.14 Distrib 5.7.37, for Linux (x86_64) using  EditLine wrapper
```

To enable database metric collection by the Datadog Agent, I edited the `conf.yaml` file in `/etc/datadog-agent/conf.d/mysql.d` with the following entries to include my instance (localhost as the MySQL DB was installed on the same Vagrant instance).

```
vagrant@vagrant:/etc/datadog-agent/conf.d/mysql.d$ cat conf.yaml
init_config:

instances:
  - dbm: true
    host: 127.0.0.1
    port: 3306
    username: datadog
    password: 'datadog'
```

Verified successful configuration by restarting the Datadog agent and running the Agent status command.

```
vagrant@vagrant:/etc/datadog-agent/conf.d/mysql.d$ sudo datadog-agent status | grep mysql -A 17
    mysql (8.0.3)
    -------------
      Instance ID: mysql:287d4371e72bc863 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/mysql.d/conf.yaml
      Total Runs: 409
      Metric Samples: Last Run: 113, Total: 46,786
      Events: Last Run: 0, Total: 0
      Database Monitoring Query Metrics: Last Run: 1, Total: 612
      Database Monitoring Query Samples: Last Run: 18, Total: 527
      Service Checks: Last Run: 3, Total: 1,227
      Average Execution Time : 33ms
      Last Execution Date : 2022-04-02 15:59:16 UTC (1648915156000)
      Last Successful Execution Date : 2022-04-02 15:59:16 UTC (1648915156000)
      metadata:
        flavor: MySQL
        version.build: unspecified
        version.major: 5
        version.minor: 7
        version.patch: 37
        version.raw: 5.7.37+unspecified
        version.scheme: semver
```

Looking at the host map in the Datadog console, I could now see the Datadog agent picking up the MySQL instance and reporting base metrics up to the cloud.

<img src="https://shivatk.s3.amazonaws.com/sql_map.png" width="786" height="228">

-------------------------------------------------------------------------------------------------------------------

### Configuring a custom Agent check

This step was straightforward too thanks to https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7.

To create a check for `my_metric`, I created a `my_metric.yaml` file in `/etc/datadog-agent/conf.d`.

Checkin `my_metric.yaml` -->

```
vagrant@vagrant:/etc/datadog-agent/conf.d$ cat my_metric.yaml 
init_config:

instances: [{}]
```

The next step was to create a python file `my_metric.py` under `/etc/datadog-agent/checks.d`

```
import random
from checks import AgentCheck

class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

Using the `random.randint` function, I can generate a random number between 0 - 1000. To configure the collection interval to 45 seconds, I added the `min_collection_interval` attribute to the `my_metric.yaml` file.

```
init_config:

instances:
        - min_collection_interval: 45
```

This overrode the default 15 second interval and set the `my_metric` check to be done every 45 seconds instead.

After restaring the Agent, I used the Agent check command for metrics, I was able to verify successful configuration of `my_metric` check.

```
vagrant@vagrant:/etc/datadog-agent/conf.d$  sudo datadog-agent check my_metric

  Running Checks
  ==============
    
    my_metric (unversioned)
    -----------------------
      Instance ID: my_metric:5ba864f3937b5bad [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/my_metric.yaml
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 1ms
      Last Execution Date : 2022-04-02 16:27:00 UTC (1648916820000)
      Last Successful Execution Date : 2022-04-02 16:27:00 UTC (1648916820000)
```

In a minute, I could see the my_metric attribute being reported in the console UI under Metric Explorer

<img src="https://shivatk.s3.amazonaws.com/my_metric.png" width="685" height="266">

However, I was noticing data points to come in at 40 and 60 seconds alternatively. Tried configuring different collection intervals (multiples of 5) and noticed similar results. I'm assuming that the underlying Agent process runs a buffer and sends data points periodically (like every 10 seconds) which would make sense as to why I'm see `my_metric` come in at 40 or 60 seconds.

#### Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes, this should be possible by simply editing the `.yaml` file for that metric and add the `min_collection_interval` attribute.

-------------------------------------------------------------------------------------------------------------------

### Visualizing data via API

To create a Timeboard by calling the Datadog API, I had to hit this endpoint - https://api.datadoghq.com/api/v1/dashboard. I started off by reading the API contract for this endpoint - https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard.

For authentication, I retrieved the API key from the Datadog console. I then had to create a new Application key for my client to leverage the APIs.

<img src="https://shivatk.s3.amazonaws.com/app-key.png" width="822" height="162">

Using both keys in the request header, I was able to authenticate successfully. For the dashboard, I chose the Timeseries widget for this task and I had to create 3 definitions under Widgets.

For `my_metric` scoped over my host - 

```
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "my_metric{host:vagrant}"
                  }
                ],
                "title": "My metric"
          }
```

For the database metric, I chose SQL lock times as this had a decent amount of fluctuation. The anomaly function with basic algorithm applied over the SQL lock metric to help visualize when the value fluctuates by more than 2 standard deviations. ->

```
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "anomalies(avg:mysql.queries.lock_time{host:vagrant}, 'basic', 2)"
                  }
                ],
                "title": "SQL locks"
          }
```

Definition for `my_metric` with the Rollup function applied to sum all values for the past hour.

```
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "sum:my_metric{host:vagrant}.rollup(sum, 3600)"
                  }
                ],
                "title": "My Metric hourly",
                "time": {
    					"live_span": "1d"
  					}
          }
```

Since the rollup function will collate all data points for the hour into a single one, I had to add the time attribute in the definition to set the Y axis scale to 1 day to visualize data better. All put together, the API can be called using cURL.

```
curl --request POST \
  --url https://api.datadoghq.com/api/v1/dashboard \
  --header 'Content-Type: application/json' \
  --header 'DD-API-KEY: REDACTED' \
  --header 'DD-APPLICATION-KEY: REDACTED' \
  --data '{
  "title": "Vagrant metrics",
  "description": "Solutions engineer assessment",
  "widgets": [
        {
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "my_metric{host:vagrant}"
                  }
                ],
                "title": "My metric"
          }
        },
				{
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "anomalies(avg:mysql.queries.lock_time{host:vagrant}, 'basic', 2)"
                  }
                ],
                "title": "SQL locks"
          }
        },
        {
          "definition": {
                "type": "timeseries",
                "requests": [
                  {
                        "q": "sum:my_metric{host:vagrant}.rollup(sum, 3600)"
                  }
                ],
                "title": "My Metric hourly",
														  "time": {
    					"live_span": "1d"
  					}
          }
        }
  ],
  "layout_type": "ordered"
}'
```

Once a 200 response code was returned from the API, I was able to see these charts in the Dashboard list.

<img src="https://shivatk.s3.amazonaws.com/crt.png" width="986" height="190">

Sending myself a snapshot of a graph displaying data over the last 5 mins.

<img src="https://shivatk.s3.amazonaws.com/snap.png" width="465" height="381">

#### Bonus Question: What is the Anomaly graph displaying?

Since I've used the basic anomaly algorithm with bounds = 2, the graphs shows when the SQL locks metric changes by more than 2 standard deviations from the norm.

<img src="https://shivatk.s3.amazonaws.com/lock_ana.png" width="676" height="228">

The lines in red show when the number of SQL locks have exceeded 2 standard deviation.

-------------------------------------------------------------------------------------------------------------------

### Monitoring data

Created a metric monitor in Datadog looking at `my_metric` to alert if its average value in the last 5 minutes was greater than 800 and warn if above 500. Configured monitor to notify my email shivatk@protonmail.com with custom messages depending on the monitor state.

```
{{#is_alert}} URGENT: my_metric over 800 detected in {{host.ip}}! {{/is_alert}}
{{#is_warning}} WARNING: my_metric over 500 detected in {{host.ip}}.{{/is_warning}}
{{#is_no_data}} URGENT: No my_metric data points reported in the last 5 minutes from {{host.ip}}.{{/is_no_data}} 

@shivatk@protonmail.com
```

Screenshot of alert notification -->

<img src="https://shivatk.s3.amazonaws.com/monitor.png" width="550" height="381">

Screenshot of warning notification -->

<img src="https://shivatk.s3.amazonaws.com/warner.png" width="550" height="434">

Screenshot of no data notification -->

<img src="https://shivatk.s3.amazonaws.com/nodata.png" width="552" height="236">

Screenshot of recovered notification -->

<img src="https://shivatk.s3.amazonaws.com/recovered.png" width="550" height="434">

**Note**: I couldn't get the `{{host.ip}}` to be populated in the notification email. I could see the host IP address under Infrastructure list; however, this variable was not being populated in the notification. I couldn't find any known issues page for this feature in Datadog and troubleshooting docs didn't contain any related data. Googled for a bit for troubleshooting help but without luck. I went with {{host.name}} for illustration purposes.

#### Bonus question : Scheduling downtime between 7 p.m. to 9 a.m on Weekdays and entire weekends.

I was able to get this configured by setting up two downtime monitors.

1. Downtime between 7 p.m. and 9 a.m. repeating everyday.

<img src="https://shivatk.s3.amazonaws.com/down_1.png" width="588" height="266">

2. Downtime from 12 a.m starting Saturdays for 48 hours repeating weekly.

<img src="https://shivatk.s3.amazonaws.com/downer.png" width="592" height="232">

Screenshots once downtimes were scheduled.

<img src="https://shivatk.s3.amazonaws.com/downer2.png" width="695" height="251">

<img src="https://shivatk.s3.amazonaws.com/downer1.png" width="686" height="273">

-------------------------------------------------------------------------------------------------------------------

### Collecting APM Data

For this exercise, I used the sample Flask app included in the repo. I started with Datadog's documentation - https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/

Got `python`, `pip`, `flask` and `ddtrace` (Datadog's python tracer) installed on my Vagrant Ubuntu instance. For the purpose of this exercise, I chose to leverage Flask's inbuilt wsgi server instead of configuring Nginx or Apache. Copied the python code into a `tracer.py` file and ran `ddtrace-run python` on it.

```
vagrant@vagrant:~$ sudo ddtrace-run python tracer.py 
 * Serving Flask app "tracer" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
INFO:werkzeug: * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2022-04-03 15:50:17,923 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
```

In a new shell window, called this application endpoints using cURL.

```
curl http://0.0.0.0:5050
curl http://0.0.0.0:5050/api
curl http://0.0.0.0:5050/api/apm
curl http://0.0.0.0:5050/api/trace
```

Within a minute, I could see the Flask app being reported in the Datadog console under APM > Services.

<img src="https://shivatk.s3.amazonaws.com/apm.png" width="822" height="190">

To be able to see more metrics in the Datadog console, I added some code to the Flask application to have some endpoints return 500 and 401s.

```
@app.route('/api/database')
def database_endpoint():
    raise Exception("Can't connect to database")

@app.route('/api/protected')
def auth_endpoint():
    abort(401)

@app.errorhandler(401)
def custom_401(error):
    return 'Authentication required.', 401
```

```
curl http://0.0.0.0:5050/api/database -> returns 500
curl http://0.0.0.0:5050/api/protected -> returns 401
curl http://0.0.0.0:5050/api/ -> returns 404 as this route is not configured
```

Additionaly, simulated delay in some endpoints by calling `time.sleep` to induce latency metrics in Datadog. Looking at APM > Trace in the Datadog console -->

<img src="https://shivatk.s3.amazonaws.com/apm-metrics.png" width="951" height="457">

Next, I wanted to test having the Datadog Agent pick up logs from my Flask app. To begin, I set `logs_enabled: true` in the `Datadog.yaml` file. Added `conf.yaml` to `/etc/datadog-agent/conf.d/python.d/` with the following entries.

```
init_config:

instances:

logs:

  - type: file
    path: /var/log/my-log.json
    service: flask
    source: python
    sourcecategory: sourcecode
```

Installed `json_log_formatter` using `pip` and added the following code to my app.

```
formatter = json_log_formatter.JSONFormatter()
json_handler = logging.FileHandler(filename='/var/log/my-log.json')
json_handler.setFormatter(formatter)
logger = logging.getLogger('my_json')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)
```

Added logging statements `logger.info('...')` to all routes in the application. After restarting the Datadog agent and hitting the app endpoints, I could see logs being written to `/var/log/my-log.json`. Within a minute, I could see these log entries being reported to Datadog cloud. Lookging at the Log Explorer section -->

<img src="https://shivatk.s3.amazonaws.com/logger.png" width="807" height="476">

The entire flask app can be found here - https://shivatk.s3.amazonaws.com/tracer.py

<img src="https://shivatk.s3.amazonaws.com/apm-services.png" width="1012" height="457">

Created a dashboard showing APM and Infrastruction metrics -->

<img src="https://shivatk.s3.amazonaws.com/dasher.png" width="1082" height="495">

Link to dashboard - https://p.datadoghq.com/sb/ce6759d2-aed8-11ec-9028-da7ad0900002-bd4be5fab8a2079c56021594fcca89e9

#### Bonus Question: What is the difference between a Service and a Resource?

A resource is usually a piece of an application like an API endpoint, Database query or a background job. A service is typically a group of resources containing APIs and database queries. In our example, the Flask application would be a service and specific endpoint like `/api/apm` would be a resouce.

-------------------------------------------------------------------------------------------------------------------

### Final question - an interesting use case for Datadog

#### Traffic light monitoring and analyzing traffic patterns

Every traffic signal and road sensor in every junction can be fitted with a micro controller that can collect data points like (red/green times, times when vehicles are waiting at a red light etc..). These data points can be sent to a central hub via any IoT protocol like ZIGBEE, MQTT. This hub can then use the Datadog agent to process/syntheize ingested data before sending it to Datadog cloud. 

Relevant authorities and analysts can use the Datadog console to visualize and analyze this data. This will help them configure traffic lights in a highly optimized way lowering the average time a vehicle has to wait at a red light. Additionally, charts and graphs can be leveraged to better understand traffic patterns across times like tourist events, weekly rush hour, weekends etc. which can help relevant parties make informed decisions in public works, advertising etc.

-------------------------------------------------------------------------------------------------------------------