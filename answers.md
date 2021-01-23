# DataDog Solutions Engineering Technical Exercise

## Foreword

I wanted to provide a brief foreword about my experience with this process and share how excited I am as a result of working through this challenge.  I felt that this challenge had excellent breadth and it pushed me to learn a few new things while also getting to experience some of the phenomenal depth that DataDog has to offer.  

***

## Prerequisites - Setup the environment

For my agent, I opted to configure the recommended linux VM using Vagrant as per the instructions provided.  The mcahine is running Ubuntu-18.04.  Once spun up, I followed the one-step instructions provided [here](https://app.datadoghq.com/account/settings#agent/ubuntu) to install the agent.

To validate that the installation was online and functioning properly I followed the commands documented [here](https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7) to execute the following:

    $ sudo datadog-agent status

***

## Collecting Metrics

Once the agent was installed and validated, I went about configuring metric collection.

**Question 1: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

To add tags, I modified to the `datadog.yaml` configuration file at `/etc/datadog-agent` to include tags for envirionment and for project. In the `@params tags` section, I included the following:

    tags:
        - envrionment:sandbox
        - project:se_hiring_example

As per the docs [here](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments) I could have similarly constructed my tags as `tags: ["envrionment:sandbox", "proejct:se_hiring_example"]` but opted for the longer list for ease of readability.

I then saved the file, waited a few minutes for the environment to update, and navigated to Infrastructure > Hostmap to see the following:

![Host Map with tags](screenshots/host_map.PNG "Host Map with Tags")


**Question 2: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

For the database, I opted to install a PostgreSQL database and then proceeded to follow the instructions under Indegrations > PostgreSQL found [here](https://app.datadoghq.com/account/settings#integrations/postgres). This required creating a datadog user with grants for `pg_montior` and `SELECT ON pg_stat_database` as per:

    > create user datadog with password 'dogspeed';
      grant pg_monitor to datadog;
      grant SELECT ON pg_stat_database to datadog;

I then verified the permissions by running:

    $ psql -h localhost -U datadog postgres -c \
    "slect * from pg_stat_database LIMIT(1);" \
    && echo -e "\e[0;32mPostgres connection - OK\e[0m" \
    || echo -e "\e[0;31mCannot connect to Postgres\e[0m"

Lastly, I enabled metric collection by creating the `conf.yaml` at `/etc/datadog-agent/conf.d/postgres.d/` as follows:

    init_config:

    instances:
        - server: localhost
          port: 5432
          username: datadog
          password: dogspeed

Once completed, I restarted my agent to apply the new configuration and begin collecting metrics.  I was then able view the newly available metrics found under Metrics > Explorer as seen below:

![Postgresql Metrics available under Metrics > Explorer](screenshots/metrics.PNG "Metrics available under Metrics > Explorer")

**Question 3: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

To create a custom agent check, I followed the instructions found in the article [Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) and modified the example provided.

In the folder `/etc/datadog-agent/checks.d/` I created a custom check `custom_my_metric.py` with the following:

    import random                                                                                                                                                
    try:
        from datadog_checks.base import AgentCheck
    except ImportError:
        from checks import AgentCheck

    __version__ = "1.0.0"

    class MyMetricCheck(AgentCheck):
        def check(self, instance):
        # Since we are generating a single random variable, gauge is used for submitting one value                      
        self.gauge('my_metric', random.random()*1000, tags=['metric_submission_type:gauge','env:sandbox', 'project:se_hiring_example'])   

 I noticed in another example provided by the article [Metric Submission: Custom Agent Check](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count) that the tags `env` and `metric_submission_type` were included, so I also included those along with the `project` tag from my previous tagging example to provide more meaningful metadata.

 In the folder `/etc/datadog-agent/conf.d/` I created the configuration for the my custom check in `custom_my_metric.yaml` with the following:

    init_config:

    instances: [{}]

Once completed, I restarte the agent and validated that I saw `my_metric` reporting under Metrics > Explorer as seen below:

![my_metric reporting](screenshots/my_metric.PNG "my_metric reporting under Metrics > Explorer")

**Question 4: Change your check's collection interval so that it only submits the metric once every 45 seconds.**

To change the `min_collection_interval` so that it only submits every 45 seconds, I followed the instructions found in the previously linked article **Writing a Custom Agent Check** by modifying our config file found at `/etc/datadog-agent/conf.d/custom_my_metric.yaml` to be the follow:

    init_config:

    instances:
        - min_collection_inerval: 45

**Bonus Question: Can you change the collection interval without modifying the Python check file you created?**

Yes, I opted to set the `min_collection_interval` in the configuration file instead of in the check file.

***

## Visualizing Data

Now that I've have created some metrics, it is time to start visualizing those metrics for continuous monitoring and explorability.

**Question 1: Utilize the Datadog API to create a Tiemboard to accomplish the following sub-tasks**

As a note, I originally searched for a Timeboard API and noticed in the documentation found [here](https://docs.datadoghq.com/dashboards/guide/timeboard-api-doc/?tab=python) that this endpoint was outdated and followed the instructions to instead use the Dashboard endpoint as part of the Datadog API found [here](https://docs.datadoghq.com/api/latest/dashboards/).

To accomplish the tasks in **Question 1** and **Question 2** the code snippets found under [`\code\create_dashboard.py`]()

As per the Dashboard enpoint docs linked above, I first went about accquire my API Key and my App Key found under Integrations > APIs so that I could define them under the `options` object. I then setup a basic script from the code example provided in the docs as a shell for me to define visualizations for the next 3 sections.

**Question 1.1: Show your custom metric scoped over your host.**

For starters, I learned that all dashboards are comprised of widgets which are effectively individual charts.  There are a variety of types of widgets as documented [here](https://docs.datadoghq.com/dashboards/widgets/) which can present metrics in variety of visualization types in a dashboard.

For my first widget on `my_metric`, I chose a timeseries as the data provided by the custom check gauge function sends a single data-point every 45 seconds.  To do so, I defined my widget with the provided JSON schema as follows:

    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            # q provides the basic query for a particular metric following the schema <METRIC>{HOST:<HOST>}
            # in this case, since we have multiple agents present, this is scoped over the host:vagrant
            {'q': 'my_metric{host:vagrant}'}
        ],
        'title': 'My Metric'
        }
    }

As a note: I scoped the query over my `{host:vagrant}` since I had expermineted in previous sections with configuring the agent on my local desktop.  Although not strictly neccessary, this was done for all subsequent sectiosn for readability and consistency.  

This object was included in the `widgets` list which I submitted through the method `api.Dashboard.create()` along with a the following other paramaters:

    title = 'SE Hiring Example Dashboard'
    description = 'A dashboard used to illustrate the Dashboard enpoint in the Datadog API.'
    is_read_only = False
    layout_type = 'ordered'

**Question 1.2: Show any metric from the Integration on your Database with the anomaly function applied.**

Since my PostgreSQL database wasn't in production and many of the metrics either reported no data, or the same value, I opted to use the metric `postgresql.max_connections` and followed the documentation found under the [Algorithms](https://docs.datadoghq.com/dashboards/functions/algorithms/) article for the `anomalies()` function.  I again chose the timeseries widget for this as I wanted to produce the anomaly banding over time.  The schema for this widget is as follows:

    {
        'definition': {
        'type': 'timeseries',
        'requests': [
            # anomalies function with the params METRIC_NAME{*}, '<ALGORITHM>', <BOUNDS>
            # in this case we are performing an anomly analysis over our postgresql.max_connections metric 
            # with the basic algorithm with a deviation of 3
            {'q': "anomalies(postgresql.max_connections{host:vagrant}, 'basic', 3)"}
        ],
        'title': 'Max Connections Anomolies'
        }
    }

**Question 1.3: Show your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket**

To apply a rollup function, I followed the documentation initially on [Arithemtic Functions](https://docs.datadoghq.com/dashboards/functions/arithmetic/) which led me to dosc for the [Rollup Function](https://docs.datadoghq.com/dashboards/functions/rollup/).  This time, since we were just producing a final rollup number, I opted to use the [`query_value`](https://docs.datadoghq.com/dashboards/widgets/query_value/) widget to present the final roll-up value produced for the past hour.  The schema for this widget is as follows:

    {
        'definition': {
        'type': 'query_value',
        'requests': [
            # the rollup() function is appended to the end of our query with parameters <METHOD>, <TIME>
            # in this case, we are performing a sum over the time period of 3600 seconds (1 hour)
            {'q': 'my_metric{host:vagrant}.rollup(sum, 3600)'}
        ],
        'title': 'My Metric'
        }
    }


After performing sub-setps 1-3, the [final dashboard](https://p.datadoghq.com/sb/7my7we8zuethfnx9-db6234b107a2374c39d85644a3344e69) I produced looks like this:

![Final Dashboard](screenshots/dashboard.PNG "Final Dashboard")

> **Note:** in addition to my script `dashboard.py` found in `/hiring-engineers/code` there is a script `clear_dashboards.py` which I used as a convenience when testing a variety of dashboard widgets. 

**Question 2: Once this is created, access the Dashboard from your Dashboard List in the UI and perform the following tasks:**

For the following questions, I navigated to Dashboards > Dashboard List > SE Hiring Example in the UI.

**Question 2.1: Set the Timeboard's timeframe to the past 5 minutes**

In the top-right of my dashboard, I selected the timeframe and changed it to "Past 5 Minutes" to produce the following: 

![Timeframe updated to 5-min](screenshots/timeframe.PNG "Timeframe updated to 5-min")

As a note, since the Query Value widget is set to a 1-hour roll-up, no data is present since there isn't a 1-hour roll-up window present for a 5-minute window.

**Question 2.2:Take a snapshot of this graph and use the @ notation to send it to yourself.**

I opted to take a snapshot of the My Metric widget showing `my_metric` graphed over a timeseries since I was unable to take a snapshot of the full dashboard and it shared a more interesting set of data.  I optionally could have created a URL for the dashboard and shared it with my user account by navigating to the Dashboard Settings > Configure Sharing and selected "Only specified people" with my user account specified.  

Below are screenshots of me making the snapshot and the email I received with the snapshot of the data:

**Creation:**

![Snapshot Dialog](screenshots/snapshot_dialog.PNG "Snapshot Dialog")

**Receiving:**

![Snapshot Email](screenshots/snapshot_email.png "Snapshot Email")

**Bonues Question: What is the Anomaly graph displaying?**

The anomaly graph  in my dashboard is showing a band of expected values with an expected standard deviation to help spot outlier datapoints more easily. I am using the basic algorithm which, as per the docs, is performing a simple lagging rolling quartile computation with a small window of the data.  For the purpose of creating basic anomaly detection on a non-production metrics as part of testing the Dashboard API, this algorithm works fine.  However, the Agile or Robust algorithms might be preferrable in production take into account level shifts, long term anomalies, and seasonal trends in the data.

***

## Monitoring Data

Naturally, now that I have produced some metrics and a dashboard to get real time insights on key performance metrics, it makes sense to create monitors to provide alerting for when I'm not watching these metrics/dashboards.  

**Question 1: Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:**

- **Warning threshold of 500**
- **Alerting threshold of 800**
- **And also ensure that it will notify you if there is No Data for this query over the past 10m**

Monitors are actually quite easy to configure using the UI.  To do so, I navigated to Monitors > New Monitors and selected the option for Metrics. Below is a screenshot of the configuration I used to achieved the needed requirements:

![my_metric Monitor](screenshots/Monitor.png "my_metric Monitor")

**Question 2: Please configure the monitor’s message so that it will do the following:**
- Send you an email whenever the monitor triggers.
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state
- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
- When this monitor sends you an email notification, take a screenshot of the email that it sends you.

To accomplish the conditional notifications based upon the value of `my_metric` over the 5 minute window, I followed the [Notifications](https://docs.datadoghq.com/monitors/notifications) docs and produced the following message with conditional formatting:

    Environment: {{host.name}}
    IP: {{host.ip}}

    Details:

    {{#is_alert}}
    my_metric has averaged above the threshold of {{threshold}} with a value of {{value}} for at least 5 minutes, please take immediate action.
    {{/is_alert}} 

    {{#is_warning}}
    my_metric has averaged above the threshold of {{warn_threshold}} with a value of {{value}} for at least 5 minutes, please review to ensure optimal performance.
    {{/is_warning}} 

    {{#is_no_data}}
    my_metric has not reported data in the past 10 minutes.  Please check if the service is still online.
    {{/is_no_data}} 

    For more details, please refer to the my_metric dashboard to dive into other causes.

     @etroberts@tableau.com

As a result, the monitor produces the following 3 conditional alert states:

1. **Alert threshold:**

![Alert threshold message](screenshots/monitor_alert.png "Alert threshold message")

2. **Warning thershold:**

![Warning threshold message](screenshots/monitor_warning.png "Warning threshold message")

3. **No data threshold:**

![No data threshold message](screenshots/monitor_no_data.png "no data threshold message")

**Bonus Question:** Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
- One that silences it from 7pm to 9am daily on M-F

To schedule downtime, I navigated to Monitors > Manage Downtime in the UI and selected the option to "Schedule Downtime."  I then configured this downtime with the following:

![Weeknight donwtime](screenshots/downtime_1.PNG "Weeknight downtime")

- And one that silences it all day on Sat-Sun.

For this downtime, I similarly created another scheduled downtime with the following configuration:

![Weekend downtime](screenshots/downtime_2.png "Weekend downtime")

- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

In both screenshots at the bottom, I have included myself in the section "4. Notify your team" and as a result received the following emails:

**Weeknight downtime**

![Weeknight donwtime](screenshots/weeknight_downtime.png "Weeknight downtime")

**Weekend downtime**

![Weekend donwtime](screenshots/weekend_downtime.png "Weekend downtime")

***

## Collecitng APM Data

For this section, the aim is to implement the [Datadog APM solution](https://docs.datadoghq.com/tracing/) to istrument the provided flask app.  Since this is written in Python, I followed the recommended [python quickstart guide](https://app.datadoghq.com/apm/docs?architecture=host-based&language=python) that was recommended by the [APM docs](https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers).  I went ahead and prepared my environment for the Flask app by installing Flask and creating `flask-app.py` with the provided code.

The first thing I did to instrument my app was follow the instructuions to install ddtrace with:

    $pip install ddtrace

I then used the provided configuration snippet generator to produce the following command to start my app:

    $ DD_SERVICE="flask-app" DD_ENV="sandbox" DD_LOGS_INJECTION=true DD_TRACE_SAMPLE_RATE="1" DD_PROFILING_ENABLED=true ddtrace-run python flask-app.py

Since this provides the bare minimum for APM instrumentation, I opted to dig into some of the suggested further reading for [Python Runtime Metrics](https://docs.datadoghq.com/tracing/runtime_metrics/python/) and modified my startup command to include the following:

    DD_RUNTIME_METRICS_ENABLED=true

This enabled me to access a wider swath of system-level metrics on the run-time performance of my application as requests came in.  

After starting my applicaition and validating that I was indeeed getting metrics like `runtime.python.cpui.percent`, I continued to dive deeper into the possibilities of instrumenation and stumbled across an article covering [Python Custom Instrumentation](https://docs.datadoghq.com/tracing/setup_overview/custom_instrumentation/python/?tab=decorator) to allow me to define traces for specific endpoints of my flask app.  In addition to the out-of-the box tracing functionality, this allowed me to define specific endpoint-level tracing for the two endpoints provided in the app: `/api/apm` and `/api/trace`. I did so by declaring the following:

    @app.route('/api/apm')
    @tracer.wrap('flask-request', service='flask-app', resource='APM', span_type='web')
    def apm_endpoint():
        return 'Getting APM Started'

    @app.route('/api/trace')
    @tracer.wrap('flask-request', service='flask-app', resource='TRACE', span_type='web')
    def trace_endpoint():
        return 'Posting Traces'


Now that I have instrumented my application for system-level and endpopint-level traces, I was able to pull together a dashboard of APM and Infrasturcture metrics as seen [here](https://p.datadoghq.com/sb/7my7we8zuethfnx9-c3c64a55e5c789c6542a6fa97fdc34c8) or below:

![APM/System Dashboard](screenshots/apm_dash.PNG "APM/System Dashobard")

***

## Final Quesiton

**Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!**

**Is there anything creative you would use Datadog for?**

In my time as an SE at Tableau, I wrote a custome Node.js application which embedded an SE time-tracking dashboard and enabled the end user to quickly and conveniently create a Salesforce record for logging their customer-facing time with meeting details, notes, stakeholders, etc.  This application grew quickly in popularity amongst the SEs and is currently deployed to over 800 SEs globally. 

 While this app has certainly served a its purpose, it is architected around 3 different APIs with its own internal API service and a data visualization piece to boot.  With all of this infrastructure, it'd be excellent to apply Datadog for continuous monitoring and detailed traces for when things go wrong.  As it stands today, I am only made aware of downtime or unexpected behavior from interacting with end users over Slack.  Even with this level of reporting, I only get as much information about what wrong as the end user provides (often times getting little to no system-level details).  Not only would Datadog's platform help me keep a pulse on the status of the system and its various components, it would enable me to dive into specific end-user issues at a system level quickly and easily to identify the problem. Additionally, I could enable my end users with real time updates on service availability and performance to reduce the amount of messages I receive overall.