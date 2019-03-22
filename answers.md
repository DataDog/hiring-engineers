<img src="" alt="U" height="500" />
Prerequisites - Setup the environment:
======================================
So, a little context on this:


I ended up using vagrant after exploring Docker and just using a standalone VM. I chose vagrant because I had an existing Ubuntu VM environment that I wanted to "vagrantize", if you will. I realize now that this somewhat defeats the purpose of vagrant boxes, as they should be small, and include provisions in the form of a shell script in the vagrant file in order to have the most portable box possible. Doombox has those provisions on the inside so it's a *little* big. If I were to approach this a second time, I would provision the vagrant box by the more standard convention, or use docker.

On the bright side, since Doombox is basically a full fledged Ubuntu machine, you can interact with it's UI by enabling that option in the vagrant file, or by clicking "show" in your VirtualBox dashboard for the machine. If you did that you could always fire up DOOM while you're in there ```/home/vagrant/restful-doom/src/restful-doom -iwad Doom1.WAD -apiport 6666 ...``` and, as you may have noticed, play the game via API calls, but that's another story for another day.

#### With all that said, [Here's Doombox in all its glory on VagrantCloud](https://app.vagrantup.com/russelviola/boxes/doombox/versions/1.0.1) (Spoiler, it's a large file)

#### To get started with this, on a machine with vagrant installed run:

```
vagrant init russelviola/doombox 
vagrant up
```

- I'm working out the kinks with the auto-ssh configuration, so you'll probably see some ```default: Warning: Authentication failure. Retrying...``` errors before the machine gives up. That's a work in progress.

- **_Then_**, when the machine tires and finally gives up all hope of connecting via private key, you can use ```vagrant ssh```, you'll be prompted for a password, which is ```vagrant```


You don't necessarily need to run this to understand my approach to this exercise, as I've documented that below, but I wanted to include access to the environment 1. because that's what vagrant is for, and 2. in the case that you'd like to explore my environment with all of the following requirements implemented.

___
Collecting Metrics:
===================
To install the agent, We can follow the steps for [Ubuntu Datadog Agent Integration](https://app.datadoghq.com/account/settings#agent/ubuntu) and run ```DD_API_KEY=<YOUR_API_KEY> -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"```, which starts up the agent after installation. Then we can look to our [Datadog Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host) and see it's installed, we'll see something like this: 

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/UbuntuHostShot.png" alt="Ubuntu Host Map Icon" height="500" />

### - Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Since we're using a Linux system, our Agent config file lives at [```etc/datadog-agent/datadog.yaml```](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/datadog-agent-config/datadog.yaml). We can open this with our favorite IDE and take a look inside.
the top of the file will show your API key, so you know you're in the right place.
```yaml
# The Datadog api key to associate your Agent's data with your organization.
# Can be found here:
# https://app.datadoghq.com/account/settings
api_key: ad00c177c779cc3d503ee10c55c302dd

# The site of the Datadog intake to send Agent data to.
# Defaults to 'datadoghq.com', set to 'datadoghq.eu' to send data to the EU site.
# site: datadoghq.com

# The host of the Datadog intake server to send Agent data to, only set this option
# if you need the Agent to send data to a custom URL.
# Overrides the site setting defined in "site".
# dd_url: https://app.datadoghq.com
```
If we look down to around row 48 we'll see the ```tags``` configuration. Un-comment the line and add our tags:
```yaml
# Set the host's tags (optional)
tags:
  - name:doombox
  - env:dev
  - role:virtual_machine
  - test_tag:hello
```
#### It's important to note that when we make changes to the agents configuration files, we need to restart it for them to take effect. In the cli run ```service datadog-agent restart```

Once our agent is up and running again, after a minute or two we'll see the results reflected on our [Host Map Details](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=878227842):

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/HostDashTags.png" alt="Host Tag View" height="230" />

### - Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
### - Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
### - Change your check's collection interval so that it only submits the metric once every 45 seconds.
___
### Bonus Question Can you change the collection interval without modifying the Python check file you created?

Temp: This configuration is handled in the yaml, so we can either edit the yaml directly, or access the datadog agent GUI.
___
Visualizing Data:
=================
### Utilize the Datadog API to create a Timeboard that contains:

### - Your custom metric scoped over your host.
### - Any metric from the Integration on your Database with the anomaly function applied.
### - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
### - Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

### Once this is created, access the Dashboard from your Dashboard List in the UI:

### - Set the Timeboard's timeframe to the past 5 minutes
### - Take a snapshot of this graph and use the @ notation to send it to yourself.

___
### Bonus Question: What is the Anomaly graph displaying?

___
Monitoring Data:
==================
### Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

### - Warning threshold of 500
### - Alerting threshold of 800
### - And also ensure that it will notify you if there is No Data for this query over the past 10m.

### Please configure the monitor’s message so that it will:

### - Send you an email whenever the monitor triggers.
### - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
### - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
### - When this monitor sends you an email notification, take a screenshot of the email that it sends you.
___
### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
### - One that silences it from 7pm to 9am daily on M-F,
### - And one that silences it all day on Sat-Sun.
### - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

___
Collecting APM Data:
===================

### Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

___
### Bonus Question: What is the difference between a Service and a Resource?
___
### Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
### Please include your fully instrumented app in your submission, as well.-

___
Final Question:
===============
### Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

### Is there anything creative you would use Datadog for?

___
