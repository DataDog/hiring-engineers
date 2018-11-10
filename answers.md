## Collecting Metrics:

- [x] Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![tags](https://user-images.githubusercontent.com/768821/48220655-bf34f400-e344-11e8-98c7-8f65130f5950.png)

- [x] Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

![mysql](https://user-images.githubusercontent.com/768821/48231498-30839f80-e363-11e8-93d2-606a71c4a5d9.png)
- [x] Create a custom Agent check that submits a metric named `my_metric` with a random value between 0 and 1000.

![my_metric](https://user-images.githubusercontent.com/768821/48236179-f2dc4200-e375-11e8-99a9-7fe118a09864.png)
- [x] Change your check's collection interval so that it only submits the metric once every 45 seconds.

File `/conf.d/random_check.yaml`:
```
init_config:

instances:
    - min_collection_interval: 45
```

- [x] **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

> According to the [documentation](https://docs.datadoghq.com/developers/integrations/new_check_howto/#metadata-csv), an integration has a CSV metadata field for `interval` that can control the collection interval. 

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

- [x] Your custom metric, `my_metric`, scoped over your host. [JSON](ruby-script/timeboard-creator/metric.json)
- [x] Any metric from the Integration on your Database with the anomaly function applied. [JSON](ruby-script/timeboard-creator/anomaly.json)
- [x] Your custom metric, `my_metric`, with the rollup function applied to sum up all the points for the past hour into one bucket [JSON](ruby-script/timeboard-creator/rollup.json)

- [x] Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

[Ruby Script](ruby-script/timeboard-creator/run_it.rb)

Once this is created, access the Dashboard from your Dashboard List in the UI:

- [x] Set the Timeboard's timeframe to the past 5 minutes
- [x] Take a snapshot of this graph and use the @ notation to send it to yourself.

![screenshot of snapshot notification](https://user-images.githubusercontent.com/768821/48292335-c5070400-e42e-11e8-99e6-d12cda8cadeb.png)

- [x] **Bonus Question**: What is the Anomaly graph displaying?

> The anomaly is looking for values outside of a standard deviation over the specified time period. In this case, highlight when the metric falls outside of 'expected' values. In this example, having more than one connection to the MySQL DB will generate an anomaly.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- [x] Warning threshold of 500
- [x] Alerting threshold of 800
- [x] And also ensure that it will notify you if there is No Data for this query over the past 10m.

![Monitor](https://user-images.githubusercontent.com/768821/48278294-fd441d80-e401-11e8-8883-00d1a6bf7df4.png)

Please configure the monitor’s message so that it will:

- [x] Send you an email whenever the monitor triggers.
- [x] Create different messages based on whether the monitor is in an **Alert**, **Warning**, or **No Data** state.
- [x] Include the metric **value** that caused the monitor to trigger and **host ip** when the Monitor triggers an Alert state.

```
Ahoy @osowskit@gmail.com :wave:

Oh my! {{#is_alert}} We've hit an Alert! IP {{host.ip}} reported: **{{value}}**   {{/is_alert}}
{{#is_no_data}} No data present? {{/is_no_data}}
{{#is_warning}} Oooo - Host {{host.name}} with IP {{host.ip}} is acting up. Getting close - it's warning time. {{/is_warning}} 
```

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![alert notification email](https://user-images.githubusercontent.com/768821/48278769-52ccfa00-e403-11e8-8a7d-45a065008361.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  - [x] And one that silences it all day on Sat-Sun.
  - [x] Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![downtime](https://user-images.githubusercontent.com/768821/48278582-cc181d00-e402-11e8-9460-a194ba3449da.png)


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

- [ ] Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

Datadog's agent will start recording events when Running the above application with `ddtrace-run`. Alternatively, Datadog provides a [Flask trace middleware](http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask) that will automatically record and report traces.

- [x] [Python App](python_script/apm_sample.py) - using the flask trace middleware


## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

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
