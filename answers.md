Your answers to the questions go here.
# Solutions Engineer Hiring Exercise



### Prerequisites - Setup The Environment


##### Vagrant

Downloaded and installed [VirtualBox 6.0](https://www.virtualbox.org/wiki/Downloads) for OS X hosts. I then downloaded and installed the [latest version of Vagrant](https://www.vagrantup.com/downloads.html) for 64-bits macOS.  

I initialized, activated and SSHed into the virtual machine using following commands on my terminal:  

```shell
  $ vagrant init ubuntu/xenial64
  $ vagrant up
  $ vagrant ssh
```
Your screen should look like below on typing the above commands on your terminal -

![vagrant set up](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/vagrant%20set%20up.png)


![vagrant ssh](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/vagrant%20ssh.png)

##### Datadog Sign up 

Signed up for [Datadg](https://app.datadoghq.com/signup), used `Datadog Recruiting Candidate` in the Company field.

##### Datadog Agent Installation

Navigated to Integrations tab on the Datadog webapp and selected Agent option. 

![integrating_agent](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/installation%20instructions.png)

Chose the correct platform which is Ubuntu in my case and followed the 1-step installation instructions

![ubuntu_agent](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/ubuntu%20agent.png)

The following command was used on terminal to install the datadog-agent

```shell
The program 'curl' is currently not installed.  You can install it by typing:
$ sudo apt-get install curl
$ DD_API_KEY=f1939bb97730746da2a69d15c07b5901 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

You can see the following success message on the terminal after correct agent installation.

![Agent is running and functioning properly](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/Agent%20installation%20success%20message.png)


<hr>



### Collecting Metrics

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Studied [how to assign tags](https://docs.datadoghq.com/tagging/assigning_tags/?) documentation to get a better idea of tags. I referred [configuration file location](https://docs.datadoghq.com/agent/faq/agent-configuration-files/?tab=agentv6) to get the location of my agent configuration file on ubuntu.   

I had to use sudo admin privildeges to acess and make changes to the datadog.yaml file. This was done by initially navigating back to the vagrant root directory and then accessing datadog.yaml file from the datadog-agent directory. Here are the commands used for the same -

```shell
  $ cd..
  $ cd /etc/datadog-agent
  $ sudo nano datadog.yaml
```

*`nano` is vagrant's built-in text editor.*

I referred[tags best practices](https://docs.datadoghq.com/getting_started/tagging/#tags-best-practices) while creating my tags. The above command opened datadog.yaml file in my terminal. I then added my respective tags to this file using the correct format as seen in the following image -

![datadog.yaml](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/tags%20file.png)

I then closed the file saving changes (using Cntrl + X) and restarted the agent

```shell
  $ sudo service datadog-agent restart
```

These tags could be reflected on the datadog webapp hostmap. To observe these changes, I navigated to Host Map under Infrastructure tab on the left navigation of datadog webapp. My Host Map with tags could be seen there as below -


![host map tags](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/tags.png)

> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Installed PostgreSQL on virtual machine. I have used PostgreSQL for this assignment as I’ve used it for a number of projects while pursuing my Masters in CS. I referred [PostgreSQL installation](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04). 

**Step 1**:
Installed postgresql using the following commands on my terminal

```shell
  $ sudo apt-get update
  $ sudo apt-get install postgresql postgresql-contrib
```
![postgres installation](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/postgres%20install.png)

Navigated to Integrations section of the webapp and looked up for PostgreSQL integration there. I then clicked into it and finished installing it. 

The configurations tab read as
create user datadog with password 'Generate Password';
grant SELECT ON pg_stat_database to datadog;

I clicked on Generate Password button to generate my PostgreSQL password. I referred [how to use postgres on ubuntu 16.0](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04) document to learn the usage of postgres on ubuntu. The following command switched me to postgres account on ubuntu

```shell
  $ sudo -i -u postgres
```

The following command was used to access the postgres prompt

```shell
  $ psql
```

I then created a user on postgres and granted permissions to him following the configuration instructions as shown below

![postgres user](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/switch%20to%20postgres%20%26%20create%20user%20with%20grant.png)

**Step 2**: Configured the agent to connect to the PostgreSQL server. For this step, I accessed conf.d/postgres.yaml file

```shell
  $ \q
  $ cd /etc/datadog-agent/conf.d
  $ sudo nano postgres.yaml
```

I added some content to the postgres.yaml file as shown and saved the changes

![postgres.yaml file](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/postgres%20yaml%20file.png)

**Step 3**: Restart the agent

```shell
  $ sudo service datadog-agent restart
```
**Step 4**: Execute the Agent status command and verify that the integration check has passed. Look for postgres under the Checks section.

```shell
  $ sudo datadog-agent status
```

![step 4 status](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/postgres%20staus%20check.png)

The terminal status as well as the webapp integration success message proved that the installation was successful.

> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Referred [writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) for this part.

The document asked me to create 2 files named my_metric.yaml and my_metric.py files such that their names should match. The check file `my_metric.py` should be placed in `checks.d` folder while the configuration file named `my_metric.yaml` of the configuration and check files must match. If your check is called `my_metric.py` your configuration file must be placed in `conf.d` folder.

I navigated to /etc/datadog-agent/checks.d directory and created a file called my_metric.py

```shell
  $ cd /etc/datadog-agent/checks.d
  $ sudo nano my_metric.py
```
Saved the following code in my_metric.py

`my_metric.py`
```python
from checks import AgentCheck
import random
class MyMetric(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randint(0,1000))
```

![my_metric.py](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my_metric.py.jpeg)

I then navigated to `/etc/datadog-agent/conf.d` and created my_metric.yaml file and created the my_metric.yaml file there

```shell
  $ cd /etc/datadog-agent/cof.d
  $ sudo nano my_metric.yaml
```
Saved the following code in my_metric.yaml

`my_metric.yaml`
```python
instances:
  [{}]
```

![my metric.yaml](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my_metric.yaml.jpeg)


Restarted the Agent for the changes to reflect and checked the agent status.

```shell
  $ sudo service datadog-agent restart
  $ sudo service datadog-agent status
```
![my metric status](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my_metric%20status%20check.png)
![my_metric check](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/my_metric%20status%20check%20copy.png)

> Change your check's collection interval so that it only submits the metric once every 45 seconds.

I opened my_metric.yaml file again to make the following changes to it before saving it again

`my_metric.yaml`
```python
instances:
    -   min_collection_interval: 45
```
![my_metric 45 secs interval](https://github.com/Shrutiku/hiring-engineers/blob/Shruti_Kulkarni_Solutions_Engineer/screenshots/45%20sec%20interval%20for%20yaml.png)

Restart the Agent for the changes to be reflect.

```shell
  $ sudo service datadog-agent restart
```
To verify if this was successful, I checked datadog-agent status using sudo datadog-agent status a couple of times and verified that the total run count was updating after 45 seconds

I found the following important point in the agent check documentation -

_The default is 0 which means it’s collected at the same interval as the rest of the integrations on that Agent. If the value is set to 30, it does not mean that the metric is collected every 30 seconds, but rather that it could be collected as often as every 30 seconds._

> Bonus Question Can you change the collection interval without modifying the Python check file you created?
Yes, the collection interval can be changed by directly changing the collection interval in the '/conf.d/my_metric.yaml' configration file like I did in the above step.

<hr>
