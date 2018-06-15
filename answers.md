*Your answers to the questions go here.*

Thanks for the oppurtunity to complete the tech challenge!  Please see my results inline.

## Vagrant Config
To start off the exercise I setup the most basic possible Ubuntu 16.04 Vagrant config:

```ruby
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "public_network"
end
```

I ran `vagrant up`, waited for the box to download, and moved onto the next step.

> **Note**: I use the combination of vagrant/Virtualbox all the time so I already had the components installed on my mac

## Signing Up
I completed the signup, but I did skip the survey as to not add 'junk' to your system since this is just a test account.

## Getting the agent installed
After the vagrant box came up I grabbed an ssh session via `vagrant ssh`.  Following the instructions of the `Install your first Datadog Agent` wizard; I ran the following command: 
  ```bash
  DD_API_KEY=<redacted> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"```
  ```
After that completed successfully I verified that the agent was running (as described in the post-install text):
  ```console
  vagrant@ubuntu-xenial:~$ sudo systemctl status datadog-agent
  ● datadog-agent.service - "Datadog Agent"
     Loaded: loaded (/lib/systemd/system/datadog-agent.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2018-06-15 13:45:30 UTC; 59s ago
   Main PID: 2942 (agent)
      Tasks: 9
     Memory: 21.8M
        CPU: 902ms
     CGroup: /system.slice/datadog-agent.service
             └─2942 /opt/datadog-agent/bin/agent/agent start -p /opt/datadog-agent/run/agent.pid
  ```
Back in the webui the `Finish` button was now 'clickable' and I continued.

## Collecting Metrics
See below for each section of the challenge.
### Add Tags
To add tags I first navigated to the `/etc/datadog-agent` location and started reviewed the `datadog.yaml` file to see how far I could get on my own (before consulting docs).  I found this in the example configuration file:

```
# Set the host's tags (optional)
# tags:
#   - mytag
#   - env:prod
#   - role:database
```

I entered a similar format into the datadog.yaml file and checked the tags assigned by navigating to the `Infrastructure` view in the WebUI and clicking on **Inspect** to get the details.  To my dismay, I didn't find the tags.  I tried restarting the agent (thinking maybe it didn't reload automatically when the config file is changed) but there was no impact.  Within the tooltip in the WebUI it said agent tags are submitted via setting in `dd-agent/datadog.conf` but I couldn't find that directory nor the file (tried to locate via mlocate).  It was time to hit the docs; my answer came on [this](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files) page.  The problem was that the `datadog.yaml` file doesn't actually accept the tags in this format (allow that is valid in other locations).  I updated my `datadog.yaml` file with tags as shown:

```yaml
tags: id:matt_laptop, env:testing, role:techchallenge, location:ohio, building:house
```

And here is the view of these glorious tags in the UI!

![glorious tags](/img/tags.jpeg)

### Database Integration
I choose to install MySQL.  Installation was simple, completed via a basic apt command:

```bash
sudo apt-get update
sudo apt-get install mysql-client mysql-server
```

When prompted, I set the root password for the database.  Here is the result:
```console
vagrant@ubuntu-xenial:/etc/datadog-agent$ mysql -uroot -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.22-0ubuntu0.16.04.1 (Ubuntu)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

To install the integration I first navigated to the `Integrations` menu item, searched for `MySQL`, hovered over it, and finally clicked **Install**.  When the `MySQL Integration` page opened I navigated to the `Configuration` tab and followed the instructions(I did have to add user/pass to the commands supplied by the Wizard):

```bash
sudo mysql -uroot -p -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '%BgoD7k2bNO9IFfiviG59Mgb';"
sudo mysql -uroot -p -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
sudo mysql -uroot -p -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
sudo mysql -uroot -p -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
```

I also successfully ran the validation scripts(results only shown here):

```console
MySQL user - OK
MySQL grant - OK
MySQL SELECT grant - OK
MySQL PROCESS grant - OK
```

I created conf.d/mysql.yaml with the following contents:

```yaml
init_config:

instances:
  - server: localhost
    user: datadog
    pass: '<redacted>'
```
Also, I adjusted the permissions to match the other files:

```bash
sudo chown dd-agent: mysql.yaml
```

Finally, I restarted the agent:

```bash
sudo systemctl restart datadog-agent
```

Back in the WebUI, I clicked on **Install Integration**.  As a final step, I ran `sudo datadog-agent check mysql` to validate that the check was working.

> **Note**: The copy/pasted config file from the WebUI did not work because it was invalid YAML. I had to put my password in single quotes to make the YAML valid.  After that the agent worked fine.

A quick screenshot of the working MySQL integration:

![mysql](img/mysql.jpeg)





