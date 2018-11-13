Your answers to the questions go here.
# Datadog Solutions Engineer Technical Exercise
## 
## Prerequisites - Setup the environment
Although Dockers can be fun and interesting to manipulate, I prefer the hardware isolation of a virtual machine when running tests on new software.  If some of the drawbacks of virtual machines, such as slow load and ssh issues, are more of a problem when setting up your environment, I recommend setting up a Docker or using a service like DigitalOcean to run your virtual machine.
When setting up the virtual machine for this exercise, I opted to use Vagrant in conjunction with VirtualBox, both open source and easy to setup.  I am using a MacOSX, so I installed [VirtualBox via its website](https://www.virtualbox.org/) and used Homebrew to install Vagrant.
If you do not have Homebrew installed, you can type the following in your terminal:
```bash
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew doctor
```
Once homebrew is installed, you can use Homebrew Cask to install Vagrant:
```bash
brew cask install vagrant
vagrant --version
```
Next we want to initialize vagrant with an Ubuntu vitual image, so we'll use `bento/ubuntu-18.04`:
```bash
vagrant init bento/ubuntu-18.04
```
To ensure you are using the right image, check the Vagrantfile for the following assignment: `config.vm.box = "bento/ubuntu-18.04"`.  Once you have initialized your Vagrantfile, you can start it by running:
```bash
vagrant up
```
You can verify that is running by the following command:
```bash
vagrant status
```
If for any reason you must stop vagrant or the service isn't working as expected and you need to start again, ensure that vagrant has stopped by using the following command:
```bash
vagrant halt
```

Once you have Vagrant up and running, it's now time to access the virtual machine via ssh:
```bash
vagrant ssh
```
If you decided to use another vagrant box, it is recommended that you use a minimum of Ubuntu `v. 16.04` to avoid dependency issue; so if your machine starts up with a version lower than this, you can run the following command to update (this can take quite a while so please be patient):
```bash
vagrant@vagrant:~$ sudo do-release-upgrade
```
When you have completed the vagrant setup and ssh'ed into the vagrant box, you should see a screen similar to:
![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_ByvUiAr6m.png)

Once you are in your machine, we can set up the Datadog Agent using the following command:
```bash
vagrant@vagrant:~$ DD_API_KEY=9544144fac3fab83bd92c8809616ed83 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
This will start the Datadog Agent automatically and should look like this upon completion:
![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_ryThhCBam.png)

You should also see an event log in your Datadog dashboard confirming that the agent has started:
![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_r1wUpAHpm.png)

## 
## Collecting Metrics
### Adding Tags
In order to add tags in the configuration file, first navigate to the folder containing it (we will need to navigate to this folder often):
```bash
vagrant@vagrant:~$ cd /etc/datadog-agent
```
In this folder, you'll find the file `datadog.yaml`, which we will edit to add our tags:
```bash
vagrant@vagrant:/etc/datadog-agent$ sudo vim datadog.yaml
```
> NOTE: I am using Vim to edit the configuration file.  If you would like to use another editor, you may need to install it with the command `sudo apt-get install <name of editor>`.  Also note that in order to save the edited file, you must add `sudo` in order to grant proper permission to edit the file.

Uncomment the section that features setting the host's tags and add your custom tags.  Below is an example:
```yaml
# Set the host's tags (optional)
tags:
   - ubuntu18
   - solengineer:challenge
   - vm:vagrant
```
![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_SyFwZJIaX.png)

You can then restart the agent to see the tags in your Datadog dashboard:
![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_ryWmMyUT7.png)

> You can also edit and add custom tags via the Datadog dashboard.  Under `Infrastructure`, click `Host Map`.  Click your virtual machine host and you will see an option named `Edit Tags`.  See below.
![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_ByDMm1Ipm.png)

### Installing a Database Integration
Now we can install a database and the respective Datadog integration for that database on our virtual box. I will be using Postgresql for this, installing using the following command:
```bash
vagrant@vagrant:~$ sudo apt-get install postgresql
vagrant@vagrant:~$ psql --version
```
Once you ave decided on a database, visit your Datadog and click `Integrations` to find and install the proper service (in this case, PostgreSQL). Once installed on the dashboard, you will need to install the Datadog Agent on your PostgreSQL server via the instructions given:
![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_rkgkw1I6X.png)

Now let's start PostgreSQL with the following command:
```bash
vagrant@vagrant:~$ sudo su - postgres
postgres@vagrant:~$ psql
postgres=# 
```
Our first instruction is to setup a read-only datadog user using the generated password provided:
```bash
postgres=# create user datadog with password '<COPY GENERATED PASSWORD>'
postgres=# grant SELECT ON pg_stat_database to datadog;
```
Once we have created our new user, we can execute the next set of commands:
```bash
postgres=# \q
postgres@vagrant:~$ psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" && \
echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```
This will then prompt you for a password, in which you use the password generated by datadog.  Upon completion you will see one row the `pg_stat_database` table.  Upon entering `q`, you will return to the terminal prompt and should see the message `Postgres connection - OK` . Now we need to configure the Agent to connect to PostgreSQL:
```bash
postgres@vagrant:~$ exit
vagrant@vagrant:~$ cd /etc/datadog-agent/conf.d/postgres.d
vagrant@vagrant:/etc/datadog-agent/conf.d/postgres.d$ sudo touch postgres.yaml && sudo vim postgres.yaml
```
Once in the file, follow the instructions for constructing the configuration file. An example configuration file is already located in this folder for reference.
```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: <ENTER DATADOG GENERATED PASSWORD>
       tags:
           - role:database
           - postgres
           - psql
```
Now we can restart the Datadog agent and run our first integration check to make sure everything has passed:
```bash
vagrant@vagrant:~$ sudo service datadog-agent restart
vagrant@vagrant:~$ sudo -u dd-agent -- datadog-agent check postgres
```
You should receive output similar to the following:
![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_HyMeEZLam.png)

![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_rJ3-E-IaX.png)

To view all checks in the `checks.d` directory, you can run the following command:
```bash
vagrant@vagrant:~$ sudo datadog-agent configcheck
```
And your output should be similar to this:

![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_H1X4sbU67.png)

![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_Hk8BsZL6Q.png)


### Creating a Custom Agent Check
In order to write a custom check, the names of the configuration and check files must match. So let's start by adding both files to the `conf.d` directory and the `checks.d` directory respectively:
```bash
vagrant@vagrant:~$ cd /etc/datadog-agent/conf.d
vagrant@vagrant:/etc/datadog-agent/conf.d$ sudo touch my_metric.yaml
vagrant@vagrant:/etc/datadog-agent/conf.d$ cd /etc/datadog-agent/checks.d
vagrant@vagrant:/etc/datadog-agent/checks.d$ sudo touch my_metric.py
```
Now that we have our files, let's start with editing the configuration file first.  We can set this file up similar to how we set up our configuration file for PostgreSQL.  We can also add custom tags as demonstrated below:
```bash
vagrant@vagrant:~$ cd /etc/datadog-agent/conf.d
vagrant@vagrant:/etc/datadog-agent/conf.d$ sudo vim my_metric.yaml
```
```yaml
init_config:

instances:
   -   username: datadog
   -   password: <CHOOSE A PASSWORD (OPTIONAL)>
   -   tags:
           - role:custom_check
           - my_metric
```
In order to write our Python file, we need to import the `AgentCheck` class from the `checks` module, so make sure to include it in the first line.  We also want the metric to return a random value between 0 and 1000, so we can import `randint` from the `random` module to model that behavior.  We use the method `self.gauge()` to send a guage of a random number between 0 and 1000 for `my_metric` every time it is called:
```bash
vagrant@vagrant:~$ cd /etc/datadog-agent/checks.d
vagrant@vagrant:/etc/datadog-agent/checks.d$ sudo vim my_metric.py
```
```python
from checks import AgentCheck
from random import randint

class My_Metric(AgentCheck):
    def check(self, instance):
        self.gauge('my metric', randint(0, 1001)
```
You can then verify the check works as expected by running the following command:
```bash
vagrant@vagrant:~$ sudo -u dd-agent -- datadog-agent check my_metric
```

![Image](/Users/wolf/Documents/developersBlackBook/medley/resources/rkwpKnH6Q_H1475BUaQ.png)

If you need to change the check's collection interval without adding logic to your Python file, you can modify your configuration file to include the following:
```yaml
init_config:

instances:
   -   username: datadog
   -   password: <CHOOSE A PASSWORD (OPTIONAL)>
   -   tags:
           - role:custom_check
           - my_metric
   -   min_collection_interval: 45
```

