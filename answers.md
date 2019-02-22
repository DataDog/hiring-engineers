# Solutions Engineer - Brendan McIlhenny
## Mac Computer Setup using Vagrant

First things first, let's download Vagrant [here](https://www.vagrantup.com/docs/installation/) and follow the prompts like any other program, which will install a Vagrant Linux Ubuntu virtual machine on my Mac laptop running MacOS Mojave.

What does Vagrant do? When dev teams are working on different operating systems and have different dependencies and you're all working on the same project, collaborating is bound to get annoying really fast. That's where Vagrant comes in. It creates an all encompassing environment using the same configurations regardless of all of these OS/ language/library versions and dependencies. With Vagrant installed I created a new folder that would serve as Root to this project and changed into it:

```
cd Development

mkdir datadog-code-challenge

cd datadog-code-challenge
```

According to the Vagrant docs I  then needed to run the command `vagrant init hashicorp/precise64` then `vagrant up`, which would build a box to hold my environment configurations but `vagrant up` gave me this error:

```
No usable default provider could be found for your system.

Vagrant relies on interactions with 3rd party systems, known as
"providers", to provide Vagrant with resources to run development
environments. Examples are VirtualBox, VMware, Hyper-V.

The easiest solution to this message is to install VirtualBox, which
is available for free on all major platforms.

If you believe you already have a provider available, make sure it
is properly installed and configured. You can see more details about
why a particular provider isn't working by forcing usage with
`vagrant up --provider=PROVIDER`, which should give you a more specific
error message for that particular provider.
```
Hmm, first roadblock but a clue! As the error message reads above, Vagrant did not have a default "provider", which serves programs like Vagrant resources to run development environments. So I went over [here](https://www.virtualbox.org/) to download Virtualbox and followed the prompts to get it up and running.

Let’s try this again.

`vagrant init hashicorp/precise64`then a `vagrant up`. Success! Since Vagrant runs the virtual machine you have to ssh into it with the command `vagrant ssh`.

![vagrant ssh](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/ssh.png)

## Collecting Metrics
With the vm all set and ready to go it's now time to install the agent. Head over to the datadog UI (https://app.datadoghq.com/account/settings#agent/ubuntu) for instructions on installing the agent. Since my virtual machine is running Ubuntu I chose the Ubuntu option and ran the commands inside my ssh'ed instance:

```
DD_API_KEY=<MY-API-KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/install_dd_agent.png)

I then got the error:
```
the program 'curl' is currently not installed.  You can install it by typing: sudo apt-get install curl
```
So I ran `sudo apt-get install curl` and installed curl in the virtual machine. This took about 10 seconds then I reran the simple one line installation again, then once the agent installed I started the agent up with the command `sudo service datadog-agent start`. And that's it for setup.

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/run_agent.png)


First step of the actual assignment is I needed to add some tags by manipulating the `datadog.yaml` configuration file. according to datadog’s docs, the configuration file is located at /etc/datadog-agent/datadog.yaml file. I'd change the documentation here slightly by explicitly stating to navigate to the file or changing the command box to something more explicit like `sudo nano /etc/datadog-agent/datadog.yaml`. I was not familiar with Linux commands before this exercise and was left scratching my head thinking what the command `/etc/datadog-agent/datadog.yaml` meant. If it's a command I'd expect something to happen when I ran `/etc/datadog-agent/datadog.yaml`.

So I ran `sudo nano /etc/datadog-agent/datadog.yaml` and this opened up a simple text editor in the vm itself so I could change the configuration file to add my host's tags. I ran into some issues here with tags not showing up so I poked around the datadog agent docs (https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6) and found that I could run the command `sudo service datadog-agent status`. I got a helpful message saying my config file could not be parsed properly, meaning the syntax I used to add tags was incorrect.  It took some finagling to get this part to work as I had to add the tags on one line like the image below. I'd make another recommendation here to change the docs to be more explicit about putting tags on one line like this winning combination:

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/tags.png)

Eventually I landed on the right syntax, restarted the agent with the command `sudo service datadog-agent restart` and my tags started showing up in the UI:

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/host_map_tags.png)

Next step was to install a database on my machine and run the corresponding integration for the datadog agent. I decided to use postgres for Linux Ubuntu, so I ran the command `sudo apt-get install postgres` courtesy of the postgres docs (http://postgresguide.com/setup/install.html).

According to the docs, this installation procedure created a user account called postgres that is associated with the default Postgres role. In order to use Postgres, we can log into that account. So I switched over to the postgres account on your server by typing `sudo -i -u postgres`, then I navigated over to the datadog integrations tab, found postgres, clicked on it, then clicked on the configuration tab and followed the prompts.

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/postgres_1.png)
![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/postgres_2.png)

Next step was writing a custom agent check that submits a metric named my_metric with a random value between 0 and 1000, then changing the collection interval so that it only submits the metric once every 45 seconds. Using these docs as reference (https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6), I navigated to the `/etc/datadog-agent` directory where the `checks.d` folder was located and created the file `custom_my_metric.py` where I was to define my check, a check that would return a metric named "my_metric" with a random value between 0 and 1000. My file looked like this:

```
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

import random

class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1001))
```

I then navigated to the `/etc/datadog-agent/conf.d` directory where I put my custom check configuration file `custom_my_metric.yaml` with the following code:

```
init_config:

