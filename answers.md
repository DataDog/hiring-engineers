**This doc and the associated git hub assets represent the submission of
a technical exercise provided to Tom O'Leary during his interview
process at Datadog (for Enterprise Sales Engineer). The exercise is
intended to familiarize candidates with Datadog.**

**Prerequisites - Setup the environment**

**Step 1) Install a New VM**

First we'll spin up a new VM. Most any VM technology can be used, but an
[Ubuntu 18.04](https://releases.ubuntu.com/18.04/) image on [VMWare
Workstation
Player](https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html)
was used for this exercise.

![](.//media/image1.png){width="6.5in" height="1.931233595800525in"}

**Step 2) Install Docker**

Well be running everything in a [Docker](http://www.docker.com/)
container to avoid any dependency conflicts. Let's install Docker on the
new VM.

***Command:** sudo apt-get install docker.io*

![](.//media/image2.png){width="6.5in" height="2.019417104111986in"}

**Step 3) Install the Datadog Agent**

We could install the Datadog Agent directly on the host VM but that
would be somewhat antithetical to using the Docker platform, so instead
let's install the dockerized Datadog Agent image:

***Command:** DOCKER_CONTENT_TRUST=1 docker run -d \--name
docker-dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v
/proc/:/host/proc/:ro -v /cgroup/:/host/sys/fs/cgroup:ro -e
DD_API_KEY=\<API KEY\> datadog/agent:*7

We can see the Agent container is up with the below Docker command.

***Command:** docker ps*

![](.//media/image3.png){width="6.5in" height="0.6280172790901137in"}

Note, the Docker daemon runs under root. For simplicity, we don't want
to preface every Docker command with "sudo", so let's create a docker
group with root access and add us to that group. [See instructions
here.](https://docs.docker.com/engine/install/linux-postinstall/)

We can also now see that the Agent is reporting data to the Datadog
platform.

<https://app.datadoghq.com/dash/host/2673579463?from_ts=1593104807629&to_ts=1593108407629&live=true>

![](.//media/image4.png){width="6.5in" height="4.423193350831146in"}

**Troubleshooting**

For Agent troubleshooting, Agent logs can be viewed in the Agent Docker
container (/var/log/datadog)

***Command:** docker exec -it dd-agent bash*

Agent status can also be seen:

***Command:** docker exec -it dd-agent agent status*

**Step 4) Install MySQL & Flask Docker containers**

Since we want to see how Datadog can be applied to monitoring real world
applications, let's install a couple of Docker containers to create an
application that exposes a simple REST service that pulls data from a
database.

**MySQL**

***Command:** docker pull mysql/mysql-server:latest*

We now have a MySQL Docker image on our VM

![](.//media/image5.png){width="6.5in" height="1.1173490813648295in"}

In order to monitor MySQL with Datadog, we'll need to do a few things
around setting up a MySQL. One is to set up a MySQL user with so the
Datadog Agent can connect to MySQL with the proper credentials (see
[MySQL Docker installation
guide](http://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/docker-mysql-getting-started.html)
for full details). We'll create SQL script for this so we can execute at
container startup

[mysql-dd-config.sql](./mysql_config/scripts/mysql-dd-config.sql)


```console

\# To run script on container lauch use

\# \--mount
type=bind,src=/home/datadog/config/scripts/,dst=/docker-entrypoint-initdb.d/
\\

CREATE USER \'dduser\'@\'%\' IDENTIFIED WITH mysql_native_password by
\'\<password\>\';

GRANT REPLICATION CLIENT ON \*.\* TO \'dduser\'@\'%\';

GRANT PROCESS ON \*.\* TO \'dduser\'@\'%\';

ALTER USER \'dduser\'@\'%\' WITH MAX_USER_CONNECTIONS 5;

GRANT SELECT ON performance_schema.\* TO \'dduser\'@\'%\';

```

[Configuring MySQL for Datadog
monitoring](http://docs.datadoghq.com/integrations/mysql/#pagetitle)

```

To run the MySQL container we will use another shell script.

```console

docker run \\

-d \\

-l \"com.datadoghq.ad.logs\"=\'\[{\"source\": \"mysql container\",
\"service\": \"mysql\"}\]\' \\

\--name=mysql1 \\

\--network ddnetwork \\

\--env=\"MYSQL_ROOT_PASSWORD=datadog\" \\

\--publish 6603:3306 \\

\--mount
type=bind,src=/home/datadog/mysql_config/data,dst=/var/lib/mysql \\

\--mount type=bind,src=/home/datadog/mysql_config/my.cnf,dst=/etc/my.cnf
\\

\--mount
type=bind,src=/home/datadog/mysql_config/scripts,dst=/docker-entrypoint-initdb.d
\\

mysql/mysql-server

```

To create some data in the database, we run the create_city_stats.sql
script in MySQL.

[create_city_stats.sql](./mysql_config/ create_city_stats.sql)

***mysql\>** source /*create_city_stats.sql

We can since we exposed the MySQL port to the host (publish 6603:3306)
we can access the data in MySQL Workbench from the decktop

![](.//media/image6.png){width="5.1325in" height="2.0733333333333333in"}

**Flask**

Flask will host the REST service that returns population data based a
requested city name.

Install Flask Docker image: [flask docker
setup](http://github.com/tiangolo/uwsgi-nginx-flask-docker).

To run our app, well need to copy it over to the Flask container,
install the Datadog trace library, MySQL python libs, then run the app
using ddtrace-run to enable tracing :

```console

\>docker cp ./flaskbuild/app/main.py flaskapp:/app

\>docker exec -it flaskapp bash

\>pip install ddtrace

\>pip install mysql-connector-python

\>ddtrace-run python main.py

```

Data has a prebuilt [Docker
Dashboard](http://app.datadoghq.com/screen/integration/52/docker---overview)
that lets us see the Docker containers are up and happy.

![](.//media/image7.png){width="5.7539774715660545in"
height="3.506666666666667in"}

Now it's time to collect and explore some metrics.

**Collecting Metrics:**

**Using Tags to help find and organize metrics**

It's useful to be able to tag our metrics by things like host,
environment, application, etc. This lets us easily locate and group
similar metrics from the same category. Tags can be added through
different methods, since we are deploying everything in Docker, and easy
way is to use put the tags in the docker run command using and the TAG
environment variable.

[mysql-dd-config.sql](./run-dd-agent.sh)

```console

docker run -d \--name docker-dd-agent \\

\--network ddnetwork \\

-v /var/run/docker.sock:/var/run/docker.sock:ro \\

-v /proc/:/host/proc/:ro \\

-v /home/datadog/dd_config/conf.d:/conf.d:ro \\

-v /home/datadog/dd_config/checks.d:/checks.d:ro \\

-v /home/datadog/dd_config/run:/opt/docker-dd-agent/run:rw \\

-v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \\

-e API_KEY=75cc324da0bc265b8883ce646853b814 \\

-e SD_BACKEND=docker \\

-e NON_LOCAL_TRAFFIC=false \\

-e DD_LOGS_ENABLED=true \\

-e DD_AC_EXCLUDE=\"name:datadog-agent\" \\

-e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true \\

-e DD_APM_ENABLED=true \\

-e DD_APM_NON_LOCAL_TRAFFIC=true \\

\-**e TAGS=docker:agent,env:testing \\**

datadog/docker-dd-Agent:latest

```

**Here we can see the tags applied to Host Map Dashboard in Datadog.**

<https://app.datadoghq.com/infrastructure/map?host=2673579463&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host>

![](.//media/image8.png){width="6.5in" height="1.8930675853018373in"}

**Monitoring MySQL**

**We can get metrics out of MySQL by configuring the Agent. In the above
Agent run script we have the line**

-v /home/datadog/dd_config/conf.d:/conf.d:ro \\

This will copy the host file mysql.yaml to the conf.d directory in the
Agent Docker container.

[mysql-dd-config.sql](./dd_config/conf.d/mysql.yaml)

**Once enabled, we can view MySQL metrics in a prebuilt** [MySQL
Dashboard](http://app.datadoghq.com/dash/integration/12/mysql---overview?from_ts=1593464430382&to_ts=1593637230382&live=true)

![](.//media/image9.png){width="6.5in" height="2.7020483377077866in"}

**Adding Custom Metrics**

**We can add custom metrics using a custom Agent checks. For example,**
submit a metric named my_metric with a random value between 0 and 1000,
at certain interval. To do this, we first create a python script to
generate the metrics and send to the Agent.

[mysql-dd-config.sql](./dd_config/checks.d/mycheck.py)

```python

import random

\# the following try/except block will make the custom check compatible
with any Agent version

try:

\# first, try to import the base class from new versions of the
Agent\...

from datadog_checks.base import AgentCheck

except ImportError:

\# \...if the above failed, the check is running in Agent version \<
6.6.0

from checks import AgentCheck

\# content of the special variable \_\_version\_\_ will be shown in the
Agent status page

\_\_version\_\_ = \"1.0.0\"

class HelloCheck(AgentCheck):

def check(self, instance):

self.gauge(\'my_metric\', random.randint(0,1000),
tags=\[\'custom:check\'\])

```

**There also needs to be a corresponding yaml in conf.d.**

[mysql-dd-config.sql](./dd_config/conf.d/mycheck.yaml)

These are copied over in the above Agent run script with these lines:

-v /home/datadog/dd_config/conf.d:/conf.d:ro \\

-v /home/datadog/dd_config/checks.d:/checks.d:ro \\

**The collection interval can be adjust in the mycheck.yaml by setting
the min_collection_interval, e.g. to 45 seconds from the default of 15
seconds.**

**- min_collection_interval: 45**

**We can see our new metric in the metric explorer.**

![](.//media/image10.png){width="6.5in" height="3.163021653543307in"}

**Visualizing Data:**

Dashboards can easily be created with drag and drop in the Datadog UI,
but we can also utilize the Datadog API to create a Timeboard Dashboad.
For example, one that that contains:

-   The above custom metric scoped over our host.

-   A metric from the Integration with MySQL with an anomaly function
    applied. The anomaly function lets us easily see when there are
    outliers from normal behavior based on analysis of historical data.
    See
    <https://docs.datadoghq.com/monitors/faq/anomaly-monitor/#pagetitle>
    for more info.

-   The above custom the rollup function applied to sum up all the
    points for the past hour into one bucket

Here is the script used to create the Dashboard/Timeboard.

[create_timeboard.sh](./timeboard/conf.d/create_timeboard.sh)

*\*Note: I had an issue running the shell script when I introduce the
anomaly function (worked fine without that), and ended up posting the
json using Postman.*

Once this is created, you can access the Dashboard from your Dashboard
List in the UI:

![](.//media/image11.png){width="6.5in" height="2.1409930008748908in"}

Note: [Click here to create an app
key.](https://app.datadoghq.com/account/settings#api)

We can also

-   Set the Timeboard\'s timeframe to the past 5 minutes. See
    <https://docs.datadoghq.com/dashboards/guide/custom_time_frames/#pagetitle>

-   Take a snapshot of this graph and use the @ notation to send it to
    yourself. See
    [[https://docs.datadoghq.com/dashboards/sharing/]{.ul}](https://docs.datadoghq.com/dashboards/sharing/)

**Monitoring Data**

Since we've already caught the custom my_metic going above 800 once, you
don't want to have to continually watch this dashboard to be alerted
when it goes above 800 again. So let's make life easier by creating a
monitor.

We can create a new Metric Monitor that watches the average of your
custom metric (my_metric) and will alert if it's above the following
values over the past 5 minutes:

-   Warning threshold of 500

-   Alerting threshold of 800

-   And also ensure that it will notify you if there is No Data for this
    query over the past 10m.

We can also configure the monitor's message so that it will:

-   Send you an email whenever the monitor triggers.

-   Create different messages based on whether the monitor is in an
    Alert, Warning, or No Data state.

-   Include the metric value that caused the monitor to trigger and host
    ip when the Monitor triggers an Alert state.

-   When this monitor sends you an email notification, take a screenshot
    of the email that it sends you.

![](.//media/image12.png){width="6.5in" height="3.4798173665791774in"}

![](.//media/image13.png){width="6.5in"
height="3.720631014873141in"}![](.//media/image14.png){width="6.5in"
height="5.44956583552056in"}

**Collecting APM Data:**

We already deployed the Flask app in the setup. We can see the APM
features of Datadog my exercising the REST API of that app, e..g. by
making REST calls directly in a browser

![](.//media/image15.png){width="6.4991666666666665in"
height="1.6266666666666667in"}

[main.py](./flask_config/app/main.py)

We can now get detailed tracing info to see where I REST service is
spending its time. down to specific details on backed calls (MySQL in
this case).

![](.//media/image16.png){width="6.5in" height="2.7428641732283463in"}

We can display trace metrics in the same Dashboard as infrastructure
metrics, helping us correlate poor performing apps to infrastructure
issues.

![](.//media/image16.png){width="6.5in" height="2.7428641732283463in"}

Importantly, Datadog allows us to monitor both services and resources. A
service is a set of processes that do the same job - for example a web
framework or database. Resources represent a particular domain of a
customer application - they are typically an instrumented web endpoint,
database query, or background job. See:

[[https://docs.datadoghq.com/tracing/guide/resource_monitor/\#pagetitle]{.ul}](https://docs.datadoghq.com/tracing/guide/resource_monitor/#pagetitle)

**Final Thoughts :**

As you can see by this exercise, Datadog is very versatile and can
collect data from any source in near real-time, visualize and correlate
that data in many ways, and provide machine learning based alerting
based on historical analysis. While typically used for IT application
and infrastructure monitoring, certainly and IoT scenario would also be
an area where Datadog can add tremendous value.
