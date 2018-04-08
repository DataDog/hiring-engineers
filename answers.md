# [TODO: TOC]


## Prerequisites: Setup the environment
We've setup a t2.micro EC2 instance from the official CentOS Linux 7 AMI, and installed Docker CE with yum following Docker CentOS install documentation:

https://docs.docker.com/install/linux/docker-ce/centos/

We using the docker-dd-agent docker image to build and run our container image on our EC2 host using the API key for our newly created Datadog account. The New Agent workflow in Datadog gives us the easy one-step install command required for Docker to work:
```
docker run -d --name dd-agent \
              -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -e DD_API_KEY=<my_api_key> \
                datadog/agent:latest
```
In short, we've pulled down the latest image from the Docker Hub registry, then ran it while bind mounting three locations on the EC2 host as read-only volumes on the container that are required by the Datadog Agent to collect and process system data. You can learn more about Docker volumes and those special Linux locations here:
- [Docker Volumes documentation](https://docs.docker.com/storage/volumes/)
- [What is  /var/run/docker.sock and why is it used?](https://medium.com/lucjuggery/about-var-run-docker-sock-3bfd276e12fd)
- [What are cgroups?](https://wiki.archlinux.org/index.php/cgroups)
- [/proc](https://www.tldp.org/LDP/Linux-Filesystem-Hierarchy/html/proc.html)

Once we give the agent a moment (typically less than one minute) to register with our Datadog account, we can see the host appear in our hostmap:

![Hello Host](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/hello-host.png)

(be sure to clear any filters being applied)

===
## Section 1: Collecting Metrics

#### 1a. "Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog."

There are a number of ways to tag a host in Datadog, and in this case, we want to update the Agent config file. However, instead of logging into the container and manually changing datadog.conf, we can effect these settings by setting environment variables as part of our Docker Run command:
```
docker run -d --name dd-agent \
              -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -e DD_API_KEY=<my_api_key> \
              -e DD_TAGS="tier:database env:test region:us-east-2 name:dd-assessment-centos role:database" \
              datadog/agent:latest
```
Within moments, our host tags appear in the Datadog console:
![Host Tags](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/host-tags.png)

Even though we only have one host here, we anticipate adding more later, and tagging all of our instances allows us to view metrics aggregated at the "service" level. Here, I've tagged this host with the following values:
- "tier:database" because we plan on installing PostgreSQL and monitoring it.
- "env:test" since this is just a test environment
- "region:us-east-2" since this is where I launched the EC2 Instance
- "name:dd-assessment-centos" since this is the Name tag I gave the EC2 instance in the AWS web console
- "role:database" since this is a name/grouping I would use for this resource in a configuration tool like Ansible, Puppet, or Chef

The `key:value` syntax is not required but is a recommended best practice. If we were also to setup the AWS Datadog integration, we would also get a number of AWS-specific tags automatically setup for EC2 hosts (e.g., availability zone). You can find more information about tagging in Datadoc in the [docs](https://docs.datadoghq.com/getting_started/tagging/)

#### 1b. "Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database."

First, we'll install postgres, a popular open source Relational Database Management System (RDMS). Enter these commands to download and setup the PostgreSQL 10 repo for CentOS7:
```
#Download and install the postgres repo
yum install wget
cd /tmp && wget https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
yum install -y pgdg-centos10-10-2.noarch.rpm
yum install -y postgresql10-server postgresql10-contrib

#Initialize the postgres db cluster
/usr/pgsql-10/bin/postgresql-10-setup initdb

#Start postgres
systemctl start postgresql-10

#Configure postgres to start automatically on OS boot
systemctl enable postgresql-10
```
You should now be able to become the `postgres` linux user (assuming you have privileged access) and access your postgres instance with the command `psql`.

Next, let's configure postgres to be reachable by our dd-agent container by creating a datadog postgres user and configuring postgres network settings. In the Datadog web console, navigate on the left to Integrations > Integrations and install the PostgreSQL integration and navigate to the Configuration tab. Follow the steps to create a read-only datadog postgres user:

```
create user datadog with password '<machine_generated_password>';
grant SELECT ON pg_stat_database to datadog;
```

However, the check provided (`psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"`) won't work since our agent is running within a container, so we'll need to update postgres' host-based authentication configuration in ~postgres/10/data/pg_hba.conf. Because our dd-agent container could be provisioned with a range of private IP's, we'll need to allow that range to access our postgres instance by adding this line to the bottom of the file:

```
# Connections from dd-agent containers
host    all             datadog         172.17.0.0/16           md5
```
This allows inbound postgres connections from the 172.17.0.0/16 space (the subnet Docker uses by default) connecting as the datadog user authenticating with user/pass credentials.

Next, let's configure postgres to listen for inbound connections to its private IP address. In ~postgres/10/data/postgresql.conf, we scroll down to `listen_addresses` and add our host's private IP:
```
listen_addresses = 'localhost,<host_private_ip>'            # what IP address(es) to listen on;
```

Don't forget to restart postgres with `systemctl restart postgresql-10` and make sure you're still able to access `psql` as the `postgres` user.

Finally, let's relaunch our dd-agent container to include a new postgres.yaml configuration file. I've setup a `postgresql.yaml` on the host at `/opt/dd-agent-conf.d/` with the same contents as the integration instructions, except using the host's private IP address instead of localhost, and adding my tags so they get added to data collected as part of our PostgreSQL integration:
```
init_config:
instances:
  - host: <host_ip>
    password: <datadog_user_password>
    port: 5432
    tags:
      - tier:database
      - env:test
      - region:us-east-2
      - name:dd-assessment-pg
      - role:database
    username: datadog
```

We can now kill and remove our existing container (`docker kill`, `docker rm`) and start a new container that will mount our new config file:

```
docker run -d --name dd-agent \
              -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -v /opt/dd-agent-conf.d:/conf.d:ro \
              -e DD_API_KEY=<your_api_key> \
              -e DD_TAGS="tier:database env:test region:us-east-2 name:dd-assessment-centos-docker role:database" \
              datadog/agent:latest
```

![PostgreSQL data!](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/dashboard-postgres.png)

_(Here I ran into some issues getting the containerized agent to reach postgres running on the
container host in order to get the integration to work completely. I was able to graph_ `postgresql.max_connection` _—see Timeboard creation below—but the provided PostgreSQL dashboards wouldn't show any data except max connections in use %. I did find the postgres error in the agent logs, but
after spending some time reading documentation and doing some online research I opted to
continue on so I could finish within a reasonable time.)_


#### 1c. "Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000."
In this section we're going to create a custom Agent Check to demonstrate how we might collect metrics from our custom applications. We can simply follow the [documentation on Writing an Agent Check](https://docs.datadoghq.com/agent/agent_checks/):

```
touch /opt/dd-agent-conf.d/my_metric.yaml

#insert this into my_metric.yaml
---
init_config:
instances:
  - host: <host_ip>

#setup a directory to mount into /checks.d to the dd-agent container in order to make the custom check available
mkdir dd-agent-checks.d

#create the custom check
cd /opt/dd-agent-checks.d
touch my_metric.py

#insert this into my_metric.py
from checks import AgentCheck
from random import randint
class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
```

After killing and removing our dd-agent container, we can perform `docker run` with our updated command to make our custom checks available to the new agent:
```
docker run -d --name dd-agent \
              -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -v /opt/dd-agent-conf.d:/conf.d:ro \
              -v /opt/dd-agent-checks.d:/checks.d:ro \
              -e DD_API_KEY=<my_api_key> \
              -e DD_TAGS="tier:database env:test region:us-east-2 name:dd-assessment-centos-docker role:database" \
              datadog/agent:latest
```

Navigate to Metrics > Explorer, search for my_metric, and voila:

![my_metric](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/my-metric.png)

#### 1d. Change your check's collection interval so that it only submits the metric once every 45 seconds. Bonus Question: Can you change the collection interval without modifying the Python check file you created?

To change our new custom metric's collection interval, we'll want to update our my_metric.yaml config as follows:

```
init_config:
instances:
  - host: <host_ip>
    min_collection_interval: 45
```
This sets the _minimum_ collection interval for this check to 45 seconds, but doesn't guarantee that it will be exactly 45s each time. The agent runs every 15 seconds and this parameter makes the agent not collect new instance data unless data was collected for the same instance more than min_collection_interval seconds ago. This only works for values > 15, it's not possible to have the agent collect data more frequently this way. (See more details from [this answer from Datadog support](https://help.datadoghq.com/hc/en-us/articles/203557899-How-do-I-change-the-frequency-of-an-agent-check-))

Since we changed the collection interval using the custom check's configuration file, we didn't have to modify the Python file to make this change.

## Section 2: Visualizing Data
#### 2a. Utilize the Datadog API to create a Timeboard that contains:
1. Your custom metric scoped over your host.
2. Any metric from the Integration on your Database with the anomaly function applied.
3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
4. Include the script that you've used to create this Timemboard.

Because [we've read the API docs on Timeboards](https://docs.datadoghq.com/api/?lang=python#timeboards), we can easily craft our own API call to create a Timeboard, see create_timeboard.py for the full script.

Instructions for running create_timeboard, from the project directory:
```
python3 -m venv create_timeboard
source create_timeboard/bin/activate
pip install datadog #if not already installed
# Navigate to the same directory as create_timeboard.py and put the required secrets in a dd_secrets.py directory
python create_timeboard.py
```
(We do it this way to avoid having to put the credentials into create_timeboard.py and to utilize best practices when managing our Python dependencies)

#### 2b. "Once this is created, access the Dashboard from your Dashboard List in the UI, set the Timeboard's timeframe to the past 5 minutes, & take a snapshot of this graph and use the @ notation to send it to yourself.

The result is our Timeboard with two graphs - one graphing `my_metric` scoped over the `dd-assessment-centos-docker` EC2 instance, with values rolled up into an hourly sum; and another graphing postgresql.percent_usage_connections on the PostgreSQL instance we setup earlier on the same host, with the anomaly function applied. Here are 5-minute and 1-hour views:

![5-minute dashboard](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/5-minute-dashboard.png)

![1-hour dashboard](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/1-hour-dashboard.png)

I used the same `pgbench` tool earlier to simulate 90 connections over a 3-minute period, which you can see on the postgresql.percent_usage_connections graph.

You can share snapshots of your views by hovering your mouse over the graph and clicking the camera icon to bring up a comment dialog, where you can @ tag your teammates and write your message. This will appear in the [Event Stream](https://docs.datadoghq.com/graphing/event_stream/).

#### 2-bonus. What is the Anomaly graph displaying?"
The anomaly function is a feature that helps users visualize when a metric's value is an outlier to historical results. You'll note the red portion of the postgresql.percent_usage_connections graphs that show the number of connections at .91, which is much higher than the historical average of near zero. Datadog offers four anomaly detection algorithms: basic, agile, robust, and adaptive, see the [docs on Anomaly Detection](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) for more details.

## Section 3: Monitoring Data
To demonstrate setting up a metric monitor, we can easily use the Datadog console, or [we could do it programmatically using the API](https://docs.datadoghq.com/api/?lang=python#monitors). In this example, we'll use the console to setup a monitor with a warning threshold of 500 and an alerting threshold of 800. We've also configured the monitor to notify if there has been no data for 10m.

![my_metric-monitor-thresholds](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/my_metric-monitor-thresholds.png)

So that we can get meaningful messages when we're notified, we can use the templating features to dynamically generate the message sent to us, such that the email notification will send a different message depending on whether the monitor is an Alert, Warning, or No Data state, and include the host ip and the metric value that caused the monitor to trigger:

![my_metric-monitor-message](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/my_metric-monitor-message.png)

Here is what a Warn email notification might look like:

![my_metric-notification-1](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/my_metric-notification-1.png)
![my_metric-notification-2](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/my_metric-notification-2.png)

Finally, since this metric is just a test and we want to minimize the noise coming from this alert, we'll setup two scheduled downtimes for this monitor: one that silences it from 7pm to 9am daily on M-F:

![maintenance-weekday](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/downtime-weekdays.png)

We'll setup another downtime for all day on Sat-Sun:

![maintenance-weekend](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/downtime-weekend.png)

Datadog will send an email notification when the downtime starts:

![maintenance-email](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/my_metric-downtime-notification.png)

## Section 4: Collecting APM Data

Let's setup APM on a test application by restarting our Agent container with new options, spinning up a basic application to instrument, then instrumenting it. In the Datadog console, navigate to APM to find additional setup details and the relevant docs for your application.

#### Restarting our containerized Agent with new options
- `DD_APM_ENABLED=true`
- a user-defined bridge network `dd-assessment` for our container (to allow the agent to send tracing data by DNS name), and
- setting the Agent's hostname to `datadog-agent`:

```
docker run -d --name datadog-agent \
              -h datadog-agent \
              --network="dd-assessment" \
              -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -v /opt/dd-agent-conf.d:/conf.d:ro \
              -v /opt/dd-agent-checks.d:/checks.d:ro \
              -e DD_API_KEY=<my_api_key> \
              -e DD_TAGS="tier:database env:test region:us-east-2 name:dd-assessment-centos-docker role:database" \
              -e DD_APM_ENABLED=true \
              datadog/agent:latest
```

#### Spinning up a basic application (with Docker)
In this example, running a minimal Flask app with uWGI and Nginx (see Dockerfile for details), starting it (on the same host where the Agent container is running) as follows:

```
docker build -t flaskapp .
docker run -d --name flaskapp \
              --network="dd-assessment" \
              -p 80:80 \
              flaskapp
```

We can now use the EC2 instance's public link to confirm the application is running: ec2-18-219-253-145.us-east-2.compute.amazonaws.com

#### Instrumenting our application
By providing to the tracer (a) our agent's DNS name (`datadog-agent`) within our user-defined bridge network (`dd-assessment`) and (b) the port it is listening for tracing data (see app/main.py). We'll visit the `/api/apm` and `/api/trace` endpoints a number of times to generate tracing data.

After a minute or so, the APM Console should now show tracing data from our application:

![apm-tracing-data](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/apm-tracing-data.png)
