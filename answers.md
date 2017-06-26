Sean Yu - Support Engineer

# Table of Contents
<!-- TOC -->

- [Table of Contents](#table-of-contents)
    - [Level 1 - Collecting your Data](#level-1-collecting-your-data)
        - [1. Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.](#1-sign-up-for-datadog-use-datadog-recruiting-candidate-in-the-company-field-get-the-agent-reporting-metrics-from-your-local-machine)
        - [2. Bonus question: In your own words, what is the Agent?](#2-bonus-question-in-your-own-words-what-is-the-agent)
        - [3. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.](#3-add-tags-in-the-agent-config-file-and-show-us-a-screenshot-of-your-host-and-its-tags-on-the-host-map-page-in-datadog)
        - [4. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.](#4-install-a-database-on-your-machine-mongodb-mysql-or-postgresql-and-then-install-the-respective-datadog-integration-for-that-database)
        - [5. Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`](#5-write-a-custom-agent-check-that-samples-a-random-value-call-this-new-metric-test-support-random)
    - [Level 2 - Visualizing your Data](#level-2-visualizing-your-data)
        - [1. Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.](#1-since-your-database-integration-is-reporting-now-clone-your-database-integration-dashboard-and-add-additional-database-metrics-to-it-as-well-as-your-test-support-random-metric-from-the-custom-agent-check)
        - [2. Bonus question: What is the difference between a timeboard and a screenboard?](#2-bonus-question-what-is-the-difference-between-a-timeboard-and-a-screenboard)
        - [3. Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification](#3-take-a-snapshot-of-your-test-support-random-graph-and-draw-a-box-around-a-section-that-shows-it-going-above-0-90-make-sure-this-snapshot-is-sent-to-your-email-by-using-the-notification)
    - [Level 3 - Alerting on your Data](#level-3-alerting-on-your-data)
        - [1. Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes](#1-set-up-a-monitor-on-this-metric-that-alerts-you-when-it-goes-above-0-90-at-least-once-during-the-last-5-minutes)
        - [2. Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.](#2-bonus-points-make-it-a-multi-alert-by-host-so-that-you-won-t-have-to-recreate-it-if-your-infrastructure-scales-up)
        - [3. Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.](#3-give-it-a-descriptive-monitor-name-and-message-it-might-be-worth-it-to-include-the-link-to-your-previously-created-dashboard-in-the-message-make-sure-that-the-monitor-will-notify-you-via-email)
        - [4. This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.](#4-this-monitor-should-alert-you-within-15-minutes-so-when-it-does-take-a-screenshot-of-the-email-that-it-sends-you)
        - [5. Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.](#5-bonus-since-this-monitor-is-going-to-alert-pretty-often-you-don-t-want-to-be-alerted-when-you-are-out-of-the-office-set-up-a-scheduled-downtime-for-this-monitor-that-silences-it-from-7pm-to-9am-daily-make-sure-that-your-email-is-notified-when-you-schedule-the-downtime-and-take-a-screenshot-of-that-notification)

<!-- /TOC -->

## Level 1 - Collecting your Data
### 1. Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
To signup for a trial account with Datadog, navigate to the datadog [website](www.datadoghq.com).
<img src="./pics/01LoginUrl_1.png">

And click on the "GET STARTED FREE" button.
<img src="./pics/01LoginUrl_2.png">

Fill up the form. Don't forget to key in Datadog Recruiting Candidate" in the "Company" field.
<img src="./pics/02Signup_1.png">

After clicking the "Sign up" button, you will be greeted by a page with a short survey.
You can fill up the form or just skip it.
<img src="./pics/03Info.png">

We are now in the page for us to setup the Datadog Agent.
Since our host machine is using Ubuntu 12.04,
lets click on Ubuntu on the left hand navigation bar.
<img src="./pics/04InstallDatadogAgent.png">
<img src="./pics/05UbuntuAgent.png">

Open a terminal and execute the code.
<img src="./pics/06CLIInstall.png">

The Datadog Agent installation is pretty quick and will show quite a long text showing the installation progress.
<img src="./pics/07CLIInstallStart.png">
<img src="./pics/08CLIInstallEnd.png">  
  
After finishing all that action in the Terminal, lets go back to our web browser and click the "Finish" button.
<img src="./pics/09NextPage_1.png">

On the next page, we should be able to see that our Ubuntu host is now sending data to our Datadog account in the cloud.
<img src="./pics/10GetAgentDone.png">

*Useful Links*
  * [Agent Status and Information](https://help.datadoghq.com/hc/en-us/articles/203764635-Agent-Status-and-Information)  
  * [Start/Stop/Restart the Datadog Agent](https://help.datadoghq.com/hc/en-us/articles/203764515-Start-Stop-Restart-the-Datadog-Agent)

### 2. Bonus question: In your own words, what is the Agent?
>An agent is an application which runs in the background, and performs different kinds of tasks. In the case of our newly installed Datadog Agent, it collects and sends metrics about our Ubuntu installation to Datadog's servers.

### 3. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.  
> Let us now add tags to our host so it can be easily be identified in our Datadog Dashboard. We first need to locate the Agent configuration file in our Ubuntu installation.
In Linux, the Agent configuration file is located at **/etc/dd-agent/datadog.conf**.  
You will need to open the configuration file with sudo, using your preferred text editor.  
The snippet below opens the Agent configuration file, with sudo privileges, using the text editor gedit.    
```
sudo gedit /etc/dd-agent/datadog.conf
```
<img src="./pics/11AgentConfigLocation.png">
Look for the line which has the text "Set the host's tags (optional)", and below that line add your tags in key:value pairs.
Try adding the line below on the datadog.conf file.

>**tags: os:ubuntu1404, country:aus**

<img src="./pics/12EditDatadogConf_1.png">

After adding the line and saving the file, go to Host Map page in your Datadog account.
To see the new tags that we just added.

<img src="./pics/13HostMapPage.png">
<img src="./pics/14HostMapPageNextPage.png">
<img src="./pics/15HostMapTags.png">

If you were not able to see the tags we added to datadog.conf,  double check if the syntax is correct.
Please see the rules for tag naming [here](https://help.datadoghq.com/hc/en-us/articles/204312749-Getting-started-with-tags).
Lastly, try restarting the Datadog agent by running the code below in the terminal:

```
sudo /etc/init.d/datadog-agent restart
```
*Useful links*
* [Where is the configuration file for the Agent?](https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-)  
* [Getting Started with Tags](https://help.datadoghq.com/hc/en-us/articles/204312749-Getting-started-with-tags)
### 4. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.  
>Run the code below in the terminal to install MySQL Server.
It will prompt us to continue or not with the installation.
We of course choose yes.
```
sudo apt-get update
sudo apt-get install mysql-server-5.5
```
<img src="./pics/16MySQLInstall.png">

The installation process will ask for a password for the MySQL root account.
Key in a new password for MySQL.
  <img src="./pics/16MySQLPassword.png">

After the installation process, we should see our Terminal displaying **mysqld** started as a process in our Ubuntu host.
  <img src="./pics/16MySQLRunning.png">

To make sure the installation was successful, run this command line snippet to test.
```
sudo netstat -tap | grep mysql
```
You should see something like the pic below:
<img src="./pics/17MySQLRunningTest.png">

To install the Datadog MySQL Agent, we first need to grant the Datadog Agent replication rights from our newly installed MySQL Server.
From the Terminal, login to MySql using the code below. It should prompt you for your MySQL password
```
mysql -u root -p
```
Let us run this code snippet, while replacing <UNIQUEPASSWORD> with your own password:
```SQL
CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<UNIQUEPASSWORD>';
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
```
Exit MySQL's command prompt by running the command quit:
```
quit
```
To verify if the creation of the new user was a success, let us run this command in the Terminal:
```
mysql -u datadog --password=<UNIQUEPASSWORD> -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"
mysql -u datadog --password=<UNIQUEPASSWORD> -e "show slave status" && \
echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
```
That was a lot of commands in succession. Your terminal should look something similar to this:  
<img src="./pics/18MySQLDataDogAccessConfig_1.png">

Now, we need to setup our Datadog Agent to connect to MySQL.
We need to open and edit the **mysql.yaml** file. In Ubuntu, we can find this file in **/etc/dd-agent/conf.d**. The **conf.d** folder has example templates for most of the integration that Datadog provides.
We could just copy the **mysql.yaml.example** file and edit that file. Lets run this in the terminal. The code below used gedit as a text editor. You can use your text editor of choice.
```
sudo cp /etc/dd-agent/conf.d/mysql.yaml.example /etc/dd-agent/conf.d/mysql.yaml
sudo gedit /etc/dd-agent/conf.d/mysql.yaml
```
Your **mysql.yaml** file would originally look like this:
<img src="./pics/19MysqlYaml.png">

The Important part of the configuration is the snippet below:
```
init_config:

instances:
  - server: localhost
    user: datadog
    pass: <UNIQUEPASSWORD>

    tags:
        - optional_tag1
        - optional_tag2
    options:
        replication: 0
        galera_cluster: 1
        disable_innodb_metrics: 1
```
_We disabled  innodb metrics , because it does not work on MySQL 5.5_

The finished **mysql.yaml** file should look like something like this:
<img src="./pics/20MysqlYamlEdited_1.png">

YAML files require the use of spaces instead of tabs. So please take care to use spaces, else the Agent will not be able to parse the information correctly.
After saving the **mysql.yaml** file, lets restart the Datadog Agent for the changes to get picked up.
Let's Run the code snippet below:
```
sudo /etc/init.d/datadog-agent restart
```
After restarting the Agent, lets verify that our configuration passed the integration check.
Lets run the Datadog Agent command called info.
```
sudo /etc/init.d/datadog-agent info
```
After running the info command we should see something like this:
<img src="./pics/21MysqlYamlCheck_1.png">

After verifying that our MySQL integration is correct, open your browser and go to the [Datadog MySQL Integration](https://app.datadoghq.com/account/settings#integrations/mysql) page and click on the "Install Integration" button.
<img src="./pics/22MyqlIntegration_1.png">

We should see that the "Install Integation" button will change from Blue to White, once the installation is done.
<img src="./pics/22MyqlIntegrationInstalled_1.png">

After successfully installing the MySQL Integration from the Datadog website, go to your Datadog Dashboard and we should see the "MySQL - Overview" in the Integration Dashboards section.
<img src="./pics/23DashboardView_1.png">

**Useful Links**
  * Step by step [instructions](http://dbadiaries.com/how-to-install-mysql-5-5-on-ubuntu-server-12-04-lts) on how to install MySQL 5 on Ubuntu 12.04.   
  * [MySQL Installer Downloads](https://dev.mysql.com/downloads/mysql/)  
  * [MySQL Datadog Integration](http://docs.datadoghq.com/integrations/mysql/)

### 5. Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

>We need to create 2 files to get this going. A check file, which is a python script and a YAML configuration file. The file name of both files must match.

Lets start with the python check file. Create a new python script called randomcheck.py
```
sudo gedit /etc/dd-agent/check.d/randomcheck.py
```
Here is the content of the python script:
```python
import random
from checks import AgentCheck
class randomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```
<img src="./pics/24RandomCheckPy.png">

Up next is the randomcheck.yaml file:
```
sudo gedit /etc/dd-agent/conf.d/randomcheck.yaml
```
The content of the yaml file:
```
init_config:

instances:
    [{}]
```
<img src="./pics/25RandomCheckYaml.png">

After creating both files, lets restart the Datadog Agent for the changes to take effect.
```
sudo /etc/init.d/datadog-agent restart
```
We should be able to see our newly created Check in the Dashboard.
<img src="./pics/26DashboardTest_1.png">

**Useful links**
  * [Agent Checks](http://docs.datadoghq.com/guides/agent_checks/)

## Level 2 - Visualizing your Data
### 1. Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.
> To clone our MySQL integration dashboard, lets navigate to it first.
<img src="./pics/27MySQLIntegrationDash_1.png">

Click the gear icon on the top most right of the screen.
<img src="./pics/28MySQLIntegrationDashGear_1.png">

You should be able to see a "Clone Dashboard" button to click on.
<img src="./pics/29MySQLIntegrationDashClone_1.png">

A prompt will come up, asking if we want to clone our dashboard. Click the blue button that reads "Clone".
<img src="./pics/30MySQLIntegrationDashCloned.png">

We should be immediately be presented with the newly cloned MySQL dashboard.
<img src="./pics/31MySQLIntegrationDashClonedGraphs.png">

Lets add a new graph looking at the database metric **mysql.performance.user_time**.
Click and hold the Timeseries icon on the widget bar on top of the page and drag and drop it on to the empty slot on the lower right.
<img src="./pics/32MySQLIntegrationDashClonedNewGraph.png">

Upon dropping the widget on the empty slot, a prompt asking for the details of the new Timeseries widget shall appear.
<img src="./pics/33MySQLIntegrationDashClonedPrompt.png">

Click the field which says **system.load.1** and type in **mysql.performance.user_time**. Press Enter and click the blue save button below.
<img src="./pics/34MySQLIntegrationDashClonedPromptDetail_1.png">

We should now be able to see our newly added MySQL metric in Out Cloned Dashboard.
<img src="./pics/35MySQLIntegrationDashClonedPromptDone_1.png">

Lets add another metric to our cloned dashboard. Let's add **test.support.random**. We shall follow the same steps we did for **mysql.performance.user_time**.
<img src="./pics/36MySQLIntegrationDashClonedPromptTest.png">
<img src="./pics/37MySQLIntegrationDashClonedTest_1.png">

### 2. Bonus question: What is the difference between a timeboard and a screenboard?
> The timeboard, as the name implies, is time bound. All graphs within a timeboard are scoped or synced to the same time.
This could be really useful when investigating an event in time, whereby multiple metrics could reveal patterns or trends that should lead to a certain outcome.  
The screenboard, in practice, could be very useful for getting a bird's eye view of a system.
It is more flexible in terms of presentation than the timeboard. Also, each widget or graph could have a different time frame.

**Useful links**
  * [What is the difference between a ScreenBoard and a TimeBoard?](https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-)

### 3. Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Let's navigate to our `test.support.random` graph:
<img src="./pics/38DashBoardTest_1.png">

To take a snapshot of the graph, we have to hover our mouse over any area of the graph. Then the snapshot icon will appear for us to click.
<img src="./pics/39DashBoardTestSnap_1.png">

We will now be presented with a snapshot of our graph. Out mouse when hovering the snapshot will turn into a pen for us to annotate the image. Let's annotate the peaks which are more than 0.90. Likewise, let us enter a message adding our email address using the @notification syntax. Don't forget to press enter to actually send the email.
<img src="./pics/40DashBoardTestAnnotate_1.png">
<img src="./pics/41DashBoardTestEnd.png">

**Useful links**
  * [Guide to Monitors ](http://docs.datadoghq.com/guides/monitors/)
  * [Graph Annotations](https://www.datadoghq.com/blog/real-time-graph-annotations/)

## Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  
### 1. Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes 

Lets navigate to the "New Monitor" page.
<img src="./pics/42NewMonitorNav_1.png">

We are going for a metric monitor type.
<img src="./pics/43NewMonitorMetric_1.png">

On the next page, we setup the fine details of the monitor.
<img src="./pics/44NewMonitorConfig_1.png">


### 2. Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  

<img src="./pics/45NewMonitorConfigMulti_1.png">

### 3. Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.  

>To get a shareable link for our test.support.random graph we need to navigate back to our Cloned MySQL Dashboard. We have to look for the `test.support.random` graph and click the pencil icon on its upper right. 
<img src="./pics/46NewMonitorConfigName_2.png">

It should prompt us a window with options for us to embed our graph in our monitor notifications. Don't forget to click the `Generate embed code`, and copy the generated code. 
<img src="./pics/46NewMonitorConfigName_3.png">

Paste the link in the Message section of the monitor configuration and save the monitor.
<img src="./pics/46NewMonitorConfigName_1.png">

**Useful links**
  * [How to share graphs](https://help.datadoghq.com/hc/en-us/articles/203765155-Is-there-a-way-to-share-or-revoke-previously-shared-graphs-)

### 4. This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

<img src="./pics/47EmailNotification.png">

### 5. Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Continuing from the same monitor window as before, click the `Manage Downtime` found on top of the Monitors page.
<img src="./pics/48DowntimeNav.png">

We will then be directed to the Manage Downtime page. Click the yelllow button named `Schedule Downtime`.
<img src="./pics/49DowntimeNav_1.png">

Set the downtime by selecting which monitor and scope to suppress, when and frequency its going to be suppressed, as well as the message for when the Downtime alert triggers. 
<img src="./pics/50DowntimeConfig_1.png">

After clicking save, we should see that the Downtime schedule has been created successfully.
<img src="./pics/51DowntimeEnd.png">

**Useful links**
  * [Schedule a downtime](https://help.datadoghq.com/hc/en-us/articles/205584645-How-can-I-schedule-downtimes-for-a-monitor-)
