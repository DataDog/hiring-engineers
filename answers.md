# Prerequisites - Setup the environment

To complete this exercise I had to download both [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

After downloading both of these programs I had to install them. Using the Vagrant [Docs](https://www.vagrantup.com/intro/getting-started/project_setup.html) I figured out the commands to install them were:

1. Make a directory (which I already have one since I have this repo.)
2. `vagrant init bento/ubuntu-16.04` to create a Ubuntu 16.04 VM
3. `vagrant up` to start the VM
4. `vagrant ssh` to use the VM


After vagrant has finished installing, I signed up for Datadog and I navigated to the Integrations Tab --> Agent Tab --> Ubuntu Tab.
![install_1](./screenshots/install_1.png)


In this tab  you will see that Datadog gives you a on line command to type into your terminal to install the client.
`DD_API_KEY={YOUR_API_KEY} bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

After you've typed this into the terminal that's running Vagrant, your terminal should look like this :

![install_2](./screenshots/install_2.png)

# Collecting Metrics

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I didn't really know what a tag was or how to implement it so I had to check out the [Tag Docs](https://docs.datadoghq.com/tagging/assigning_tags/?tab=go) which showed me how to  implement a tag using the terminal.

1. You have to `cd ..` until you hit the root directory of the VM.
2. Then navigate to `/etc/datadog-agent` . In this directory you'll find a file named `datadog.yaml`.
3. Vagrant has a built in editor named nano that we can use. We can open the file with `sudo nano datadog.yaml` You need to include the `sudo` or else you won't have permissions to change the file!

These are my tags :

![host_map_1](./screenshots/host_map_1.png)

Upon saving these changes , you have to restart the agent using `sudo service datadog-agent restart`. After you've restarted the agent, you can go to the Datadog web application and click the Infrastructure then click Host Map to see your tags.

This is how it should appear :

![host_map_2](./screenshots/host_map_2.png)

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

The database I chose to install was PostgreSQL since I have experience using this the most . To install Postgresql on Ubuntu I simply had to refer to the [PostgreSQL docs](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04). Here I was able to find the commands needed to install and run PostgreSQL.

1. `sudo apt-get update`
2. `sudo apt-get install postgresql postgresql-contrib`

Now that I've downloaded and installed PostgreSQL I can now head over to the Datadog web applications and look under Integrations to find PostgreSQL.

![postgreSQL_1](./screenshots/postgreSQL_1.png)

The directions on the Integration told to me to do the following steps :

1. create user datadog with password ( press the generate password key and your password will show up)
2. grant SELECT ON pg_stat_database to datadog;
3. I then had to navigate to `/etc/datadog-agent/conf.d/postgres.d` where I found the `conf.yaml.example` file.
4. I opened the editor using `sudo nano conf.yaml.example` and made some changes.

![postgreSQL_2](./screenshots/postgreSQL_2.png)

5. I then pressed `control x ` and nano asked me to save. I clicked yes and then renamed the file `conf.yaml` since it's no longer an example and something I need to use.

6. I restarted the Datadog Agent and ran a status check by running `sudo datadog-agent status`, and the PostgreSQL integration check was successful.

![postgreSQL_3](./screenshots/postgreSQL_3.png)

After that I went back into the browser and finished installing the PostgreSQL Integration.

![postgreSQL_4](./screenshots/postgreSQL_4.png)


## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Upon reading the [Writing a custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) I had to create two files

1. A Check file (which is just a regular python file) that needs to be created in the `/etc/datadog-agent/checks.d` directory.
2. A YAML configuration file that needs to be created in the `/etc/datadog-agent/conf.d` directory.

The first thing I did was create a Check file named `my_metric.py` which contains code found in the aforementioned docs. It looks like this :

![my_metric_1](./screenshots/my_metric_1.png)

The YAML configuration file named `my_metric.yaml` looks something like this , for now :

`instances: [{}]`

Even though it's empty , for now , it is quite necessary to have in your configuration file.

I restarted the Datadog Agent. my_metric check is successfully being submitted after checking with `sudo datadog-agent status`.

![my_metric_2](./screenshots/my_metric_2.png)

## Change your check's collection interval so that it only submits the metric once every 45 seconds.

All I had to do here was go back into my YAML config file named `my_metric.yaml` and add some things in. Now my YAML file looks like this:

![my_metric_3](./screenshots/my_metric_3.png)

The only way I was able to check if this was indeed working was running `sudo datadog-agent status` and timing when the total run count  incremented. Upon testing this a few times, it was indeed  updating around 45 seconds.


## Bonus Question Can you change the collection interval without modifying the Python check file you created?

By changing my check's collection interval in the YAMl file , I never had to modify my Python file that I have created.


# Visualizing Data

## Utilize the Datadog API to create a Timeboard that contains:

1. Your custom metric scoped over your host.
2. Any metric from the Integration on your Database with the anomaly function applied.
3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket


So upon looking at the [Datadog Api Docs](https://docs.datadoghq.com/api/?lang=python#timeboards) I figured out that to use the Datadog Api, I have to first install it (DUH!)

To do this I have to first install pip onto my operating system.

`sudo apt-get install python-pip`

Once pip is installed I have to install Datadog.

`pip install datadog`

Next, Datadog API takes in two keys . The "api_key" and the "app_key". We have the API key but we have to go generate our app_key. We navigate on our browser to Integrations and then API and you'll see  where it says generate app_key.

Once you've generated your app_key we create this [Python file](https://github.com/EliasAHH/hiring-engineers/blob/Juan_Solutions_Engineer/codeanswers/timeboard.py) and run `python timeboard.py` in our terminal.

Resources I used to complete this code were :

1. [Anomalies](https://docs.datadoghq.com/monitors/monitor_types/anomaly/)
2. [Graphing](https://docs.datadoghq.com/graphing/)
3. [PostgreSQL](https://docs.datadoghq.com/integrations/postgres/)
4. [Timeboards](https://docs.datadoghq.com/api/#timeboards)


After running the `python timeboard.py ` command I went to my dashboard to see if it was created . Indeed it was :

![datadog_timeboard](./screenshots/datadog_timeboard.png)

When I click the timeboard, three graphs are displayed .

![timeboard_1](./screenshots/timeboard_1.png)

##Once this is created, access the Dashboard from your Dashboard List in the UI:

## Set the Timeboard's timeframe to the past 5 minutes

The only way to actually obtain the 5 minute goal is to manually click on the graph it self and move it until you've reached 5 minutes .

![timeboard_2](./screenshots/timeboard_2.png)

## Take a snapshot of this graph and use the @ notation to send it to yourself.

There's a camera button on the top right of the graph you're currently on . Click that to take a snapshot.

![timeboard_3](./screenshots/timeboard_3.png)


Here's the email I received from it.

![timeboard_4](./screenshots/timeboard_4.png)

## Bonus Question: What is the Anomaly graph displaying?

The Anomaly graph is displaying the maximum number of connections to my PostgreSQL database and would tell me if there are any abnormalities. My graph at the moment is showing the max number of 100  and since it's all blue lines it means there are no abnormal behaviors at the moment


# Monitoring Data

## Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

1. Warning threshold of 500
2. Alerting threshold of 800
3. And also ensure that it will notify you if there is No Data for this query over the past 10m.


With the help of the Datadog monitoring [docs](https://docs.datadoghq.com/monitors/) I was able to set up my monitor.

I first Navigated to the Monitors --> New Monitor --> Metric Tab on the left.

I then had to complete the information.

![alert_1](./screenshots/alert_1.png)

## Please configure the monitor’s message so that it will:

1. Send you an email whenever the monitor triggers.
2. Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
3. Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![alert_2](./screenshots/alert_2.png)

Here are my emails I received for both alerts.

![alert_3](./screenshots/alert_3.png)

![alert_4](./screenshots/alert_4.png)


## Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

1. One that silences it from 7pm to 9am daily on M-F,
2. And one that silences it all day on Sat-Sun.


7pm to 9am Daily :

![downtime_week](./screenshots/downtime_week.png)

Sat-Sun

![downtime_weekend](./screenshots/downtime_weekend.png)


## Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


Weekly Alert

![downtime_1](./screenshots/downtime_1.png)


Weekend Alert
![downtime_2](./screenshots/downtime_2.png)


# Collecting APM Data:

Using the Datadog APM [docs](https://docs.datadoghq.com/tracing/setup/#agent-configuration) I figured out how to set up my config files to start tracing .

1. Edit the `datadog.yaml` file to enable trace collection for the Trace Agent and configure the environment

It should look something like this

![config_file](./screenshots/config_file.png)

2. Next we have to install flask since we need to use it for this part of the challenge

`pip install flask`

3. Now we need to install the trace

`pip install ddtrace`

4. Next we create a file [app.py](https://github.com/EliasAHH/hiring-engineers/blob/Juan_Solutions_Engineer/codeanswers/app.py) that stores the flask file we were given.

5. Next run `ddtrace-run python app.py`

6. After running the ddtrace you now have access to port 5050 . You can open the terminal and start navigating to these routes

`curl localhost:5050/`
`curl localhost:5050/api/apm`
`curl localhost:5050/api/trace`

## Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

According to the Datadog graphing [docs](https://docs.datadoghq.com/graphing/dashboards/#what-is-the-difference-between-a-screenboard-and-a-timeboard) the best way for us to share our dashboard is to use a screenboard .

In the screenboard , we created timeseries for three different things :

- system.cpu.user (The percent of time the CPU spent running user space processes)
- system.net.bytes_sent (The number of bytes sent from a device per second)
- trace.flask.request.hits (The number of flask requests made)

After creating this we generate the url at the top right  part of your screen
 [Juan's Screenboard](https://p.datadoghq.com/sb/9e1e0d971-ac0446e91a294cce2bb434f7e8384920)


Screenshot of a dashboard

![flask](./screenshots/flash.png)

## Please include your fully instrumented app in your submission, as well.

[App](https://github.com/EliasAHH/hiring-engineers/blob/Juan_Solutions_Engineer/codeanswers/app.py)



## Bonus Question: What is the difference between a Service and a Resource?

A Service is made up of set of processes that work together to provide a feature set. For instance, a simple web application may consist of a few services database services , webapplication services , query services. Essentially things that help users obtain information.

A resource is a particular query to a service. An example of this would be an SQL query(SELECT * from Authors) or trying to access a patricular route (/home)


# Final Question:

## Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?

 Coming from an area where crime rate is high you have to learn to adapt fast. Datadog can help with this by monitoring high crime rate areas. We can monitor places that were affected, times that these crimes happed and the victims targeted by these crimes. . With this technology hopefully we can help predict times in which the most crime has happened and areas to help people avoid them and hopefully minimize the amount of illegal activities that occur.
