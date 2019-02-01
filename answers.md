# Getting up and running with Datadog

For this project you'll need:

- A clean Ubuntu 16.04 Xenial install
- Root privileges
- A web browser
- A Datadog Account
- A text editor 
- A web browser


Let's begin with a fresh install of Ubuntu 16.04. Run `sudo apt-get update -y` followed by  `sudo apt-get upgrade -y` to ensure all default packages are up to date.

You'll need root privileges throughout this tutorial, so run `sudo su` in the terminal now to escalate to root.

## Installing the Datadog Agent

First, you'll need to install the Datadog agent, so head over to the [Datadog API](https://app.datadoghq.com/account/settings#api) to locate and copy your API key, then run hop into a terminal and run the following command to execute the agent installation script:

`DD_API_KEY=<YOUR_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

After a few moments you'll see a message letting you know the agent has been installed and is running:

![alt text](dd_images/dd_01.png)

## Tagging your agent host

It's important to utilize good resource organization practices by tagging them using key:value pairs. To tag your host you'll need to edit the `datadog-agent.yaml` file, so open `/etc/datadog-agent/datadog.yaml` in your terminal.

Once the file is opened, find the line pertaining to host tags:

![alt text](dd_images/dd_02.png)

Go ahead and edit the existing tags or make your own:

![alt text](dd_images/dd_03.png)

Save and close your editor after editing the tags, then run `service datadog-agent restart` to update the host with your new tags.

After a moment run `service datadog-agent status` to ensure the agent is running as it should. 

Now head to the [Infrastructure Map](https://app.datadoghq.com/infrastructure/map) to get view a visual representation of your host and see its tags. You may encounter a message telling you that WebGL is required:

![alt text](dd_images/dd_04.png)

I get this notification because I use a locked-down version of Firefox that doesn't allow WebGL, but Safari displays the map for me:

![alt text](dd_images/dd_05.png)

Clicking on the ubuntu-xenial host I can see which apps are running, some system information, and my newly created tags:

![alt text](dd_images/dd_06.png)

Now that the agent is installed and the host tags are set up, it's time to install PostgreSQL version 10.

## Installing Postgres

Per the [Postgres documentation](https://www.postgresql.org/download/linux/ubuntu/) you need to create a file in your `apt` sources list for the Postgres repository and add a link to the repository within that file. Run `touch /etc/apt/sources.list.d/pgdg.list` to create the file, and `sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'` to add the repository link.

Next, import the repository's signing key with  `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -` and run `apt-get update -y` to update your system accordingly. Now install Postgres with `apt-get install postgresql-10 -y`. Confirm that all packages are installed by running `dpkg -l | grep postgres`:

![alt text](dd_images/dd_07.png)

Fire up the Postgres service with `service postgresql start` and confirm it's running with `ps -ef | grep postgres`:

![alt text](dd_images/dd_08.png)

Now that the Postgres service is up and running, create a database from which metrics will be pulled. Run `su postgres` in the terminal to assume the postgres user. 

Now enter the Postgres console by running the `psql` command. Note the change to the prompt in your terminal:

![alt text](dd_images/dd_09.png)

Create a new database by running the `CREATE DATABASE` command:

![alt text](dd_images/dd_10.png)


## Configuring the Datadog Postgres Integration

Datadog ships with a pre-made integration for Postgres which once configured will provide real-time metrics and monitoring for the database. To begin the configuration process, create a read-only Postgres user named datadog with `CREATE USER datadog WITH PASSWORD 'your_secure_password';`
and give the datadog user access to pg_monitor with `GRANT pg_monitor TO datadog;`

Now that the datadog user has been granted read access to the database, hit CTRL+Z to get out of the Postgres console, then type `exit` twice to get back to the root user.

Create a configuration file to store the database information and credentials by first copying the sample configuration to a new file with `cp /etc/datadog-agent/conf.d/postgres.d/conf.yaml.example /etc/datadog-agent/conf.d/postgres.d/conf.yaml`, then open the new file in your text editor.

Uncomment the the `username`, `password`, and `dbname` lines and enter datadog as the user, the password you just created, and the name of the database you created. Save and exit, then restart the Datadog agent with `service datadog-agent restart`. After a few moments run `cat /var/log/datadog/agent.log | grep postgres` to see that some checks have been performed and completed:

![alt text](dd_images/dd_11.png)

Head over to the [Infrastructure List](https://app.datadoghq.com/infrastructure) to confirm the Postgres integration is running:

![alt text](dd_images/dd_12.png)

You can dig a little deeper by clicking on your host and scrolling to the bottom of the dashboard, where you'll see an active Postgres connection:

![alt text](dd_images/dd_13.png)

## Creating a custom check

Perhaps you have a unique system or you'd just like to create checks for metrics you define. First, let's create a configuration file called `demo_check.yaml` with 
`touch /etc/datadog-agent/conf.d/demo_check.yaml`.

Next, create and edit a Python file -- also named `demo_check` -- in the `checks.d` directory to create the check itself. For this example, `demo_check` will have a custom metric `my_metric`, a gauge which returns a random number between 0 and 1000. Create a new file in the `checks.d` directory with `touch /etc/datadog-agent/checks.d/demo_check.py` and open it in your text editor to add the following code:

```python
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class TestCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1001))
```



Save and exit the file, then restart the Datadog agent with `service datadog-agent restart`.

Run `datadog-agent check my_metric` and you'll get in response some JSON that shows `my_metric` returning a random number:

![alt text](dd_images/dd_15.png)

`demo_check` is running every 15 seconds as all checks do by default:

![alt text](dd_images/dd_16.png)

You can change the interval to 45 seconds by opening `/etc/datadog-agent/conf.d/demo_check.yaml` and adding:

```
init_config:

instances:
  - min_collection_interval: 45
```

The demo_check configuration looks like this:

![alt text](dd_images/dd_17.png)

Save and close the file, then run `service datadog-agent restart` to update the service with the new configuration. Now run `cat /var/log/datadog/agent.log | grep demo_check` to see the new collection interval:

![alt text](dd_images/dd_18.png)

__Bonus Question__

One of the takeaways from editing the `demo_check.yaml` configuration is that you need not change `min_collection_interval` from within the Python file, rather you can do so on a per-instance basis by setting `min_collection_interval` in the yaml file instead.

