Your answers to the questions go here.

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
  <summary>It should look like this...</summary>
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
+ Adding some tags using the configuration files!

⋅⋅⋅So, as per your Datadog's [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/), I found the yaml file by `$cd`-ing into the `/etc/datadog-agent/conf.d` directory and opening up the `datadog.yaml` using vim (after installing vim with `sudo apt-get install vim`).

<details>
  <summary>See image here</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog.agent.png></img>
</details>

⋅⋅⋅Because the file is a readme (that I didn't have the permissions to update and save the file, I ran `sudo vim datadog.yaml` and added some tags:

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

However, it took me a little time to figure out that I had to restart the agent for the tags to happen. Whoops. And also... that I totally overlooked the whole "You see both forms in the `yaml` configuration files, but for the `datadog.yaml` init file only the first form is valid." (referring to the format below):

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

Kewl. Next!

+ Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

⋅⋅⋅Since PostgreSQL is the only database we learned at GA, I installed this by running the following commands in my root directory:

```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install postgresql postgresql-contrib
```

⋅⋅⋅I ran into a little speed bump here as I was receiving an authentication error, and needed to alter the authentication config file... so I did! I ran `$ sudo nano /etc/postgresql/9.1/main/pg_hba.conf` and wrote `local all postgres peer`, which...according to [this handy site](https://chartio.com/resources/tutorials/how-to-set-the-default-user-password-in-postgresql/), this is an authentication rule that "simply tells Postgres that for local connections established to all databases for the user postgres, authenticate using the peer protocol." Then I ran `sudo -u postgres psql` and was in!

⋅⋅⋅Aaannnddd back to the docs. So I created a user with proper access to my PostgreSQL server by running the commands
```
create user datadog with password '<PASSWORD>';
grant SELECT ON pg_stat_database to datadog;
CREATE DATABASE pg_stat_database;
```

⋅⋅⋅Then, I ran the permissions:
```
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);"
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

⋅⋅⋅After I entered the password...
<details>
  <summary>Here's what my terminal looked like</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+password.png></img>
</details>

⋅⋅⋅Then edited the `conf.yaml` file in the `/etc/datadog-agent/conf.d/postgres.d` directory:
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

⋅⋅⋅I restarted the agent.

⋅⋅⋅Man I love when things just work out:
<details>
  <summary>Postgres Status</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+status.png></img>
</details>

<details>
  <summary>.</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+install.png></img>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+hostmap.png></img>
</details>

+ Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
⋅⋅⋅As per the [Datadog docs](https://docs.datadoghq.com/agent/agent_checks/), I `cd`d into `/etc/datadog-agent/conf.d` and created a `my_metric.yaml` file, and a `my_metric.py` file in the `etc/datadog-agent/checks.d`. To start, I simply used the example in the docs. Then, after some googling what the syntax should be for Javascript's "math.random()" in Python, I declared a global variable (`random`) and called the python method `randomint(0,1000)`.

in `my_metric.yaml`:
```
init_config:

instances:
    [{}]
```

and in `my_metric.py`:
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

+ Change your check's collection interval so that it only submits the metric once every 45 seconds.
⋅⋅⋅As per your docs, I edited the `my_metric.yaml` file under `init_config` by including `min_collection_interval: 45`:
<details>
  <summary>`my_metric.yaml`</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/my_metric_yaml+45+sec.png></img>
</details>
<details>
  <summary>Metric with 45 seconds in UI</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/my_metric_yaml+46+sec_UI.png></img>
</details>

__Bonus__ Can you change the collection interval without modifying the Python check file you created?
Hm, because this is a bonus question, I'm fairly certain I could have done this wrong, as I _ONLY_ updated the `yaml` file.

## Visualizing Data

Utilize the Datadog API to create a Timeboard that contains:
+ Your custom metric scoped over your host.
+ Any metric from the integration on your Database with the anomaly function applied.
+ Your custom metric with the rollup function applied to sum up all points for the past hour into one bucket.
⋅⋅⋅ This one seemed like a lot, here are the steps I took:
1. Read the [docs](https://docs.datadoghq.com/api/?lang=python#timeboards).
2. Since it looks like we'll need an `APP KEY`, I had to generate one of those in my dashboard when I go to Integrations--APIs.
<details>
  <summary>Here's where to look</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/app+keys.png></img>
</details>
3. I used Postman to help with this as per this [tutorial][https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs]. I was able to add a couple of graphs via Postman.
<details>
  <summary>Here's what my postman interface looked like</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postman.png></img>
</details>
<details>
  <summary>And my dashboard showed that I had added a new timeboard</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/dashboard_custom+timeboard.png></img>
</details>
<details>
  <summary>And the actual timeboard graphs</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/custom+timeboard_graphs.png></img>
</details>
4.
