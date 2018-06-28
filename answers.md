# Datadog Solutions Engineer Exercises - Matthew Tessler

## Prerequisites - Setup the Environment

This was my first time using Datadog's platform so the engineering exercise was a great learning experience. I think I've really gotten a grasp on how the platform works and I'd be excited to learn more. The documentation, videos, and blog posts are all great for learning the vast set of resources and capabilities that Datadog makes available. The responses I've given are to the best of my current abilities. I got better at using Datadog as I went further with the exercise, and I think I know much more than I did before.

These are my responses for the engineering exercise:

### Vagrant VM Creation

I am completing this exercise on a Mac OS X operating system. To avoid dependency issues, as the instructions recommended, I decided to spin up a fresh linux VM via Vagrant. Although I've had experience with linux virtual machines, this was my first time using Vagrant. I followed their [instructions](https://www.vagrantup.com/intro/getting-started/). I ran the command `vagrant init hashicorp/precise64` to create the virtual machine. 

![vagrant init hashicorp/precise64 command](images/init.png)

Then I started up the virtual machine with the command `vagrant up` and ran the command `vagrant ssh` to interface with the virtual machine.

![vagrant up and vagrant ssh command](images/up_ssh.png)

### Datadog Account Creation

I then signed up for a Datadog account.

![sign up](images/sign_up.png)

After that I followed the instructions in the sign up process. When I got to the "Agent Setup" step I chose the "Installing on Ubuntu" option because I was using an Ubuntu VM with Vagrant. 

### Agent Installation

![ubuntu install](images/ubuntu_install.png)

I followed the "Installing with Ubuntu" steps. I entered the one line of commands from the instructions. The installation sequence ran, and at its completion, the message from the datadog-agent informed me the Agent was running and functioning properly.

![install start](images/start_of_install.png)
...
![install end](images/end_of_install.png)

After that I was able to complete the setup process and was taken to the main dashboard. 

![main dashboard](images/main_dashboard.png)

## Collecting Metrics

### Adding Tags

The instructions next said to "Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog."

I had to do some research to find where the Agent config file was located. I found the answer at this [resource](https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-). After moving to the `etc/datadog-agent` directory, I located the `datadog.yaml` file. I opened the file to edit it. 

This was my first time editing `yaml` files so I had to do a little research on the syntax. I had some debugging to do with syntax before I got things exactly right. I added some tags according to these instructions on this [page](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files), and then I went back to look at the host map. **I'm still not sure how to get the tags to reflect immediately on the host map.** I restarted the service, but I didn't see immediate effects on the platform. It just seemed to update after a certain interval. I'd like to learn more about how that runs. Regardless, now my Agent configuration file and the host map both reflect the same tags. 

The tags are visible in the configuration file at the bottom of the terminal window:

![config file](images/config_file.png)

And here are the tags in the host map:

![host map](images/host_map.png)

### Installing Database

Next I needed to install a database on the machine and then install the respective Datadog integration for that database. I decided to go with MongoDB as I'd used it before and was familiar with the interface and using it on the command line. First I updated my Ubuntu operating system from 12.04 to 14.04 in line with the instructions on MongoDB's [website](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) to install the Community Edition on Ubuntu.