instances:
    -   min_collection_interval: 45
```

As the instructions said and as the documentation read, you can change the minimum collection interval by specifying a number of seconds (45). In this case the my_metric metric could be collected every 45 seconds. I ran into some issues finding the checks.d folder as well as the conf.d folder and I'd recommend putting a corresponding file structure map on these parts of the docs that rely on the datadog-agent file structure that shows the user where all of these important folders are located.

## Visualizing Data

Next up was creating a time board via the API. I noticed via the docs that in order to use the API I not only needed my API key, which was automatically generated for me when I signed up for Datadog but I also needed to have an application key in order to write to my Datadog app. So I generated a new application key to be used in my ruby script via the Integrations > API tab:

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/app_key.png)

I then wrote a simple Ruby script based off the examples provided in the API Dashboard section of the docs (https://docs.datadoghq.com/api/?lang=ruby#dashboards) with the my_metric scoped over the host (`my_metric{host:precise64}`), the anomaly function applied to my database's postgresql.bgwriter.buffers_backend{*} (anomalies(postgresql.bgwriter.buffers_backend{*}, 'basic', 2)), and the  my_metric with the rollup function applied to sum up all the points for the past hour into one bucket (my_metric{*}.rollup(sum, 3600)), the 3600 here representing 3600 seconds in an hour.

```
require 'pry'
require 'dogapi'

api_key = <MY-API-KEY>
app_key = <MY-APP-KEY>

datadog_timeboard = Dogapi::Client.new(api_key, app_key)

title = "Brendan's Code Project Timeboard"
widgets = [{
    "definition": {
        "type" => "timeseries",
        "requests" => [
            {"q" => "my_metric{host:precise64}"},
            {"q" => "anomalies(postgresql.bgwriter.buffers_backend{*}, 'basic', 2)"},
            {"q" => "my_metric{*}.rollup(sum, 3600)"},
        ],
        "title" => "my_metric scoped over host, my_metric with rollup(1 hour) and postgresql anomalies"
    }
}]
layout_type = "ordered"

description = "A dashboard with code challenge info."
is_read_only = true
notify_list = [<MY-EMAIL>]
template_variables = [{
    "name" => "host1",
    "prefix" => "host",
    "default" => "my-host"
}]

config = {
  "description" => description,
  "is_read_only" => is_read_only,
  "notify_list" => notify_list,
  "template_variables" => template_variables
}

