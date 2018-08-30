Your answers to the questions go here.

## Prerequisites - Setup the environment

Summary:
For this part I decided to use Vagrant and Virtualbox. Following the guide I installed both Vagrant and Virtualbox. I'm currently using a mac, so I downloaded both of them for the mac (.dmg extension). Following the instructions that comes with the installers I installed both Vagrant and VirtualBox (Detailed explanation is listed at the end). 

Once installation is completed I created a folder to hold all the work and then I went into the folder and set up vagrant with linux version 16.04. All vagrant boxes versions can be found here: https://app.vagrantup.com/boxes/search. ubuntu/xenial64 is 16.04, so I went with that. 

```
$vagrant init ubuntu/xenial64
```

Once vagrant is finished being set up, I started it with:
```
$vagrant up
```

At this point vagrant will run a VirtualBox with Linux version 16.04. I then SSH'd into it using:
```
$vagrant ssh
```

At this point my user on my terminal changed to "vagrant@ubuntu-xenial" so I knew everything was working as intended. 

I registered for a 14 day trial account here: https://www.datadoghq.com/ and clicked the "get started free" button on the upper right. Once registered I skipped the part where I describe my stack.

```
Detailed:
For Vagrant I went to https://www.vagrantup.com/downloads.html and downloaded the macOS 64-bit installer. Once it finished downloading, I double clicked the downloaded file and then double clicked the vagrant.pkg icon. At this point after clicking continue and then next, the installer proceeded and started installing into the computer. There will be a security prompt that pops up asking for your computer password to finish the installation. Once installed the downloaded file can be safely deleted.

For virtualbox I went to https://www.virtualbox.org/wiki/Downloads and downloaded the VirtualBox for OS X hosts. I repeated the steps listed above in the vagrant installation and installed the VirtualBox on my computer.
```

## Collecting Metrics:

To start collecting metrics I had to install the agent into my virtual machine. Since my virtual machine is running linux, I went with the ubuntu installation instructions here: https://app.datadoghq.com/signup/agent#ubuntu. I was able to find that installing the agent was as simple as running a command in the command line in my virtual machine via ssh. Since I wasn't upgrading, I went with option 1.

```
DD_API_KEY=<API KEY HERE> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

I knew everything was running fine since I saw on both https://app.datadoghq.com/signup/agent#ubuntu and my terminal was saying that the agent is running properly. 


### Assigning tags:
I looked at this page: https://docs.datadoghq.com/tagging/assigning_tags/ for information on how to add custom tags for my host. To add tags I would have to edit the datadog.yaml file. The datadog.yaml file is located in /etc/datadog-agent according to https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-. To edit the file, I had to use vi text editor(vi) with elevated privileges (sudo).
```
$sudo vi datadog.yaml
```

Once inside datadog.yaml loaded on my SSH terminal, I went and explored it a bit and found tags were there already, just commented out. I uncommented it by deleting the "#" and added my own custom tags in accordance to https://docs.datadoghq.com/tagging/assigning_tags/.
```
tags:
   - name:steven
   - gender:male
   - role:trial
```
Two things I noted was that the host map on the datadog website took a few mins to update and also to not use tab indentation on .yaml files. 

```
Usefull Vi editor commands:
i   : insert edit mode
esc : exit edit mode
x   : delete at position when not in edit mode
:w  : save file
:q  : quit
```

###Installing a database and integrating:
I picked MySQL for this part. Installation of MySQL into the virtual machine was done using the following commands in the SSH:
```
$sudo apt-get update
$sudo apt-get install mysql-server
```
The installation will download and set up the MySQL server. After installation I made a passwordsimple password and used it to go into MySQL using: 
```
$mysql -u root -p
```

Once there, I prepped MySQL for the datadog integration by following this guide:https://docs.datadoghq.com/integrations/mysql/. I created a user called datadog: 
```
CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'test123';
```
I then exited mysql and verified the datadog user using:
```
mysql -u datadog --password=test123 -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"

mysql -u datadog --password=test123 -e "show slave status" && \
echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
```

The first one came back green and ok, the second one was missing REPLICATION CLIENT grant. To fix that I went back into MySQL and did the following:
```
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
GRANT PROCESS ON *.* TO 'datadog'@'localhost';
```
I exited MySQL again and tested the command that failed last time and this time it passed. Following the guide I granted access to perfomance schema by running the following: 
```
GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
```

Following the guide I navigated to /etc/datadog-agent/conf.d/mysql.d and created a file called conf.yaml and opened it again in my terminal editor Vi.
```
sudo touch conf.yaml
sudo vi conf.yaml
```

I copied the supplied code snippet provided in the guide https://docs.datadoghq.com/integrations/mysql/.
```
  init_config:

  instances:
    - server: 127.0.0.1
      user: datadog
      pass: 'test123' # from the CREATE USER step earlier
      port: 3306 # 3306 is default MySQL port, since I didn't change it should be still 3306
      options:
          replication: 0
          galera_cluster: 1
          extra_status_metrics: true
          extra_innodb_metrics: true
          extra_performance_metrics: false
          schema_size_metrics: false
          disable_innodb_metrics: false
```

I then restarted the agent by running and checked the agent status to see if my MySQL was integrated:
```
$sudo service datadog-agent restart
$sudo datadog-agent status
```


###Creating a custom Agent check

From reading the guide at https://docs.datadoghq.com/developers/agent_checks/, I gathered that I needed to create a my_metric.py inside /etc/datadog-agent/checks.d. Also, I needed to make my_metric.yaml inside /etc/datadog-agent/conf.d. The names of the py file must match with the yaml file. In my case it would be my_metric.py and my_metric.yaml. The guide provides the template and with a small alteration, we can change the value being sent from 1 to a random number between 1 and 1000.
```
my_metric.py:
    import random
    from checks import AgentCheck
    class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my metric value', random.randint(1, 1000))


my_metric.yaml:
    init_config:

    instances:
        [{}]
```

The agent check can be verified by checking the status of the agent or by going on to datadog website and looking at the host. There should be a new app in blue once you click on the host. If you click the newly appeared app you can see our custom metric being sent in.


###Setting a collection interval for my metric

A minimal interval can be set by editing the my_metric.yaml file inside /etc/datadog-agent/conf.d. This can be achieved by adding min_collection_interval into our yaml file and setting it equal to the minimum amount of time in between checks. In our case 45 seconds. Alternatively, you can also edit the python file to add a delay using time.sleep() method(I think?). I lack the knowledge of the inner workings of the datadog agent so I'm not entirely sure if this will mess with anything else.
```
my_metric.yaml:
instances:
    - min_collection_interval: 45

my_metric.py
import random
from checks import AgentCheck
class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my metric value', random.randint(1, 1000))
        time.sleep(45)

```

###Bonus
As mentioned above, to add a minimum interval for the agent check can be achieved by editing the .yaml file inside the /etc/datadog-agent/conf.d. Each agent check file inside /etc/datadog-agent/checks.d has a corresponding .yaml file inside /etc/datadog-agent/conf.d that shares the same name. For example /etc/datadog-agent/checks.d/hello.py and /etc/datadog-agent/conf.d/hello.yaml. By adding min_collection_interval option to hello.yaml, we only set a minimum interval collection for hello.py. All other checks inside the checks.d will be unaffected. 


## Visualizing Data: