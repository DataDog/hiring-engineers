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

## Creating a Timeboard with the Datadog API

To glean visual insights from our `my_metric` check, look for anomalous metrics coming from our database, or perform computations on metrics to customize the data on your dashboard, use the `Timeboard` endpoint from the [Datadog API](https://docs.datadoghq.com/api/?lang=python#timeboards)

We're going to use Python3 to create a script to:

- Scope `my_metric` over the `ubuntu-xenial` host

- Look for anomalies in the number of rows returned in the database created earlier

- Use a rollup function to add up the last hour's data points from the `my_metric` check

First, go to your [Datadog account's API page](https://app.datadoghq.com/account/settings#api) to generate an Application Key to give the script access to the Datadog API. Scroll down to Application Keys, enter a name for your new key, then click Create Application Key.


Next, install pip3 and the required libraries:

`apt-get install python3-pip`

`pip3 install datadog datadog_checks_base prometheus_client`


Now create a file called `demo_timeboard` in your preferred directory with `touch demo_timeboard.py`, open the file in your text editor, and add your API and App keys.


```python

from datadog import initialize, api
  
options = {
    'api_key': '<YOUR_API_KEY>',
    'app_key': '<YOUR_APP_KEY>'
}

initialize(**options)

title = "My Timeboard"
description = "Timeboard for my_metric and Postgres."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:ubuntu-xenial}"}
            ],
        "viz": "timeseries"
    },
    "title": "my_metric"
},

{
    "definition": {
        "events":[],
        "requests": [
            {"q": "anomalies(avg:postgresql.rows_returned{host:ubuntu-xenial}, 'basic', 1, direction='above')"}
            ],
        "viz": "timeseries"
        },
    "title": "Postgres rows returned"

},

{

    "definition": {
        "events":[],
        "requests": [
            {"q": "my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
            ],
        "viz": "timeseries"
        },
    "title": "Sum of all points for my_metric over the last hour"

}]

template_variables = [{
    "name": "ubuntu-xenial",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```


A few things to note about this code:

- The line `{"q": "my_metric{host:ubuntu-xenial}"}` denotes a request query for `my_metric` on the `ubuntu-xenial` host.

- `{"q": "anomalies(avg:postgresql.rows_returned{host:ubuntu-xenial}, 'basic', 1, direction='above')"}` -- This query looks for anomalies in the database within the scope of the `ubuntu-xenial` host. Specifically, it's checking to see if the number of rows returned is one standard deviation above the normal value observed in the past. `basic` denotes the algorithm used to detect anomalies, which as the name implies is the most basic of the three detection algorithms available:

![alt text](dd_images/dd_19.png)

- `{"q": "my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}` -- This query seeks the sum of all points returned in the last hour for `my_metric`, scoped over the `ubuntu-xenial` host. The `rollup` function aggregates data over a time period you specify. You can choose to aggregate by average (`avg`), maximum (`max`), minimum (`min`), or sum (`sum`). For the example you'll want the sum of all points for the last hour, thus the call to `rollup(sum, 3600)` on `my_metric`.

- `"viz": "timeseries"` -- All of these graphs use a timeseries to visualize the data, which will show the evolution of a given metric over a time window you define. There are numerous [options for data visualization](https://docs.datadoghq.com/graphing/dashboards/widgets/).

Save and close the editor and run `python3 demo_timeboard.py` to execute the script. 


## Viewing the new timeboard

Head to the [Dashboard list](https://app.datadoghq.com/dashboard/lists) and click on the newly created timeboard. You'll see the three graphs defined in your script. Looking at the __Postgres rows returned__ graph, you can see an increase in the number of rows returned beginning at the 23:00 mark, with the anomalous data showing in red:


![alt text](dd_images/dd_20.png)

At the top right of the timeboard you'll see the available default time intervals. You can customize these time intervals by pressing alt+] to decrement or alt+[ to increment the interval, all the way down to a five minute window. Depending on your browser you may have issues with the decrement/increment feature -- it didn't work on my locked-down version of Firefox, but worked flawlessly on Safari.

## Taking a snapshot of a graph

Perhaps you find something on a graph that sticks out and you'd like to notify other members of your team. Hover your mouse over the graph to locate the camera icon:

![alt text](dd_images/dd_21.png)

Click the camera, and a text box will appear. Enter a comment and use `@` to mention a member of your team. Once you've finished, press return and a notification will appear letting you know a screenshot has been created. The team member you mentioned in your comment will receive an email containing the comment, the name of the graph in question, and the screenshot of the graph:

![alt text](dd_images/dd_22.png)

__Bonus Question__

The anomaly graph is displaying the variance in the behavior of a metric at a specific point compared to previously observed points. As shown above there are three different algorithms available to detect these variances.

