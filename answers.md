Your answers to the questions go here.

# Prerequisites - Setup the environment
You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues.
You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.
Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.


## Answer: Instruction for setup the environment:

* Install virtualbox and vagrant for MacOS via brew.
  * brew cask install virtualbox
  * brew cask install vagrant
* Bring up the vm
  * vagrant init hashicorp/bionic64
  * vagrant up
* SSH into the vm
  * vagrant ssh


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
  
  ![screenDowntime](images/Snip20200630_38.png)

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

Steps: <br>
Install ddtrace by **pip install ddtrace** <br>
By default, Flask runs apps on port 5000. The Datadog agent also uses 5000 by default, so this command below specifies a different Flask port to avoid any conflit<br>

```
FLASK_APP=sample_app.py DATADOG_ENV=flask_test ddtrace-run flask run --port=4999
```

![screenAPM](images/Snip20200701_42.png) 

https://app.datadoghq.com/apm/services?end=1593640453237&env=flask_test&paused=false&start=1593636853237


* **Bonus Question**: What is the difference between a Service and a Resource?

Services are the building blocks of microservice architectures - broadly a service groups together endpoints, queriers, or jobs for the purposes of building your application. An example would be a database like MySQL. <br>

Resources are particular action for a given service. They are typically an instrumented web endpoint, database query, or backgroud job. Same like the MySQL database example as a service, the actual SQL query would be a resource.<br>

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

![screenAPM](images/Snip20200701_44.png) 

https://app.datadoghq.com/dashboard/n6z-296-72s/zhangs-timeboard-1-jul-2020-1509?from_ts=1593638483258&live=true&to_ts=1593642083258

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

My interest is to use Datadog to provide end to end service visibility, which includes end user monitoring by synthetic monitoring, APM traces, metrics and application logs. Just knowing that the application performance is degraded is not good enough, we need to correlate to the business services so that we can quick identify when certain alerts were triggered, what specific business services that the application provides were affected. This will be very helpful to understand the real impact caused by the issue. For example, for Ecom application, “check-out” is definitely a critical service. Every time the alerts are triggered, I need to quickly verify if “check-out” service is being affected.  Datadog as the platform, that integrates end user monitoring, APM traces and logs, enables us to see this flow in one place. By configuring end user monitoring, we can pro-actively identify issues before real customers are getting impacted. APM metrics provide us indicators of performance degradation and it is also where correlation with business services happens by identifying the important APIs/classes/methods that contribute to the services and setup alerts against those metrics. And logs help us to dig in to understand “what” caused the issue.<br> 









