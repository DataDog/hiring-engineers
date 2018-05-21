## Prerequisites - Setting up!

I am working on an early 2015 MacBook Pro on macOS High Sierra (10.13.4), and spun up a virtual machine using Virtual Box and the Vagrant Ubuntu environment. I simply followed the installation instructions on the docs, but here's the TLDR:

1. Download and install [Virtual Box](https://download.virtualbox.org/virtualbox/5.2.10/VirtualBox-5.2.10-122088-OSX.dmg "Download VirtualBox for macOS")  and [Vagrant](https://releases.hashicorp.com/vagrant/2.1.1/vagrant_2.1.1_x86_64.dmg "Download Vagrant for macOS").

2. Make a directory where you'd like to do your work in (mine is called `datadog_vagrant`), `$cd` into this directory, and run:
```
$ vagrant init hashicorp/precise64
$ vagrant up
$ vagrant ssh
```
You should now see `vagrant@precise64:~$` in your terminal.

3. Create a Datadog account and all that jazz by clicking on the "Get Started Free" button at the top right of the data dog site. A form should come up.
<details>
  &nbsp;&nbsp;&nbsp;&nbsp;<summary>It should look like this...</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/create_account_form.png></img>
</details>

4. Now install curl by running `sudo apt-get install curl` and then run the sweet, sweet command on the DataDog docs:
```
DD_API_KEY=3840599a1d800170269b6a93c2471c73 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
It's always delicious to see when things work. If everything goes according to plan, you'll see this message in your terminal:
<details>
  <summary>Installation Confirmation Image</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/DDAgent_confirmation.png></img>
</details>

## Collecting Metrics
**Adding some tags using the configuration files!**

So, as per your Datadog's [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/), I found the yaml file by `$cd`-ing into the `/etc/datadog-agent/conf.d` directory and opening up the `datadog.yaml` using vim (after installing vim with `sudo apt-get install vim`).

<details>
  <summary>See image here</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog.agent.png></img>
</details>

<br>Because the file is a readme (that I didn't have the permissions to update and save the file, I ran `sudo vim datadog.yaml` and added some tags:

```
- tag1:value1
- tag2:value2
- tag3:value3
```
<details>
  <summary>Updated tags in `.yaml` file</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog.agent_addedtags.png></img>
</details>
<details>
  <summary>This is what rendered in the UI</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/datadog_hostmap_tags.png></img>
</details>

<br>However, it took me a little time to figure out that I had to restart the agent for the tags to happen. Whoops. And also... that I totally overlooked the whole "You see both forms in the `yaml` configuration files, but for the `datadog.yaml` init file only the first form is valid." (referring to the format below):

```
tags: key_first_tag:value_1, key_second_tag:value_2, key_third_tag:value_3
```

heh... so I updated the file to the correct format...

<details>
  <summary>Corrected `.yaml` file</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog_addedtags_correct.png></img>
</details>
And here's what it looked like in the UI.

<details>
  <summary>Hostmap tags</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/datadog_hostmap_tags_correct.png></img>
</details>
<details>
  <summary>Charts</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/datadog_hostmap_charts.png></img>
</details>

<br>Kewl. Next!

**Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

Since PostgreSQL is the only database we learned at GA, I installed this by running the following commands in my root directory:

```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install postgresql postgresql-contrib
```

I ran into a little speed bump here as I was receiving an authentication error, and needed to alter the authentication config file... so I did! I ran `$ sudo nano /etc/postgresql/9.1/main/pg_hba.conf` and wrote `local all postgres peer`, which...according to [this handy site](https://chartio.com/resources/tutorials/how-to-set-the-default-user-password-in-postgresql/), this is an authentication rule that "simply tells Postgres that for local connections established to all databases for the user postgres, authenticate using the peer protocol." Then I ran `sudo -u postgres psql` and was in!

Aaannnddd back to the docs. So I created a user with proper access to my PostgreSQL server by running the commands
```
create user datadog with password '<PASSWORD>';
grant SELECT ON pg_stat_database to datadog;
CREATE DATABASE pg_stat_database;
```

Then, I ran the permissions:
```
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);"
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

After I entered the password...
<details>
  <summary>Here's what my terminal looked like</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+password.png></img>
</details>

