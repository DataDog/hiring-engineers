# Getting up and running with Datadog

For this project you'll need:

- A clean Ubuntu 16.04 Xenial install
- Root privileges
- A web browser
- A Datadog Account
- A text editor 
- A web browser


Let's begin with a fresh install of Ubuntu 16.04. We'll run `sudo apt-get update -y` followed by `sudo apt-get upgrade -y` to ensure all default packages are up to date.

We're going to need root privileges throughout this tutorial, so let's avoid repeating the `sudo` command by running `sudo su` in the terminal right now to escalate to root.

## Installing the Datadog Agent

We need to install the Datadog agent, so let's head over to the [Datadog API](https://app.datadoghq.com/account/settings#api) to locate and copy our API key, then hop into a terminal and run the following command to execute the agent installation script:

`DD_API_KEY=<YOUR_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

After a few moments you should see a message letting you know the agent has been installed and is running:

![alt text](dd_images/dd_01_copy.png)

## Tagging your agent host

Let's utilize some good resource organization practices by tagging our host with key:value pairs. To do this we'll need to edit our Agent's YAML configuration file, so let's run `/etc/datadog-agent/datadog.yaml` in our terminal.

Once the file is opened, we want to find the line pertaining to host tags.

![alt text](dd_images/dd_02.png)

Go ahead and edit the existing tags or make your own

![alt text](dd_images/dd_03.png)

Once you've added your tags, save and close the editor, then run `service datadog-agent restart` to update the host with your new tags.

After a few moments you can check to ensure everything is running smoothly with the `service datadog-agent status` command. 

After a few minutes you can head to the [Infrastructure Map](https://app.datadoghq.com/infrastructure/map) to get view a visual representation of your host and see its tags. You may encounter a message telling you that WebGL is required:

![alt text](dd_images/dd_04.png)

I get this notification because I use a locked-down version of Firefox that doesn't allow WebGL, but Safari displays the map for me:

![alt text](dd_images/dd_05.png)

Clicking on my ubuntu-xenial host I can see which apps are running, some system information, and my newly created tags:

![alt text](dd_images/dd_06.png)

Now that the agent is installed and we've got our host tags set up, let's install PostgreSQL version 10.

## Installing Postgres

Per the [Postgres documentation](https://www.postgresql.org/download/linux/ubuntu/) we need to create a file in our `apt` sources list for the Postgres repository and add a link to the repository within that file. Let's run `touch /etc/apt/sources.list.d/pgdg.list` to create the file, and `sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'` to add our repository link to it.

Next, we'll import the repository's signing key with  `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -` and run `apt-get update -y` to update our system accordingly. Now we can install Postgres with `apt-get install postgresql-10 -y`. We can confirm that all packages are installed by running `dpkg -l | grep postgres`:

![alt text](dd_images/dd_07.png)

Let's fire up the Postgres service with `service postgresql start` and confirm it's running with `ps -ef | grep postgres`:

![alt text](dd_images/dd_08.png)

Now that the Postgres service is up and running we'll want to create a database from which metrics will be pulled. You wouldn't want to use the default postgres user on a production machine, but it's fine for this demonstration. Let's run `su postgres` in the terminal to assume the postgres user. 

Now we can enter the Postgres console by running the `psql` command. Note the change to the prompt in your terminal:

![alt text](dd_images/dd_09.png)

Let's create a new database called test_db by running the `CREATE DATABASE` command:

![alt text](dd_images/dd_10.png)

## Configuring the Datadog Postgres Integration

Datadog ships with a pre-made integration for Postgress that once configured will give us real-time metrics and monitoring for our database. To begin the configuration process, let's create a read-only Postgres user named datadog with `CREATE USER datadog WITH PASSWORD '<your_secure_password>';`

and give our datadog user access to pg_monitor with `GRANT pg_monitor TO datadog;`

Now that our datadog user has been granted read access to the database, hit CTRL+Z to get out of the Postgres console, then type `exit` to get back to our root user.

From here we'll need to create a configuration file to store our database information and credentials. Let's copy the sample configuration to a new file with `cp /etc/datadog-agent/conf.d/postgres.d/conf.yaml.example /etc/datadog-agent/conf.d/postgres.d/conf.yaml` then open the new file in your text editor.

We'll want to uncomment the the `username`, `password`, and `dbname` lines and enter datadog as the user, the password we just created, and the name of the database we created. Save and exit, then restart the Datadog agent with `service datadog-agent restart`. After a few moments the Datadog agent should be up and running again, and if we run `cat /var/log/datadog/agent.log | grep postgres` we should see that some checks have been performed and completed:

![alt text](dd_images/dd_11.png)

Head over to the [Infrastructure List](https://app.datadoghq.com/infrastructure) to confirm the Postgres integration is running:

![alt text](dd_images/dd_12.png)

We can even dig a little deeper by clicking on our host and scrolling to the bottom of our dashboard, where we'll see an active Postgres connection:

![alt text](dd_images/dd_13.png)

## Creating a custom check

Perhaps you have a unique system or you'd just like to create checks for metrics you define -- not a problem! First, let's create a configuration file called `demo_check.yaml` with 
`touch /etc/datadog-agent/conf.d/demo_check.yaml`.

The next step is to create and edit a Python file with the same name in our `checks.d` directory and create the check itself. For this example, our `demo_check` will have a custom metric `my_metric`, a gauge which returns a random number between 0 and 1000. Create a new file in the `checks.d` directory with `touch /etc/datadog-agent/checks.d/demo_check.py` and open it in your text editor to add the following code:

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




Save and exit the file, then restart the Datadog agent with `service datadog-agent restart`

If we run `datadog-agent check my_metric` we'll get back some JSON that shows our `my_metric` check returning a random number:

![alt text](dd_images/dd_15.png)

Our `demo_check` is running every 15 seconds as all checks do by default:

![alt text](dd_images/dd_16.png)

Let's change the interval to 45 seconds by opening `/etc/datadog-agent/conf.d/demo_check.yaml` and adding

```
init_config:

instances:
  - min_collection_interval: 45
```

Our demo_check conf should look like this:

![alt text](dd_images/dd_17.png)

Save and close the file, then run `service datadog-agent restart` to update the service with our new configuration. Now when we run `cat /var/log/datadog/agent.log | grep demo_check` we see our check's interval has changed to 45 seconds:

![alt text](dd_images/dd_18.png)

__Bonus Question__

One of the takeaways from editing our `demo_check.yaml` configuration is that we need not change `min_collection_interval` from within the Python file, rather we can do so on a per-instance basis by setting `min_collection_interval` in the yaml file instead.




