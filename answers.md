## Prerequisites - Setup the environment

### OS setup
I have used Ubuntu on top of VMware for this. Skipping the walkthrough of that part because we have bigger concern here.

### Datadog agent setup

**Step 1: Account Create**

Setup a free trial account from Datadog site [here]( https://app.datadoghq.com/signup "Datadog signup") and start using 14 days of evaluation.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Datadog_account_page.jpg" />
</div>

**Step 2: Agent Installation**

Now that the account has been created, the first landing page after login to the portal will ask to choose the OS. Select Ubuntu there:
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Datadog_agent_page.jpg" />
</div>

The next page will provide a command to run in the OS:
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Datadog_Ubuntu_agent_page.jpg" />
</div>

```
DD_API_KEY=02f734414a40cee6e9861fa0cee0fb3a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
Simply run the commad and the agent will be installed automatically.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Agent_ins_start.jpg" />
</div>

Below massage will be shown upon successful installation:
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Agent_ins_fin.jpg" />
</div>

Once completed the Agent status can be seen with the command ``datadog-agent status`` in the command window.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Agent_status.jpg" />
</div>

### Collecting Metrics:

**1. Add tags**

To add tag we need to edit the ``datadog.yaml`` file under ``/etc/datadog-agent`` which is the default directory of Datadog agent.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/add_tags_yaml.jpg" />
</div>

Simply add the tags in ``key:value`` format.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/host_tags.jpg" />
</div>

Once done, dont forget to restart the agent using commad ``systemctl restart datadog-agent``

Now the freshly added tags are seen in the Datadog Host Map page.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/DD_hostmap_full.jpg" />
</div>

**2. Datadog integration for database**

Fist we need to install postgresql database. Its easy in Ubuntu, just need to run a single commad and sit back.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/postgresql_ins_start.jpg" />
</div>

Once that done, we need to go to Integration page of Datadog site.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/integration.jpg" />
</div>

And find PostgreSQL there. Clicking on it provides us all the commands required to configure agent for the database.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/DD_postgresql_config.jpg" />
</div>

Login to the postgresql database and run the first SQL there to create datadog user and grant in permission.

```
create user datadog with password 'nD7kgb57p06o34cwTfDV30ww';
grant SELECT ON pg_stat_database to datadog;
```

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/psql_creat_user.jpg" />
</div>

Next, logout from the database and run rest of the commands to verify the connection.

```
psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" && \
echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/psql_conn_ok.jpg" />
</div>

After that, we need to configure the agent to connect to the DB. The config file is ``conf.yaml`` and located under ``/etc/datadog-agent/conf.d/postgres.d`` directory.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/psql_conf_file.jpg" />
</div>

Restart the agent using ``systemctl restart datadog-agent`` and after few seconds the agent will start sending metrics to Datadog for postgresql DB. Check the status using ``datadog-agent check postgres``
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/psql_DD_status.jpg" />
</div>

We can now click on **Install Integration** button to finish the integration. 
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/DD_psql_integration_button.jpg" />
</div>

Host Map page now has Postgresql metrics available.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_psql_metrics.jpg" />
</div>

**3. Custom Agent check**

To create the required agent check, we need to create two files with same name but different extension in two location.

- Create ``mycheck_random.yaml`` file in directory ``/etc/datadog-agent/conf.d`` having below lines:

```
init_config:

instances:
    [{}]
```

- Create ``mycheck_random.py`` file in directory ``/etc/datadog-agent/checks.d`` having below lines:

```python
from checks import AgentCheck
from random import randint

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
```

Once the agent is restarted the metric will be available in Datadog GUI.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_my_metric.jpg" />
</div>

**4. Changing collection interval**

Collection interval can be changed simply by adding ``min_collection_interval:`` parameter in the ``mycheck_random.yaml`` file. The new file entry will be:

```
init_config:
        min_collection_interval: 45

instances:
    [{}]
```

Reference [here]( https://docs.datadoghq.com/developers/agent_checks/ "Agent Check")

**Bonus Question: Changing collection interval without changing the Python file**

Yes it is possible, you'd know that by now if you were giving concentration.

### Visualizing Data:

**1. Creating Timeboard using API**

- For this we need to prepare a script as per the Datadog API documentation given [here]( https://docs.datadoghq.com/api/?lang=python#timeboards "Timeboard API"). First we need API and APP key. We can find or create keys in below location of the Datadog consol.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/DD_API_GUI.jpg" />
</div>

- Next we prepare the script. The API provided in the documentation is already structured. Further we can find the documentation on rollup function [here]( https://docs.datadoghq.com/graphing/#aggregate-and-rollup "Rollup function") and Anomaly function [here]( https://docs.datadoghq.com/monitors/monitor_types/anomaly/ "Anomaly function"). Taking all these into account below is the final Python script to fire the API.

Coppied the script to ``timeboardapi.py`` file.

```Python
from datadog import initialize, api

options = {
    'api_key': '02f734414a40cee6e9861fa0cee0fb3a',
    'app_key': '04a248ce38eeb00900e4528122c6e337e4468e0a'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Custom metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "custom metric rollup"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "anomalies postgresql connections percentage"
}
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

```

- Finally we have to run the prepared Python script. To do that we need to resolve the dependencies first. As we are calling ``datadog`` module in the script, we need to install that first. Below are the commands required to run:

```
apt install python-minimal
apt-add-repository universe
apt install python-pip
pip install datadog
```

Now we can run the script using command `` python timeboardapi.py`` and the timeboard should get generated. Go to **Dashboards>Dashboard List** and the newly created dashboard will be there.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_timeboard.jpg" />
</div>

**2. Set Timeboard's timeframe**

Past 5 min can be selected by draging the mouse and selecting only last 5min.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_timeboard_5min.jpg" />
</div>

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_timeboard_5min_2.jpg" />
</div>

**3. Send a snapshot**

Take a snapshot by clicking on the below highlited button and send it to someone by start typing with @
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_snapshot_taking.jpg" />
</div>

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_snapshot_sending.jpg" />
</div>

Snapshot will be sent to the mentioned mail.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_snapshot_mail.jpg" />
</div>

**Bonus Question: What is the Anomaly graph displaying?**

Anomaly graph is predicting normal value range for any particular metric and the range is shown by the grey area. If the actual value of the metric goes beyond that range, it will be considered as abnormal.

### Visualizing Data:

- To creat a metric monitor first we go to the monitor page <img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_link.jpg" /> and select metric <img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_metric.jpg" />

- Next we setup the metric name and threshold values as per the requirements
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_config.jpg" />
</div>

- Lastly we can create the email notification by writting down in the **Say what's happening** section.

```
{{#is_alert}}
Light up the Bat signal!
my_metric of **{{host.ip}}** has reached **{{value}}** . Threshold value is **{{threshold}}**
You can run for your life or login to **{{host.name}}** and do your magic.
{{/is_alert}}

{{#is_warning}}
Its just a warning, no need to wake up. Just read the text and go back to sleep.
my_metric of **{{host.ip}}** has reached **{{value}}** . Threshold value is **{{warn_threshold}}**
{{/is_warning}}

{{#is_no_data}}
Where is The Food!
{{/is_no_data}}

@tosrif@gmail.com
```

Upon saving the monitor, the notification mails will start to come. Below are the screenshots of the emails received.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_warning_mail.jpg" />
</div>

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_alert_mail.jpg" />
</div>

**Bonus Question:**

We can configure downtime from the **Monitors>Manage Downtime** page. Respective configuration given below.

- One that silences it from 7pm to 9am daily on M-F
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_downtime_config_WD.jpg" />
</div>

- And one that silences it all day on Sat-Sun.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_downtime_config_WE.jpg" />
</div>

- System sends notification mails when downtime is scheduled. 
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_downtime_config_WD_mail.jpg" />
</div>

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/dd_new_monitor_downtime_config_WE_mail.jpg" />
</div>


### Collecting APM Data:

To instrument the given Python Flask application, we need to add the ``ddtrace`` module to the provided app. We can find the guideline to do that from [here]( https://docs.datadoghq.com/tracing/setup/python/ "Python") and [here]( http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask "Flask").

First we need to install required modules to run the application. 

```
pip install flask
pip install ddtrace
```

Then we put the script in a convenient location to run. In my case I created ``/etc/datadog-agent/scripts/flaskapp.py`` file. 

```Python
from flask import Flask
import logging
import sys
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="my_flask_app", distributed_tracing=False)


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

Once the file is created, we can trace the app while it runs using below command:

```
ddtrace-run python flaskapp.py
```

While the app is running we need to trigger the URL to send request to the app. We can use curl command from same server.

```
curl http://localhost:5050/
curl http://localhost:5050/api/apm
curl http://localhost:5050/api/trace
```

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/APM_triggers.jpg" />
</div>

This will send the trace back to Datadog which we can find from **APM>Traces** or **APM>Services** . Link to the dashboard [here]( https://app.datadoghq.com/apm/service/my_flask_app/flask.request?start=1537132593578&end=1537218993578&paused=false&env=prod "APM Dashboard")

Also here are the dashboard screenshots.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/flaskapp_apm_1.jpg" />
</div>

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/flaskapp_apm_2.jpg" />
</div>

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/flaskapp_apm_3.jpg" />
</div>

<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/flaskapp_apm_4.jpg" />
</div>

**Bonus Question: What is the difference between a Service and a Resource?**

Service is set of process or commands that can accomplish any given objective. Whereas, resources are the elemets used by Service to do the objective. Services are dependent on various Resources. For example, the **Datadog-agent** is a Service and the config file **datadog.yaml** is one of its resources.


### Final Question:

The most vital marketing tool is now a days is Human behavior analysis or prediction. Datadog can be used to analysis and trace human expenses patern. For example, mobile operators can use this tool to analysis their customer mobile expenses trend and based on that they can plan their product promotion and desired subscriber base.