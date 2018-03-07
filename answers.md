
# Datadog Introduction Guide
Datadog is a monitoring service for applications at scale. I will show the setup from first installing the agent to customizing a dashboard and setting up email alerts.

This demonstration will monitor several applications running in an Ubuntu image managed by Vagrant. The host operating system is a Debian laptop.

- [Setup the environment](#setup-the-environment)
  - [Install VirtualBox](#install-virtualbox)
  - [Install Vagrant](#install-vagrant)
- [Collecting Metrics](#collecting-metrics)
  - [Install Datadog agent](#install-datadog-agent)
  - [Add tags to Agent](#add-tags-to-agent)
  - [Install Postgres and Integrate with Datadog](#install-postgres-and-integrate-with-datadog)
  - [Writing an Agent Check](#writing-an-agent-check)
  - [Agent Check](#agent-check)
  - [Collection Interval](#collection-interval)
  - [Bonus Questoin: Collection Interval](#bonus-questoin-collection-interval)
- [Visualizing Data](#visualizing-data)
  - [Timeboards](#timeboards)
  - [Bonus Question: Anomoly function](#bonus-question-anomoly-function)
- [Monitoring Data](#monitoring-data)
  - [Alerts](#alerts)
  - [Scheduling Downtime](#scheduling-downtime)
  - [Using cURL API](#using-curl-api)
- [Collecting APM Data](#collecting-apm-data)
- [Final Question](#final-question)
- [Final Thoughts](#final-thoughts)

## Setup the environment
### Install VirtualBox
[Available here](https://www.virtualbox.org/wiki/Linux_Downloads), I followed the instructions that added it to my apt-get library to make it easier to update in the future. My current version is VirtualBox 5.2.

Make sure [virtualization technology is enabled](http://hackaholic.info/enable-hardware-virtualization-vt-x-amd-v-for-virtualbox) in your BIOS. Many Debian systems have this disabled by default.

### Install Vagrant
[Vagrant](https://www.vagrantup.com/intro/index.html) is available through `apt-get install vagrant`. 

As of writing this document, I encountered an issue with downloading vagrant through apt-get. Downloading through apt-get gives me Vagrant 1.9. This version [doesn't seem to be compatible with VirtualBox 5.2](https://github.com/geerlingguy/drupal-vm/issues/1587). I uninstalled Vagrant then reinstalled the latest Vagrant 2.0.2, which resolved my issue. Find instructions [here](https://github.com/openebs/openebs/issues/32).

---

Now all of the basic tool have been installed. Before continuing I recommend watching the [DataDog 101 course](https://www.youtube.com/watch?v=uI3YN_cnahk&list=PLdh-RwQzDsaOoFo0D8xSEHO0XXOKi1-5J) and skimming through [the docs](https://docs.datadoghq.com/getting_started/).

## Collecting Metrics
The basis of Datadog's functionality comes from the metrics it collects from your hosts. In order to send metrics to Datadog, we have to install the agent on our system. After that we will configure some applications to send their metrics.

### Install Datadog agent
When you first log in to Datadog you will see instructions on how to install the Datadog agent. For our Vagrant setup, we will be copying the [Ubuntu installation commands](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/) into a bootstrap shell script which will be triggered when we run `vagrant up`. This is what the file looks like right now:

```bash
#!/usr/bin/env bash

echo "bootstrap.sh 1: allow apt to install through https"
sudo apt-get update
sudo apt-get install apt-transport-https

echo "bootstrap.sh 2: set up the Datadog deb repo on system and import Datadog's apt key"
sudo sh -c "echo 'deb https://apt.datadoghq.com/ stable 6' > /etc/apt/sources.list.d/datadog.list"
sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 382E94DE

echo "bootstrap.sh 3: install the Agent"
sudo apt-get update
sudo apt-get install datadog-agent

echo "bootstrap.sh 4: copy the example config and plug in API key from .env"
source .env
echo "api key: $DATADOG_API_KEY"
sudo sh -c "sed 's/api_key:.*/api_key: $DATADOG_API_KEY/' /etc/datadog-agent/datadog.yaml.example > /etc/datadog-agent/datadog.yaml"

echo "boostrap.sh 5: start the datadog agent"
sudo initctl start datadog-agent
```
And the Vagrantfile:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"
  
  config.vm.provision :file, source: ".env", destination: ".env"
  config.vm.provision :shell, path: "bootstrap.sh"
end
```

In order to keep my Datadog API key secret, I have added a .env file which is excluded from git tracking. The file is uploaded to the ubuntu image on startup, then accessed by the bootstrap script. This method seemed to me to be the easiest to implement and most extendible for future updates that may need more secrets available.

Now that [bootstrap.sh](dd_agent_bootstrap.sh) is written, the key has been added to [.env](.env), and the [Vagrantfile](Vagrantfile) is calling both, we are ready to run `vagrant up`. The process should take a few minutes, but at the end we should see something like:

```
default: boostrap.sh 5: start the datadog agent
default: datadog-agent start/running, process 1313
```

I can now go to the Datadog website, and see that my image is sending data. I ran a couple commands to throttle the CPU (check out [stress](https://www.hecticgeek.com/2012/11/stress-test-your-ubuntu-computer-with-stress/)), just to see how the graphs would react, and I seemed to get the exact output I would expect from throttling 1, then 2 CPUs.

![stress test on ubuntu image](screenshots/initial_dashboard.png)

### Add tags to Agent
One of the most important configurations to set up is tagging. Datadog is meant to monitor large quantities of hosts, and without a way to organize them, important patterns and information could be lost in the noise. Tags allow you to organize your metrics and create more usable visualizations and alerts.

Tags can be set in the datadog.yaml file, the same config file that we set the API key. You can also set them manually in your host map view, but something like this should really be automated. This can be done in a couple ways, but the simplest for this demo was to add a line in the agent bootstrap file:

```bash
sudo sed -i 's/# tags:.*/tags: role:database, region:us/' /etc/datadog-agent/datadog.yaml
```

Now when we look at this VM, the tags `role:database` and `region:us` are listed.

![ubuntu host tags](screenshots/host_tagging.png)

### Install Postgres and Integrate with Datadog
The Datadog agent is now on the image, so we can set up integrations with any applications running. Integrations are available for [hundreds of applications](https://docs.datadoghq.com/integrations/). We will be setting up a [PostgreSQL DB system](https://www.postgresql.org/about/). The default Vagrant setup files listed in the [Postgres wiki](https://wiki.postgresql.org/wiki/PostgreSQL_For_Development_With_Vagrant#Vagrant) worked fine for me, so I will just merge both Vagrantfiles, and import the relevant files into my repo.

Our new Vagrantfile looks like this:

```ruby
$script = <<SCRIPT
  echo I am provisioning...
  date > /etc/vagrant_provisioned_at
SCRIPT

Vagrant.configure('2') do |config|
  config.vm.box = 'ubuntu/trusty64'

  config.vm.provision 'shell', inline: $script
  config.vm.provision :shell, path: 'postgres_bootstrap.sh'
  config.vm.network 'forwarded_port', guest: 5432, host: 15_432

  config.vm.provision :file, source: '.env', destination: '.env'
  config.vm.provision :shell, path: 'dd_agent_bootstrap.sh'
end
```

I got most of the [postgres_bootstrap.sh](postgres_bootstrap.sh) from the wiki, but added a few lines to create a table and connect a `datadog` user to it. This user I created is what the Datadog agent will use to monitor the db and send metrics. Adding a user this way is only for demonstration purposes, most databases would have a more stable user provisioning system than a shell script hardcoding SQL into a vagrant vm. Well, they should at least.

After reloading vagrant to take our new provisioning into effect we are rewarded with seeing postgres metrics listed in our host map:

![postgres metrics](screenshots/postgres_integration.png)

### Writing an Agent Check
### Agent Check
If you cannot find an integration available for your software and still want to collect metrics on it, then you have [multiple options](https://docs.datadoghq.com/developers/metrics/) available to you: the API, DogStatsD, and agent checks. We will quickly implement an agent check here.

In order to create an agent chekc we need to have a configuration file and then a python script which inherits from AgentCheck. We will have send a random number between 0 and 1000 as a metric.

[random_value.py](bootstrap_scripts/random_value.py)
```python
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('random.number', random.randint(0, 1000))
```

[random_value.config](bootstrap_scripts/random_value.yaml)
```yaml
init_config:

instances:
  [{}]
```
This is all that's needed to see our metric in a timeboard:

![random number agent check](screenshots/random_agent_check.png)

### Collection Interval
The boilerplate config becomes more useful when we have more complex setting we wish to use. For example we can change the update interval from the default 20 seconds, to instead only send data every 45 seconds.

```yaml
init_config:
  min_collection_interval: 45
instances:
  [{}]
```

This doesn't mean the the data is sent every 45 seonds though. The Datadog agent is configured to collect and send data every 15 seconds, adding this 45 makes it so that this metric will be skipped until 45 seconds has passed. So after 15 seconds the agent will skip this file, then 30 seconds it will skip again, and after 45 seconds the metric will be sent.

### Bonus Questoin: Collection Interval
> **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

The collection interval can be set through the `min_collection_interval` value under `init_config` in the yaml file, as shown above. It could also be modified by increasing the interval of the agent itself using the datadog.yaml file, since if the agent only collects data every 60 seconds, then by defalt the agent check will also.

Judging by how this bonus question mentions modifying the Python file though, I assume it can also be done by editing the AgentCheck instance variable directly in the Python check file e.g. `self.min_collection_interval = 60`, however when I tried this it didn't seem to reflect in the dashboard, and I wasn't able to find any documentation showing how to edit the value through the constructor. It would seem to be accessible based on the source code I see [here](https://github.com/DataDog/dd-agent/blob/master/checks/__init__.py#L337), but I may be misunderstanding the Agent lifecycle, or Python object inheritance. (or have a typo)

## Visualizing Data
### Timeboards
We have already seen/ created a few timeboards in the Datadog app, but we can also create them using the[ Datadog API](https://docs.datadoghq.com/api/?lang=python#timeboards), along with basically any other task we'd want to on the site. In this case the docs are so comprehensive, that there is basically no work to do besides fill in the details. An easy way to generate the data is to go to the app and create a dashboard and use the UI there, then copy from the JSON tab. 

![time gui json](screenshots/timeboard_api_gui_json.png)

It may seem counterintuitive to basically be doing this twice, but the goal of the API, isn't really to make a single quick dashboard. Some reasons to use the API to create timeboards are to backup your definitions as code and allow version control of the dashboards.

My implementation of the dashboard is visible in [timeboard.py](timeboard.py). I added the following metrics:

* **random.number**: this is the metric coming in from the custom agent we installed. 
* **random.number - rollup sum**: this overlays another metric in the same timeboard. It takes the random number metric and for each interval sums all data in the interval to a single point. I set it to rollup over a 5 minute interval. So the sums are hovering around 10K.
* **postregressql.db.count - anomolies**: this metric is on a seperate board, otherwise it would not be visible at all compared to the scale random.number is at. This metric checks how many databases there are in the postgres server, and the anomaly function highlights any sudden changes in red.

![timeboards](screenshots/timeboards.png)

### Bonus Question: Anomoly function
> **Bonus Question**: What is the Anomaly graph displaying?

The [anomaly function](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) is an algorithm that detects unusual changes based on previous metrics history. This can be used for very complex trends, taking into account several variables, but for our situation it just colored the graph when I created a spike in number of databases from 1 to 5.

## Monitoring Data
### Alerts 
We have our graph, but what happens when something goes wrong? What if those random numbers ever get really high? I'll certainly want to konw if that random number goes over say 800, that could be important. But I don't want to sit and watch it all day. To solve this problem we can use monitors. 

From either the timeboard gear icon, or the monitor section in the sidebar, I can choose to create a new monitor for the metric random.number. Then we just fill out the form. 

One of the issues that gave me trouble was that in order to use the host.name variable in my message, I had to make sure the alert was a multi alert, triggered separately per host. Without this feature enabled the Datadog alert wouldn't know what host it's coming from, in order to included it in the message.

The alert will trigger every 5 minutes, emailing me if that random number is in any ineresting zones.

![Email alert](screenshots/alert_email.png)

### Scheduling Downtime
As important as this alert is, we only care about it during work hours. After work emails should be limited to only the most important. Luckily we can schedule downtime. The page is accessible through the submenu of monitoring. I created two schedules, on for weekdays from 7pm to 9am the next day, and another for weekends. When scheduling I made sure to include a description and tagged myself so that I got an email.

![schedule downtime email](screenshots/disable_monitoring.png)

### Using cURL API
Once again these tools don't need to be created with the GUI, the API has endpoints for all these alerts and monitoring tools. Instead of Python, this time I have created a small shell script making a cURL request to Datadog that will generate the exact same monitors and schedules. Check it out [here](curl_monitor.sh). One of the benefits of cURL over Python, is that the Python API doesn't have all functionality yet, while cURL can use every endpoint.

## Collecting APM Data
* link agent to flask api
> **Bonus Question**: What is the difference between a Service and a Resource?

## Final Question
> Is there anything creative you would use Datadog for? 

I always thought that creativity requires a bit of structure. Before I think of an interesting use, I want to figure out what things Datadog excels at, abstracted out beyond infrastructure and applications, that might give me some better ideas.

* monitoring live events
* sending out alerts for anomolies and threshholds
* simplifying complex systems into human parseable visualizations
* overlaying data from disparate sources in order to establish patterns

So I would want to be alerted when a some kind of threshhold is exceeded, and the data is coming from a complex source. 

My immediate thought is groceries. I would want to somehow feed grocery data into Datadog, all of my staple food items would have a timeboard showing each brands' current/future price. If a gallon milk goes below $4, I want to be notified so that I can pick it up on the way home. This seems pretty useful to me since I could overlay several brands from several stores. Accurate data collection might be difficult though.  Creating all the timeboards and linking the various brands for every common food type could also be more trouble than it's worth. It seems like something that might be automatable through AI, if a decent API doesn't already exist though. 

## Final Thoughts

This is my first time working with a lot of this technology. At every chance where I could choose the technologies I chose something I was less familiar with. Postgres over MySql, Vagrant over Docker, etc. I thought these exercises would be a good opportunity to increase my knowledge of these tools, which is great for me, but may impact the quality of the explanations. If there are any inaccuracies or silly mistakes I made when using these tools I would appreciate correction.

Another new tool I learned was [bfg](https://rtyley.github.io/bfg-repo-cleaner/), at some point in the process I accidentally uploaded an api key to GitHub. This is just a trial account and I immediately updated my keys through the website, but I thought it would be cool to use bfg to also scrape my history clean. [Here](https://github.com/draav/hiring-engineers/commit/fbd9edf19f5322a20783b7a14786fc4d88450f3e#diff-e4e349f3dcefcaa939b79b899a041181) is an example of a file that had it's text replaced.

My final new tool I'll talk about is the laptop I'm developing on. I just got a used laptop a week or two back to code on (My main desktop is just a time sink of Reddit and Steam games). I installed Debian, since I've never used Linux outside of a VM. Writing this guide has given me a great chance to flesh out my development environment and figure out what tools I like best. It also let me tackle some interesting challenges like getting virtualization working in order to use Vagrant. 

If you've made it this far, thanks for reading.