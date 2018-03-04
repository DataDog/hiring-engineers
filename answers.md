

## Prerequisites * Setup the environment
Datadog is a monitoring service for applications at scale. I will show the setup from first installing the agent to customizing a dashboard and setting up email alerts.

This demonstration will monitor several applications running in an Ubuntu image managed by Vagrant. The host operating system is a Debian laptop.

### Install VirtualBox
[Available here](https://www.virtualbox.org/wiki/Linux_Downloads), I followed the instructions that added it to my apt-get library to make it easier to update in the future, my current version is VirtualBox 5.2.

Make sure [virtualization technology is enabled](http://hackaholic.info/enable-hardware-virtualization-vt-x-amd-v-for-virtualbox) in your BIOS. Many Debian systems have this disabled by default.

### Install Vagrant
[Vagrant](https://www.vagrantup.com/intro/index.html) is available through `apt-get install vagrant`. 

As of writing this document, I encountered an issue with this. Downloading through apt-get gives me Vagrant 1.9. This version [doesn't seem to be compatible with VirtualBox 5.2](https://github.com/geerlingguy/drupal-vm/issues/1587). I uninstalled Vagrant then reinstalled the latest Vagrant 2.0.2, which resolved my issue. [Find instructions on how to do that here](https://github.com/openebs/openebs/issues/32).

---

Now all of the basic tool have been installed. Before continuing I recommend watching the [DataDog 101 course](https://www.youtube.com/watch?v=uI3YN_cnahk&list=PLdh-RwQzDsaOoFo0D8xSEHO0XXOKi1-5J) and skimming through [the docs](https://docs.datadoghq.com/getting_started/).

## Collecting Metrics
The basis of Datadog's functionality comes from the metrics it collects from your hosts. In order to send metrics to Datadog, we have to install the agent on our system. After that we will configure some applications to send their metrics.

### Install Datadog agent
When you first log in to Datadog you will see instructions on how to install the Datadog agent. For our Vagrant setup, we will be copying the [Ubuntu installation commands](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/) into a bootstrap shell script which will be triggered when we run `vagrant up`.

In order to keep my Datadog API key secret, I have a .env file which is excluded from git tracking. The file is uploaded to the ubuntu image on startup, then accessed by the bootstrap script. This method seemed to me to be the easiest to implement and most extendible for future updates that may need more secrets available.

Now that bootstrap.sh is written, the key has been added to .env, and the Vagrantfile is calling both, we are ready to run `vagrant up`. The process should take a few minutes, but at the end we should see something like:

```
default: boostrap.sh 5: start the datadog agent
default: datadog-agent start/running, process 1313
```
I can now go to the Datadog website, and see that my image is sending data. I ran a couple commands to throttle the CPU (check out [stress](https://www.hecticgeek.com/2012/11/stress-test-your-ubuntu-computer-with-stress/)), just to see how the graphs would react, and I seemed to get the exact output I would expect from throttling 1, then 2 CPUs.

![stress test on ubuntu image](https://github.com/draav/hiring-engineers/raw/solutions-engineer/screenshots/initial_dashboard.png)

# TODO

* Install Mongo
* update vagrant provisioner to include a script that sends random data
* update interval, probably in python script that sends checks
* bonus: update interval outside of script, probably in some config file or through datadog site

## Visualizing Data

* create timeboard using a script
* mess around with timeboard inthe dashboard
* bonus: answer what the anomoly grpah does

## Monitoring Data
* create metric monitor
* make it send a dynamic email
    * screenshot of email
* bonus: limit emails to work hours

## Collecting APM Data
* link agent to flask api
* bonus: What is the difference between a Service and a Resource?

## Final Question
Is there anything creative you would use Datadog for? 

Abstract out what the primary purposes of Datadog are
* tracking live activities that update often
* things that have triggers that you want to know baout but not watch constantly
* difficult to see all objects in system (contrained by time, quantity, etc)

grocery stores/shopping lists, resources in libraries, meeting rooms in office