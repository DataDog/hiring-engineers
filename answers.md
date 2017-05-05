Your answers to the questions go here.

# Getting Started with DataDog
## Table of Contents
[Overview](#overview)

[Preparation](#preparation)

[Level 0](#level-0)
- [Walkthrough](#walkthrough-0)
- [Thinkthrough](#thinkthrough-0)

[Level 1](#level-1)
- [Walkthrough](#walkthrough-1)
- [Thinkthrough](#thinkthrough-1)

[Level 2](#level-2)
- [Walkthrough](#walkthrough-2)
- [Thinkthrough](#thinkthrough-2)

[Level 3](#level-3)
- [Walkthrough](#walkthrough-3)
- [Thinkthrough](#thinkthrough-3)

[Appendix](#appendix)

## Overview
This document will provide a walkthrough on how to set up a monitored host in Datadog, and from there, add a custom metric with checks and alerts. 

Each level will be broken up into 2 sections.
1. **Walkthrough**: This catalogues the steps you would take to accomplish the tasks in the level. It's written as though it might be used as a guide for a customer
2. **Thinkthrough**: This section is to give you insight into my process going through the level. I'll share what was straightforward, where I encountered problems, how I approached those problems, how I fixed them (if I did), and other insights.

## Preparation
This project was started on May 3, 2017.  
Before I started the levels, I read through the reference links and took notes in order to prime myself on the material. You can find those notes in notes.md.  
I also did a quick tutorial [online](http://www.markdowntutorial.com/) (See Appendix) for writing in markdown so that I could write a good-looking answers.md. 

I had originally planned to write this all in Google docs, but after seeing the repository, 
I decided it made more sense to use markdown. Especially sense most github readme's tend to use it, and so do Datadog's notifications and docs!

## Level 0 
### Set up an Ubuntu VM - (Optional)
This step is optional but it will help you to avoid any dependency issues. You may use any VM of your
choice. We chose to use Ubuntu 12.04 run with Vagrant.

### Walkthrough 0

1. Install Virtualbox. Here is the [Download](https://www.virtualbox.org/wiki/Downloads)  
To verify it installed, just run `virtualbox` in your terminal, and the virtualbox GUI will launch
![Running Virtualbox](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/virtualbox-installed.png)
2. Install Vagrant. Here is the [Download](https://www.vagrantup.com/)  
You should see a window like this appear when installation is complete.
![Vagrant Installed](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/vagrant-installed.png)
Alternatively, you can verify the installation by running `vagrant -v` and you 
should see the following output
```
$ vagrant -v
Vagrant 1.9.4
```
3. Launch an Ubuntu 12.04 VM using Vagrant with the following commands
```
$ vagrant init hasicorp/precise64
$ vagrant up
```
4. SSH into the new Vagrant host
``` 
$ vagrant ssh
```
Congrats! You're now ready to get started with Datadog

### Thinkthrough 0
I noticed initially that the instructions for Vagrant in the readme on Github had linux commands for starting vagrant.
```
$ vagrant init hasicorp/precise64
$ vagrant up
```
So I figured I should run the VM on my laptop's linux partition to make it easy for setup.

I've installed Virtualbox several times for previous jobs so I just followed the install wizard after
downloading it from the website. Since I'm running 64-bit Ubuntu 16.04, I downloaded the AMD64 version for Ubuntu 16.04.

Vagrant gave the option of a 64-bit debian installer on their website. Ubuntu is based on Debian, so I downloaded that. I avoided using my package manager with `$ sudo apt-get install` because I've had
cases in the past where the package manager version was behind the software's official download.

I checked that vagrant installed correctly with the proper version with `vagrant -v` and that was all good. But, as you can see in the screen shot below, VT-x was disabled in the bios, and that caused 
an error when vagrant attempted to use virtualbox.
![VT-x Error](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/VT-x_disabled.png)

After Enabling virtualization in the bios, vagrant worked!
![VT-x enabled](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/bios-vt.jpg)
![Vagrant is up](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/vagrant-up.png)

As an extra check, after I SSH'd into vagrant, I ran `ping www.google.com` to make sure I had network
access. If I didn't have access, that might cause me some problems with the Datadog agent later!
```
vagrant@precise64:~$ ping www.google.com
PING www.google.com (172.217.6.68) 56(84) bytes of data.
64 bytes from sfo07s17-in-f68.1e100.net (172.217.6.68): icmp_req=1 ttl=63 time=18.8 ms
64 bytes from sfo07s17-in-f4.1e100.net (172.217.6.68): icmp_req=2 ttl=63 time=17.8 ms
64 bytes from sfo07s17-in-f68.1e100.net (172.217.6.68): icmp_req=3 ttl=63 time=20.0 ms
64 bytes from sfo07s17-in-f4.1e100.net (172.217.6.68): icmp_req=4 ttl=63 time=18.5 ms
64 bytes from sfo07s17-in-f68.1e100.net (172.217.6.68): icmp_req=5 ttl=63 time=19.4 ms
^C
--- www.google.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4013ms
rtt min/avg/max/mdev = 17.826/18.939/20.003/0.767 ms
```

## Level 1
###Collecting your Data
You will create a DataDog Account, modify the Agent's configuration, install a database, add the DataDog integration for that DB, and write a custom agent check.

Bonus question: In your own words, what is the Agent?  
Reference link: http://docs.datadoghq.com/guides/basic_agent_usage/  
Idea: Draw a diagram outlining the 3 key components and how they work together

### Walkthrough 1

1. Go to https://www.datadoghq.com and click the "Get Started Free" button
2. Enter your Username and Password and other account details, then click next
3. Give us a little information about your stack, then click next
4. Select the OS of the first machine you'd like to monitor, since I used vagrant,
I'll be selecting Ubuntu
![install agent](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/install-first-agent.png)
5. Back on your terminal run `vagrant ssh` to get back into your Virtualbox VM
6. Now follow the installation steps listed for your particular OS
![install ubuntu agent](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/install-first-agent-ubuntu.png)
    - Since I installed on Ubuntu, it was a one-step install. I ran the command
`DD_API_KEY=5691d1878b78b28e9945edbbb37afea4 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"`
    - You will see a bunch of output to the screen as the install grabs the 
necessary packages
    - When it's all done, you should see something like this
![datadog agent installed](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/datadog-agent-installed.png)
    - You can click finish on the datadog webpage
7. Go to https://app.datadoghq.com/infrastructure and you should see your VM in the
host list!
![host online](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/host-shown-online.png)
8. Great, now our host is being monitored! Let's add some tags to it so we can find
it easily through search and group it with other hosts (once we add more!). We 
could do it through the infrastructure web page, but lets edit the config file.
Lets do `cd /etc/dd-agent` and use our favorite text editor (I won't make any VI
vs Emacs comments here) to find these lines
```
# Set the host's tags (optional)
# tags: mytag, env:prod, role:database

```
remove the "# " comment symbol. You can use the defaults or choose any set 
of tags you'd like. It should now look like this
```
# Set the host's tags (optional)
tags: mytag, env:prod, role:database

```
Save and exit. The next step is to restart the agent so the configuration will be loaded. My Ubuntu agent restart command: 
```
$ sudo /etc/init.d/datadog-agent restart
 * Stopping Datadog Agent (stopping supervisord) datadog-agent              [ OK ] 
 * Starting Datadog Agent (using supervisord) datadog-agent                 [ OK ] 
```

9. Let's make sure the tags were loaded. Go to the [Host Map page](https://app.datadoghq.com/infrastructure/map)
![host map](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/host-map.png)
and click on your host, and you'll be greeted with additional details like metrics and your Datadog Agent tags
![host map](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/host-map-with-tags.png)

10. Good job. So far we just have metrics for our host, let's monitor something else on our host too, like a database. I recommend PostgreSQL, it's free and pretty
easy to install. Here's their [install guide](https://www.postgresql.org/download/linux/ubuntu/) for your reference, but I'll show you my process below
```
$ sudo vi /etc/apt/sources.list.d/pgdg.list
// I added the line for the postgresql repository and saved
// deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
$ sudo apt-get update
$ apt-get install postgresql-9.4
```

Postgres is installed. Now we just need to be able to login. Follow my process or
refer to this [helpful online post](https://www.codeproject.com/Articles/898303/Installing-and-Configuring-PostgreSQL-on-Linux-Min)
```
vagrant@precise64:/etc/dd-agent$ sudo su -
root@precise64:~# su - postgres
postgres@precise64:~$ psql
psql (9.4.11)
Type "help" for help.

postgres=# CREATE USER vagrant
postgres-# WITH SUPERUSER CREATEDB CREATEROLE
postgres-# PASSWORD 'datadoginterview'
postgres-# ;
CREATE ROLE
postgres=# \q
postgres@precise64:~$ exit
logout
root@precise64:~# exit
logout
vagrant@precise64:/etc/dd-agent$ psql postgres
psql (9.4.11)
Type "help" for help.

postgres=#
```
11. Time to install an integration for our database. If you used a core integration, like postgres or mysql, you don't need to do a separate install.
Core integrations are installed with the agent.  
Otherwise, for non-core integrations, run `sudo apt-get install dd-check-integration` and just replace the integration with what you want. e.g. dd-check-custom

12. Go to the [integrations page](https://app.datadoghq.com/account/settings#integrations)
![Integrations Page](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/integrations-page.png)
 and click install for the one that matches your database.  
![Postgres Integration Install](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/install-postgres-integration.png)  
Then follow the instructions or click the "Install Integration" button.
![Postgres instructions](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/postgres-instruct.png)

13.Verify your integration is working by running `sudo /etc/init.d/datadog-agent info`
And see if your check is OK. 
```
    postgres (5.13.0)
    -----------------
      - instance #0 [OK]
      - Collected 12 metrics, 0 events & 1 service check
```
    - If you want to go even further, check [this page](http://docs.datadoghq.com/integrations/postgresql/) for custom metrics you can configure for PostgreSQL

14. You've got your first integration running, you're almost a pro! Now let's write our own custom check. We'll use "Agent Check," a Python Plugin, to achieve
this. We'll just do something easy, and create a custom check called randomsample.

15. Create randomsample.yaml in `/etc/dd.agent/conf.d` and randomsample.py in `/etc/dd.agent/check.d`  
Make sure the names of the .py and .yaml file match. Any check you write will 
follow these rules and exist in these two locations. This is how the agent knows
how to find your check!
    - You might need to run your text editor with sudo to save these files

16. For randomsample.yaml, paste this code
```
init_config:
    min_collection_interval: 3

instances:
    [{}]

```
This just tells our check to be ran every 3 seconds.

17. For randomsample.py, paste this code
```
from checks import AgentCheck
import random
class RandomSampleCheck(AgentCheck):
    def check(self, instance):
        self.gauge('random.sample', random.random())
```
All checks derive from the AgentCheck class. When it is run, the check method is
called, and we will sample a simple gauge metric. In this case, a random value
between \[0.0, 1.0\). If you want to try something more difficult, read [this page](http://docs.datadoghq.com/guides/agent_checks/)

18. Now restart your agent with `sudo /etc/init.d/datadog-agent restart`  
You can verify your check is working with `sudo /etc/init.d/datadog-agent info`
![Random Info OK](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/random-check-info-OK.png)

19. Then go to your host map, you should see something like this!
![Random Host Map](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/random-check-success.png)

20. Congratulations, you just wrote your first custom check! We'll use this check
in Level 2.

### Thinkthrough 1
Signing up was straight forward. Since I did Level 0 the evening before Level 1, 
once I got to the Install an Agent screen, I went back to my terminal and double 
checked that my VM was still running by running `vagrant ssh`. 

When I first ran the "one-step install," I got an error since didn't have curl 
installed on my VM so I ran `sudo apt-get install curl`.
Then I reset my terminal with clear so I could get a screenshot with no bugs

I reran the one-step install, and I saw a bunch of installation output, so I waited until it was done. Once I saw the following, it looked like it was working, and I 
went to https://app.datadoghq.com/infrastructure to verify the agent was submitting
```
* Adding your API key to the Agent configuration: /etc/dd-agent/datadog.conf

* Starting the Agent...

 * Stopping Datadog Agent (stopping supervisord) datadog-agent
   ...done.
 * Starting Datadog Agent (using supervisord) datadog-agent
   ...done.

Your Agent has started up for the first time. We're currently verifying that
data is being submitted. You should see your Agent show up in Datadog shortly
at:

    https://app.datadoghq.com/infrastructure

Waiting for metrics.................................

Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.
```
I remembered from my notes before I started the Levels, that I could run
`sudo /etc/init.d/datadog-agent info` to verify the agent had no errors
![no agent errors](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/no-agent-errors.png)
I saw all Green "OK" so that looked good enough for me to continue

The next guideline was to add tags in the agent config file. I noticed that
I could do that from the infrastructure page on app.datadoghq.com but I wanted to
check out the config file to see what it looked like.

![update host tags online](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/update-host-tags.png)

Back to my notes.md, I remembered the /etc/dd-agent/conf.d location and figured that
was a good place to look for a config file. I ran `ls` in that directory and a huge
number of example files were shown on the screen.  
Then I thought, oh there's that Agent Overview page in the github readme, so I went
there and clicked on the [Agent Guides by Platform: Ubuntu](http://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/)
and voila! "The configuration file for the Agent is located at /etc/dd-agent/datadog.conf"
![datadog.conf](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/datadog-conf-location.png)

I opened the datadog.conf.example file first to see all the options I could put in
 and I noticed
```
# Set the host's tags (optional)
# tags: mytag, env:prod, role:database
```
That looked about right, so I opened datadog.conf with vi and got a warning that it was read-only so I checked it with
```
vagrant@precise64:/etc/dd-agent$ ls -al
-rw-r-----  1 dd-agent dd-agent 10500 May  4 23:26 datadog.conf
```
That showed only root has write privileges and so I reopened it with `sudo vi datadog.conf` to add my own tags. A quick google of "datadog tags" brought me to the
[tagging guide](http://docs.datadoghq.com/guides/tagging/). Key-value pairs were 
recommended. I modified some of the examples, and added my own 
```
tags: env:test, role:database, purpose:interview
```
I checked the infrastructure page to look at the host tags, and they weren't 
updated. I probably need to restart the agent to have it update it's configuration,
but I googled just in case there was a way to do it without an agent restart.
A [help post by Dustin Lawler](https://help.datadoghq.com/hc/en-us/articles/203764515-Start-Stop-Restart-the-Datadog-Agent) said a reload of agent configuration
requires a restart, so I did that.
```
sudo /etc/init.d/datadog-agent restart
```

Then I went to the [Host map](https://app.datadoghq.com/infrastructure/map) via the navigation bar under infrastructure and saw the tags when I clicked on my host.

---
Time to install a database. MySQL is [EOL/deprecated](https://www.mysql.com/support/eol-notice.html) for Ubuntu 12.04, and Postgres had a [pretty simple install](https://www.postgresql.org/download/linux/ubuntu/) for 
Ubuntu. So I decided on postgres. You can see the process for installatin below
```
$ sudo vi /etc/apt/sources.list.d/pgdg.list
// I added the line for the postgresql repository and saved
// deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
$ sudo apt-get update 
$ apt-get install postgresql-9.4 
vagrant@precise64:/etc/dd-agent$ sudo vi conf.d/postgres.yaml
```
I googled for how to start the postgres server and found a few different pages 
[1](https://www.postgresql.org/docs/9.4/static/tutorial-createdb.html), 
[2](https://www.postgresql.org/docs/9.1/static/server-start.html),
[3](https://www.codeproject.com/Articles/898303/Installing-and-Configuring-PostgreSQL-on-Linux-Min)
and settled on the 3rd guide. 
```
vagrant@precise64:/etc/dd-agent$ sudo su -
root@precise64:~# su - postgres
postgres@precise64:~$ psql
psql (9.4.11)
Type "help" for help.

postgres=# CREATE USER vagrant
postgres-# WITH SUPERUSER CREATEDB CREATEROLE
postgres-# PASSWORD 'datadoginterview'
postgres-# ;
CREATE ROLE
postgres=# \q
postgres@precise64:~$ exit
logout
root@precise64:~# exit
logout
vagrant@precise64:/etc/dd-agent$ psql postgres
psql (9.4.11)
Type "help" for help.

postgres=# 
```

---
Now that the database is installed, I need to install the integration. I went to the Datadog docs site, and found the [Installing Integrations Page](http://docs.datadoghq.com/guides/installcoreextra/). 
I also found the [Integrations install dashboard](https://app.datadoghq.com/account/settings#integrations).  
I decided to try out the install from the website, to see if it would push the installation to my host. 
It looks like the dashboard page give instructions on how to configure the 
integration once its installed. so I ran the installer, and then followed the main steps. 
```
vagrant@precise64:/etc/dd-agent$ psql postgres
psql (9.4.11)
Type "help" for help.

postgres=# create user datadog with password 'hYrmS03SQVy6sPWcYmt0cSzk';
CREATE ROLE
postgres=# grant SELECT ON pg_stat_database to datadog;
GRANT
postgres=# \q
vagrant@precise64:/etc/dd-agent$ psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"  
Password for user datadog: 
vagrant@precise64:/etc/dd-agent$ sudo vi conf.d/postgres.yaml
// Then I pasted in the default config for the agent to connect to postgres and saved
vagrant@precise64:/etc/dd-agent$ sudo /etc/init.d/datadog-agent restart
 \* Stopping Datadog Agent (stopping supervisord) datadog-agent              [ OK ] 
 \* Starting Datadog Agent (using supervisord) datadog-agent                 [ OK ] 
vagrant@precise64:/etc/dd-agent$ sudo /etc/init.d/datadog-agent info 
```
The info command let me know that the postgres check was OK. Sweet!
![Postgres Check OK](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/postgres-check-OK.png)

And I checked the hostmap to see if it showed up on my host. It did!
![postgres on hostmap](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/hostmap-shows-postgres.png)

---
Time for the custom agent check! I started by looking at the reference page for [writing an agent check](http://docs.datadoghq.com/guides/agent_checks/)

Before I create the python check, I figured I should make a config file first.
I decided on the name randomsample, so I need matching names with randomsample.yaml
in conf.d and randomsample.py in checks.d

I started by pasting the "Hello World" example from the guide, and seeing if that
was able to run after restarting the agent. Looks like it worked!
![Hello World Check](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/hello-world-check.png)

Alright now its time to start writing the random sample. But first, I want to build out my configuration file. I know the check needs to be run multiple times so that
there will be enough data to have visuals for in Level 2. I'll put min_collection_interval of 3 (seconds) so that I can see if its working quickly
 I'm not sure what to put for the instances section yet, but I'll come back to that.

Now to write the randomsample.py.
Your readme mentioned grabbing a random value with random.random() in python, so
I checked the [python docs](https://docs.python.org/2/library/random.html) to see the usage
```
random.random()
    Return the next random floating point number in the range [0.0, 1.0).

```
So roughly 10% of the time, I should see a 0.9 or greater, Cool.
Going off the hello world example, I used self.gauge again, since it seems to be 
used to sample a simple metric. self.rate, self.increment, etc are for more complex
metrics involving rates and incrementing counters and the like.  
I replaced `self.gauge('hello.world', 1)` with `self.gauge('random.sample', random.random())` as a preliminary test.  
Time to restart the agent, and check my host map!

Success! The random app now appears on my hostmap
![Random Host Map](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/random-check-success.png)

Then I clicked on the "random dashboard" \([link](https://app.datadoghq.com/dash/integration/custom%3Arandom?live=true&tpl_var_scope=host%3Aprecise64&page=0&is_auto=false&from_ts=1493953750085&to_ts=1493957350085&tile_size=m)\)
and I can see my values that are being sampled. Sweet!
![Random Dashboard](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/random-dashboard.png)
Just one last check, I ran the info command for the agent, and I got an OK for my random sample check
![Random Info OK](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/random-check-info-OK.png)

Well that looks like the end of level 1 besides the bonus! Time to finish 
the walkthrough section

## Level 2
###Visualizing your Data
You will clone the starting dashboard, add additional metrics, and make sure your email recieves a snapshot with @notification.

Bonus question: What is the difference between a timeboard and a screenboard?

### Walkthrough 2

### Thinkthrough 2

## Level 3
###Alerting on your Data
You will set up a monitor for your metric (it should alert you within 15 minutes).

Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  
Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

### Walkthrough 3

### Thinkthrough 3

## Appendix

### Software Used
- Ubuntu 16.04 LTS - Partition on my Personal Computer. This is my preferred coding environment.
- VIM - for editing Mhttps://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/earkdown files
- git - Version control, used to push changes to my fork of the github repository
- Github - to store my fork of the original github repo
- Markdown - for all text files in my github submission
- Vagrant - for creating a VM to work in
- PostgreSQL - Database that was monitored with a Datadog integration

### Online Reference Material
- [Markdown Tutorial](http://www.markdowntutorial.com/)
- [Markdown Quick Reference](https://en.support.wordpress.com/markdown-quick-reference/)
- [Markdown Linking](http://stackoverflow.com/questions/2822089/how-to-link-to-part-of-the-same-document-in-markdown)
- [Datadog Guides](http://docs.datadoghq.com/)
