## Prerequisites - Setup the environment

For this part I spun up a simple ubuntu vm in [proxmox](https://www.proxmox.com/en/) as I already had it setup and in use for a few other containers/vms that I run.
<img width="1226" alt="setup" src="https://user-images.githubusercontent.com/4121314/154208933-1207bfea-dcde-4c23-94dc-b5e1eb730b9d.png">



## Collecting Metrics:

1) Setup agent
After following the [official guidelines](https://docs.datadoghq.com/getting_started/agent/) for getting the Ubuntu agent installed and the agent started reporting, I added a few tags to the .yaml config file as seen below
<img width="1282" alt="Screen Shot 2022-02-16 at 15 24 25" src="https://user-images.githubusercontent.com/4121314/154209220-6c624013-a01a-4ce4-83f5-75480babb24e.png">

2) Setup DB integration
Next I proceeded to install and start [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) as a service, setup the MongoDB integration and add some [data](https://media.mongodb.org/zips.json) to MongoDB.
I've used MongoDB in one form or another in various projects in the past, especially in docker containers. But for this I went with a simple baremetal install.
There were some initial complications here as apt was using the new MongoDB v5 which requires a newer CPU architecture than I had on my proxmox, so it took some time fiddling around to downgrade to a previous, working version.

<img width="896" alt="Screen Shot 2022-02-16 at 21 16 10" src="https://user-images.githubusercontent.com/4121314/154262808-5e0919c0-4c11-4efc-ba96-5f34a75ae9fc.png">

<img width="1274" alt="image" src="https://user-images.githubusercontent.com/4121314/154266083-650c3539-2d6c-4622-8529-73369c7fd223.png">

3) Setup custom Agent
Next, I proceeded to check the [documentation on custom agents](https://docs.datadoghq.com/developers/custom_checks/write_agent_check) and created a simple metric providing random numbers.
<img width="445" alt="image" src="https://user-images.githubusercontent.com/4121314/154276144-de0a52d1-cee3-4a7b-82c7-a68843689723.png">

Re-using the example and adding a simple [random number generator](https://docs.python.org/3/library/random.html), I got the metric showing in the dashboard.

<img width="834" alt="image" src="https://user-images.githubusercontent.com/4121314/154276923-a1fd0f74-1512-4f34-9148-d911e287028c.png">

4) change collection interval
Following [here](https://docs.datadoghq.com/developers/custom_checks/write_agent_check/#updating-the-collection-interval) it was straightforward to change the interval in the .yaml config. No need to modify the python file.
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
<img width="94" alt="Screen Shot 2022-02-16 at 22 45 42" src="https://user-images.githubusercontent.com/4121314/154277523-41f740a2-2130-49ef-b7fe-e1a229cd7f2b.png"> <img width="85" alt="Screen Shot 2022-02-16 at 22 45 48" src="https://user-images.githubusercontent.com/4121314/154277534-213ff472-6f9a-4a4c-90ac-e36ce364175e.png">

**Comment:** While it should, according to [documentation](https://docs.datadoghq.com/metrics/summary/#interval) be possible to set metric metadata interval via the GUI, it did not seem to have any effect.

## Visualizing Data:
```
Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
```
First of all, I looked in the API documentation for Timeboards but moved on to [Dashboards](https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard) as timeboards have been deprecated in favour of them.
Based on the great examples there, I chose to re-use the Python example and adapted it to my metric.


Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
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
