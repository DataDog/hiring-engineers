## Tiffany Monroe
Solutions Engineer Applicant

## Prerequisites - Setting up the environment

Used MacBook Pro OS High Sierra 10.13.4

### Github Setup

Forked Datadog Hiring Engineers Repository (https://github.com/DataDog/hiring-engineers/)

Cloned on local computer: ```git clone https://github.com/tiffanymonroe/hiring-engineers.git```

Changed directories: ```cd hiring-engineers```

Created new branch to work on: ```git checkout -b Tiffany_Monroe_Solutions_Engineer_Revised```

Used Atom to edit text in answers.md.

Checked Github:
```
git add .
git commit -m "new branch"
git push origin Tiffany_Monroe_Solutions_Engineer_Revised
```

Github worked.

### Vagrant Setup

Used instructions from
Downloaded [VirtualBox 5.2.18](https://www.virtualbox.org/wiki/Downloads) platform packages for OS X.

Installation failed: "System software from Oracle America, Inc. was blocked from loading."

Went to System Preferences to "allow" software to load, installation successful.

Downloaded and installed [Vagrant 2.1.5](https://www.vagrantup.com/downloads.html) 64-bit for OS X.

```
vagrant init hashicorp/precise64
vagrant up
```

<img src="img/0/vagrant_init.png"/>

<img src="img/0/vagrant_up.png"/>

Reviewed instructions, added SSH: ```vagrant ssh```

<img src="img/0/vagrant_ssh.png"/>

### Datadog Setup

Went to Datadog [website](https://datadoghq.com/), signed up for a free trial, put "Datadog Recruiting Candidate" in "Company" field, skipped the "Tell us about your stack" option.

Installed the [Agent](https://app.datadoghq.com/signup/agent) for OS X by typing provided code in Command Line:
 ```
 DD_API_KEY=ecbbdce5a2bc9bb8dc9145af1e490e3a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"
 ```

<img src="img/0/agent_installed.png"/>

Checked that Agent reports metrics: ```datadog-agent status```

<img src="img/0/agent_status.png"/>

Finished setup on [GUI](https://app.datadoghq.com/help/quick_start#mac): "You have 1 host reporting data to Datadog"

<img src="img/0/agent_reporting.png" />

## Collecting Metrics

### Tags
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.


Read documentation on tags, including [getting started](https://docs.datadoghq.com/tagging/) with tags, [assigning](https://docs.datadoghq.com/tagging/) tags, and [using](https://docs.datadoghq.com/tagging/using_tags/) tags.

Read how to [assign tags](https://docs.datadoghq.com/tagging/assigning_tags/#assigning-tags-using-the-configuration-files) in the Agent config file.

Read how to [locate](https://app.datadoghq.com/account/settings#agent/mac) the Agent config file.

Changed directories to locate the Agent config file:

```
cd ../../opt/datadog-agent/etc/conf.d
```

Could not find ```datadog.yaml``` in directory. Went up a level to see which files were located there.

```
cd ..
ls
```

Found ```datadog.yaml``` located in ```etc``` directory.

Uncommented out "tags" section, assigned tags.

<img src="img/1/tags.png"/>

Host Map did not show tags.

Restarted Agent.

Tags listed in "Stream."

<img src="img/1/stream.png"/>

Went to "Open Web UI" in the Datadog Agent.

Located "Datadog Agent Manager" in "Settings."

<img src="img/1/datadog_agent_manager.png"/>

Added an extra line between commented out line and "tags" to save.

Restarted Agent, checked Host Map, shows tags.

<img src="img/1/host_map.png"/>


### Database Integration
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.


<b>Part 1: Install Database</b>

Read documentation on [installing](https://www.postgresql.org/download/macosx/) PostgreSQL, and installing [Homebrew](https://brew.sh/) packages.

Installed Homebrew from Command Line:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Response:
>Installation successful!

Installed PostgreSQL using [Homebrew](https://formulae.brew.sh/formula/postgresql):

```
brew install postgresql
```

Response:
>Pouring postgresql-10.5.high_sierra.bottle.1.tar.gz

Checked PostgreSQL.

```
psql -l
```

Response:
>psql: could not connect to server: No such file or directory
	Is the server running locally and accepting
	connections on Unix domain socket "/tmp/.s.PGSQL.5432"?

Read PostgreSQL installation instructions in Command Line.
>To have launchd start postgresql now and restart at login:
  brew services start postgresql
Or, if you don't want/need a background service you can just run:
  pg_ctl -D /usr/local/var/postgres start

```
pg_ctl -D /usr/local/var/postgres start
psql -l
```

<img src="img/1/psql.png" />



<b>Part 2: Install Integration</b>

Read documentation on [Integrations](https://docs.datadoghq.com/integrations/postgres/) and, specifically, configuring [PostgreSQL](https://app.datadoghq.com/account/settings#integrations/postgres).

<img src="img/1/postgres_gui.png"/>

Created a database for integration:

```
createdb pg_stat_database
psql pg_stat_database
```

>psql (10.5)
Type "help" for help.
pg_stat_database=#

Created a read-only "datadog" user with access to PostgreSQL:

```
pg_stat_database=# create user datadog with password 'O10a8OAheqedH8jD9AG9NKb0';
CREATE ROLE
pg_stat_database=# grant SELECT ON pg_stat_database to datadog;
GRANT
pg_stat_database=# \q
```

Verified permissions:

```
psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" && \
echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

Response:
>\e[0;32mPostgres connection - OK\e[0m

Changed directories to configure the Agent to connect to the PostgreSQL server:

```
cd ~/../../opt/datadog-agent/etc/conf.d/postgres.d
mv conf.yaml.example conf.yaml
atom .
```

Edited ```postgres.d/conf.yaml``` file, restarted Agent, ran ```datadog-agent status```, installed integration button:

<img src="img/1/edit_conf.png"/>

<img src="img/1/agent_status.png"/>

<img src="img/1/integration_installed.png"/>


### Agent Check
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.


Read documentation on [Agent Checks](https://docs.datadoghq.com/developers/agent_checks/), researched how to generate a [random number in Python](https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/).
