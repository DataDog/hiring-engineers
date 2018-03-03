# **DATADOG TUTORIAL**
In this tutorial we will be installing Datadog and exploring some of the great features it has to offer while using Mac OS X.  Throughout this tutorial there will be links, screenshots and documentation to help you get through each step.  If you have any questions along the way please go to our help center for further support. <https://help.datadoghq.com/hc/en-us>

## SETTING UP YOUR ENVIRONMENT
------------------------------

We will be using a linux virtual machine during this tutorial.  This will keep you from running into any operating system or dependency issues and help get you up and running quickly.  To begin lets go ahead and get the necessary programs installed on our computer.  If you are new to virtual machines check out these resources to get more acquainted with what they do:
1. <https://en.wikipedia.org/wiki/Virtual_machine>
2. <https://www.youtube.com/watch?v=yIVXjl4SwVo>

### Installing VirtualBox
You will need to download and install VirtualBox to use Vagrant.  Click on the link below to begin downloading the OS X version of VirtualBox for your computer.
<https://www.virtualbox.org/wiki/Downloads>  
Make sure that your computer allows VirtualBox to install.  You can look to see if your computer is blocking any installations under the security and privacy page in your settings.

### Installing Vagrant
Vagrant is a tool for building and managing virtual machine environments.  Click on the link below and click on the OS X version to begin downloading.
<https://www.vagrantup.com/downloads.html>

#{show vagrant_download_page screen shot}

After downloading the appropriate version follow the instructions for installation on your local computer.  Like VirtualBox make sure your computer allows for installation.

Once finished installing head over to the getting started page for Vagrant here: <https://www.vagrantup.com/intro/getting-started/>.  Since you've already installed vagrant you only need to verify that the installation was successful.  Follow the instructions on verifying the installation was successful.

Next go to the project setup page.  <https://www.vagrantup.com/intro/getting-started/project_setup.html> You have the option of either creating a new directory or incorporating Vagrant in a pre-existing directory.  Please choose the appropriate option for your needs and then follow the instructions on the page.

#{show vagrant_project_setup}

Lets now head over to the Boxes page.
<https://www.vagrantup.com/intro/getting-started/boxes.html>
Follow the instructions to create a Ubuntu 12.04 LTS 64-bit box by using the command in your terminal or command-line:
```
$ vagrant box add hashicorp/precise64
```
In the terminal please choose VirtualBox for the choices of providers.  

#{show terminal_creating_box}

You should see a similar terminal indicating the creation was successful.

#{show successful_box_creation}

Now open up the vagrantfile in your project.

#{show project_config}  

Follow the instructions to set the box you just created as the base box you will be working with.

Resources:
<https://www.vagrantup.com/intro/getting-started/up.html>

### Signing up for Datadog

Head over to Datadog's website <https://www.datadoghq.com/> and click on 'GET STARTED FREE'.  Fill out the appropriate fields to set up your account.

#{show datadog_signup}

On the Agent Setup page download the OS X agent for your local machine then follow the installation instructions.

#{show agent_setup}

Next we will get the agent up and running:

```
$ datadog-agent start
```

If it started successfully the agent setup page will tell you so and you can go on to the next step!

After the agent is done installing go into the terminal to get your virtual machine up and running:

```
$ vagrant up
```

Then move into the machine by running this command:
```
$ vagrant ssh
```

You are now running a linux OS using a virtual machine!

To learn more about what the Agent does and how to better us it you can look through the documentation here <https://docs.datadoghq.com/agent/>.

## Collecting Metrics
---------------------

NOTE: Due to running into errors while using the virtual machine I decided to continue this tutorial using my Mac OS X operating system.

#### Adding tags
Read through the documentation for learning about tags. <https://docs.datadoghq.com/getting_started/tagging/>

Lets start by adding tags to our config file by going into our console and typing the command:
```
$ open /opt/datadog-agent/etc/datadog.yaml

```
Scroll down until you find the "Set the hosts tags" section.  Remove the hashes to uncomment the area and add any tags you want using the key value format.  

#{show assigning_tags_config}

You can then see your host and new tags in the host map tab for Datadog.

#{IMPORTANT! SHOW host_map_tags}

#### Installing a database
Next we will install PostgreSQL to use as our server.  If you don't have PostgreSQL installed already you can follow the instructions from here to install PostgreSQL using homebrew: <https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb>

Once PostgreSQL is installed create a database on the command line:
```
$ createdb [your database name here]
```

Next we need to integrate PostgreSQL with Datadog using Datadog's provided integration.  We'll start by first adding a postgres.yaml file in the agent's conf.d directory.  To do so follow these commands in the command-line:
```
$ cd ~/.datadog-agent/conf.d/
$ touch postgres.yaml
```

You can read about this step and more regarding integrations here: <https://docs.datadoghq.com/integrations/postgres/>

Now lets go to <https://app.datadoghq.com/account/settings#integrations/postgres> to create the integration. Follow the instructions to install the integration.

#{show postgres_integration}

#### Creating a custom agent check
Lets check out the documentation for creating a custom check:
<https://docs.datadoghq.com/agent/agent_checks/#directory-structure>

Follow the instructions below: (just change the metric name in python file to my_metric instead of 'hello.world' and change the value to 500).

- Create a my_check.yaml file in the conf.d folder located at /opt/datadog-agent/etc/conf.d

