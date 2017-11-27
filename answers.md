This is Long Liu's answer.
# Step 0: Setup an Ubuntu VM.
Setup a virtual machine by utilizing [Vargrant](https://www.vagrantup.com/intro/getting-started/index.html).

# Level 1 - Collecting your Data
## Step 1: Sign up for Datadog, get the Agent reporting metrics from your local machine.
The local machine is a virtual machine in VirtualBox running Ubuntu 12.04 LTS 64-bit. 

Follow the [instruction](https://app.datadoghq.com/account/settings#agent/ubuntu) to install Datadog Agent on local machine.

Once the installation is completed, the status of the Agent can be checked by:
```bash
$sudo \etc\init.d\datadog-agent status
```
The information of the Agent can be checked by:
```bash
$sudo \etc\init.d\datadog-agent info
```

**Definition of Agent**

## Step 2: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
[Tags](https://docs.datadoghq.com/guides/tagging/) are very useful to group machines and metrics for monitoring. Assigning tags using the Agent configuration file will define the tag for the overall agent.

The configuration file is saved in `/etc/dd-agent`. And the Agent configuration file is named as `datadog.conf`.

To add the tags in the Agent configuration file, we should firstly edit the configuration file:
```bash
$sudo nano \etc\dd-agent\datadog.conf
```
Then find these lines:
```bash
# Set the host's tags (optional)
# tags: mytag, env:prod, role:database
```
Uncomment the second line, and change the name of tags to `host:long-test`:
```bash
# Set the host's tags (optional)
tags: long-test
```
![Alt text](https://github.com/longliuau/hiring-engineers/tree/support-engineer/conf_file.png "Agent tag")

Press ctrl + o to save the file, and then exit it by pressing ctrl + x.
