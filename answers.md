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
