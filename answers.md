Your answers to the questions go here.
## Collecting Metrics:
* Using a VM Ubuntu 16.04 as host machine.

* Add tags in the Agent config file, located on the host machine at: */etc/datadog-agent/datadog.yaml*:
	*
	```yaml
	# Set the host's tags (optional)
	tags:
	   - region:westcoast
	   - env:test
	   - hiremelol
	```

	* Here is a screen shot of the machine in the Host Map page in Datadog:
	![alt text](./screenshots/hostmap.png)

* Install MySQL on the host and then install the respective Datadog integration. Then create the following mysql configuration in */etc/datadog-agent/conf.d/mysql.d/conf.yaml*
	* 
	```yaml
	init_config:

	instances:
	  - server: localhost
	    user: datadog
	    pass: 'teapot00'
	    tags:
		- optional_tag1
		- optional_tag2
	    options:
		replication: 0
		galera_cluster: 1
	```
	
	* graphs of sql metrics on the dashboard: 
	![alt text](./screenshots/sql_graphs.jpg)

* Create *hello.yaml* and *hello.py* files in the *./config.d/* and *./check.d/* directories, respectively.
	* *hello.yaml*
	``` yaml
	init_config:

	instances:
	    [{}]
	```
	* *hello.py*
	```python
	from checks import AgentCheck
	import random


	class HelloCheck(AgentCheck):
	    def check(self, instance):
		self.gauge('my_metric', random.randint(0,1001))
	```
	
	* Screenshot of my metric on Data Dog
	![alt text](./screenshots/my_metric.png)

* To change the check's collection interval to every 45sec (in v6), I added the *min_collection_interval* instance parameter in the check config file (*/config.d/hello.yaml*), and set it to 45. It will skip 2 checks and gauge the metric once every 3rd check.
	* updated *hello.yaml* file
	``` yaml
	init_config:

	instances:
	    - min_collections_interval: 45
	```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
	* The above method does not modify the python file.


## Visualizing Data
Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

 Python script used to create this dashboard:
  ```python
  from datadog import initialize, api
 import json

 d = None
 with open('./keys.json') as json_data:
     d = json.load(json_data)

 API_KEY = d["api_key"]
 APP_KEY = d["app_key"]

 options = {
     'api_key': API_KEY,
     'app_key': APP_KEY
 }

 initialize(**options)

 title = "Visualizing Data Timeboard"
 description = "DataDog challenge second question on visualizing data."
 graphs = [{
     "definition": {
         "events": [],
         "requests": [
             {"q":"avg:my_metric{host:utsav-VirtualBox}"}
         ],
         "viz": "timeseries"
     },
     "title": "My Metric"
 },

 {
     "definition": {
         "events": [],
         "requests": [
             {"q": "anomalies(avg:mysql.performance.cpu_time{host:utsav-VirtualBox}, 'basic', 1)"}
         ],
         "viz": "timeseries"
     },
     "title": "SQL Performance Metric"
 },

 {
     "definition": {
         "events": [],
         "requests": [
             {"q":"avg:my_metric{host:utsav-VirtualBox}.rollup(avg, 3600)"}
         ],
         "viz": "timeseries"
     },
     "title": "My Metric (Rollup - 1hr)"
 }
 ]

 template_variables = [{
     "name": "host1",
     "prefix": "host",
     "default": "host:my-host"
 }]

 read_only = True
 response = api.Timeboard.create(title=title,
                      description=description,
                      graphs=graphs,
                      template_variables=template_variables,
                      read_only=read_only)

 print(response)
  ```
  * Screenshot of Timeboard:
  ![alt text](./screenshots/visualizing_data_timeboard.png)
  
  * **Bonus**: The anomaly function uses an algorithm to identify when a metric is behaving differently than it has in the past, taking into account trends.
 

## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

	* Screenshot of Monitor Details:
	![alt text](./screenshots/metric_monitor.png)
	
	* Screenshot of Monitor Alert Email:
	![alt text](./screenshots/monitor_alert_email.png)

	* Screenshot of Monitor Scheduled Downtime Email:
	![alt text](./screenshots/downtime_email.png)
