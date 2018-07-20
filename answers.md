# Datadog Solutions Engineer Technical Exercise: Answers

###### Name: Sondhayni Murmu
###### Username: [smurmus](https://github.com/smurmus)

###### *Notes:*
- Each section of the hiring exercise has been listed below in order with their respective headers.
- All scripts and external articles/documentation are hyperlinked
- Some scripts have been embedded, but they can all be found in full in the `/scripts` folder
- Screenshots are shown in sequence below, but can also be found at `<hiring_exercise_section>/<img_name>.png` (e.g. `Collecting-Metrics/datadog-my-metric.png`)

## PREREQUISITES/SETUP:

I spun a fresh linux VM via vagrant (so I would be using Ubuntu 16.04) using its set up [documentation](https://www.vagrantup.com/intro/getting-started/index.html):

![vagrant installation](./Prereqs/vagrant-setup.png?raw=true "Vagrant Setup")

Then, completed my sign up for Datadog, installed the agent on Ubuntu, and set up the config file via the instructions provided on the integrations page:

![datadog agent installation](./Prereqs/ubuntu-datadog-install.png?raw=true "Datadog Agent Setup")

## COLLECTING METRICS:

### Adding Tags:

I added some tags to the Agent [config file](./scripts/datadog.yaml) located at `/etc/datadog-agent/datadog.yaml`:

      tags: sondhayni, key-test:key-value, sondhayni-ubuntu-test


It took a couple of restarts, but eventually the tags appeared on the Host Map page in Datadog as well:

![datadog hostmap with tags](./Collecting-Metrics/ubuntu-hostmap-tags.png?raw=true "Datadog Hostmap Tags")

### Installing MySQL:

I chose to use MySQL. I installed it on to my VM following [these instructions](https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/).

Following the [Datadog docs](https://docs.datadoghq.com/integrations/mysql/#prepare-mysql), upon installing MySQL, I created a `datadog@localhost` user and granted it the appropriate permissions:

![create datadog user](./Collecting-Metrics/ubuntu-create-datadog-user.png?raw=true "Create Datadog User")


I then set up a MySQL [config file](./scripts/mysql.yaml) at `/etc/datadog-agent/conf.d/mysql.yaml`:

      init_config:

        instances:
          - server: localhost
            user: datadog
            pass: passdd
            tags:
              - smurmu-ubuntu-tag-1
              - smurmu-ubuntu-tag-2
          options:
            replication: 0
            galera_cluster: 1
            extra_status_metrics: true
            extra_performance_metrics: true


I ensured that MySQL was integrated/installed correctly by running a `sudo datadog-agent status` which showed:

![mysql agent check](./Collecting-Metrics/ubuntu-mysql-passes-checks.png?raw=true "MySQL Datadog Integration Successful")

### Custom Metric/Agent Check:

I consulted the Datadog docs about the options for [custom metrics](https://docs.datadoghq.com/developers/metrics/) as well as the example provided in the docs for [custom agent checks](https://docs.datadoghq.com/developers/agent_checks/). Following the example, I created two files for `my_metric`.

[my_metric_check.py](./scripts/my_metric_check.py) (in  `/etc/datadog-agent/checks.d/`):

    from checks import AgentCheck

    import random

    class RandVal(AgentCheck):
      def check(self, instance):
        self.gauge('my_metric', random.randint(0,1001))


[my_metric_check.yaml](./scripts/my_metric_check.yaml) (in `/etc/datadog-agent/conf.d`).

    init_config:

    instances:
     [{}]

To ensure it was running properly, I first ran a `sudo datadog-agent status` check:

![my_metric terminal](./Collecting-Metrics/ubuntu-my-metric-check.png?raw=true "my_metric terminal check")

Then, I looked at the timeseries graph in my Metrics Explorer:

![my_metric timeseries](./Collecting-Metrics/datadog-my-metric.png?raw=true "Datadog Metrics Explorer")

*[The long line in the center is from the downtime of when my laptop was off, so metrics weren't being collected.]*

#### Changing Collection Intervals

In order to modify the collection interval, I simply modifed `my_metric_check.yaml` to account for a 45 second interval:

      init_config:

      instances:
       -  min_collection_interval: 45

On Datadog, the timeseries now looked like this:

![my_metric 45s collection interval](./Collecting-Metrics/datadog-my-metric-45.png?raw=true "Datadog my_metric 45s timeseries")

#### Bonus Question: *Can you change the collection interval without modifying the Python check file you created?*

Yes. Setting the collection interval in the first place did not require any changes to the Python check file; changing the interval would require updating the `min_collection_interval` value found in the related config file.

## VISUALIZING DATA

### Utilizing Datadog API:

In order to create a Timeboard that contained the requested metrics, which were:

- Your custom metric scoped over your host.
- Any metric from the Integration on your Database with the anomaly function applied.
- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

[*The other metric I chose besides the custom `my_metric` was `mysql.performance.cpu_time` since that would have data without my having to run queries.*]

I consulted the [API documentation](https://docs.datadoghq.com/api/?lang=python#timeboards) for options and examples.

For the use of special functions, I looked at the articles about available [functions](https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup) and [anomalies](https://docs.datadoghq.com/monitors/monitor_types/anomaly/). I also used the Web UI graph creator within a Timeboard to make sure my request syntax was correct, by selecting metrics and functions and looking at their JSON representation:

![datadog timeboard creator ui](./Visualizing-Data/datadog-timeboard-ui.png?raw=true "Datadog Timeboard Graph UI")

After creating an app key and finding my api key from the integrations page, I had to make sure to install the dependencies with `sudo apt-get install datadog`.

The final script, [create_timeboard.py](./scripts/create_timeboard.py) which was located at `/etc/datadog-agent/`, looked like this:

    from datadog import initialize, api

    options = {
      'api_key': '********************************',
      'app_key': '***************************************'
    }

    initialize(**options)

    title = "Visualizing Data Timeboard"
    description = "Timeboard containing three metrics for the Hiring Solutions Engineer Exercise"
    graphs = [{
       "definition": {
           "events": [],
           "requests": [{"q":"avg:my_metric{host:ubuntu-xenial}"}],
           "viz": "timeseries"
       },
       "title": "my_metric vs time" },
       {
       "definition": {
           "events": [],
           "requests": [{"q":"anomalies(avg:mysql.performance.cpu_time{host:ubuntu-xenial},'basic', 3)"}],
           "viz": "timeseries"
       },
       "title": "Anomaly function applied to mysql.performance.cpu_time vs time" },
       {
       "definition": {
           "events": [],
           "requests": [{"q":"avg:my_metric{host:ubuntu-xenial}.rollup(avg, 120)"}],
           "viz": "timeseries"
       },
       "title": "Rollup function applied to my_metric vs time"
    }]

    template_variables = [{
       "name":"ubuntu-xenial",
       "prefix": "host",
       "default": "host:ubuntu-xenial"
    }]

    read_only = True

    api.Timeboard.create(title=title,
                         description=description,
                         graphs=graphs,
                         template_variables=template_variables,
                         read_only=read_only)

On Datadog, the dashboard looked like this:

![datadog timeboard from api](./Visualizing-Data/datadog-viz-timeboard.png?raw=true "Datadog Timeboard from API")

### Utilizing Dashboard UI:

To set the Timeboard's timeframe to the past five minutes, I clicked and dragged over a span of what represented five minutes across the x-axis on one of the graphs. All of the graphs in the Timeboard then updated to have the same timeframe.

![datadog timeboard ui timeframe changed](./Visualizing-Data/datadog-viz-timeboard-5m.png?raw=true "Datadog Timeboard UI 5m Timeframe")

In order to send a notification of a graph (since the instructions did not specify, I chose the `mysql.performance.cpu_time` metric graph), I hovered over it and a camera icon appeared in its header, which takes a snapshot. I could then comment on it and tag someone:

![datadog graph snapshot](./Visualizing-Data/datadog-graph-snapshot.png?raw=true "Datadog Graph Snapshot")

This notification/comment then showed up both in the event stream, and also in an email I received:

![datadog graph email notif](./Visualizing-Data/datadog-graph-notif.png?raw=true "Datadog Graph Email Notification")

#### Bonus Question: *What is the Anomaly graph displaying?* ####

The anomaly graph displays the normal values metric of mysql.performance.cpu_time over time, but with a background band that predicts and shows the normal range of values/data based on past trends. Any discrepancies in data that occur are shown as points outside this band, and in a different color from the rest of the "normal flow" of the data in the graph.

## MONITORING DATA

### Creating a New Metric Monitor

I utilized the UI in order to create a new metric monitor with the given requirements:

- Warning threshold of 500 (over the past 5m)
- Alerting threshold of 800 (over the past 5m)
- Ensure that it will notify you if there is No Data for this query over the past 10m.

The UI was straightforward to use for basic setup of sending notifications at these threshold points.

In order to configure the monitor messages for each type of status, I consulted the docs regarding template variables and [conditional variables](https://docs.datadoghq.com/monitors/notifications/#conditional). After creation, I can see the properties I created it with under 'Manage Monitors' in the Datadog UI:

![datadog monitor properties](./Monitoring-Data/datadog-monitor.png?raw=true "Datadog Monitor Properties")

As the alert happens pretty often, I received several email notifications to this effect:

![datadog monitor alert email](./Monitoring-Data/datadog-monitor-alert-email.png?raw=true "Datadog Monitor Alert Email")

#### Bonus Question: *Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor.* ####

The first requested downtime (to silence it from 7pm to 9am daily M-F) looks as follows:

![datadog monitor weekday downtime](./Monitoring-Data/datadog-monitor-downtime-weekday.png?raw=true "Datadog Monitor Downtime - Weekday")

And the second requested downtime (to silence it all day Sat-Sun) looks like this:

![datadog monitor weekend downtime](./Monitoring-Data/datadog-monitor-downtime-weekend.png?raw=true "Datadog Monitor Downtime - Weekend")

Whenever downtime is scheduled, I receive an email notification that looks like this:

![datadog scheduled downtime notification](./Monitoring-Data/datadog-scheduled-downtime.png?raw=true "Datadog Scheduled Downtime Email Notif")

>*Note: The times were set up correctly as you can see from the Datadog UI screenshot, but the email seems to display PDT times instead of EDT (i.e. 11pm - 1pm instead of 7pm - 9am). However, the notification email is actually sent at the correct time as you can see here (at the top right):*

>![datadog email timestamp](./Monitoring-Data/datadog-time-stamp.png?raw=true "Datadog Email Timestamp")

## COLLECTING APM DATA

In order to instrument the provided Flask app, I chose Python.

### Setting up Python

To set it up, I first had to run `sudo apt-get install python-pip` so I would have access to other relevant downloads. Then, I followed along with the Datadog docs about [tracing Python](https://docs.datadoghq.com/tracing/setup/python/).

This required a few simple pip installs:

- `sudo pip install ddtrace`
- `sudo pip install blinker`

### Instrumenting Flask App in Python

Afterwards, I turned the provided app into [apm_flaskapp.py](./scripts/apm_flaskapp.py) which was located in `/etc/datadog-agent`. At first, I tried to run the app and it didn't work, until I realized I had to make sure I was using the right host/port, so I changed the values in one line towards the end. I modified the host and port from `0.0.0.0:5050` to `127.0.0.1:8080` respectively:

      if __name__ == '__main__':
          app.run(host='127.0.0.1', port='8080')

I chose to run ddtrace rather than inserting Middleware, based on the [Python Datadog Trace documentation](http://pypi.datadoghq.com/trace/docs/#):

![ubuntu flask app running](./Collecting-APM/ubuntu-flask-app-run.png?raw=true "Ubuntu run ddtrace")

To check whether the endpoints were being hit, I ran some queries with `curl` which gave the expected output:

![ubuntu flask app curl](./Collecting-APM/ubuntu-flask-app-curl.png?raw=true "Ubuntu run ddtrace curl")

### Viewing APM Metrics on Datadog UI

Then, I went back to Datadog and saw my traces now being collected from this flask app:

![datadog flask app service](./Collecting-APM/datadog-flask-service.png?raw=true "Datadog APM Flask Service")

![datadog flask app](./Collecting-APM/datadog-apm-trace-graphs.png?raw=true "Datadog APM Trace Metrics")

### Creating a Dashboard with APM + Infrastructure Metrics

In order to make the final Dashboard, I went to create a Screenboard (so that it could be publicly shared). The infrastructure metrics were straightforward to add, since those were the same as the timeseries graphs I had created earlier.

To ensure I was correctly querying APM Metrics, I went to "edit" the *Total Requests* graph from the Flask app in the APM tab. This showed me the right options for the metrics I needed to add:

![datadog flask app graph metrics](./Collecting-APM/datadog-apm-metrics-edit.png?raw=true "Datadog APM Trace Metrics")

Using that information, I proceeded to create a [ dashboard](https://p.datadoghq.com/sb/28675d3e2-7a35ae1480cfa921d37dda515c8c821c) with both APM and Infrastructure Metrics:

![datadog apm and infra metrics](./Collecting-APM/datadog-APM-infra-metrics-board.png?raw=true "Datadog APM and Infra Metrics Dash")

#### Bonus Question: *What is the difference between a Service and a Resource?* ####

A service is a set of processes that contribute to a feature set (for example: in a web app, services include a `webapp` and `database` service), while a resource is a specific query *related to* a service.<sup>1</sup>

<sup>1</sup> Reference: [What is the Difference Between "Type", "Service", "Resource", and "Name"?](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-)

## FINAL QUESTION:
### *Is there anything creative you would use Datadog for?* ####

After reading through some of the blog posts I found online (the *Pokemon Go* article was fun in particular), I think I'd use it for something in the same vein. I'm not personally a streamer, but I follow a handful of them on Twitch.

I think it'd be interesting to use data created in some kind of app via the Twitch API to monitor certain metrics that are maybe specific to certain games/streaming regions/etc. These metrics could include the load/frequency of chatbot use, current user load/counts, and how users/the network reacts to actions that are available within the Twitch API.

I haven't personally used it (only skimmed the [documentation](https://dev.twitch.tv/docs/)), but it's possible to create all sorts of apps from it that could let streamers or gamers (who do the dev work) to better gauge something like their engagement.  
