# **DATADOG TUTORIAL**
In this tutorial, you will be installing Datadog and exploring some of the great features it has to offer. This tutorial will be explained while using Mac OS X.  Throughout this tutorial there will be links, screenshots, and documentation to help you get through each step.  If you would rather use a virtual machine for this tutorial, please follow the instructions under “Setting Up Your Environment” to do so.  Otherwise, skip down to the “Signing up for Datadog” section.

If you have any questions along the way, please go to our help center for further support. <https://help.datadoghq.com/hc/en-us>

## SETTING UP YOUR ENVIRONMENT TO USE A VIRTUAL MACHINE
------------------------------

To begin, you will need to get the necessary programs installed on your computer.  If you are new to virtual machines, check out the following resources to get more acquainted with what they do:
1. <https://en.wikipedia.org/wiki/Virtual_machine>
2. <https://www.youtube.com/watch?v=yIVXjl4SwVo>

#### Installing VirtualBox
You will need to download and install VirtualBox.  Click on the link below to begin downloading the OS version of VirtualBox for your computer.
<https://www.virtualbox.org/wiki/Downloads>  

#### Installing Vagrant
Vagrant is a tool for building and managing virtual machine environments.  Click on the link below. On the pop-up screen, click on the appropriate OS version to begin downloading.
<https://www.vagrantup.com/downloads.html>

