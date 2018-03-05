# DataDog Solutions Engineer Exercise
Datadog is a cloud monitoring service for different applications. They can analyze and monitor servers, containers, container managements services, datadabases or if they don't have the integration you can make it :)

If you want more information or want to see it in action log in for their trial at [Datadog](https://datadoghq.com)

## Environment
- I created a droplet in [DigitalOcean](https://m.do.co/c/a4c588c90cf4), you can use the referral code if you want to test it out.
- You can simply start an Ubuntu 16.04 or any version of Ubuntu with a simply click.
- Install the agent 
```bash 
DD_API_KEY=$YOUR_API_KEY_HERE bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
- You will get a confirmation that its running and how to start / stop it. If you want more set of commands for the latest agent you can go to [Agent Usage](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/)
- All the configuration of the agent can be found
```bash
/etc/datadog-agent/datadog.yaml
```

## Collecting Metrics:
### Tagging
> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Based on the [Tagging Documentation](https://docs.datadoghq.com/getting_started/tagging/) we created the following tags
```bash
tags:
   - ddse
   - env:dev
   - role:app
   - hosted:digitalocean
   - region:us_east
```
You can see the tags on the Host in the following screenshot
![cli_tags](/images/cli_tags.png)

And then we can validate them on the Datadog UI
![ui_tags](/images/ui_tags.png)

### Databases
> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Selected to install MySQL with the following 3 commands
```bash
sudo apt-get update
sudo apt-get install mysql-server
mysql_secure_installation
```
Then we need to install & configure the mysql agent. Luckily most of the agents are already installed in the `conf.d` under the `datadog-agent` folder.
```bash
/etc/datadog-agent/conf.d/mysql.d/
```
It has an example configuration named `conf.yaml.example`. 
For readability, I chose to call it `mysql.yaml` and added the basic configuration 
```bash
init_config:

instances:
  - server: localhost
    user: datadog
    pass: <removed>
    port: 3306             
    tags:                  
      - mysql_do
    replication: 0
    galera_cluster: 1
    extra_status_metrics: true
    extra_performance_metrics: true
    schema_size_metrics: false
    disable_innodb_metrics: false
```
Finally we reloaded the Datadog configuration `sudo service datadog-agent restart` and then check the mysql configuration using the `status`
```bash
ddse:/etc/datadog-agent/conf.d/mysql.d# sudo datadog-agent status | grep -A6 mysql
    mysql
    -----
      Total Runs: 188
      Metrics: 61, Total Metrics: 11467
      Events: 0, Total Events: 0
      Service Checks: 1, Total Service Checks: 188
```
With this we have double checked that its running and it has metrics.
Finally after a few minutes we checked it in the UI as well as the console
![cli_mysql_statusCheck](/images/cli_mysql_statusCheck.png)
![ui_mysql_hostCheck](/images/ui_mysql_hostCheck.png)

### Custom Agents
> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
We created a custom Metric analizying and reviewing the [documentation](https://docs.datadoghq.com/agent/agent_checks/) the code can be seen below and in the scripts directory
```python
import random
from checks import AgentCheck

class CustomAgent(AgentCheck):
  def check(self, instance):
    self.gauge('ddse.my_metric',random.randint(0,1000))
```
and the configuration
```yaml
init_config:

instances:
    [{}]
```

This can be checked via the status
```bash
ddse:/etc/datadog-agent/checks.d# sudo datadog-agent status | grep -A6 customagent
    customagent
    -----------
      Total Runs: 81
      Metrics: 1, Total Metrics: 81
      Events: 0, Total Events: 0
      Service Checks: 0, Total Service Checks: 0
```
And the same can be seen in the UI.

> Change your check's collection interval so that it only submits the metric once every 45 seconds.
I modified it using the configuration in the yaml file which answers the bonus question below.

> Bonus Question Can you change the collection interval without modifying the Python check file you created?
```yaml
init_config:
    min_collection_interval: 45
instances:
    [{}]
```
## Visualizing Data
> Utilize the Datadog API to create a Timeboard that contains:
> - Your custom metric scoped over your host.
> - Any metric from the Integration on your Database with the anomaly function applied.
> - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
> 
> Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.
The following code is an excerpt that will create the timeboard (3 of them)  as described above. The full code can be found in the scripts section named `timeboard.py`
```python
graphs = [
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "ddse.my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Custom Metric"
  },
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.performance.user_time{*}, 'basic', 2)"},
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies - MySQL Performance User Time"
  },
  {
    "definition": {
      "viz": "query_value",
      "events": [],
      "requests": [
        {"q": "avg:ddse.my_metric{*}.rollup(sum, 3600)"}
      ]
    },
    "title": "Average Custom Metric RollUp Sum last hour",
  } 
]
```
> Once this is created, access the Dashboard from your Dashboard List in the UI:
> - Set the Timeboard's timeframe to the past 5 minutes
> - Take a snapshot of this graph and use the @ notation to send it to yourself.
![snapshot_email](/images/snapshot_email.png)

The below will show the last hour with the full RollUp
![timeboard-lasthour](/images/timeboard-lasthour.png)

And then 
![timeboard-last5mins](/images/timeboard-last5mins.png)

> - Bonus Question: What is the Anomaly graph displaying?

The anomaly is an algorithmic feature, that displays a metric and analyzes the current, and past data to detect what is normal and what is not. Considering that if the data is brand new it might not have all the prediction needed to be accurate. IT also depends on the bounderies that you give it and the type of algorithm that its selected.
In my case I selected the basic type and a bound of 2.

## Monitoring Data
> Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
> 
> Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
> - Warning threshold of 500
> - Alerting threshold of 800
> - And also ensure that it will notify you if there is No Data for this query over the past 10m.

After creating the alert here is the exported JSON
```json
{
	"name": "Custom Metric is Alerting",
	"type": "metric alert",
	"query": "max(last_5m):avg:ddse.my_metric{ddse} > 800",
	"message": "{{#is_alert}} Metric is too high! {{/is_alert}}\n @emvp84@gmail.com",
	"tags": [],
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": true,
		"notify_no_data": true,
		"renotify_interval": "0",
		"evaluation_delay": "",
		"escalation_message": "",
		"no_data_timeframe": 10,
		"include_tags": false,
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}
```
> Please configure the monitor’s message so that it will:
> - Send you an email whenever the monitor triggers.
Just add the team member in step 5
> - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
> - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
```markdown
{{#is_alert}}
ALERT on Custom Metric. 
Value is: {{value}} 
Passed the threshold of: {{threshold}}
{{/is_alert}}
{{#is_warning}}
Warning on Custom Metric. 
Value is: {{value}} 
Passed the threshold of: {{threshold}}
{{/is_warning}}
{{#is_no_data}}There is no data for Custom Metric{{/is_no_data}} @emvp84@gmail.com
```
> - When this monitor sends you an email notification, take a screenshot of the email that it sends you.
![monitor_notification](/images/monitor_notification.png)

> Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
> - One that silences it from 7pm to 9am daily on M-F,
> - And one that silences it all day on Sat-Sun.
> - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![daily_downtime](/images/daily_downtime.png)
![daily_downtime2](/images/daily_downtime.png)
![weekend_downtime](/images/weekend_downtime2.png)
![weekend_downtime2](/images/weekend_downtime2.png)

## Collecting APM Data
Given the flask app, connect it to Data Dog APM or ddtrace and run the APM.
Here you can see the App being monitored by the APM
![apm_working](/images/apm_working.png)

> Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
The combined infrastructure can be found here https://app.datadoghq.com/dash/630840/apm--infrastructure
or viewed here
![combined_apm_infra](/images/combined_apm_infra.png)

> Bonus Question: What is the difference between a Service and a Resource?
"Service"  is the name of the processes that work together to resolve the code, in our case is Flask (since we are using the standard cli for ddtrace, but it can be modified in the Middleware, for example
```python
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
```
In the above example, the service would be named `my-flask-app`

"Resource" is an specific query to a service. For example in our case, we are hitting the `/` root of by executing a loop 
```bash
for i in {1..500}; do curl 127.0.0.1:5000; done
```
and that will query according to the code the following piece:
```python
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'
```
So the function or Resource being tracked will be `api_entry`
![apm_service_resource](/images/apm_service_resource.png)

## Final Question
> Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
> Is there anything creative you would use Datadog for?
A few ideas that come to my mind are:
1. How many times we are leaving one set of lights during a day on or off. Have metrics compared how much electricity we are using during the day wwhen its sunny and the light doesn't need to be on.
2. Gather how many times the metro in DC has been delayed and gather statistics on the cost of commute that the delay represents
3. Compare number 2 with the cost of the HOV / EZ Pass lanes are, to validate if its worth it driving vs metroing
4. Get at regular intervals the traffic of a given distance (for commuting purposes) to know what is are the best times in different days.