After installing MongoDB, I began the install for the Integration for Datadog. I followed these [instructions](https://docs.datadoghq.com/integrations/mongo/#setup). I set up the `conf.yaml` file, set up the user in the `mongo` shell, and installed the integration on Datadog. Here you can see some screenshots on Datadog that the MongoDB integration is up and running on the host. 

![host with mongo](images/host_with_mongo.png)
![mongo integration installed](images/mongo_integration_installed.png)
![mongo dashboard](images/mongo_dashboard.png)

Running an info status check, `sudo datadog-agent status`, the checks appear for MongoDB. Here is a screenshot:

![mongo status check](images/mongo_status_check.png)

### Creating a Custom Agent Check

The next instructions are to "create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000." I read these [directions](https://docs.datadoghq.com/developers/agent_checks/#agentcheck-interface) to learn how custom agent checks work and how to submit a metric.

Following those instructions, I created a `custom_check.yaml` file in the `conf.d` directory. I also created a `custom_check.py` file in the `checks.d` directory. I used the `random.randint()` function to make the submissions random within the specified range. Both the aforementioned files are included in the repository.

The my_metric dashboard is now available on the host. I'm not sure why it says (no-namespace). I went back and double-checked the tutorial for custom agent checks, and I couldn't see any places where I'd differed from the instructions. Regardless, the metric submits with no problem. It is shown here on the infrastructure list page under the host I've been running.

![custom metric running](images/custom_metric_running.png)

Next up was to change the collection interval so it only submits the metric once every 45 seconds. The **bonus question** asks if this can be done without modifying the Python check file that I created. I'm actually not sure of how to modify the interval by changing the Python file. Maybe it's something obvious like creating an if-statement that only lets it run once every three times, but the way I found how to do it when researching was not through that. 

According to the documentation for the custom agent check, the checks run every 15-20 seconds depending on how many integrations there are. The way to change how often the metric is submitted is to add the `min_collection_interval` property in the `yaml` file that corresponds with the custom agent check. The way that works -based on my understanding of the documentation- is that when the collection check comes around every 15-20 seconds, it'll see if 45 seconds have elapsed since it last submitted the metric. If 45 seconds have not elapsed, it won't submit the metric. If 45 seconds have elapsed, it will. 

In my experience, this means that it either submits the my_metric every 40 seconds, or every 60 seconds. Before I changed the collection interval, it was submitting every 20 seconds. When I changed it, it does 40 seconds or 60 seconds. I kind of get why it is doing that, but not completely. Regardless, I think the `min_collection_interval` is the best way to change the submission interval.

![collection interval change](images/collection_interval_change.png)

Here is a screenshot of the my_metric dashboard. You can see that after I changed the collection interval at around 8:50 AM, the points space out. They are spaced by mostly 40 second, but some 60 second intervals.

## Visualizing Data

Next I was to use the Datadog API to create a Timeboard with three metrics on the same timeseries graph. Doing so required a bit of research. First I read the general graphing [documentation](https://docs.datadoghq.com/graphing/) for the UI. Once I was familiar, I read the [documentation](https://docs.datadoghq.com/graphing/miscellaneous/graphingjson/) about editing graphs with JSON. This is how I would be primarily editing the graph I was creating. Finally, I researched the [functions](https://docs.datadoghq.com/graphing/miscellaneous/functions/) I would be using the `anomalies()` and `.rollup()` function. I added the three metrics described in the bullet points (custom metric scoped over host, any method from Integration from database with anomaly function applied, and custom metric with rollup function). 

The script for this Timeboard is included in the repository as `timeboard.json`. Here is the completed Dashboard. I could not figure out how to set the timeframe for the Timeboard to just the last five minutes so I set it to the past hour. Here is a screenshot of the timeseries graph: 

![timeseries graph](images/timeseries_graph.png)

I then took a snapshot of the graph and used the -at- notation to send it to myself. Here is the notification showing up in my events:

![notification for graph](images/notification.png)

As for the **bonus question**, I don't think the anomaly part of the graph is displaying anything for me besides just the regular metric line because my MongoDB database doesn't have any anomalous changes to its metrics. It was completely consistent for the snapshot I took.

## Monitoring Data

### Setting Up Monitor

Next up is creating a Metric Monitor to watch the average of my custom metric and alert for certain events. I used the form to create the monitor. It notifies for a warning threshold of 500 (for a 5 minute average), notifies for an alerting threshold of 800 (for a 5 minute average), and notifies if there is No Data for the query over the past 10 minutes. This was easy enough to figure out how to do. 

I then set up the monitor's message to have special notes with each trigger. The three alerts will send the host name and host ip with their notes, and the Alert and Warning will include the metric number that triggered the monitor.

Here are screenshots of the setup:

![metric monitor 1](images/metric_monitor_1.png)
![metric monitor 2](images/metric_monitor_2.png)
![metric monitor 3](images/metric_monitor_3.png)

Here is a screenshot of an email it sent me:

![monitor email](images/monitor_email.png)

### **Bonus** Setting Up Downtime

For the **bonus question** I set up the scheduled downtime for Monday-Friday 7:00 PM-9:00 AM and Saturday-Sunday all day.

Here is the M-F downtime setup and the corresponding email notification:

![weekday downtime](images/downtime_1.png)
![weekday email](images/email_1.png)

Here is the S-S downtime setup and the corresponding email notification:

![weekend downtime](images/downtime_2.png)
![weekend email](images/email_2.png)

## Collecting APM Data

Next in the directions was instrumenting a web application using Datadog's APM solution. I decided to try using the given Flask app as I have no experience with Ruby or Go and not much experience building Flask apps. I used `pip` to install Flask (version 1.02), and then I used these [directions](http://flask.pocoo.org/docs/1.0/quickstart/) to run the Flask app. When I tried to run it `export FLASK_APP=apm_flask.py` and then `python flask -m run` it gave me an error. Here is the error:

![Python 2 Error](images/python_2_error.png)

I Googled the error, which was "AttributeError: 'module' object has no attribute 'SSLContext", and it turned out it was a common issue with running older versions of Python 2.7. The only feasible fixes I saw were to upgrade Python. The Ubuntu VM via Vagrant that I was running on the suggestion of the instructions had 2.7.6 downloaded as its default Python 2 version. So, in theory, upgrading past Python 2.7.9 would fix it. However, before I tried that, I wanted to try running it with Python 3 to see if that worked. Running it with Python 3 also gave me an error. Here is the error:

![Python 3 Error](images/python_3_error.png)

The error was "OSError: [Errno 98] Address already in use". This sounded like an issue with ports already being in use. However, I used the command `lsof -i :5050` to see what process was running on that port, and there was none. I tried changing the port that the Flask app ran on and it gave me the same error. This confused me, so I decided to go back to the Python 2 route.

I researched how to upgrade Python on Ubuntu from 2.7.6 to 2.7.14 (the latest version of Python 2.7) and I didn't find any official resources for doing so. Most resources asserted that it would not be easy. I didn't want to risk messing up the VM or the Datadog agent within it and having to start over or reinstall everything. I tried the steps on this blog [post](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/) but they didn't work. I thought maybe using virtualenv would do the trick, but I still couldn't figure out a good way to upgrade the version to one that would work. 

I thought I might try running the Flask app and doing the APM data collection from my local environment, but I had trouble installing the trace agent after successfully downloading the regular agent.

I tried a few more ways to get the Flask app to run, including just running a barebones Flask app and then working up from there, but this yielded the same errors. I'm not quite sure how to fix the issues I've been running into, so I decided to detail these notes after a few hours of trying to get it to work. The directions for installing the trace agent on Ubuntu and instrumenting the Flask app seemed pretty straightforward, I just couldn't get to the steps beyond running the Flask app.

I might be making some obvious errors or there might be easy fixes for this, but I'm not sure what they are. If I was working with other engineers, at this point I'd probably ask for help from someone more knowledgeable than me. I was able to complete all of the other technical sections of the engineering exercise, but this one I could not.

## Final Question

I think a creative way to use Datadog would be to monitor noise pollution in New York and/or 311 complaints in New York. NYC Open Data would be a good resource for that. I think hosts could be blocks on the grid, or streets, or neighborhoods, and then the 311 complaints could be submitted metrics. They could be divided up by their specific metrics (e.g. loud parties, cars honking, construction, etc.) and aggregated. Metric monitors could be triggered if certain areas went over a threshold, and the police could be notified. It could be a great way to deploy resources, organize data about a common issue, and allow people to make informed decisions about where they lived and/or worked. In the longterm, this could be used to affect zoning and policy decisions. 