datadog_timeboard.create_board(title, widgets, layout_type, config)
```

My script ran without any errors so I went back to the UI and saw my Timeboard.

![install agent](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/postgres_2.png)

I did some reading up on the anomaly detection function and what it does is it looks for weird behavior for a metric given how the metric performed in the past. For instance, Philadelphia Eagles legendary Super Bowl LII winning quarterback Nick Foles plays extremely well in the post season given his past historical performance. If he went out there for the NFC championship and threw 10 picks and threw for 0 touchdowns the anomaly function would catch this. That being said, I was forced to use the basic version of the anomaly algorithm as recommended by the docs given I don’t have much historical data for my database and the other versions are best with plentiful historical data.

```
Basic uses a simple lagging rolling quantile computation to determine the range of expected values. It adjusts quickly to changing conditions but has no knowledge of seasonality or long-term trends.
```

The instructions told me to change the timeframe to the last 5 minutes, I tried to change the timeframe to the last 5 minutes in the top right time interval bar but was not able to find an option smaller than the past 1 hour. So I went over to the Datadog youtube page and watched the Datadog 101 series and saw that if I clicked and dragged on a Timeboard I could change the time of that board to whatever interval I wanted. Once I adjusted the time I clicked on the snapshot button at the top of the board, tagged myself then received an email notification with that Timeboard. Here's an image of the Timeboard with the past 5 minute time interval as well as the notification I received when I tagged myself after highlighting the last 5 minutes of activity for the Timeboard:

![tag myself](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/tag_myself.png)
![email notification past 5 minutes](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/email_past_5_min.png)

## Monitoring Data

Setting up the monitor was very straight forward. Using the markdown and the simple if/if not logic I had the monitor set up to trigger a warning when the value was 500, an alert when it was above 800 and a notice when no data with different notification bodies for each type of monitor.
![monitor](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/notification_body.png)

Also, checked the box to make sure I was alerted when no data was coming in for the past 10 minutes.
![no data alert](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/no_data.png)

But then noticed that the alert was a) not triggering even though the directions explicitly said wait for avg to trigger an 'alert' so changed it from 'avg' to 'at least once' so I could at least get the picture of the email for the hiring challenge but more importantly b) the template variable {{host.ip}} wasn’t returning anything in the email, it came back blank. So I added host:precise64 to the `define the metric` section and then it starting to work:

![host ip email alert](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/my_metric_alert_host_ip.png)

Here's a screenshot of me changing the monitor to trigger when the threshold reaches a level of 800 or higher using the "at least once" threshold to get it to trigger:
![host ip](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/avg_threshold_vs_only_once.png)

######Bonus Question
In order to set up the downtime, I went to the UI and first was a bit confused because there was no option to set a weekly recurring downtime on the UI where I could check physical days. I'd suggest to add a little toggleable question bubble next to the days to make it more obvious that that's how you set weekly reminders. I started messing around with the time options and eventually found the weekly option.

Here are the screenshots of the downtime emails as well as the settings page for each downtime.

Weekend downtime Sat Sun all day:
![host ip](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/down_time_sat_sun.png)
![weekend downtime setting](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/weekend_downtime_setting.png)

Weekly downtime 7pm - 9 am:
![host ip](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/downtime_weekly_mon_tue_wed_thur_fri.png)
![host ip](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/weekly_downtime_setting.png)

## Collecting APM Data

I copied and pasted the flask app included in the code challenge and followed the apm installation docs (https://docs.datadoghq.com/agent/apm/?tab=agent630#agent-configuration), however I ran into an issue during this section. I followed the directions by installing `pip install ddtrace`, but I kept getting the error:

```
vagrant@precise64:~$ pip install ddtrace
Downloading/unpacking ddtrace
  Cannot fetch index base URL http://pypi.python.org/simple/
  Could not find any downloads that satisfy the requirement ddtrace
No distributions at all found for ddtrace
Storing complete log in /home/vagrant/.pip/pip.log
vagrant@precise64:~$
```

I googled around and went down a few rabbit holes including one on a raspberry pi forum.

Someone suggested this:
"Found some entries for "pip-cannot-install-anything" indicating it could be a ssl-problem, so be sure your system is on current level ("sudo apt-get update" and then "sudo apt-get upgrade")."

So I tried those commands and things seemed to be happening, so I tried once again to install ddtrace using `sudo pip install ddtrace` but still the same error, shucks!

I found others on Stackoverflow and Github (https://github.com/pypa/pip/issues/4817) were having similar issues with pip in general so I tried to install a few random packages using pip but to no avail. I read on Stackoverflow that http was automatically blocked by pip in the most recent versions and that I should instead specify to download using the https version of pip "https://pypi.python.org/simple/" but that didn’t work either.

I tried `sudo pip install -v ddtrace -i https://pypi.python.org/simple/` and BOOM it started working!

