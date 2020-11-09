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

I did not include any options to change the axis, color, line styles, etc. However, that is all possible through the UI and API and recommended for ideal readability. 

To send a snapshot to myself, I clicked the my_metric graph and clicked on the snapshot option. There I had the option to write a comment and include @beardbradleyj@gmail.com to send the snapshot to myself. Here is what the email looks like as well as an image of the dashboard itself with the timeframe set to 5 minutes:

[![Datadog-snapshot.png](https://i.postimg.cc/2jxBQLW4/Datadog-snapshot.png)](https://postimg.cc/NL5MYMpM)

[![my-metric-dashboard.png](https://i.postimg.cc/TYwhn7f6/my-metric-dashboard.png)](https://postimg.cc/K46Z251q)

From left to right we have the my_metric timeseries graph, the MySQL Connection anomoly graph, and the average of my_metric over the chose timeframe. The middle anomoloy graph shows the average mysql connections, as well as a gray outline to show the expect bounds of normal behavior for this metric. 


### Monitoring Data 

To create a monitor around my_metric I went to the Monitor section of the UI and followed the workflow. I set the monitor to warn if the average of my_metric stays above 500 for 5 minutes and alerts if it stays over 800. It also notifies me if there is no data for more than 10 minutes. Here are the monitor settings:

[![Monitor-Settings.png](https://i.postimg.cc/x8dHJ96r/Monitor-Settings.png)](https://postimg.cc/XGTXt6Mx)

One interesting aspect to this section is the ability to create different email templates based on which monitor is triggered. My template for these emails is shown here:

```
{{#is_alert}} 
my_metric has exceeded 800 on host {{host.ip}} with a value of {{value}} over the last 5 minutes
{{/is_alert}} 

{{#is_warning}} Warning: my_metric is between 500 and 800 over the last 5 minutes {{/is_warning}}

{{#is_no_data}} No data received from monitor for the past 10 minutes {{/is_no_data}} @beardbradleyj@gmail.com
```

Here is an example of the email I received when my_metric stayed in the warning zone for 5 minutes: 

[![Monitor-Email.png](https://i.postimg.cc/c4kcDs7Z/Monitor-Email.png)](https://postimg.cc/RNffhxbb)

To schedule downtime for this monitor, I simply went to the 'Manage Downtime' tab. The example for my weekday nightly downtime can be found here: 

[![Downtime-Settings.png](https://i.postimg.cc/dV0qbLLc/Downtime-Settings.png)](https://postimg.cc/dLzPdQ25)

When this downtime was scheduled, I made sure I was notified through email, shown below:

[![Downtime-Notification-Email.png](https://i.postimg.cc/43tjqgbT/Downtime-Notification-Email.png)](https://postimg.cc/v1YPxCNP)

Time is shown in UTC. 

### Collecting APM Data

To collect APM data, I used the following Flask python script and instrumented it by running 'ddtrace-run python3 my_app.py' in the command line. 

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
```

After doing this and restarting the agent, traces start collecting in the APM section of the UI:

[![Traces.png](https://i.postimg.cc/L5wjPrqx/Traces.png)](https://postimg.cc/7J1C8tnz)

Below is a simple dashboard I created using a my_metric, the CPU usage, the service map, and the CPU percentage the trace agent is using:

[![APM-Dashboard.png](https://i.postimg.cc/dVpSvVJx/APM-Dashboard.png)](https://postimg.cc/YvNxzkG6)


### Final Question 

It's clear that Datadog can be used almost anywhere through the out-of-the-box integrations and ability to create custom integrations. Coming from a networking background, one creative use case I can imagine is to detect wireless clients in a building and send the total clients to Datadog to monitor building capacity. This would be a very nice use case during the pandemic, as capacity rules are changing often and many businesses could use a simple way to track their capacity in real-time. 


Thank you for taking the time to read through this exercise, I learned quite a bit. Again, if there's any clarification I can provide please don't hesitate to reach out. 

