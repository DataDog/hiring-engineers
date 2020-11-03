**Name:** Bradley Beard

**Postion:** Datadog Solutions Engineer

Hello - Below are my responses to the hiring excercise. For this exercise I set up an Ubuntu VM through Vagrant and Virtualbox and installed the agent directly onto Ubuntu. If there's any clarification I can provide please let me know. Thank you. 


### Collecting Metrics

I started by adding a role, location, and resource_name tag to datadog.yaml file. After restarting the agent, they appeared as host tags in the dashboard. See the screenshot of the host in the hostmap below:

[![host-tags.png](https://i.postimg.cc/gj0wZTyh/host-tags.png)](https://postimg.cc/xJWTrg4j)


I then installed MySQL and set up the corresponding integration through following directions on the integrations section of the dashboard. 


[![My-SQL-Integration.png](https://i.postimg.cc/JzR55Qy5/My-SQL-Integration.png)](https://postimg.cc/fJgdwmfV)


To create the custom metric, I went through the documentation to get a working example and understanding of the architecture. After than I modified it to produce the random number between 1 and 1000. The custom check consisted of two files. One is the configuration file in the conf.d directory I labeled checkvalue.yaml. Seen below:

```yaml
init_config:

instances: [{}]
```

The other aspect to the custom check is the python script that generates the metric itself. I've labeled it checkvalue.py and placed it in the checks.d directory. The contents are below:

```python
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
  def check(self,instance):
    self.gauge('my_metric', random.randint(1,1000))
```

To change the collection interval from the default interval of 15 seconds up to 45 seconds, I changed the configuration file to include the min_collection_interval parameter. Modified configuration file below:

```yaml
init_config:

instances: 
  - min_collection_interval: 45
```

This is done without modifying the check python file at all. 

### Visualizing Data 

The next step was to create a dashboard using the Datadog API. To get an understanding of this piece, I first worked through building a similar dashboard in the UI and looking at its JSON makeup. After that, I practiced API calls using the Datadog collection in Postman and generated a POST request to create the dashboard for the exercise. Finally, I generated a Python script for the request through Postman that uses the request library. The script of the API call can be seen here:

```python
import requests

url = "https://api.datadoghq.com/api/v1/dashboard"

payload="{ \"description\": \"This is a test of the Datadog API to create a dashboard\", \"is_read_only\": false, \"layout_type\": \"ordered\", \"notify_list\": [], \"title\": \"Bradley Beard API Dashboard\", \"widgets\": [ { \"definition\": { \"title\": \"my_metric over time\", \"type\": \"timeseries\", \"requests\": [ { \"q\": \"avg:my_metric{host:vagrant}\" } ] } }, { \"definition\": { \"title\": \"Avg of mysql.net.connections\", \"type\": \"timeseries\", \"requests\": [ { \"q\": \"anomalies(avg:mysql.net.connections{host:vagrant}, 'basic', 2)\" } ] } }, { \"definition\": { \"title\": \"Avg of my_metric over host:vagrant\", \"type\": \"query_value\", \"requests\": [ { \"q\": \"avg:my_metric{host:vagrant}.rollup(avg, 3600)\" } ], \"type\": \"query_value\" } } ] }"

headers = {
  'Content-Type': 'application/json',
  'DD-API-KEY': '67941e6a4871a8eba7358556258f5410',
  'DD-APPLICATION-KEY': '23402c2c18fbc6e851d7c75dd432fc5892997612',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