![Imgur](https://i.imgur.com/n1dGDJQ.png)

After downloading the appropriate version for your computer, follow the instructions for installation on your local computer.

Once you are finished installing the software, navigate to the “getting started” page for Vagrant here: <https://www.vagrantup.com/intro/getting-started/> and follow the instructions on verifying the installation was successful. Since you have already installed vagrant, you will only need to verify that the installation was successful.

Next, go to the project setup page.  <https://www.vagrantup.com/intro/getting-started/project_setup.html> You have the option of either creating a new directory or incorporating Vagrant in a pre-existing directory.  Please choose the appropriate option for your needs and then follow the instructions.

![Imgur](https://i.imgur.com/63Kilfx.png)

Now head over to the Boxes page.
<https://www.vagrantup.com/intro/getting-started/boxes.html>
Follow the instructions to create an Ubuntu 12.04 LTS 64-bit box by using the following command in your terminal or command-line:

```
$ vagrant box add hashicorp/precise64
```
In the terminal, please choose VirtualBox from the list of providers.  

![Imgur](https://i.imgur.com/PCwhK1H.png)

You should see a similar terminal indicating that the creation was successful.

![Imgur](https://i.imgur.com/yJAHHnF.png)

Now, open up the vagrantfile in your project.

![Imgur](https://i.imgur.com/cjEG58S.png)

Follow the instructions to set the box you just created as the base box that you will be working with.

Navigate to the terminal to get your virtual machine up and running:

```
$ vagrant up
```

Once the virtual machine is running successfully, move into the machine by running this command:

```
$ vagrant ssh
```

You are now running a linux OS using a virtual machine!

Resources:
<https://www.vagrantup.com/intro/getting-started/up.html>

#### Signing up for Datadog

Head over to Datadog's website <https://www.datadoghq.com/> and click on 'GET STARTED FREE'.  Fill out the appropriate fields to set up your account.

![Imgur](https://i.imgur.com/odUjhnw.png)

On the Agent Setup page, download the appropriate "version 6" agent for your local machine and follow the installation instructions.

![Imgur](https://i.imgur.com/OWLy246.png)

Next, get the agent up and running in the terminal:

```
$ datadog-agent start
```

If started successfully, the agent setup page will tell you so and will prompt you to the next step!

To learn more about what the Agent does, you may view the documentation here:
<https://docs.datadoghq.com/agent/>.

## Collecting Metrics
---------------------

#### Adding tags
Tags are a great way to add scope to your data.  Read through the documentation for learning about tags:
<https://docs.datadoghq.com/getting_started/tagging/>

First start by adding tags to your config file by going into your console and typing the command:

```
$ open /opt/datadog-agent/etc/datadog.yaml
```
Scroll down until you find the "Set the hosts tags" section.  Remove the hashes to uncomment the area and add any tags that you desire using the key value format.  

![Imgur](https://i.imgur.com/7BPkr5v.png)

You should now be able to see your host and new tags in the host map tab for Datadog.

![Imgur](https://i.imgur.com/vOzKhNe.png)

#### Installing a database
Next, you will install PostgreSQL to use as your server.  If you don't have PostgreSQL installed already, you can follow these instructions to install PostgreSQL using homebrew: <https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb>

Once PostgreSQL is installed, create a database on the command line:

```
$ createdb [your database name here]
```

Next, you will need to integrate PostgreSQL with Datadog using Datadog's provided integration.  You will start by first adding a postgres.yaml file in the agent's conf.d directory.  To do so follow these commands in the command-line:

```
$ cd ~/.datadog-agent/conf.d/
$ touch postgres.yaml
```

You can read more about this step and using the PostgreSQL integration here: <https://docs.datadoghq.com/integrations/postgres/>

Now, go to <https://app.datadoghq.com/account/settings#integrations/postgres> to create the integration. Follow the instructions to install the integration.

![Imgur](https://i.imgur.com/6lhlIrZ.png)

#### Creating a custom agent check
Check out the documentation for creating a custom check:
<https://docs.datadoghq.com/agent/agent_checks/#directory-structure>

Follow the instructions below:
Change the metric name in python file to my_metric instead of ‘hello.world’
Change the value to 500
-  Create a my_check.yaml file in the conf.d folder located at /opt/datadog-agent/etc/conf.d
-  Create a my_check.py file in the checks.d folder located at /opt/datadog-agent/etc/checks.d

![Imgur](https://i.imgur.com/IMfWldW.png)

You will want to return a random value to the metric in the my_check.py file.  To do so, you will need to import randint from random then call the function in the gauge like so:

![Imgur](https://i.imgur.com/XiO1wWs.png)

Stop the agent then restart it in the console.  Then, go to the metric summary board in Datadog.

![Imgur](https://i.imgur.com/g9MvPmu.png)

You should see the new metric 'my_metric' in the summary.  Additionally, you can run this command in the console to see details regarding your metric:

```
$ datadog-agent check my_check
```

Under the Running Checks section, you should see something similar to the image below.

![Imgur](https://i.imgur.com/vPaisa1.png)

#### Change your checks collection interval

To change the collection interval of your check, you may add a method in the init config for your <your check name>.yaml file.

![Imgur](https://i.imgur.com/Na1SYNR.png)

## Visualizing Data
-------------------

#### Utilizing the Datadog API to create a Timeboard

Let’s look at the documentation again to learn more about the Datadog API here:
<https://docs.datadoghq.com/api/?lang=ruby#timeboards>

![Imgur](https://i.imgur.com/XXJMCIz.png)

You will use Ruby for your API request.  Create <your file name>.rb file in your project directory.

Copy and paste the example request in your new script file and change out the api key and app key for your own.  You can find your keys here:
<https://app.datadoghq.com/account/settings#api>
Ensure that you are getting a response by printing out the last line of code by adding a 'p' in front of it like so:

![Imgur](https://i.imgur.com/4tNKBGp.png)

Next, open up your console and run:

```
$ ruby <your file name>.rb
```

You should see a response similar to the response on the documentation page.

#### Adding your custom metric to the Timeboard
Let’s look at more documentation for making certain requests from the API,  specifically adding metrics.  <https://docs.datadoghq.com/getting_started/from_the_query_to_the_graph/>

You will start by adding your custom metric scoped to your host.  In your new script file replace the default query for your own metric that is scoped over our host.  It should look like:
 "q" => “<your_metric_name>{$host}”

![Imgur](https://i.imgur.com/4g2Uogi.png)

Feel free to change the description and titles in your script file to whatever you like.

#### Adding a metric with the anomaly function applied and adding the rollup function to your custom metric
You can read about how functions work here:
<https://docs.datadoghq.com/graphing/miscellaneous/functions/>
You can also read about how the anomaly function works here:
<https://docs.datadoghq.com/monitors/monitor_types/anomaly/>

Go back into your script file and make the following changes to the graphs requests:

![Imgur](https://i.imgur.com/KSCwYnb.png)

Now, go back into your console and re-run: 
```
$ ruby <your file name>.rb
```

Next, go into your Datadog dashboard list.  You should see your newly created Timeboard!  Go check it out.

#### Set the timeboard's timeframe to 5 minutes and send to yourself using the annotation feature

You can hold down your mouse and scroll over the timeframe that you want to select.  Scroll over the past 5 minutes then click on the camera icon to send a snapshot.  Use the @ symbol to send it to yourself.

![Imgur](https://i.imgur.com/cvJXmDs.png)

![Imgur](https://i.imgur.com/w8G1yHN.png)

#### Bonus question: What is the anomaly graph showing

The anomaly function works by calculating the data of the past and predicting what it should be in the future.  Check out this great article on how it works in detail:
<https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/>

Note: The anomaly graph that is showing for me is indicating spikes in the number of commit transactions being submitted to PostgreSQL.

## Monitoring Data

#### Creating a new Metric Monitor

Click on the "New Monitor" tab located in the monitors section of your Datadog navigation bar.

![Imgur](https://i.imgur.com/H4RvX1Z.png)

Choose the “Metric” option to begin creating your custom metric.  Also, check out these documentation pages on monitors to better understand how they work:
<https://docs.datadoghq.com/monitors/monitor_types/>
<https://docs.datadoghq.com/monitors/>

Lets walk through these steps to set up your Monitor:
For your monitor you will use the Threshold Alert option.

![Imgur](https://i.imgur.com/qALF0y0.png)


2. Choose my_metric and leave the other options as is.

![Imgur](https://i.imgur.com/MupBcVk.png)


3. Choose to trigger the metric when it is above the average threshold during the last 5 minutes.  You should have an Alert threshold of 500 and a Warning threshold of 800. Also change the option to notify yourself if data is missing for more than 10 minutes.

![Imgur](https://i.imgur.com/3AQir4R.png)


4. Lastly, set up your monitor message that you will receive when any thresholds are met.  You can also look at this documentation to see all of the notification options:
  <https://docs.datadoghq.com/monitors/notifications/>

Let’s set up your Monitor Message to give specific messages based on what thresholds are being triggered.  You will also add the value and Host IP to the message if the Alert threshold is met.  Lastly, tag yourself in order to receive an alert email.

![Imgur](https://i.imgur.com/Wrn6vox.png)

#### Bonus question: Scheduling downtimes

Here you can find how to setup downtimes:
<https://docs.datadoghq.com/monitors/downtimes/>

Under the Monitors tab click on the “Manage Downtime” option then click on the Schedule Downtime button.

![Imgur](https://i.imgur.com/02Y2aF4.png)

You are going to schedule 2 downtimes.

For the first schedule:
- Select the Monitor you just created and whichever host/hosts you'd like to apply the downtime to.
- Click the Recurring option and choose Repeat Every 1 weeks for Monday - Friday, beginning at 7:00 p.m. until 9:00 a.m.
- Add any message you'd like to notify anyone of the downtime.
Click Save

![Imgur](https://i.imgur.com/Wbq71cs.png)

For the second schedule:
- Select the same options for the Monitor and hosts
- Click the Recurring option and choose Repeat Every 1 weeks for Saturday and Sunday, beginning at 12:00 a.m. until 12:00 a.m.
Click Save

![Imgur](https://i.imgur.com/VeDl2iv.png)

## Collecting APM Data

You are going to create a Ruby on Rails app and integrate Datadog's APM solution.  This part of the tutorial will assume you have Ruby and Rails installed on your local machine.  If you do not follow the instructions in the Ruby and Rails documentation:
Ruby install: <https://www.ruby-lang.org/en/documentation/installation/>
Ruby on Rails install: <http://installrails.com/>

Once you have completed installation, start up a Rails app in the command line:

```
$ rails new datadog_apm -T -d postgresql --skip-turbolinks
```

Next, go onto Datadog and navigate to the APM option. Click “Get Started”.  Choose Ruby then the Rails option.

![Imgur](https://i.imgur.com/5H3ArNV.png)

Install the Ruby client by adding it in your Gemfile.

![Imgur](https://i.imgur.com/rzidNxO.png)

Then run:

```
$ bundle install
```

Add the initializer file and code in your config folder.

![Imgur](https://i.imgur.com/Qum1tHO.png)

Next, you will get the Datadog APM agent running.  <https://github.com/DataDog/datadog-trace-agent#run-on-osx>

Since you already have the Datadog agent installed, you just need to download the latest OSX Trace Agent (or the agent for whichever operating system you are using).  Since you are using version 6 of the agent your datadog.conf file is named datadog.yaml.  Run this command in the terminal:

```
./trace-agent-osx -config /opt/datadog-agent/etc/datadog.yaml
```

If you haven’t set up your API key in your new app, you may receive an error similar to this:

```
you must specify an API Key, either via a configuration file or the DD_API_KEY env var
```

If that is the case, run this command to setup your API key:

```
$ DD_API_KEY=<your API key here without quotes> ./trace-agent-osx -config /opt/datadog-agent/etc/datadog.yaml
```

Lastly, create whatever controllers, routes,and views you'd like in you Rails app and then run:

```
rails s
```

Open up a new browser and navigate to localhost:3000.  You should see some activity in the trace-agent-osx logs.

#### Make a new Dashboard with both APM and Infrastructure Metrics

Lets make a new Dashboard called APM and Infrastructure Metrics.  Pick the “Timeseries” widget and drag it down to make a new graph.

![Imgur](https://i.imgur.com/gM3Hnk2.png)

Now pick any Infrastructure metric and APM metric you'd like.

![Imgur](https://i.imgur.com/sAwuUUG.png)

![Imgur](https://i.imgur.com/xWq9jvY.png)

#### Bonus question: Difference between a Service and a Resource
<https://docs.datadoghq.com/tracing/terminology/>

![Imgur](https://i.imgur.com/kpiHXcr.png)

## What would I use Datadog for?

The first thing that came to my mind when I thought of using Datadog would be to monitor river systems and weather.  As an owner of a small fly fishing company in Yosemite, I'm constantly looking at water levels and weather for the dozens of rivers and streams within the area.  

Often times, the websites I use are inaccurate or off-line.  They also have lackluster visualizations to show their data.  Showing consistent and reliable weather forecasts is also a huge pain in the butt!  I would love to use Datadog to combine these into an easy to use, accurate, and visually pleasing app.