- Create a my_check.py file in the checks.d folder located at
/opt/datadog-agent/etc/checks.d

#{show creating_check}

We want to return a random value to the metric in the my_check.py file.  You will need to import randint from random then call the function in the gauge like so:
#{show custom_check}

Stop the agent then restart it in the console.  Then go to the metric summary board in Datadog.
#{show metrics_summary_page}

You should see the new metric 'my_metric' in the summary.  Additionally, you can run this command in the console:
```
$ datadog-agent check my_check
```

Under the Running Checks section you should see something similar to the below image.
#{show agent_check}

#### Change your checks collection interval

To change the collection interval of your check you can add a method in the init config for your <your check name>.yaml file.

#{show init_config}

#### Bonus question for collection interval
WORK ON THIS ONE!

## Visualizing Data
-------------------

#### Utilizing the Datadog API to create a Timeboard

Lets again check out the documentation to learn about the Datadog API here:
<https://docs.datadoghq.com/api/?lang=ruby#timeboards>
#{show api_reference}

We will use Ruby for our API request.  Create <your file name>.rb file in your project directory.

Copy and paste the example request in your new script file and change out the api key and app key for your own.  You can find your keys here:
<https://app.datadoghq.com/account/settings#api>
Lets make sure that we are getting a response by printing out the last line of code by adding 'p' in front of it like so:
#{show print_api_response}

Next open up your console and run:
```
$ ruby <your file name>.rb
```

You should see a response similar to the response on the documentation page.

#### Adding your custom metric to the timeboard
Lets look at more documentation for making certain requests from the API,  specifically adding metrics.  <https://docs.datadoghq.com/getting_started/from_the_query_to_the_graph/>

We'll start by adding our custom metric scoped to our host.  In our new script file lets replace the default query for our own metric that is scoped over our host.  It should look like "q" => "<your_metric_name>{$host}"
#{show custom_metric_query}

Feel free to change the description and titles in your script file to whatever you like.

#### Adding a metric with the anomaly function applied and adding the rollup function to our custom metric
You can read about how functions and the anomalies function work here:
<https://docs.datadoghq.com/graphing/miscellaneous/functions/>
<https://docs.datadoghq.com/monitors/monitor_types/anomaly/>

Go back into your script file and lets change some things in the graphs requests.  We will make two more requests like so:
#{show metrics_request}

Now go back into your console and re run:
```
$ ruby <your file name>.rb
```

Next go into your Datadog dashboard list.  You should see your newly created Timeboard!  Go check it out.

#### Set the timeboard's timeframe to 5 minutes and send to yourself using the annotation feature

You can hold down your mouse and scroll over the timeframe you want to select.  Scroll over the past 5 minutes then click on the camera icon to send a snapshot.  Use the @ symbol to send it to yourself.
#{show annotation}

#### Bonus question: What is the anomaly graph showing

The anomaly function works by calculating the data of the past and predicting what it should be in the future.  Check out this great article on how it works in detail:
<https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/>

The anomaly graph that is showing for me is indicating spikes in the number of commit transactions being submitted to PostgreSQL.

## Monitoring Data

#### Creating a new Metric Monitor

Click on the "New Monitor" tab located in the monitors section of your Datadog navigation bar.
#{show new_monitor_page}

Choose the Metric option then we will begin creating our custom metric.  Also check out these documentation pages on monitors to better understand how they work:
<https://docs.datadoghq.com/monitors/monitor_types/>
<https://docs.datadoghq.com/monitors/>

Lets walk through these steps to set up our Monitor:
1. For our monitor we will use the Threshold Alert option.
  #{show threshold_alert_option}

2. Choose my_metric and leave the other options as is.
  #{show define_metric}

3. Choose to trigger the metric when it is above the average threshold during the last 5 minutes.  You should have an Alert threshold of 500 and a Warning threshold of 800.  Lets also change the option to notify us if data is missing for more than 10 minutes.
  #{show alert_conditions}

4. Lastly lets set up our monitor message that we will receive when any thresholds are met.  You can also look at this documentation to see all of the notification options:
  <https://docs.datadoghq.com/monitors/notifications/>

Lets set up our Monitor Message to give specific messages based on what thresholds are being triggered.  We will also add the value and Host IP to the message if the Alert threshold is met.  Lastly tag yourself in order to receive an alert email.
  #{show monitor_message}


#### Bonus question: Scheduling downtimes

Here you can find how to setup downtime:
<https://docs.datadoghq.com/monitors/downtimes/>

Under the Monitors tab click on the Manage Downtime option then click on the Schedule Downtime button.
#{show schedule_downtime}
We are going to schedule 2 downtimes.

For the first we'll:
- Select the Monitor we just created and whichever host/hosts you'd like to apply the downtime to.
- Click the Recurring option and choose Repeat Every 1 weeks for Monday - Friday, beginning at 7:00 p.m. until 9:00 a.m.
- Add any message you'd like to notify anyone of the downtime.
- Click Save
#{show downtime_options_1}

For the second:
- Select the same options for the Monitor and hosts
- Click the Recurring option and choose Repeat Every 1 weeks for Saturday and Sunday, beginning at 12:00 a.m. until 12:00 a.m.
- Click Save
#{show downtime_options_2}

## Collecting APM Data
