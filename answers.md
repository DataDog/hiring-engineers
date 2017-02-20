<p>This exercise is also availabe for review via my screen recorder</p>
 <a href="https://drive.google.com/open?id=0B49Pl4e8A5AeWHZZcDB1R0pxRTA">Please click on this link to view the video in it's entirety</a>
 <h1> Level 0 (optional) - Setup an Ubuntu VM </h1>
<ol>
<li> Downloaded and installed Vagrant:  https://www.vagrantup.com/downloads.html<br>
<li>Downloaded and installed VirtualBox: https://www.virtualbox.org/<br>
<li> Initializing VM:  C:\Windows\System32>vagrant.exe init hashicorp/precise64<br>
<li>Started VM:  C:\Windows\System32>vagrant.exe up <br>
<li>logging in to new vm using ssh and putty:
<ol>
<li>Host: 127.0.0.1<br>
<li>Port: 2222<br>
<li>Username: vagrant<br>
<li>password: encrypted<br>
<li>Private key: C:/HashiCorp/Vagrant/bin/.vagrant/machines/default/virtualbox/private_key<br></ol></Ol>

<h1>Level 1 - Collecting Data from host using DataDog Agent</h1>


<ol>
<li><b>Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.</b>
<ol>
<li>Signed up for Datadog SaaS service:  https://app.datadoghq.com/trace/home?intro=true
<li>Installed Datadog agent on the new VM using following commands:</li>
<ol>
<li> sudo apt-get update

  <li>  sudo apt-get install apt-transport-https
  <li>  sudo sh -c "echo 'deb https://apt.datadoghq.com/ stable main' > /etc/apt/sources.list.d/datadog.list"
  <li>  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C7A7DA52
  <li>  sudo apt-get update
  <li>  sudo apt-get install datadog-agent
  <li>  sudo sh -c "sed 's/api_key:.*/api_key: b09d2829f93f972fd0b9616854c8652a/' /etc/dd-agent/datadog.conf.example > /etc/dd-agent/datadog.conf"
  <li>  sudo /etc/init.d/datadog-agent start
  <li> check the agent status to insure agent started successfully:   sudo /etc/init.d/datadog-agent info



</ol>

</ol>

<li> <b>Bonus question: In your own words, what is the Agent?</b><br>
 Datadog agent is a daemon like process that runs on the host where metrics are to be collected.
The agent is designed to collect default ‘out of the box’ metrics, performance data points for the specified Integrations and custom Checks,
 and aggregate those data points back to the Datadog SaaS server. These useful metrics are then presented back to the
Datadog user where they can monitor the health of their cloud scale applications and/or datacenter.

<li><b> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.</b><br>
 I Modified the agent config file located at  /etc/dd-agent/datadog.conf as below and included four tags identifying the hosts based on their geographic locations:<br>
<code># Set the host's tags (default: no tags)	</code>
<br><code>tags: region:eastern, region:western, region:southern, region:northern</code>
<li> restarted the agent:  sudo /etc/init.d/datadog-agent restart<br>
<h3>Tags</h3>

![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/tags.GIF "Tags")

<br>
<li> <b>Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.</b><br>
I Installed MongoDB, Tomcat, and Java on the Host machine and configured Integration with DataDog:<br>

<ol>
<li><code>sudo apt-get install -y mongodb</code><br>
<li><code>sudo apt-get install openjdk-7-jdk</code><br>
<li><code>curl -O http://apache.mirrors.ionfish.org/tomcat/tomcat-8/v8.5.11/bin/apache-tomcat-8.5.11.tar.gz</code><br>
<li><code>sudo tar xzvf apache-tomcat-8*tar.gz -C /opt/tomcat --strip-components=1</code>
</ol>

The corresponding yaml files for Tomcat and MongoDB is also updated and the integration has been confirmed as working via:<br>
<code>sudo /etc/init.d/datadog-agent info</code>

Checks<br>
  ======<br>

    random
    ------
      - instance #0  [OK]
      - Collected 1 metric, 0 events & 0 service checks

    mongo
    -----
      - instance #0 [OK]
      - Collected 75 metrics, 0 events & 1 service check
      - Dependencies:
          - pymongo: 3.2

    ntp
    ---
      - Collected 0 metrics, 0 events & 0 service checks

    disk
    ----
      - instance #0 [OK]
      - Collected 40 metrics, 0 events & 0 service checks

    network
    -------
      - instance #0 [OK]
      - Collected 15 metrics, 0 events & 0 service checks

    tomcat
    ------
      - instance #tomcat-localhost-8787 [OK] collected 137 metrics
      - Collected 137 metrics, 0 events & 0 service checks


<h4><a href="https://app.datadoghq.com/account/settings" >Installed and Configured Integrations</a></h4>

![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/MongoDB3.GIF "MongoDB")

<h4>MongoDB Metrics</h4>
![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/MongoDB2.GIF "MongoDB2")


<li> <b>Write a custom Agent check that samples a random value. Call this new metric: test.support.random</b>

Python Code for the custom Check:<br>
<code>cd /opt/datadog-agent/agent/checks.d/</code><br>
<code>cat random.py</code><br>
<code>from checks import AgentCheck</code><br>
<code>from random import randint</code><br>
<code>import random</code><br>
<code>class HelloCheck(AgentCheck):</code><br>
    <code>def check(self, instance):</code><br>
        <code>self.gauge('test.support.random', random.random())</code><br>

</ol>

Screen shot of random custom Check metric:<br>


![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/random.GIF "random")

<h1>Level 2 - Visualizing the collected Data</h1>

<b>Since your database integration is reporting now, clone your database integration dashboard and add additional 
database metrics to it as well as your test.support.random metric from the custom Agent check.</b><br><br>

<ol><li>New Dashboard link: 
<center>https://app.datadoghq.com/screen/157835/main-dashboard</center><br>
New Dashboard Screen shot: <br></ol>
 
![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/Dash2.gif "Dash2")


2. <b>What is the difference between a timeboard and a screenboard?</b>
<ol>
<li>ScreenBoards : Can have different Widgets each pertaining to a different time frame. Comparing metrics from today with 
the previous week for example. ScreenBoards can be shared live and as a read-only, whereas TimeBoards cannot.
<li>TimeBoards: all metrics and graphs are from the same time interval Graphs will always appear in a grid-like fashion. 
This makes them generally better for troubleshooting and correlation. Graphs from a TimeBoard can be shared individually

<li>
<b>Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification</b>



![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/snapshot.GIF "Snapshot")

<li> Email Received:


![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/snapshotemail.GIF "Snapshot")

</ol></ol>



<h1>Level 3 - Alerting on Data</h1>
<ol>
<li> <b>Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.
Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes</b>

Note that this is a multi alert. Therefore, if a downtime scope is set for host:X and a multi alert is triggered on both host:X and host:Y, Datadog will generate a monitor notification for host:Y, but not host:X.

Alert URL:  https://app.datadoghq.com/monitors#1635154?group=all&live=1h

![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/monitor2.gif "monitor.GIF")

Alert Received in Email:

![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/emailmonitor.GIF "emailmonitor.GIF")

<li><b>Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.</b>

Downtime scheduled:

https://app.datadoghq.com/monitors#downtime?id=213777869

![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/2downtime.GIF "downtime.GIF")

Downtime Email received:


![Alt text](https://github.com/opguyallahiscool91/hiring-engineers/blob/solutions-engineer/downtimeemail.GIF "downtimeemail.GIF")





