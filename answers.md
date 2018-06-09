Your answers to the questions go here.

Edwin Zhou
Solutions Engineer
Technical Exercise

## Disclaimer - The Environment
In this exercise, I chose to set up my environment on Windows 10. I recognize that the exercise recommends to use a virtual machine or a Containerized approach, which heavily simplifies the setup process. However, for the past few years, I've set up a comfortable environment for myself using exclusively Windows and its Powershell, having used NodeJS and Python virtual environments under this operating system. I'm confident to demonstrate that the limitations from the Windows operating system are slim, and that I'm capable of completing the exercise with the environment I am most comfortable with.

## Installing the Agent
Create your account on Datadog.

<a href="https://app.datadoghq.com/account/settings#agent/windows">Download the Datadog Agent for Windows here.</a>

In a Windows Command Prompt, in the directory of the installer just downloaded, run:

```
msiexec /qn /i datadog-agent-6-latest.amd64.msi APIKEY="YOUR_API_KEY" HOSTNAME="my_hostname" TAGS="mytag1,mytag2"
```

<a href="https://app.datadoghq.com/account/settings#api">Your API key can be found here</a>

You may alternatively use the installation GUI and manually input your API key from there.

Lastly, open a command prompt as *Adminstrator* and go to the directory:
```
C:\Program Files\Datadog\Datadog Agent\embedded
```

and run the command

```
.\agent.exe start
```

You may now access the Agent gui from `127.0.0.1:5002`

## Collecting Metrics

### Adding Tags
In order add tags to your host we must access the `datadog.yaml` file under `C:\ProgramData\Datadog\`. Inside this configuration file we may add tags under the `tag:` key.

```yaml
C:\ProgramData\Datadog\datadog.yaml

...
# Add new tags here
tags:
  - "testtag"
  - "newtag"
...
```

**ADD SCREENSHOT HERE**

We can also use the Agent GUI at `127.0.0.1:5002` to access the settings page.
**1.5 TAGS**
After adding the tags here, we may restart the agent.

### Setting Up PostgreSQL via BigSQL
Open up Windows Command Prompt as *Administrator* and run the following command:

`@powershell -NoProfile -ExecutionPolicy unrestricted -Command "iex ((new-object net.webclient).DownloadString('https://s3.amazonaws.com/pgcentral/install.ps1'))"`

After BigSQL completes unpacking, we will install PostgreSQL 10 with the following commands:

```
  cd bigsql
  ./pgc.bat install pg10
```

We will need to add environment variables in order to run PostgreSQL commands directly from the command prompt without needing to be in the PostgreSQL directory.

From the start menu, search 'environment variable'
**1 ENVVAR**
Click on Environment Variables...
**2 ENVVAR**
Click on Path, then click Edit
**3 ENVVAR**
Click New, and add the install directory of bigsql followed by `\pg10\bin`, i.e. `C:\Windows\system32\bigsql\pg10\bin`
**4 ENVVAR**

Additionally, we must specify where the database data will be stored in your harddrive.

`$Env:PGDATA = "C:\Users\Edwin Zhou\bigsql\data\pg10"`

Now we must initialize the database and assign a name for the superuser role:
`initdb -U root`
Note that this role does not have a password, and if you expect to use this database in the future, you may run the command with the `-W` flag to prompt a password.


Then we must start the psql server.
`./pgc.bat start pg10`

Finally, access your database with the following command:
```
psql -h localhost -U root postgres
```

Finally, we can create our Datadog role using the password generated in the integration setup on the Datadog Application:

```
postgres=# create user datadog with password 'Jp9mTWQzOS8bhwCLqHRY8kBO';
postgres=# grant SELECT ON pg_stat_database to datadog;
```

Now we must access our PostgreSQL conf.d file under `C:\ProgramData\Datadog\conf.d\postgres.d\conf.yaml`

and add the following lines:
```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: Jp9mTWQzOS8bhwCLqHRY8kBO
       tags:
            - optional_tag1
            - optional_tag2
```

Restart your agent.

To verify that the database is integrated into Datadog, in the directory `C:\Program Files\Datadog\Datadog Agent\embedded\` run `.\agent.exe check postgres`.

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
To create a custom agent, make a new check `custom_check.py` in `C:\ProgramData\Datadog\checks.d`
In `custom_check.py`, insert the following code:
```python
from checks import AgentCheck
import random

class CustomCheck(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randrange(1000), tags=['my_metric_tag'])

```
This check will submit a metric with a random value from 0 to 1000.
Then, make a new configuration directory for your new check. Note that the name of the new check must match the name of the new directory, in this case `custom_check`.
```
mkdir C:\ProgramData\Datadog\conf.d\custom_check.d\
```
Create a new configuration file named `conf.yaml` in this folder.
In `conf.yaml`, insert the following:
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
This configuration will change the collection interval of the check to occur once every 45 seconds.
This is done external to the python file and can also be edited in the agent GUI under Checks->Manage Checks.


## Visualizing Data
To create a new Timeboard, go to Dashboards->New Dashboard and click New Timeboard.
