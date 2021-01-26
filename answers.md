## Datadog Solution Engineering Exercise
## Candidate: Matt Glenn
## Datadog Login: mfglenn@outlook.com

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
    * See the */environment/Vagrantfile* containing the configuration for the Vagrant Ubuntu VM.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Once this is ready, sign up for a trial Datadog at https://www.datadoghq.com/

**Please make sure to use “Datadog Recruiting Candidate” in [the “Company” field](https://a.cl.ly/wbuPdEBy)**

Then, get the Agent reporting metrics from your local machine and move on to the next section...
### Answer: ![PR01 - Metric Capture](/images/PR01 - Metric Capture.png)

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
    * **Answer**: See */config/datadog.yaml* file adding the "environemnt:dev" and "exercise:collecting_metrics" tags to the host.
    * **Answer**: See ![CM01 - Host Map and Tag Capture](/images/CM01 - Host Map and Tag Capture.png)
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
    * **Answer**: See the *install_mongo.sh* script file used to install the MongoDB Community Edition, and create the datadog account for the datadog integration.
    * **Answer**: See the */config/conf.yaml* configuration file for the MongoDB integration assigning the datadog account and creating a custom query.
    * **Answer**: See ![CM02 - MongoDB Integration Metrics](/images/CM02 - MongoDB Integration Metrics.png)
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
    * **Answer**: See the */environment/checks/custom_metric_check.py* file containing the **custom_metric_check** logic.
    * **Answer**: See the */environment/checks/custom_metric_check.yaml* configuration file for the **custom_metric_check**.
    * **Answer**: See ![CM03 - Custom Agent Check - my_metric](/images/CM03 - Custom Agent Check - my_metric.png)
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
    * **Answer**: See the */environment/checks/custom_metric_check.yaml* configuration file for the *min_collection_interval* for the **custom_metric_check**.
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
    * **Answer**: By modifying the */environment/checks/custom_metric_check.yaml* configuration file it is possible to adjust the *min_collection_interval* for the custom check without modifying the corresponding Python file.  

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
    * **Answer**: See ![VM01 - Visualizing Data Exercise](/images/VM01 - Visualizing Data Exercise.png)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
* **Answer**: See the */timeboards/VisualizingDataExercise.json* file exported from the client. 

Once this is created, access the Dashboard from your Dashboard List in the UI:
* **Answer**: See ![VM02 - Exercise Dashboards List](/images/VM02 - Exercise Dashboards List.png)

* Set the Timeboard's timeframe to the past 5 minutes
    * **Answer**: See ![VM03 - Datadog Timeboard - 5 Min](/images/VM03 - Datadog Timeboard - 5 Min.png)
* Take a snapshot of this graph and use the @ notation to send it to yourself.
    * **Answer**: See the */snapshots* directory for the emailed snapshots.
    
* **Bonus Question**: What is the Anomaly graph displaying?
    * **Answer**: The anomaly graph is displaying the results of the basic anomaly detection methodology for the timeseries of the selected metric.  The graph provides a gray background showing the expected behaivor for the series based on the past and the bounding parameters, while highlighting the portion of the timeseries that falls outside of the expected behavior range.  Adjusting the timeframe of the timeboard impacts the calculation and display of the expected beahvior for the graph timeseries based on the selected interval.

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

### Answer: 
* Per the instructions the Custom Metric Monitor has been added to monitor the "my_metric" values.  In addition to the alert and warning thresholds, this monitor also implements the recovery thresholds.
* See the editor https://app.datadoghq.com/monitors#29272181/edit
* See ![MM01 - Custom Metric Monitor](/images/MM01 - Custom Metric Monitor.png)
* See the */monitors/CustomMetricMonitor.json* file exported from the client.
* See the associated notifications in the */notifications* directory. 

### Bonus Answer: 
* Per the instructions the daily and weekend downtimes have been configured for the Custom Metric Monitor.
* See the daily monitor configuration: ![MM02 - Custom Metric Monitor Daily Downtime](/images/MM02 - Custom Metric Monitor Daily Downtime.png)
* See the weekend monitor configuration: ![MM03 - Custom Metric Monitor Weekend Downtime](/images/MM03 - Custom Metric Monitor Weekend Downtime.png)
* See the associated notifications in the */notifications* directory.


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
* **Answer**: When I first became aware of the Datadog solution I was reminded of many occasions during my oil and gas career where operational insights where obstructed due to the lack of visibility into the applications monitoring oil and gas drilling, hydraulic fracturing, and production operations. Although it was possible to gather the disparate data streams into a singular source, there was no widely available solution that could effectively monitor all each of the applications in a consolidated interface.  While working for the company I developed a home-grown solution to gather and analyze these data streams, to populate a dashboarding solution that would allow engineers to quickly gain insights into the current status of their projects, report ongoing issues, and identify potential inefficiencies in our operations. ## Complete Write Up ##


## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)
