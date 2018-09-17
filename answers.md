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

- Next we prepare the script. The API provided in the documentation is already structured. Further we can find the documentation on rollup function [here]( https://docs.datadoghq.com/graphing/#aggregate-and-rollup "Rollup function") and Anomaly function here]( https://docs.datadoghq.com/monitors/monitor_types/anomaly/ "Anomaly function") . Taking all these into account below is the final Python script to fire the API.

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