I then ran ddtrace-run python my_app.py according to the APM install datadog docs (https://app.datadoghq.com/apm/install#) but got error:

```
Flask ImportError: No Module Named Flask
```

Ok, I thought. That one's easy.
```
sudo pip install -v flask -i https://pypi.python.org/simple/
```

Following the APM install docs I ran the command `ddtrace-run python my_app.py` and the flask app was finally running on 0.0.0.0:5050, but nothing changed on the Datadog UI. Here's a screenshot after running the `ddtrace-run python my_app.py command`:

![host ip](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/apm_running.png)


I went searching for some tracer logs to see what was up at `/var/log/datadog/trace-agent.log`.

![host ip](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/no_data_received_tracer.png)

A combination of no data received from the api as well as parsing errors in the yaml file. Decided to fix the yaml file first. According to the docs I had to configure my app to allow tracing by uncommenting the lines in my datadog.yaml file:

```
apm_config:
  enabled: true
```

Restarted the agent then looked back at the UI but still nothing seemed to change. Because I was ssh'ed into my instance I was trying to figure out how to visit the routes I had defined in the Flask app to see if phyisically visiting those resources would trigger a trace, but since there's no browser built into the command line environment I was using to navigate my virtual machine I started googling how to ping a site given that I knew this app was running at `0.0.0.0:5050`.

Enter `curl`.

First I had to download `curl` to curl into that port hoping that I would at least get a message in the tab I was running ddtrace in, and I was!

```
2019-02-21 20:58:34,602 - werkzeug - INFO - 127.0.0.1 - - [21/Feb/2019 20:58:34] "GET /api/apm HTTP/1.1" 200 -
2019-02-21 20:58:35,294 ERROR [ddtrace.writer] [writer.py:138] - cannot send spans to localhost:8126: [Errno 111] Connection refused
2019-02-21 20:58:35,294 - ddtrace.writer - ERROR - cannot send spans to localhost:8126: [Errno 111] Connection refused
```

Connection refused. My hypothesis was that my flask app wasn’t able to talk to my virtual machine I’ve sshed into running the datadog agent. To be sure I looked back at the ``/var/log/datadog/trace-agent.log` logs:

2019-02-21 20:24:53 INFO (main.go:160) - trace-agent running on host precise64
2019-02-21 20:24:53 INFO (api.go:140) - listening for traces at http://localhost:8126
2019-02-21 20:25:03 INFO (api.go:324) - no data received
2019-02-21 20:25:53 INFO (service_mapper.go:59) - total number of tracked services: 0
2019-02-21 20:26:03 INFO (api.go:324) - no data received

No data being received. My hypothesis is that there's a mismatch here, listening for traces at port 8126 but the app being traced was run on a different port and somehow i haven’t configured the two to know that. Back to google. Someone also had this error on Stackoverflow (https://stackoverflow.com/questions/49699969/datadog-errorddtrace-writercannot-send-services-to-localhost8126-errno-111) but the solutions offered were very unclear.

As a last ditch effort I tried using the Middlewareinstead of running the ddtrace-run function because the instructions said that you could use either the ddtrace-run or manually insert the Middleware. I ended up using this person's app as a blueprint to incorporate the Middleware: https://stackoverflow.com/questions/52390804/datadog-how-to-implement-ddtrace-on-flask-application. The file for the flask app is located in this repo at [my_app.py](./my_app.py).


I restarted the Datadog agent again, ran my new flask app without the built-in ddtrace-run function, sent a few curls to the host at port 5050 and BOOM, it started working! Finally, traces were showing up in the UI. Here is a a screenshot of the the traces getting logged to my vm's console.

![host ip](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/finally_reporting_traces.png)

Here's another one of the Datadog UI with infrastructure metrics and APM metrics on one timeboard as well. To get the APM trace metrics into a timeboard I first had to export the individual charts from the APM services section by clicking on APM > Services > Flask. Here's a link to my APM/Infrastructure dashboard: https://app.datadoghq.com/dashboard/ujx-h6v-9m9/dashboard-with-both-apm-and-infrastructure-metrics?tile_size=m&page=0&is_auto=false&from_ts=1550872080000&to_ts=1550875680000&live=true.

![host ip](https://raw.githubusercontent.com/bmcilhenny/hiring-engineers/master/images/trace_charts.png)


###### APM Bonus

APM agents monitor applications at the code level: where people are on your site, transactions, db queries, API calls and other things. Infrastructure monitors your hosts at the OS level: CPU, memory, etc.

With that context, a service is a piece of software that is self contained, such as a flask app. your flask app could be one service that makes up your online business, perhaps you have a shopify app that handles payments for your business. That would be another example of a service. A resource is a particular component of an individual service responsible for a task. For the instrumented flask app, the endpoints for the web app are resources as they correspond to a specific function is responsible for one thing.

##LAST QUESTION

######I think it would be cool to use Datadog to monitor your music listening habits and build out a profile/DNA.

I’m really interested in the types of music people listen to and the patterns you can infer from them. I grew up in Southern New Jersey so Bruce Springsteen is in my blood, but I attended high school in Philly and started really getting into r&b/hip hop and The Roots. Then I moved to New Orleans and got really into the Meters and the New Orleans funk movement. Geography plays a huge role in the types of music you’re exposed to, but it’s certainly not the only one. It would be super interesting to see how different factors like time, geography, seasonality, mood, weather, relationships piece together your music DNA and how you can use a combination of monitors, dashboards and algorithms to predict where you fit on the music spectrum, learn to predict what type of music you’d like, or maybe even find an ideal boyfriend/girlfriend.

You could use the Spotify API to record the music you and your friends/family listen to, the time they listened, the location they listened to it, and the weather at the time you listened and get data from an API that records when new music gets released. With a bigger picture of your listening context, you can use Datadog dashboards to see your personal distribution of music listens based on genre and learn to predict what types of music you gravitate towards. Do you listen to more depressing music in the winter methods like Radiohead? If so, are there outliers in the winter months that you can catch with monitors? Sounds like a good use for the the anomaly datadog algorithms. Are there certain relationships you can map out between people and the types of music they listen to?

Can you build out dashboards that prove that your friend’s music tastes rubbed off on you, which in turn you shared with your other friends who have now shared it with their friends? You could use monitors for health reasons. For instance set up a monitor to alert you when you’re listening to too uplifting music at night so that you won’t be too amped to fall asleep at night.