<br>Then edited the `conf.yaml` file in the `/etc/datadog-agent/conf.d/postgres.d` directory:
```
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: YBFne6UGENk9tpoqyQ84hMSJ
    dbname: pg_stat_database
#    ssl: False
#    use_psycopg2: False # Force using psycogp2 instead of pg8000 to connect. WARNING: psycopg2 doesn't support ssl mode.
    tags:
       - optional_tag1
       - optional_tag2
```

I restarted the agent.

Man I love when things just work out:
<details>
  <summary>Image of postgres Status in terminal after running `sudo datadog-agent status`</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+status.png></img>
</details>
<details>
  <summary>Image of postgres in UI</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+install.png></img>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+hostmap.png></img>
</details>

**Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**
As per the [Datadog docs](https://docs.datadoghq.com/agent/agent_checks/), I `cd`d into `/etc/datadog-agent/conf.d` and created a `my_metric.yaml` file, and a `my_metric.py` file in the `etc/datadog-agent/checks.d`. To start, I simply used the example in the docs. Then, after some googling what the syntax should be for Javascript's "math.random()" in Python, I declared a global variable (`random`) and called the python method `randomint(0,1000)`.

In `my_metric.yaml`:
```
init_config:

instances:
    [{}]
```

And in `my_metric.py`:
```
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric',random.randint(0,1000))
```

<details>
  <summary>And here's what the UI looks like:</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/my_metric_UI.png></img>
</details>

Change your check's collection interval so that it only submits the metric once every 45 seconds.
As per your docs, I edited the `my_metric.yaml` file under `init_config` by including `min_collection_interval: 45`:
<details>
  <summary>my_metric.yaml</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/my_metric_yaml+45+sec.png></img>
</details>
<details>
  <summary>Metric with 45 seconds in UI</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/my_metric_yaml+46+sec_UI.png></img>
</details>

**Bonus: Can you change the collection interval without modifying the Python check file you created?**
Hm, because this is a bonus question, I'm fairly certain I could have done this wrong, as I _ONLY_ updated the `yaml` file.

## Visualizing Data

**Utilize the Datadog API to create a Timeboard that contains:**
+ **Your custom metric scoped over your host.**
+ **Any metric from the integration on your Database with the anomaly function applied.**
+ **Your custom metric with the rollup function applied to sum up all points for the past hour into one bucket.**

This one seemed like a lot, here are the steps I took:

1. Read the [docs](https://docs.datadoghq.com/api/?lang=python#timeboards).

2. Since it looks like we'll need an `APP KEY`, I had to generate one of those in my dashboard when I go to Integrations--APIs.
<details>
  <summary>Here's where to look</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/app+keys.png></img>
</details>

3. I used Postman to help with this as per this [tutorial](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs). I was able to add a couple of graphs via Postman.
<details>
  <summary>Here's what my postman interface looked like</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postman.png></img>
</details>
And the request script:

```
{
      "graphs" : [{
          "title": "Custom Timeboard: Metric over Host",
          "definition": {
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ]
          },
          "viz": "timeseries"
      },{
          "title": "PSQL with Anomaly",
          "definition": {
              "requests": [
                  {"q": "anomalies(avg:postgresql.commits{*}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      },{
         "title": "Rollup",
         "definition": {
             "requests": [{"q": "avg:my_metric{*}.rollup(sum, 3600)"}]
         },
          "viz": "timeseries"
      }],
      "title" : "Custom Timeboard: Hiring Exercise",
      "description" : "Timeboard",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
```

<details>
  <summary>Here's the dashboard showed that I had added a new timeboard</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/dashboard_custom+timeboard.png></img>
</details>
<details>
  <summary>And the actual timeboard graphs</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/custom+timeboard_graphs.png></img>
</details>

I found the [Anomaly function here](https://docs.datadoghq.com/graphing/miscellaneous/functions/#anomalies), and [Rollup function here](https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup).

**Set the Timeboard's timeframe to the past 5 minutes**
This wasn't quite as intuitive for me, but I figured it out. I had to click on the graph and drag to zoom in on a 5 minute timeframe.
<details>
  <summary>Image</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/5+minutes.png></img>
</details>

**Take a snapshot of this graph and use @notation to send it to yourself**
I referenced [this post](https://www.datadoghq.com/blog/real-time-graph-annotations/) to create this notation.

1. Click on the graph, and select _Annotate this graph_
  <details>
    <summary>Image</summary>
    <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/annotate+this+graph.png></img>
  </details>

2. Send email using @notation in the comments:
  <details>
    <summary>Comments section</summary>
    <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/%40notation.png></img>
  </details>
  <details>
    <summary>Email received in inbox!</summary>
    <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/email.png></img>
  </details>

**Bonus: What is the Anomaly graph displaying?**
Okay, according to your docs, the anomaly detection is the "algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past." The literal "grey area" on the graph are its bounds, set to two-- and the red parts of the line indicate when the values are outside of that range...I believe.

Phew. Next!

## Monitoring Data
Create a new metric monitor that watches the average of `my_metric` and will alert if it's above 800 and warn above the threshold of 500. Also notify you if there's No Data in the query over the past 10 minutes.

1. Go to Monitors-- New Monitor in the dashboard nav. Here's the form with the filled out fields:
<details>
  <summary>Image</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/threshold+form.png></img>
</details>

2. Receive that email!
<details>
  <summary>Image</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/email2.png></img>
</details>

**Bonus**
**Scheduling downtime for 7p-9a daily on M-F**
**Downtime all day Sat-Sun**

1. Go to _Manage Downtime_ on the top nav.
  <details>
    <summary>See here</summary>
    <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/downtime_menu.png></img>
  </details>

2. Fill out fields as needed on form.
  <details>
    <summary>See here</summary>
    <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/downtime_form.png></img>
  </details>

3. Get those email alerts!
  <details>
    <summary>Downtime for M-F</summary>
    <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/downtime+email+alert+1.png></img>
  </details>
  <details>
    <summary>Downtime for Sat-Sun</summary>
    <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/downtime+email+alert+2.png></img>
  </details>

## Collecting APM Data
Annnddd.... time to read the [Datadog docs for APM Data](https://docs.datadoghq.com/tracing/setup/)...

1. Follow the [Flask docs](http://flask.pocoo.org/docs/1.0/installation/#python-version) to create your virtualenv environment.

2. In my `datadog.yaml` config file (which can be found in the `etc/datadog-agent` directory), I enabled the `apm_config:` key to be set to `true`.
```
apm_config:
  enabled: true
```

3. After activating the environment by running `$ . venv/bin/activate`, I ran `pip install ddtrace` and `ddtrace-run python apmapp.py` (`apmapp.py` is the file I created for the Flask app below)
```
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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
    app.run()
```
Here's where I've run into a hiccup and got this error:
<details>
  <summary>Error image</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/error.png></img>
</details>

<br>Now, after going down some rabbit holes and some digging around on the interweb, creating a new Flask app in a different directory just to make sure I wasn't missing any steps, I tried again and got the same errors. I figured it had something to do with how the ports were set up. So, aftermore digging and [research on Flask apps](https://www.tutorialspoint.com/flask/flask_application.htm) and the `.run()` method, I figured I could try setting the port in my `.py` file with the following:
```
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8126)
```
<details>
  <summary>Now, I tried running the `ddtrace-run` command again, I got this crazy thing happening</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/error2.png></img>
</details>

<br>To me, it looks like a connection is still refused from localhost 8126, tried to call the endpoint, but recieved a `404` error instead. I also saw that the error might have been lookign for the blinker middlewear. So, I installed the Blinker middlewear, edited my `apmFlask.py` file, and ran `python apmFlask.py`. This removed the middlewear error, but still no connection.
<details>
  <summary>See Error here</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/error3.png></img>
</details>

## Final Question
**Is there anything creative you'd use datadog for?**
In January, [Strava accidentally exposed secret military bootcamps based on their activity hot spots](https://www.theguardian.com/world/2018/jan/28/fitness-tracking-app-gives-away-location-of-secret-us-army-bases)... I found this incredibly interesting, and I would love to take this a step further into a cultural realm.
I am pretty passionate about living a balanced, healthy lifestyle. Having an apple watch and being a part of a fairly modern gym with its own tracking app keeps me accountable. I know this might seem like a stretch, or maybe even something that already exists, I would love to see an integration to help monitor not only motion and fitness, but activity on social media accounts, location checkins (foursquare, instagram), seamless orders, grocery orders, spending/budgeting, and sleep-- honestly, something along the lines of [gyrosco.pe](https://gyrosco.pe/). But--the information would be shared in the similar way that Strava shares its hot-spotting activity. I think there's a lot we can learn about ourselves and our values if we see the amount of time spent on different things based on region.
