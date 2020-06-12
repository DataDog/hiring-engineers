# Ubuntu Agent Installation

[Ubuntu Agent Installation Documentation](https://app.datadoghq.com/account/settings#agent/ubuntu)

## Command Line Installation

```commandline
vagrant@vagrant:~$ DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=XXXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 15102  100 15102    0     0   182k      0 --:--:-- --:--:-- --:--:--  182k

* Installing apt-transport-https

Get:1 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
Hit:2 http://archive.ubuntu.com/ubuntu bionic InRelease
Ign:3 https://dl.bintray.com/sbt/debian  InRelease
Get:4 https://dl.bintray.com/sbt/debian  Release [815 B]
Get:5 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]
Ign:6 https://apt.datadoghq.com stable InRelease
Get:7 http://security.ubuntu.com/ubuntu bionic-security/main Translation-en [236 kB]
Get:8 https://apt.datadoghq.com stable Release [8,324 B]
Get:10 https://apt.datadoghq.com stable Release.gpg [819 B]
Ign:11 https://adoptopenjdk.jfrog.io/adoptopenjdk/deb bionic InRelease
Get:12 https://apt.datadoghq.com stable/7 amd64 Packages [4,149 B]
Hit:13 https://adoptopenjdk.jfrog.io/adoptopenjdk/deb bionic Release
Get:14 http://security.ubuntu.com/ubuntu bionic-security/universe Translation-en [223 kB]
Get:15 http://archive.ubuntu.com/ubuntu bionic-backports InRelease [74.6 kB]
Get:17 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 Packages [969 kB]
Get:18 http://archive.ubuntu.com/ubuntu bionic-updates/main i386 Packages [694 kB]
Get:19 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 Packages [1,081 kB]
Get:20 http://archive.ubuntu.com/ubuntu bionic-updates/universe i386 Packages [1,018 kB]
Fetched 4,487 kB in 3s (1,719 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
apt-transport-https is already the newest version (1.6.12ubuntu0.1).
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.
Reading package lists...
Building dependency tree...
Reading state information...
dirmngr is already the newest version (2.2.4-1ubuntu1.2).
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.

* Installing APT package sources for Datadog

Warning: apt-key output should not be parsed (stdout is not a terminal)
Executing: /tmp/apt-key-gpghome.zuARa5my8p/gpg.1.sh --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 A2923DFF56EDA6E76E55E492D3A80E30382E94DE
gpg: key D3A80E30382E94DE: "Datadog, Inc <package@datadoghq.com>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1

* Installing the Datadog Agent package

Ign:1 https://apt.datadoghq.com stable InRelease
Hit:2 https://apt.datadoghq.com stable Release
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following packages will be upgraded:
  datadog-agent
1 upgraded, 0 newly installed, 0 to remove and 1 not upgraded.
Need to get 153 MB of archives.
After this operation, 44.6 MB of additional disk space will be used.
Get:1 https://apt.datadoghq.com stable/7 amd64 datadog-agent amd64 1:7.20.0-1 [153 MB]
Fetched 153 MB in 17s (8,963 kB/s)
(Reading database ... 72331 files and directories currently installed.)
Preparing to unpack .../datadog-agent_1%3a7.20.0-1_amd64.deb ...
Removed /etc/systemd/system/multi-user.target.wants/datadog-agent-process.service.
Removed /etc/systemd/system/multi-user.target.wants/datadog-agent-trace.service.
Removed /etc/systemd/system/multi-user.target.wants/datadog-agent.service.
Removing integrations installed with the 'agent integration' command
Unpacking datadog-agent (1:7.20.0-1) over (1:7.19.2-1) ...
Setting up datadog-agent (1:7.20.0-1) ...
Enabling service datadog-agent
Created symlink /etc/systemd/system/multi-user.target.wants/datadog-agent.service → /lib/systemd/system/datadog-agent.service.
Created symlink /etc/systemd/system/multi-user.target.wants/datadog-agent-process.service → /lib/systemd/system/datadog-agent-process.service.
Created symlink /etc/systemd/system/multi-user.target.wants/datadog-agent-trace.service → /lib/systemd/system/datadog-agent-trace.service.
(Re)starting datadog-agent now...
Processing triggers for systemd (237-3ubuntu10.41) ...
Processing triggers for ureadahead (0.100.0-21) ...
W: --force-yes is deprecated, use one of the options starting with --allow instead.

* Keeping old datadog.yaml configuration file

/bin/systemctl
* Starting the Agent...



Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.

If you ever want to stop the Agent, run:

    sudo systemctl stop datadog-agent

And to run it again run:

    sudo systemctl start datadog-agent
```


## Check Agent Status

```commandline
vagrant@vagrant:~$ sudo service datadog-agent status
● datadog-agent.service - Datadog Agent
   Loaded: loaded (/lib/systemd/system/datadog-agent.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2020-06-11 23:01:57 UTC; 43min ago
 Main PID: 5902 (agent)
    Tasks: 9 (limit: 1109)
   CGroup: /system.slice/datadog-agent.service
           └─5902 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/agent.pid

Jun 11 23:31:58 vagrant agent[5902]: 2020-06-11 23:31:58 UTC | CORE | INFO | (pkg/serializer/serialize
Jun 11 23:31:58 vagrant agent[5902]: 2020-06-11 23:31:58 UTC | CORE | INFO | (pkg/serializer/serialize
Jun 11 23:31:59 vagrant agent[5902]: 2020-06-11 23:31:59 UTC | CORE | INFO | (pkg/collector/runner/run
Jun 11 23:31:59 vagrant agent[5902]: 2020-06-11 23:31:59 UTC | CORE | INFO | (pkg/collector/runner/run
Jun 11 23:32:02 vagrant agent[5902]: 2020-06-11 23:32:02 UTC | CORE | INFO | (pkg/metadata/host/host.g
Jun 11 23:32:02 vagrant agent[5902]: 2020-06-11 23:32:02 UTC | CORE | INFO | (pkg/serializer/serialize
Jun 11 23:36:57 vagrant agent[5902]: 2020-06-11 23:36:57 UTC | CORE | INFO | (pkg/serializer/serialize
Jun 11 23:36:58 vagrant agent[5902]: 2020-06-11 23:36:58 UTC | CORE | INFO | (pkg/serializer/serialize
Jun 11 23:41:58 vagrant agent[5902]: 2020-06-11 23:41:58 UTC | CORE | INFO | (pkg/serializer/serialize
Jun 11 23:41:58 vagrant agent[5902]: 2020-06-11 23:41:58 UTC | CORE | INFO | (pkg/serializer/serialize
```
