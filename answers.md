Your answers to the questions go here.


### Intro: Agent Set Up


Because the environment variables I set when creating the agent shaped my approach in building several of the features, I wanted to preface my responses by reviewing these customizations.  and I inc wanted to start by reviewing how these custom parameters


#### Agent Setup

I created an agent in a Docker container using the dockerized Datadog Agent image by running the following command:

```bash
docker run -d --name dd-agent
-p 8126:8126/tcp
-v /var/run/docker.sock:/var/run/docker.sock:ro  \
-v /proc/:/host/proc/:ro \
-v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
-v /Users/siobhanpmahoney/Development/take-home-assignments/datadog/hiring-engineers/SiobhanMahoneyAssignment/datadog-agent-conf.d:/conf.d:ro \
-v /Users/siobhanpmahoney/Development/take-home-assignments/datadog/hiring-engineers/SiobhanMahoneyAssignment/datadog-agent-checks.d:/checks.d:ro \
-e DD_APM_ENABLED=true \
-e DD_APM_NON_LOCAL_TRAFFIC=true \
-e DD_API_KEY=4dc7304832d0ab2d0d1048ab35c0b86f datadog/agent:latest \
```

The above command includes several environment variables in addition those included in the [Docker Agent one-step install instruction](https://app.datadoghq.com/account/settings#agent/docker) that I found to be helpful, if not necessary, in completing the assignment:

- Mounting directories:

```bash
-v [..]/datadog-agent-conf.d:/conf.d:ro
-v [..]/datadog-agent-checks.d:/checks.d:ro
```

The above commands mount YAML configuration files and Python files in the host's local `/conf.d` and `check.d` directories to the agent container, copying them the agent's `/etc/datadog-agent/conf.d/` and `/etc/datadog-agent/check.d/` directories when the container starts. By mounting these two directories, files can be created locally and accessed by the container — which proved helpful when writing the `my_metric` custom Agent check.

- Tracing-related: the following allowed for the agent to trace data from an application outside it's container:  

| Commmand | Description |
|-|-|
|`-p 8126:8126/tcp`|Enables tracing on port 8126/tcp from any host |
|`-e DD_APM_ENABLED=true`| Enables the trace-agent to run along with the infrastructure Agent, allowing the container to accept traces on `8126/tcp`|
|`-e DD_APM_NON_LOCAL_TRAFFIC=true`| Allows for non-local traffic when tracing from other containers |


#### Part 1: Collecting Metrics:


> 1. _Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog._

I accessed the Agent's config file (`datadog.yaml`) through the container's shell and running `vim`:

  ```bash
  docker exec -it dd-agent /bin/bash
  vim /etc/datadog-agent/datadog.yaml
   ```

I then added the `tag` property and a list of tags in a `<key>:<value>` format:

  <a href='./images/1.01-datadog.yaml-tag-screenshot.jpeg'><img src="Images/1.01-datadog.yaml-tag-screenshot.jpeg" width="500" height="332" alt="datadog.yaml-tag-code"></a>


I saved my changes and exited vim's edit mode by entering pressing `esc`, followed by `:wq`. I then exited the container's terminal (by running `exit`), and restarted the agent:

  * Restart your Datadog agent with the following command:

  ```sh
  docker container stop dd-agent
  docker container start dd-agent
  ```

  * Navigate to Host Map in your Datadog Dashboard and you should see the new tags listed:

  <a href='./images/1.01-datadog.yaml-tag-screenshot.jpeg'><img src="images/1.01-dashboard-tag-screenshot.jpeg" width="500" alt="datadog.yaml-tag-code"></a>


> 2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I selected PostgreSQL from the list of Integration options and followed directions the as summarized (with additional annotations) below:


* I created a read-only datadog user with proper access to your PostgreSQL Server by running the following command in a `psql` shell:

```sql
create user datadog with password <PASSWORD>;
grant SELECT ON pg_stat_database to datadog;
```

After exiting the `psql` shell, I confirmed that the permissions were set by running:

```sh
psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" && echo -e "\e[0;32mPostgres connection - OK\e[0m" || echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

* I created the `postgres.yaml` config file in the `/datadog-agent-conf.d/` local directory with the below contents. Because this directory is mounted to the container, it will be copied to the container's `conf.d` directory.

```yaml
init_config:

instances:
  - host: host.docker.internal
    port: 5432
    username: datadog
    password: <FILL IN>
```



* I then restarted the agent. To verify that Postgres had been successfully integrated, I ran the agent status command to make sure the `postgres` section under `Checks` did not include any errors.

```sh
docker container stop dd-agent
docker container start dd-agent
sudo docker exec -it dd-agent agent status
```

  <a href='./images/1.02-agent-db-check-screenshot.jpeg'><img src="images/1.02-agent-db-check-screenshot.jpeg" width="500" alt="datadog.yaml-tag-code"></a>




> 3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Creating a custom Agent check involves creating a config (YAML) file and corresponding check file Because the local `/datadog-agent-conf.d` and `/datadog-agent-checks.d` directories are mounted to the agent container, the necessary config and check files for `my_metric` can be created locally and stored in the respective directory.

  - `mymetric.yaml` code

    ```yaml
    init_config:

    instances: [{}]
    ```

  - `mymetric.py` code

    ```py
  try:
    from checks import AgentCheck
  except ImportError:
    from datadog_checks.checks import AgentCheck

    __version__ = "1.0.0"

    import random

    class HelloCheck(AgentCheck):
      def check(self, instance):
        self.gauge('my_metric', random.randint(1,1000))
  ```
  - dashboard // take screen shot after before adding back interval






> 4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

- process: updating `mymetric.yaml` by adding `min_collection_interval: 45`
- screenshots/visuals:
  - updated yaml file
  - screen shot of mymetric check status results
  - screen shot of mymetric dashboard graph

> 5. Bonus Question Can you change the collection interval without modifying the Python check file you created?



### II. Visualizing Data:

([ref](https://docs.datadoghq.com/graphing/graphing_json))

Utilize the Datadog API to create a Timeboard that contains:

> _1. Your custom metric scoped over your host._

  <a href='./images/2.01-timeboard_graph1_my_metric.jpeg'><img src="images/2.01-timeboard_graph1_my_metric.jpeg" width="500" alt="datadog.yaml-tag-code"></a>

> _2. Any metric from the Integration on your Database with the anomaly function applied._

  <a href='./images/2.02-timeboard_graph2_postgres_metric.jpeg'><img src="images/2.02-timeboard_graph2_postgres_metric.jpeg" width="500" alt="datadog.yaml-tag-code"></a>

> _3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket._

  <a href='./images/2.03-timeboard_graph3_my_metric_anomaly.jpeg'><img src="images/2.03-timeboard_graph3_my_metric_anomaly.jpeg" width="500" alt="datadog.yaml-tag-code"></a>

> _4. Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard._

Once this is created, access the Dashboard from your Dashboard List in the UI:

> _5. Set the Timeboard's timeframe to the past 5 minutes_

<a href='./images/2.05-timeboard-5min.jpeg'><img src="images/2.05-timeboard-5min.jpeg" width="500" alt="datadog.yaml-tag-code"></a>


> _6. Take a snapshot of this graph and use the @ notation to send it to yourself._

<a href='./images/2.06-timeboard-email.jpeg'><img src="images/2.06-timeboard-email.jpeg" width="500" alt="datadog.yaml-tag-code"></a>


> _Bonus Question: What is the Anomaly graph displaying?_


 #### III. Monitoring Data

> *1. Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:*
> - Warning threshold of 500
> - Alerting threshold of 800
> - And also ensure that it will notify you if there is No Data for this query over the past 10m.

I configured a Metric alert using the [Create Monitor](https://app.datadoghq.com/monitors#/create) tool to  meet the conditions described above:




> _2. Please configure the monitor’s message so that it will_:
  > - _Send you an email whenever the monitor triggers.
  > - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
  > - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state._

I created distinct content for each of the alert, warning, and no data notification types within the same message using Datadog's tag notation:

-----
  __{{#is_alert}}__
  `my_metric`  ALERT In the past 5 minutes,  the values produced by `my_metric` averaged at {{value}}, surpassing  the alert threshold of 800. @siobhan.p.mahoney@gmail.com

  Host Info:
  name: {{host.name}}
  ip: {{host.ip}}
  __{{/is_alert}}__


  __{{#is_warning}}__
  `my_metric` WARNING:  In the past 5 minutes,  the values produced by `my_metric` averaged at {{value}}, surpassing  the warning threshold of 500

  @siobhan.p.mahoney@gmail.com  
  __{{/is_warning}}__



  __{{#is_no_data}}__
  NOTIFICATION: `my_metric` produced no data in the past 10 minutes.
  @siobhan.p.mahoney@gmail.com  
  __{{/is_no_data}}__
-----


> _When this monitor sends you an email notification, take a screenshot of the email that it sends you._

<a href='./images/3.02-my_metric-monitor-alert-notification-email.jpeg'><img src="images/3.02-my_metric-monitor-alert-notification-email.jpeg" width="500" alt="datadog.yaml-tag-code"></a>



#### Collecting APM Data:

Here's an overview of the steps I took to implement the collection of APM data:

1. I began by configuring my agent for trace collection by updating `datadog.yaml` (located in the agent container's `/etc/datadog-agent/datadog.yaml` directory) by adding the `apm_config` key and parameters:

```yaml
listeners:
  - name: docker
config_providers:
  - name: docker
    polling: true
tags:
  - env:production
  - app:web
  - version:1

apm_config:
  enabled: true # enables collection of tracing data
  apm_non_local_traffic: true # enables agent to collect tracing data outside of the docker container
  receiver_port: 8126 # sets port that agent trace receiver listen on.
  analyzed_spans: #make available in trace searches
    flask|flask.request: 1

```
2. I next built a Python app outside of the agent container, which involved:
  - Installing the necessary packages, including:
    - __Flask__ web framework (`pip install flask`)
    - __ddtrace__ library, which will connect the application to our agent, enabling the application to be traced (`pip install ddtrace`)
  - Retrieved the agent's hostname by running `hostname -I` in the agent container's shell
  - Saved the app code provided in the assignment's ReadMe file with the following line:

    ```py
    tracer.configure(hostname='172.17.0.2', port=8126)
    ```

    Here, the application's default ddtrace.tracer object is modified to use the agent's hostname and port, the agent to collect trace data.
3. I then ran the app by prepending `dd-trace` to the run command:

  ```sh
  ddtrace-run python FlaskApp/flaskapp.py
  ```

Once the app was up and running, the tracing data will be available to view in the Datadog platform, both in the host's main infrastructure map and under the APM tab, which offers visuals for the collected data at both the app (or __service__) and individual route (or __resource__) levels:


_Infrastructure Map_:
<a href='./images/4.01-infrastructure-map-with-tracing.jpeg'><img src="images/4.01-infrastructure-map-with-tracing.jpeg" width="500" alt="04.01"></a>


_APM Tab — Service View:_

<a href='./images/4.02.1-trace-data-service.jpeg'><img src="images/4.02.1-trace-data-service.jpeg" width="500" alt="04.01"></a>

_APM Tab — `/get` Resource View:_

<a href='./images/4.02.2-trace-data-resource.jpeg'><img src="images/4.02.2-trace-data-resource.jpeg" width="500" alt="04.01"></a>


> _Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics_.

I created a dashboard titled 'APM + Infrastructure Metrics', which includes clones of the host's top host-level metrics and the Flask Application's Latency on Service data:

[APM + Infrastructure Metrics Dashboard Link](https://app.datadoghq.com/dash/1026232/apm--infrastructure-metrics?tile_size=m&page=0&is_auto=false&from_ts=1545264540000&to_ts=1545268140000&live=true)
<a href='./images/4.03-APM-infrastructure-metric-dashboard.jpeg'><img src="images/4.03-APM-infrastructure-metric-dashboard.jpeg" width="500" alt="04.01"></a>

> _Please include your fully instrumented app in your submission, as well_.
