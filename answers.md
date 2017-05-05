Your answers to the questions go here.

# Getting Started with DataDog

## Overview
This document will provide a walkthrough on how to set up a monitored host in Datadog, and from there, add a custom metric with checks and alerts. 

Each level will be broken up into 2 sections.
1. Walkthrough: This catalogues the steps you would take to accomplish the tasks in the level. It's written as though it might be used as a guide for a customer
2. Thinkthrough: This section is to give you insight into my process going through the level. I'll share what was straightforward, where I encountered problems, how I approached those problems, how I fixed them (if I did), and other insights.

## Prework
This project was started on May 3, 2017.  
Before I started the levels, I read through the reference links and took notes in order to prime myself on the material. You can find those notes in notes.md.  
I also did a quick tutorial [online](http://www.markdowntutorial.com/) (See Appendix) for writing in markdown so that I could write a good-looking answers.md. 

I had originally planned to write this all in Google docs, but after seeing the repository, 
I decided it made more sense to use markdown. Especially sense most github readme's tend to use it, 
and so do Datadog's notifications!

## Level 0 (optional) - Set up an Ubuntu VM
This step is optional but it will help you to avoid any dependency issues. You may use any VM of your
choice. We chose to use Ubuntu 12.04 run with Vagrant.

### Walkthrough

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

### Thinkthrough
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

## Level 1 - Collecting your Data
You will create a DataDog Account, modify the Agent's configuration, install a database, add the DataDog integration for that DB, and write a custom agent check.

Bonus question: In your own words, what is the Agent?  
Reference link: http://docs.datadoghq.com/guides/basic_agent_usage/  
Idea: Draw a diagram outlining the 3 key components and how they work together

### Walkthrough

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
Lets `cd /etc/dd-agent` and using your favorite text editor (I won't make any VI
vs Emacs comments here), find these lines
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
10. 



### Thinkthrough
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
Back to my notes, I remembered the /etc/dd-agent/conf.d location and figured that
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

Then I went to the [Host map](https://app.datadoghq.com/infrastructure/map) via the navigation bar under infrastructure and saw the tags when I clicked on my host.
---
Time to install a database. MySQL is deprecated for Ubuntu 12.04, and Postgres had a [pretty simple install](https://www.postgresql.org/download/linux/ubuntu/) for 
Ubuntu. You can see the process next
```
$ sudo vi /etc/apt/sources.list.d/pgdg.list
// I added the line for the postgresql repository and saved
// deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
$ sudo apt-get update 
$ apt-get install postgresql-9.4 
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




## Level 2 - Visualizing your Data
You will clone the starting dashboard, add additional metrics, and make sure your email recieves a snapshot with @notification.

Bonus question: What is the difference between a timeboard and a screenboard?

## Level 3 - Alerting on your Data
You will set up a monitor for your metric (it should alert you within 15 minutes).

Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  
Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


## Appendix

### Software Used
- Ubuntu 16.04 LTS - Partition on my Personal Computer. This is my preferred coding environment.
- VIM - for editing Mhttps://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/earkdown files

### Online Reference Material
- [Markdown Tutorial](http://www.markdowntutorial.com/)
- [Markdown Quick Reference](https://en.support.wordpress.com/markdown-quick-reference/)
