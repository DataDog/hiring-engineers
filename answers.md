Your answers to the questions go here.

### Collecting Metrics

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

/etc/datadog-agent/datadog.yaml<br>
`tags: ["environment:demo", "os:ubuntu"]`
![screenshotHostMap](images/Snip20200629_11.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

MySql and integration installed. <br>
Created /etc/datadog-agent/conf.d/mysql.d/conf.yaml <br>
```
    instances: 
       - server: 127.0.0.1
         user: datadog
         pass: "password"
         port: 3306
         options:
           replication: 0
           galera_cluster: 1
           extra_status_metrics: true
           extra_innodb_metrics: true
           extra_performance_metrics: true
           schema_size_metrics: false
           disable_innodb_metrics: false
 ```

![screenshotMySQL](images/Snip20200630_14.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. <br>
**Note:Documentation needs to be corrected. The example code doesn't work as expected. Should be updated as below https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7** <br>
![screenUpdate](images/Snip20200630_16.png)

1. Create **custom_mycheck.py** under /etc/datadog-agent/checks.d folder <br>

![screenPy](images/Snip20200630_19.png)

2. Create **custom_mycheck.yaml** under /etc/datadog-agent/conf.d folder <br>

![screenYaml](images/Snip20200630_18.png)

3. Check by `sudo -u dd-agent -- datadog-agent check custom-mycheck` <br>

![screenCustomAgentCheck](images/Snip20200630_17.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

Modify the custom_mycheck.yaml file by changing **min_collection_interval: 45** <br>

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

I did not change the Python file, instead I modified the yaml file above.<br>
Another solution would be to create a cron job, which calls the check with "sudo -u dd-agent -- datadog-agent check custom_mycheck" <br>

#### Documentation that I used to complete this section:
https://www.vagrantup.com/intro/getting-started <br>
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7 <br>
https://support.rackspace.com/how-to/install-mysql-server-on-the-ubuntu-operating-system/<br>
https://docs.datadoghq.com/integrations/mysql/ <br>



## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Script is as below: <br>

```
api_key=1d277ec3da15e2ad90fca7de484a9315
app_key=16e7f5eff2caba4208fd90884caae4dbbd3907c5

curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "My Timeboard Final Version",
      "read_only" : "True",
      "graphs" : [{
          "title": "my_metric scoped over host",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:vagrant}"}
              ],
              "viz": "timeseries"
          }
      },
      {
	      "title": "MySQL CPU time anomalies",
	      "definition": {
		  "events": [],
		  "requests": [
			{"q": "anomalies(avg:mysql.performance.cpu_time{host:vagrant}, \"basic\", 3)"}
		  ],
		  "viz": "timeseries"
               }
	},
	{	
		"title": "my_metric with rollup to sum up all the points for the past hour",
        	"definition": {
            	"events": [],
            	"requests": [
                	{ "q": "avg:my_metric{host:vagrant}.rollup(\"sum\", 3600)"}
            ]
   		 }
	}
      ]
}' \

```


Once this is created, access the Dashboard from your Dashboard List in the UI:
Here is the link to the dashboard: https://app.datadoghq.com/dashboard/m9w-te7-88z/my-timeboard-final-version?from_ts=1593539069918&to_ts=1593542669918&live=true <br>

* Set the Timeboard's timeframe to the past 5 minutes

**Note: Incrementing time frames via keyboard and entering custom timeframes is in beta, it doesn't work on timeboard. I had to select the past 15 mins and then click and zoom on one of the graph and selecting a 5 mins interval** <br>
![screen5mins](images/Snip20200630_23.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.

![screen5mins](images/Snip20200630_24.png)

* **Bonus Question**: What is the Anomaly graph displaying?
The anomly graph is designed to identify when a metric is deviating from the majority of historical behavior. <br>


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

![screenAlert1](images/Snip20200630_26.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![screenAlert2](images/Snip20200630_32.png)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.


![screenEmail](images/Snip20200630_34.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

This can be accomplished via the manage downtime. <br>

  * One that silences it from 7pm to 9am daily on M-F,
  
  ![screenEmail](images/Snip20200630_37.png)
  
  * And one that silences it all day on Sat-Sun.
  
  ![screenEmail](images/Snip20200630_37.png)
  
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
