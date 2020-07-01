**Prerequisites - Setup the environment**

You can utilize any OS/host that you would like to complete this
exercise. However, we recommend one of the following approaches:

-   You can spin up a fresh linux VM via Vagrant or other tools so that
    you don't run into any OS or dependency issues. [Here are
    instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for
    setting up a Vagrant Ubuntu VM. We strongly recommend using
    minimum v. 16.04 to avoid dependency issues.

-   You can utilize a Containerized approach with Docker for Linux and
    our dockerized Datadog Agent image.

Then, sign up for Datadog (use "Datadog Recruiting Candidate" in the
"Company" field), get the Agent reporting metrics from your local
machine.

Spin up a Ubuntu VM

![](.//media/image1.png)

Installed Docker with command: sudo apt-get install docker.io

![](.//media/image2.png){width="6.5in" height="2.019417104111986in"}

Installed the dockerized Datadog Agent image:

DOCKER_CONTENT_TRUST=1 docker run -d \--name dd-agent -v
/var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v
/cgroup/:/host/sys/fs/cgroup:ro -e
DD_API_KEY=75cc324da0bc265b8883ce646853b814 datadog/agent:7

![](.//media/image3.png){width="6.5in" height="1.7861373578302713in"}

Host datadog1 agent up and reporting metrics:

<https://app.datadoghq.com/dash/host/2673579463?from_ts=1593104807629&to_ts=1593108407629&live=true>

![](.//media/image4.png)

Alternate agent install in Docker container

docker pull datadog/docker-dd-agent

![](.//media/image5.png)

For agent troubleshooting, logs can be viewed in the agent Docker
container

sudo docker exec -it docker-dd-agent bash

cd /var/log/datadog

Agent status can also be seen:

sudo docker exec -it \<CONTAINER_NAME\> agent status

**Collecting Metrics:**

-   Add tags in the Agent config file and show us a screenshot of your
    host and its tags on the Host Map page in Datadog.

-   Install a database on your machine (MongoDB, MySQL, or PostgreSQL)
    and then install the respective Datadog integration for that
    database.

> <https://www.datadoghq.com/blog/mysql-monitoring-with-datadog/>
>
> Follow instructions to install MySQL in Docker container:
>
> <https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/docker-mysql-getting-started.html>
>
> Installed MySQL as Docker container:

docker pull mysql/mysql-server:latest

> Started MySQL container with (run-mysql.sh):

sudo docker run \\

-d \\

\--name=mysql1 \\

\--env=\"MYSQL_ROOT_PASSWORD=datadog\" \\

\--publish 6603:3306 \\

\--mount type=bind,src=/home/datadog/config/my.cnf,dst=/etc/my.cnf \\

\--mount type=bind,src=/var/lib/mysql,dst=/var/lib/mysql \\

mysql/mysql-server

> <https://app.datadoghq.com/screen/integration/52/docker---overview>
>
> To allow remote access (e.g. to enable access from MySQL Workbench) :

docker exec -it mysql mysql -uroot --p

mysql\> CREATE USER \'datadog\'@\'%\' IDENTIFIED BY \'datadog\';

mysql\> GRANT ALL PRIVILEGES ON \*.\* TO \'root\'@\'%\' WITH GRANT
OPTION;

mysql\> SELECT user,host FROM user;

> Change the run script to mount the YAML config file for MySQL to
> further configure the agent to monitor MySQL:
>
> Copy example file to the host.
>
> sudo docker cp docker-dd-agent:/etc/dd-agent/conf.d/mysql.yaml.example
> mysql.yaml

mkdir /opt/dd-agent-conf.d

touch /opt/dd-agent-conf.d/nginx.yaml

> Fully enable MySQL performance metrics (non-prod DB only)
>
> ![](.//media/image6.png){width="4.042204724409449in"
> height="3.0533333333333332in"}
>
> <https://app.datadoghq.com/dash/integration/12/MySQL%20-%20Overview?tpl_var_scope=host%3Adatadog1&from_ts=1593263610416&to_ts=1593267210416&live=true>

-   Create a custom Agent check that submits a metric named my_metric
    with a random value between 0 and 1000.

> <https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count>
>
> NOTE: Following the instructions produced an error parsing the yaml
> file (this did not happen on native Windows install):
>
> 2020-06-30 14:01:34 UTC \| ERROR \| dd.collector \|
> config(config.py:1052) \| Unable to parse yaml config in
> /etc/dd-agent/conf.d/hello.yaml
>
> Needed to change yaml to the below (per youtube video
> <https://www.youtube.com/watch?v=kGKc7423744>)
>
> *init_config:*
>
> *instances:*
>
> *- min_collection_interval:*

-   Change your check\'s collection interval so that it only submits the
    metric once every 45 seconds.

-   **Bonus Question** Can you change the collection interval without
    modifying the Python check file you created?

**Visualizing Data:**

Utilize the Datadog API to create a Timeboard that contains:

-   Your custom metric scoped over your host.

-   Any metric from the Integration on your Database with the anomaly
    function applied.

-   Your custom metric with the rollup function applied to sum up all
    the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the
script that you\'ve used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in
the UI:

To create the app key.

[Click here to create an app
key.](https://app.datadoghq.com/account/settings#api)

-   Set the Timeboard\'s timeframe to the past 5 minutes

-   Take a snapshot of this graph and use the @ notation to send it to
    yourself.

-   **Bonus Question**: What is the Anomaly graph displaying?

**Monitoring Data**

Since you've already caught your test metric going above 800 once, you
don't want to have to continually watch this dashboard to be alerted
when it goes above 800 again. So let's make life easier by creating a
monitor.

Create a new Metric Monitor that watches the average of your custom
metric (my_metric) and will alert if it's above the following values
over the past 5 minutes:

-   Warning threshold of 500

-   Alerting threshold of 800

-   And also ensure that it will notify you if there is No Data for this
    query over the past 10m.

Please configure the monitor's message so that it will:

-   Send you an email whenever the monitor triggers.

-   Create different messages based on whether the monitor is in an
    Alert, Warning, or No Data state.

-   Include the metric value that caused the monitor to trigger and host
    ip when the Monitor triggers an Alert state.

-   When this monitor sends you an email notification, take a screenshot
    of the email that it sends you.

-   **Bonus Question**: Since this monitor is going to alert pretty
    often, you don't want to be alerted when you are out of the office.
    Set up two scheduled downtimes for this monitor:

    -   One that silences it from 7pm to 9am daily on M-F,

    -   And one that silences it all day on Sat-Sun.

    -   Make sure that your email is notified when you schedule the
        downtime and take a screenshot of that notification.

**Collecting APM Data:**

Given the following Flask app (or any Python/Ruby/Go app of your choice)
instrument this using Datadog's APM solution:

from flask import Flask

import logging

import sys

\# Have flask use stdout as the logger

main_logger = logging.getLogger()

main_logger.setLevel(logging.DEBUG)

c = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(\'%(asctime)s - %(name)s - %(levelname)s -
%(message)s\')

c.setFormatter(formatter)

main_logger.addHandler(c)

app = Flask(\_\_name\_\_)

\@app.route(\'/\')

def api_entry():

return \'Entrypoint to the Application\'

\@app.route(\'/api/apm\')

def apm_endpoint():

return \'Getting APM Started\'

\@app.route(\'/api/trace\')

def trace_endpoint():

return \'Posting Traces\'

if \_\_name\_\_ == \'\_\_main\_\_\':

-   **Note**: Using both ddtrace-run and manually inserting the
    Middleware has been known to cause issues. Please only use one or
    the other.

-   **Bonus Question**: What is the difference between a Service and a
    Resource?

Provide a link and a screenshot of a Dashboard with both APM and
Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

Install Flask Docker image

<https://github.com/tiangolo/uwsgi-nginx-flask-docker>

Install MySQL python libs

<https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html>

**Final Question:**

Datadog has been used in a lot of creative ways in the past. We've
written some blog posts about using Datadog to monitor the NYC Subway
System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

**Instructions**

If you have a question, create an issue in this repository.

To submit your answers:

-   Fork this repo.

-   Answer the questions in answers.md

-   Commit as much code as you need to support your answers.

-   Submit a pull request.

-   Don\'t forget to include links to your dashboard(s), even better
    links and screenshots. We recommend that you include your
    screenshots inline with your answers.
