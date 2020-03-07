# Answers - Fernando Melone

## Setting up the environment

I used [multipass](https://multipass.run/) instead of vagrant as I was already familiar with it and it's much faster to spin up and manage.

## Collecting Metrics:

* Tagged Agent and screenshot of the Host Map page in Datadog.

  <img src="https://i.ibb.co/QkwBPQL/host-map.jpg"></a>
* PostgreSQL Installed in ddx-psql and Datadog integration enabled for that database.

  <img src="https://i.ibb.co/THLr0nd/psql-metrics.jpg"></a>  
  [Dashboard Link](https://app.datadoghq.eu/dash/integration/58/postgres---metrics)
* Custom Agent check created, submitting a metric named my_metric with a random value between 0 and 1000

  <img src="https://i.ibb.co/r7Fqxff/custom-check.jpg"></a>

  <img src="https://i.ibb.co/7jmLDj8/my-metric-chart.jpg"></a>
* Changed the check's collection interval to 45 seconds, without modifying the python check code, this includes the **Bonus Question's** answer.  

  **How it was done:** Modified the minimum collection interval in the configuration file of the check. This means that the collection will try to run the check every 45 seconds, but not guaranteeing the delivery of the metric to datadoghq.eu, as it might need to wait in line for other integrations enabled on the same agent [as specified here.](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval)

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Custom metric chart scoped over the host.

  <img src="https://i.ibb.co/nbPzQ7M/custom-metric-scoped-chart.png"></a>
* PostgreSQL System Load chart with the anomaly function applied.

  <img src="https://i.ibb.co/NK3gFvk/psql-anomaly-chart.png"></a>
* Custom metric chart with the rollup function applied to sum up all the points for the past hour into one bucket  
  _I didn't have enough data to do 1h rollups so they are 120s sums instead of 3600s, but I got the idea_

  <img src="https://i.ibb.co/kStqW9n/custom-metric-rolledup-chart.png"></a>

Script used to create this located in `./src/create_timeboard.py`

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes ❌
  * The lowest timeframe available through the UI for Timeboards (or ordered dashboards) is 15min
* Take a snapshot of this graph and use the @ notation to send it to yourself. ✔️

  <img src="https://i.ibb.co/CJHXC29/snapshot-shared.png" width="450"></a>
* **Bonus Question**: What is the Anomaly graph displaying?
  * It is displaying that the metric values go above or below the expected range based on past trends.

## Monitoring Data

Created a monitor with the following configuration for the metric `my_metric`

* Warning threshold of 500 ✔️
* Alerting threshold of 800 ✔️
* Notify if No Data for this query over the past 10m. ✔️

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers. ✔️
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state. ✔️
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state. ✔️

  ```
    {{#is_alert}}
    Critical Alert: **my_metric** has a value of {{value}} and it is above {{threshold}}
    Host IP: {{host.ip}}
    @fermelone+dd@gmail.com 
    {{/is_alert}}

    {{#is_warning}}
    Warning: **my_metric** has a value of {{value}} and it is above {{warn_threshold}}
    @fermelone+dd@gmail.com 
    {{/is_warning}}

    {{#is_no_data}}
    No Data Detected: **my_metric** has reported no data for a period of 10m
    @fermelone+dd@gmail.com 
    {{/is_no_data}}

    {{#is_recovery}}
    Recovery Message: **my_metric** has recovered from an alert with a value of {{ok_threshold}}
    @fermelone+dd@gmail.com 
    {{/is_recovery}}
    ```
* Email sent by monitor (for Alert):

  <img src="https://i.ibb.co/3m7nFFd/monitor-alert.png" width="450"></a>

* **Bonus Question**: Since this monitor is going to alert pretty often, we don’t want to be alerted when we are out of the office. Two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F ✔️
  * And one that silences it all day on Sat-Sun ✔️
  * Email notification received:
  
    <img src="https://i.ibb.co/T1jjvW2/downtime-schedule-email.png" width="450"></a>

## Collecting APM Data:

The following application was instrumented using Datadog’s APM tracing solution:

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
    app.run(host='0.0.0.0', port=5050)
```

* **Note**: Instrumented it by using parametrized `ddtrace-run` command.

* **Bonus Question**: What is the difference between a Service and a Resource?
  * Assuming you are talking about Web Services and not coal mining, a Service is software that makes itself available over the internet, to communicate specific data to another service or to recieve data to fulfill a specific task. With that mentioned, a resource is data or functionality which is accessed using unique identifiers and a well defined set of operations. In Web Services, resources are generally associated with RESTful Web Services, in which they are identified & accessed using URIs and HTTP methods.

Dashboard with APM & Infrastructure Metrics:

  <img src="https://i.ibb.co/8MR712X/apm-and-infra-dashboard.png" width="600"></a>  

  [Dashboard Link](https://app.datadoghq.eu/dashboard/sfj-ibb-vif/apm--infrastructure-dashboard)

Instrumented app included in `./src/myApp.py`

## Final Question:

_Is there anything creative you would use Datadog for?_  

There is actually! I have extended a JS package that gathers metrics from a WAMP API from a crypto-mining pool.  
This code is running in my RPi and emits metrics to DD using the NodeJS DD package to communicate with the DD API [node-datadog-metrics](https://github.com/dbader/node-datadog-metrics)  
I have also made a pull request to this repo so it can support other endpoints, such as the `api.datadoghq.eu` realm, as I am using an EU account and this package did not support parametrization of the endpoint [_pull request here_](https://github.com/dbader/node-datadog-metrics/pull/50)  

The results are a simple dashboard that shows all I want to know about the `status`, `hashrate` (power), and `results` of my miner, in real-time, divided by `miner type`, `miner name`, `algorithm`, and `coin name`:  

![Prohashing Dashboard](img/12_prohashing_dashboard.png.jpg?raw=true)

<img src="https://i.ibb.co/DtkRrG3/prohashing-dashboard.png" width="600"></a>  

[Dashboard Link](https://app.datadoghq.eu/dashboard/jmf-mrf-b3w/prohashing-mining-dashboard)

_To protect my privacy I have omitted some metrics like location, balance, etc_  
_It still shows what's possible with this integration_