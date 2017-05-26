Your answers to the questions go here.

Steps I Took:

1.) Set up an Ubuntu 16.04 VM in VirtualBox on Mac OSX

2.) Sign up for Datadog, using "Datadog Recruiting Candidate" in the "Company" field.

3.) Bonus Question: What is the agent?
The DataDog Agent is a program that runs on one's host (can also run in Docker or a VM) that aggregates events and methods, and sends them to DataDog. It is composed of three parts, which are, in turn, controlled and coordinated by a supervisor process.
-The collector (a program that runs continously and checks on integrations, in addition to system stats such as CPU usage, disk latency, network traffic, etc) 
-Dogstatsd (a backend server that utilizes etsy's stats aggregation daemon (statsd) to receive custom metrics)
-Forwarder (a program that aggregates data from the collector and dogstatsd to present to DataDog) 

4.) Installed the DataDog agent for Ubuntu:
root@zaps-VirtualBox:~# DD_API_KEY=d5ed33bc1830f93767bbc1a16056ca95 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  9911  100  9911    0     0  17690      0 --:--:-- --:--:-- --:--:-- 17698

* Installing apt-transport-https

Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
Hit:2 http://us.archive.ubuntu.com/ubuntu xenial InRelease
Get:3 http://us.archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]
Get:4 http://us.archive.ubuntu.com/ubuntu xenial-backports InRelease [102 kB]
Fetched 306 kB in 0s (525 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following packages will be upgraded:
  apt-transport-https
1 upgraded, 0 newly installed, 0 to remove and 93 not upgraded.
                                                               Need to get 0 B/26.1 kB of archives.
                   After this operation, 1,024 B of additional disk space will be used.
(Reading database ... 207993 files and directories currently installed.)
Preparing to unpack .../apt-transport-https_1.2.20_amd64.deb ...
Unpacking apt-transport-https (1.2.20) over (1.2.19) ...
Setting up apt-transport-https (1.2.20) ...

* Installing APT package sources for Datadog

Executing: /tmp/tmp.1cE2dLojbX/gpg.1.sh --recv-keys
--keyserver
hkp://keyserver.ubuntu.com:80
C7A7DA52
gpg: requesting key C7A7DA52 from hkp server keyserver.ubuntu.com
gpg: key C7A7DA52: public key "Datadog Packages <package@datadoghq.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
Executing: /tmp/tmp.Tch89GsVxN/gpg.1.sh --recv-keys
--keyserver
hkp://keyserver.ubuntu.com:80
382E94DE
gpg: requesting key 382E94DE from hkp server keyserver.ubuntu.com
gpg: key 382E94DE: public key "Datadog, Inc <package@datadoghq.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)

* Installing the Datadog Agent package

Ign:1 https://apt.datadoghq.com stable InRelease
Get:2 https://apt.datadoghq.com stable Release [2,367 B]
Get:3 https://apt.datadoghq.com stable Release.gpg [473 B]
Get:4 https://apt.datadoghq.com stable/main amd64 Packages [9,752 B]
Get:5 https://apt.datadoghq.com stable/main i386 Packages [8,382 B]
Fetched 21.0 kB in 0s (40.8 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following NEW packages will be installed:
  datadog-agent
0 upgraded, 1 newly installed, 0 to remove and 93 not upgraded.
Need to get 69.4 MB of archives.
After this operation, 223 MB of additional disk space will be used.
Get:1 https://apt.datadoghq.com stable/main amd64 datadog-agent amd64 1:5.13.2-1 [69.4 MB]
Fetched 69.4 MB in 21s (3,206 kB/s)
                                   Selecting previously unselected package datadog-agent.
(Reading database ... 207993 files and directories currently installed.)
Preparing to unpack .../datadog-agent_1%3a5.13.2-1_amd64.deb ...
Prepare Datadog Agent keys rotation
  Add the new 'Datadog, Inc <package@datadoghq.com>' key to the list of APT trusted keys.... key already installed
Unpacking datadog-agent (1:5.13.2-1) ...
Processing triggers for systemd (229-4ubuntu16) ...
Processing triggers for ureadahead (0.100.0-19) ...
Setting up datadog-agent (1:5.13.2-1) ...
Registering service datadog-agent
Enabling service datadog-agent
Creating dd-agent group
Creating dd-agent user
W: --force-yes is deprecated, use one of the options starting with --allow instead.

* Adding your API key to the Agent configuration: /etc/dd-agent/datadog.conf

* Starting the Agent...


Your Agent has started up for the first time. We're currently verifying that
data is being submitted. You should see your Agent show up in Datadog shortly
at:

    https://app.datadoghq.com/infrastructure

Waiting for metrics.....................................

Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.

If you ever want to stop the Agent, run:

    sudo /etc/init.d/datadog-agent stop

And to run it again run:

    sudo /etc/init.d/datadog-agent start

5.) Added tags in the Agent config file (etc/dd-agent/datadog.conf)
# Set the host's tags (optional)
tags: env:vm, database:mysql

6.) Restarted DataDog service in order for the tags to show up
/etc/init.d/datadog-agent restart
