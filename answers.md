### Prerequisites - Setup The Environment

###### GitHub
Fork the [repository](https://github.com/DataDog/hiring-engineers/tree/solutions-engineer) and clone [the fork](https://github.com/cwithac/hiring-engineers/tree/solutions-engineer) into my local environment, checking out _solutions-engineers_ and building branch "Cathleen_Wright_Solutions_Engineer" for unique access to the directory and _answers.md_ in the text editor [Atom](https://atom.io/).  

```shell
  $ git clone git@github.com:cwithac/hiring-engineers.git
  $ cd hiring-engineers
  $ git checkout solutions-engineer
  $ git checkout -b "Cathleen_Wright_Solutions_Engineer"
  $ atom .
```

###### Vagrant

Download and install [VirtualBox 5.2](https://www.virtualbox.org/), 5.2.16 platform packages for OS X hosts.  Download and install the [latest version of Vagrant](https://www.vagrantup.com/downloads.html) for macOS, 64-bit.  Initialize, activate and SSH into the virtual machine.  

```shell
  $ vagrant init hashicorp/precise64
  $ vagrant up
  $ vagrant ssh
```

_Welcome to your Vagrant-built virtual machine._

###### Datadog and Agent Reporting Metrics

Get Started with Datadog using Datadog Recruiting Candidate as the Company. Follow the instructions to install your first Datadog Agent for Ubuntu.

![Instructions to install your first Datadog Agent for Ubuntu](https://i.imgur.com/nG4CXDv.png)

```shell
The program 'curl' is currently not installed.  You can install it by typing:
$ sudo apt-get install curl

$ DD_API_KEY=c802ac74556f263f47de0d8cddd8131a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

Agent is running and functioning properly.  Your first Datadog Agent is reporting.

![Agent is running and functioning properly](https://i.imgur.com/9cU6eQg.png)

![Initial Dashboard](https://i.imgur.com/YVjtSIO.png)

<hr>

### Collecting Metrics

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Research [how to assign tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) in the documentation, specifically [assigning tags using the configuration files](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files), information about the [configuration files and folders for the Agent locations](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/#configuration) and [troubleshooting forums](https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-) for specific file locations.  I referred to [tags best practices](https://docs.datadoghq.com/getting_started/tagging/#tags-best-practices) when creating my tags.  

As a backup, created a temporary copy of the original .yaml file.  

```shell
  $ sudo cp /etc/datadog-agent/datadog.yaml /tmp
```

Modify `/etc/datadog-agent/datadog.yaml` in vi, restarting service to force change.

```shell
  $ sudo vi /etc/datadog-agent/datadog.yaml
  $ sudo service datadog-agent restart
```

![datadog.yaml before change](https://i.imgur.com/wPXbUf9.png)

![datadog.yaml after change](https://i.imgur.com/Qjp3Y10.png)

![host map tags](https://i.imgur.com/d8lls61.png)

> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Install MongoDB 2.0.4 on virtual machine.  [Follow configuration instructions](https://app.datadoghq.com/account/settings#integrations/mongodb), including insertion of datadog user.

[Configuration](https://app.datadoghq.com/account/settings#integrations/mongodb) **Step 1**:

![mongodb install](https://i.imgur.com/vpuRyud.png)

![mongodb ok](https://i.imgur.com/OFDWUO3.png)

**Step 2**: Edit `/etc/datadog-agent/conf.d/mongo.d/conf.yaml` and add the MongoDB instances to instances:

![edited yaml](https://i.imgur.com/t8migsU.png)

*Note: File name varies between configuration instructions,  [mongo.d/conf.yaml](https://docs.datadoghq.com/integrations/mongo/#configuration) & [conf.d/mongo.yaml](https://app.datadoghq.com/account/settings#integrations/mongodb).  Used `mongo.d/conf.yaml`.*

**Step 3**: Restart the agent.

```shell
  $ sudo service datadog-agent restart
```
**Step 4**: Execute the info command and verify that the integration check has passed.

```shell
  $ sudo datadog-agent status
```
![step 4 infocheck](https://i.imgur.com/es3dwJE.png)

![mongodb dashboard](https://i.imgur.com/4AFbmsg.png)

> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

> Change your check's collection interval so that it only submits the metric once every 45 seconds.

> Bonus Question Can you change the collection interval without modifying the Python check file you created?

<hr>

### Candidate Information

Solutions Engineer Hiring Challenge - Cathleen Wright

- [LinkedIn](https://www.linkedin.com/in/cathleenmwright/)
- [GitHub](https://github.com/cwithac)
