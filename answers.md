Your answers to the questions go here.

Edwin Zhou
Solutions Engineer
Technical Exercise

## Installing the Agent
Create your account on Datadog.

<a href="https://app.datadoghq.com/account/settings#agent/windows">Download the Datadog Agent for Windows here.</a>

In the Linux termnal, run:

```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

```

<a href="https://app.datadoghq.com/account/settings#api">Your API key can be found here</a>

The Datadog agent should have started on its own, if not, run:
```
sudo service datadog-agent start  
```

## Collecting Metrics

### Adding Tags
In order add tags to your host we must access the `datadog.yaml` file under `/etc/datadog-agent/`. Inside this configuration file we may add tags under the `tag:` key beginning on line 35.

```yaml
/etc/datadog-agent/datadog.yaml

...
# Add new tags here
tags:
  - "custom-tag"
  - "custom-tag-2"
...
```

**ADD SCREENSHOT HERE**

After adding the tags here, restart the agent using:
```
sudo service datadog-agent restart
```

### Setting Up PostgreSQL via BigSQL
To install PostgreSQL, run:
```
sudo apt-get install postgresql-10
```

Run the command:
```
sudo -u postgres -i psql
```

To create the `datadog` role, run:
```
create user datadog with password 'your_password';
grant SELECT ON pg_stat_database to datadog;
```


Now we must access our PostgreSQL conf.d file under `/etc/datadog-agent/conf.d/postgres.d/conf.yaml` and add the following lines:
```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: your_password
       tags:
            - optional_tag1
            - optional_tag2
```

Restart your agent.

To verify that the database is integrated into Datadog, run `sudo -u dd-agent -- datadog-agent check postgres`.

You should receive the following snippet as the result if setup successfully:
```
  Running Checks
  ==============
    postgres
    --------
      Total Runs: 1
      Metrics: 14, Total Metrics: 14
      Events: 0, Total Events: 0
      Service Checks: 1, Total Service Checks: 1
      Average Execution Time : 110ms
```

### Creating a Custom Agent
To create a custom agent, make a new check `my_metric.py` in `/etc/datadog-agent/checks.d/`
In `my_metric.py`, insert the following code:
```python
from checks import AgentCheck
import random

class CustomCheck(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randrange(1000), tags=['my_metric_tag'])

```
This check will submit a metric with a random value from 0 to 1000.
Then, make a new configuration directory for your new check. Note that the name of the new check must match the name of the new directory, in this case `my_metric`.
```
mkdir /etc/datadog-agent/conf.d/my_metric.d/
```
Create a new configuration file named `conf.yaml` in this folder.
In `conf.yaml`, insert the following:
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
This configuration will change the collection interval of the check to occur once every 45 seconds.


## Visualizing Data
Using the Datadog API, we can send requests to create timeboards without needing to access the application itself.

First, we create a virtual environment in order to isolate our Python environment, and to prevent interference with other projects we may have.

We must install virtualenv,
```
sudo apt install virtualenv
```

Next, go to your desired directory of your project, and create the virtualenv.
```
virtualenv venv
```
Now activate the virtual environment
```
source venv/bin/activate
```

We can now install the Datadog package into our environment.
```
pip install datadog
```

The Python script below will create three custom metrics:
* my_metric scoped over the host.
* A metric from PostgreSQL called postgres.bgwriter.checkpoints_timed with the anomaly function applied.
* my_metric with the rollup function applied that sums up all of the points for the hour into one bucket.