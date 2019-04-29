## The environment

For my environment, I am using a small kubernetes cluster in GKE.  It has 3 nodes in the worker pool. Since this is a clustered environment, I used the cluster scope instead of host whenever possible.

The Datadog agent was installed using the instructions provided here:
https://app.datadoghq.com/account/settings#agent/kubernetes

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I added the `DD_TAGS` environment variable to the DaemonSet container spec with and set the tag as `kennonkwokhost:true`

Here's one of the hosts from the Host Map with the tag added

![Host with tag](https://github.com/kennonkwok/hiring-engineers/raw/solutions-engineer/images/host_with_tag.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Deployed a single-pod deployment of PostgreSQL with a persistent volume for the /var/lib/postgresql/data/postgres directory.  The persistent volume allows the database (along with the datadog agent credentials) to be retained if the pod is rescheduled. All of the kubernetes manifests are in the `files/manifests` directory.

The following annotations on the pod were used to configure the postgres checks via auto discovery:

```yaml
    ad.datadoghq.com/postgres.check_names: '["postgres"]'
    ad.datadoghq.com/postgres.init_configs: '[{}]'
    ad.datadoghq.com/postgres.instances: '[{"host":"%%host%%","port":"5432","username":"datadog","password":"datadog"}]'
```

I ran `pgbench` on the pod to generate some load for the database and captured the metrics.

![Postgres Metrics](https://github.com/kennonkwok/hiring-engineers/raw/solutions-engineer/images/postgres_metrics.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

The following python check was created and a ConfigMap created using `create configmap datadog-conf --from-file=conf.d` and `create configmap datadog-checks --from-file=checks.d .  The contents of the ConfigMaps were mounted at /conf.d and /checks.d on the datadog-agent pods.

```python
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

import random

class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

my_metric.yaml contains the `min_collection_interval: 45` setting

```yaml
init_config:

instances:
  - min_collection_interval: 45
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes, the only change required is in my_metric.yaml.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

I created the following yaml file to desribe the Timeboard:

```yaml
{
    "title" : "Kennon's Metrics",
    "widgets" : [{
       "definition": {
            "type": "query_value",
            "requests": [
                {
                    "q": "sum:my_metric{*}.rollup(sum, 3600)",
                    "aggregator" : "last"
                 }
            ],
            "title": "my_metric last hour",
            "autoscale": true,
            "precision": 1
        }
      },
      {
        "definition": {
            "type": "timeseries",
            "requests": [
                {"q": "sum:my_metric{*} by {host}"}
            ],
            "title": "Average my_metric"
        }
      },
      {
        "definition": {
            "type": "timeseries",
            "requests": [
                {"q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"}
            ],
            "title": "Postgres Connection Anomalies"
        }
      }
    ],
    "layout_type": "ordered",
    "description" : "A dashboard with memory info.",
    "is_read_only": true,
    "notify_list": ["kennon.kwok@gmail.com"]
}
```

Then using `curl`, I posted the json file to create the dashboard via the API.  `DD_APIKEY` and `DD_APPKEY` were exported into my environment before running the command.

```bash
$ curl  -X POST -H "Content-type: application/json" -d @kennons_metrics_new.json "https://api.datadoghq.com/api/v1/dashboard?api_key=${DD_APIKEY}&application_key=${DD_APPKEY}"
```

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

* Take a snapshot of this graph and use the @ notation to send it to yourself.

  ![Snapshot Email](<https://raw.githubusercontent.com/kennonkwok/hiring-engineers/solutions-engineer/images/snapshot_email.png>)


* **Bonus Question**: What is the Anomaly graph displaying?

  Anomaly detection uses algorithms to detect when a metric is behaving differently than it has in the past while taking in to account any temporal patterns. This anomaly graph is tracking the Postgres connection capacity.  At this point, any connections are an anomaly since the DB isn't being used.


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

  ![Monitor email](https://github.com/kennonkwok/hiring-engineers/raw/solutions-engineer/images/monitor_alert.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,

  * And one that silences it all day on Sat-Sun.

  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

    ![Downtime email](https://github.com/kennonkwok/hiring-engineers/raw/solutions-engineer/images/monitor_downtimes.png)

## Collecting APM Data:

Since I'm running on a Kubernetes cluster, I packaged the flask app using Docker with ddtrace-run as the CMD to start the app.  Then, in GKE, I set up a deployment, and a service to pull my image from docker hub and run it on my cluster and expose the service via a Google Cloud load balancer.  Additionally, I set up Datadog Synthetic checks to generate traffic to the api endpoints.

* **Bonus Question**: What is the difference between a Service and a Resource?

A service is the name of a set of processes that do the same job - in this case, flask in the service.
A resource is the particular action, in this case it's the API end points /, /api/trace, and /api/apm.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

![Infra+APM](https://github.com/kennonkwok/hiring-engineers/raw/solutions-engineer/images/infra_apm_screenboard.png)

Live Link: https://p.datadoghq.com/sb/31ca42880-55f38b67416dca871165b0cd3e48b62b

The Python app and Dockerfile are in the `flask-apm` directory. Kubernetes manifest in `manifests/flask-apm.yaml` and `manifests/flask-apm-service.yaml`

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

I run a lot of IoT components in my house - that would be an easy target and super useful for me.  Included in there would be weather/temperature monitors, power consumption, EV charging metrics, and BBQ!!