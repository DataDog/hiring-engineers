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
  -e DD_TAGS=tier:database,env:test,region:us-east-2,name:dd-assessment-centos,role:database \
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
  -e DD_TAGS=tier:database,env:test,region:us-east-2,name:dd-assessment-centos-docker,role:database \
  datadog/agent:latest
```

Phew! Go grab a drink and break for a few minutes. When you're back, you should be able to see PostgreSQL data by checking out one of the Postgres dashboards in Dashboards > Dashboard List. (You can generate load on your postgres like I did by using the [pgbench utility](https://www.postgresql.org/docs/10/static/pgbench.html), ex: `/usr/pgsql-10/bin/pgbench -c 50 -P 3 -T 300`):

![PostgreSQL data!](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/dashboard-postgres.png)

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
  -e DD_TAGS=tier:database,env:test,region:us-east-2,name:dd-assessment-centos-docker,role:database \
  datadog/agent:latest
```

Navigate to Metrics > Explorer, search for my_metric, and voila:

![my_metric](https://s3.us-east-2.amazonaws.com/dd-assessment-djkahn/my-metric.png)

#### 1d. Change your check's collection interval so that it only submits the metric once every 45 seconds.
```
Note: I haven't gotten this working after trying to follow the docs. I also tried manually
editing the my_metric metadata to set the value to 45 but the graph is still showing
data points every 20 seconds.
```

To change our new custom metric's collection interval, we'll want to update our my_metric.yaml config as follows:

```
init_config:
    min_collection_interval: 45

instances:
  - host: <host_ip>
```
This sets the _minimum_ collection interval for this check to 45 seconds, but doesn't guarantee that it will be exactly 45s each time. Depending on how often the agent runs (which depends on how many integrations are enabled), a given interval could be a little longer (on the order of seconds).

## Section 2: Visualizing Data
#### Utilize the Datadog API to create a Timeboard that contains:
1. Your custom metric scoped over your host.
2. Any metric from the Integration on your Database with the anomaly function applied.
3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
4. Include the script that you've used to create this Timemboard.

Because [we've read the API docs](https://docs.datadoghq.com/api/?lang=python#timeboards), we can easily craft our own API call to create a Timeboard:
```
from datadog import initialize, api

options = {
    'api_key': '<my_api_key>',
    'app_key': '<my_app_key>'
}

initialize(**options)

title = "My Awesome Timeboard"
description = "The seed of something great."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{name:dd-assessment-centos-docker}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric over time"
}]

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs)
```


#### Once this is created, access the Dashboard from your Dashboard List in the UI, set the Timeboard's timeframe to the past 5 minutes, & take a snapshot of this graph and use the @ notation to send it to yourself. Bonus Question: What is the Anomaly graph displaying?
