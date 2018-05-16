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
  <summary>_It should look like this..._</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/create_account_form.png></img>
</details>

4. Now install curl by running `sudo apt-get install curl` and then run the sweet, sweet command on the DataDog docs:
```
DD_API_KEY=3840599a1d800170269b6a93c2471c73 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
It's always delicious to see when things work. If everything goes according to plan, you'll see this message in your terminal:
<details>
  <summary>_Installation Confirmation Image_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/DDAgent_confirmation.png></img>
</details>

## Collecting Metrics
+ Adding some tags using the configuration files!

⋅⋅⋅So, as per your Datadog's [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/), I found the yaml file by `$cd`-ing into the `/etc/datadog-agent/conf.d` directory and opening up the `datadog.yaml` using vim (after running `sudo apt-get install vim`, of course).

<details>
  <summary>_See image here_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog.agent.png></img>
</details>

⋅⋅⋅Because the file is a readme (that I didn't have the permissions to update and save the file, I ran `sudo vim datadog.yaml` and added some tags:

```
- tag1:value1
- tag2:value2
- tag3:value3
```
<details>
  <summary>_Updated tags in `.yaml` file_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog.agent_addedtags.png></img>
</details>
<details>
  <summary>_This is what rendered in the UI_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/datadog_hostmap_tags.png></img>
</details>

However, it took me a little time to figure out that I had to restart the agent for the tags to happen. Whoops. And also... that I totally overlooked the whole "You see both forms in the `yaml` configuration files, but for the `datadog.yaml` init file only the first form is valid." (referring to the format below):

```
tags: key_first_tag:value_1, key_second_tag:value_2, key_third_tag:value_3
```

heh... so I updated the file to the correct format...

<details>
  <summary>_Corrected `.yaml` file_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog_addedtags_correct.png></img>
</details>
And here's what it looked like in the UI.

<details>
  <summary>_Hostmap tags_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/datadog_hostmap_tags_correct.png></img>
</details>
<details>
  <summary>_Charts_</summary>
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
```

Man I love when things just work out:
<details>
  <summary>_Creating role and granting access_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+create.png></img>
</details>

Then, I ran the permissions:
```
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);"
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

After I entered the password...
<details>
  <summary>_Here's what my terminal looked like!_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+password.png></img>
</details>
<details>
  <summary>_And UI_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/postgres+install.png></img>
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
  <summary>_And here's what the UI looks like:_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/my_metric_UI.png></img>
</details>

+ Change your check's collection interval so that it only submits the metric once every 45 seconds.
⋅⋅⋅As per your docs, I edited the `my_metric.yaml` file under `init_config`:
<details>
  <summary>_`my_metric.yaml`_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/my_metric_yaml+45+sec.png></img>
</details>

Annnddd... UI:
<details>
  <summary>_Metric with 45 seconds_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/my_metric_yaml+46+sec_UI.png></img>
</details>

__Bonus__ Can you change the collection interval without modifying the Python check file you created?
Now I'm fairly certain I did this wrong, as I ONLY updated the `yaml` file... hm. Will revisit.

## Visualizing Data

Utilize the Datadog API to create a Timeboard that contains:
+ Your custom metric scoped over your host.
+ Any metric from the integration on your Database with the anomaly function applied.
+ Your custom metric with the rollup function applied to sum up all points for the past hour into one bucket.
⋅⋅⋅ This one seemed like a lot, here are the steps I took:
1. Click on the "A new timeboard" button in the dashboard and chose "my_metric" in the dropdown:
<details>
  <summary>_Image here_</summary>
  <img src=https://s3.amazonaws.com/juliewongbandue-ddhiring/new+timeboard.png></img>
</details>
2.
