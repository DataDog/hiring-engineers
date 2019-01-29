# Datadog Exercise Overview - Suzy Lockwood

This exercise is used to apply as a Solutions Engineer at Datadog. Sweet! Let's do it!

Main objectives:

1. Collect Metrics
2. Visualize Data
3. Monitor Data
4. Collect APM Data

# Prerequisites -Setting Up Environment

## Setup Ubuntu VM on Local Machine

First, as per recommendations, I started off by installing Vagrant and VirtualBox in order to create a Vagrant Ubuntu VM. Although I have never used them before, it was pretty easy to setup:

- [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)
- [What are Vagrant and VirtualBox and How Do I Use Them?](https://www.taniarascia.com/what-are-vagrant-and-virtualbox-and-how-do-i-use-them/)

### Upgrade Ubuntu VM OS

The next step was to upgrade to at least Ubuntu Linux 16.04 to avoid dependency issues.

- [How to upgrade to Ubuntu Linux 18.04](https://www.zdnet.com/article/how-to-upgrade-to-ubuntu-linux-18-04/)

During the Ubuntu upgrade, I came across an unexpected prompt asking which device to install GRUD, but some research revealed that I should select /dev/sda and all seemed good to go for next steps.

- [Ask Ubuntu - GRUD install devices](https://askubuntu.com/questions/23418/what-do-i-select-for-grub-install-devices-after-an-update)
- [Vagrant GitHub Issue - What is grub-pc?](https://github.com/hashicorp/vagrant/issues/289)

After upgrading Ubuntu, I received a few errors that did not seem to affect the success of the upgrade, but I searched for solutions in case it was a quick fix.

- ![Screenshot of Upgrade](screenshots/Linux_Upgrade_via_Vagrant.PNG)

- [Ask Ubuntu - linux-image-generic error](https://askubuntu.com/questions/899739/linux-image-generic-error)

- [How To Solve “sub process usr bin dpkg returned an error code 1″ Error in Ubuntu](https://itsfoss.com/dpkg-returned-an-error-code-1/)

The issue seemed a common one and simple to fix. Here is ultimately what I executed to remove and then subsequently fix the broken and unnecessary packages:

```
sudo apt-get autoremove --purge
sudo apt-get -f install
```

### Setup Ubuntu VM on Local Machine - THE UNEXPECTED PART TWO

In our next exciting episode of "Let's Earn a Job at Datadog", our VM was not booting up for us after several attempts. To save time, we spun up a new VM and tried the ubuntu/xenial64 box to give us version 16.04 from the beginning. It actually worked even better without errors!

- ![Screenshot of Xenial64 Success](screenshots/Linux_New_Ubuntu_Xenial_via_Vagrant.PNG)

### Extra Setup - GUI and Chrome Installation

- [Extra Step to get GUI Working in VirtualBox](https://stackoverflow.com/questions/18878117/using-vagrant-to-run-virtual-machines-with-desktop-environment)
- [Extra Step to install Google Chrome in VirtualBox](https://linuxconfig.org/how-to-install-google-chrome-browser-on-ubuntu-16-04-xenial-xerus-linux)
- [Archive Error Resolution](https://askubuntu.com/questions/91543/apt-get-update-fails-to-fetch-files-temporary-failure-resolving-error)

## Installing Datadog Agent

After signing up, Datadog gives you an easy one-step process for installing the Agent via Ubuntu. I successfully installed the Agent and had it start automatically.

- ![Screenshot of Datadog Agent Installation Success](screenshots/Install_Datadog_Agent.PNG)

# Collect Metrics

In this section, we have specific tasks or questions to complete from Datadog, which we will attempt to answer under each respective list item.

1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

- ![Screenshot of Host Map Page](screenshots/Datadog_Host_Map_Tags.PNG)

2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

- ![Configuring Agent to Connect to PostgreSQL](screenshots/Configuring_Agent_to_Connect_to_PostgreSQL.PNG)
- ![Screenshot of PostgreSQL Agent Status](screenshots/Agent_Status_with_Postgres_Integration_Check.PNG)

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

- ![Creating Custom Agent Check Files](screenshots/Creating_Custom_Agent_Check_Files.PNG)
- ![Verifying Check is Running](screenshots/Verifying_Check_is_Running.PNG)

4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

- ![Updating Collection Interval](screenshots/Updating_Collection_Interval.PNG)
- [Extra: Learned you cannot use Tabs in YAML](https://github.com/moraes/config/issues/1)

5. Bonus Question: Can you change the collection interval without modifying the Python check file you created?

- Response: I believe editing the files is the only way, or at least it is not obvious there's another way from the documentation. According to Datadog documentation, "For Agent 6, min_collection_interval must be added at an instance level and is configured individually for each instance." So it seems to me that you have to change the configuration file for each instance level (Agent 5 was global).

# Visualize Data - Part One

For this section, we need to utilize the Datadog API to create a Timeboard that contains certain aspects. We will include a screenshot of the logic for each and the overall timeboard.

- ![Overall Timeboard](screenshots/Timeboard.PNG)

1. Your custom metric scoped over your host (I also added my hello.world custom metric as a constant).

- ![my_metric Timeseries](screenshots/my_metric_Timeseries.PNG)

2. Any metric from the Integration on your Database with the anomaly function applied.

- ![PostgreSQL with Anomalies](screenshots/PostgreSQL_with_Anomalies.PNG)

3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

- ![my_metric with Rollup](screenshots/my_metric_with_Rollup.PNG)

# Visualize Data - Part Two

Now that the Timeboard is created, we need to access the Dashboard from your Dashboard List in the UI and do a few tasks.

1. Set the Timeboard's timeframe to the past 5 minutes

- ![Timeboard Last Five Minutes](screenshots/Timeboard_Last_Five_Minutes.PNG)

2. Take a snapshot of this graph and use the @ notation to send it to yourself.

- ![Send Snapshot to Myself](screenshots/Send_Snapshot_to_Myself.PNG)

3. Bonus Question: What is the Anomaly graph displaying?

- Response: Based on an algorithm that takes into account historical trends of the metric, the gray band shows the anomaly-detection algorithm’s predicted range. If any data falls outside that range, it's considered an anomaly.

# Monitor Data

Now, we need to create a new Metric Monitor that watches the average of our custom metric (my_metric) and will alert if it’s above the values below over the past 5 minutes. We will provide screenshots of our progress!

1. Warning threshold of 500
2. Alerting threshold of 800
3. And also ensure that it will notify you if there is No Data for this query over the past 10m.

- ![Metric Monitor Setup - Alert Conditions](screenshots/Metric_Monitor_Alert_Conditions.PNG)

Next, we need to configure the monitor’s message so that it will:

1. Send you an email whenever the monitor triggers.
2. Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
3. Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
4. When this monitor sends you an email notification, take a screenshot of the email that it sends you.

- ![Metric Monitor Setup - Notifications](screenshots/Metric_Monitor_Notifications.PNG)

* ![Metric Monitor Email](screenshots/Metric_Monitor_Email.PNG)

5. Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
   a. One that silences it from 7pm to 9am daily on M-F.
   b. And one that silences it all day on Sat-Sun.
   Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

- ![Bonus Question - Metric Monitor Downtime Weekdays](screenshots/Metric_Monitor_Downtime_Weekdays.PNG)

- ![Bonus Question - Metric Monitor Downtime Weekends](screenshots/Metric_Monitor_Downtime_Weekends.PNG)

- ![Bonus Question - Downtime Email](screenshots/Downtime_Email.PNG)

# Collect APM Data

We have been given a Flask app (or any Python/Ruby/Go app of our choice) to instrument using Datadog’s APM solution. Screenshots to follow of our progress and answers!

1. Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

- ![Dashboard for myapp APM.PNG](screenshots/myapp_APM.PNG)

2. Please include your fully instrumented app in your submission, as well.

- ![Node Web Application app.js File](screenshots/Node_Web_Application_File.PNG)
- ![Node Web Application Up and Running](screenshots/Node_Web_Application_Works_Browser.PNG)

3. Bonus Question: What is the difference between a Service and a Resource?

- Response: A service is a collection of processes that form a feature such as a webapp or database service. A resource is a subset of a service like the underlying SQL in a query to the database. For more information, I found this Datadog [article](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-) and [documentation](https://docs.datadoghq.com/tracing/visualization/).

# Final Question

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

- Response: Well, my first thought when I saw Datadog is that I have applications that I've deployed on Heroku and it's not always the easiest to monitor what is going on once they're deployed. I bet Datadog would be a great asset here. Maybe a more creative thought, I like metadata, so it would be interesting to monitor various infrastructure monitoring tools or even the same tool (like Datadog) across customers/hosts. I am also a huge gamer so monitoring whether a server is down (on my various online games, many of which have multiple servers) might give me a quick consolidated view of what is up and ready to play that night!
