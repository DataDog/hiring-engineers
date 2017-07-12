# Executive Summary
Today's enterprise IT shops are dealing with a complex, hybrid IT environment.  Infrastructure and application monitoring have to span legacy and cloud environments.  For IT operations it is impossible to tie all of the various data feeds together to get a view of how business services are performing for the end users.  Application outages are obviously costly but performance degradation can be just as costly from lost revenue opportunites.  Datadog allows IT operations to gain visibility into all aspects of an application and allows IT to react in real-time to issues that may be occuring in the environment before end users are impacted.  This excercise was a great example of how easy it is to setup and monitor a simple application as well as reduce the noise of false alarms that distract IT operations from reacting to relevant issues.

# Solution Engineer Hiring Excercise
## Level 0 (optional) - Setup an Ubuntu VM
> While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues.

I setup the excercise on my home PC and took your advice to setup a Vagrant Ubuntu VM.  It was very easy to install VirtualBox and  Vagrant on my Windows desktop.  To create an Ubuntu image, I simply executed the following commands:

**$ vagrant init hashicorp/precise64**

**$ vagrant up**

## Level 1 - Collecting your Data
>Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

I followed the [documentation](https://app.datadoghq.com/account/settings#agent/ubuntu) to install the agent on Ubuntu by executing this singular command:

**DD_API_KEY=4a3ba2f5aa972d69d2a9161c976a3658 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"**

It produced an error but provided a solution by executing the **fix-missing** option in this command:

**sudo apt-get install datadog-agent --fix-missing**

The recommended fix worked and I could validate the agent was running by executing:

**sudo /etc/init.d/datadog-agent info**

![l1 agent health](https://user-images.githubusercontent.com/29982897/28100239-766c79f0-6686-11e7-8944-f15075c6324f.PNG)

I checked the Infrastructure in Datadog and saw the agent was reporting metrics:

![l1 metrics](https://user-images.githubusercontent.com/29982897/28090555-506b34fa-6652-11e7-9df1-dca6b0133812.PNG)

>Bonus question: In your own words, what is the Agent?

**The agent is a metrics collector for the host machines.  This provides the most flexibility and control for collecting metrics from the host and its applications.  The agent is also a forwarder to the Datadog service.  This allows the agent to queue information and bulk send to limit the network traffic as well as route through a proxy if needed.**

>Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Tags are important to Datadog as they allow you to correlate infrastructure and applications easily by simple configuration.  I update the datadog.conf file on my machine to present 3 descriptive tags: application, environment and location:

![agent tags](https://user-images.githubusercontent.com/29982897/28090549-50586546-6652-11e7-96df-0ceba32ec73b.PNG)

These tags are readily available from the Datadog UI and can be used to group infrastructure for reporting and monitoring.  This easily allows applications teams the ability to apply tagging through standard configuration tools like Chef or Puppet and have that automatically group the application and services together for the operations team to effectively monitor them.

![custom tags](https://user-images.githubusercontent.com/29982897/28100502-06d2b29c-6688-11e7-840e-cb4ac9c3f82f.PNG)

> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed PostgreSQL on my machine by executing:

**sudo aptitude install postgresql**

I installed the Postgres configuration on the Datadog website, and configured the machine to communicate:

1. Create a read-only datadog user with proper access to your PostgreSQL Server
2. Configure the Agent to connect to the PostgreSQL server 
A snippet of the postgres.yaml config:
![l1 db config](https://user-images.githubusercontent.com/29982897/28100867-71af01fe-668a-11e7-82a7-0a8b03566f61.PNG)

3. Restart the Agent
4. Execute the info command and verify that the integration check has passed.
![db](https://user-images.githubusercontent.com/29982897/28090550-50583f44-6652-11e7-8030-722161931756.PNG)

> Write a custom Agent check that samples a random value. Call this new metric: test.support.random

Custom agent checks provide unlimited flexibility to gather metrcis from a host.  For this, I created a gbcheck.py script to generate a random value and then a gbcheck.yaml to retrieve the data.  Here is the code:
![agent check](https://user-images.githubusercontent.com/29982897/28090553-505bddb6-6652-11e7-9dda-07ec5ae7c9fe.PNG)

## Level 2 - Visualizing your Data
> Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

I created a timeboard dashboard to view the Postgres data as well as the test.support.random metric.  For the metric I created a timeseries graph to track the random value over time as well as a query value graph to show the latest value.  For the query value I applied a green background from values <= to 0.9 and a red background for any value higher than 0.9. 
![dashboard](https://user-images.githubusercontent.com/29982897/28090552-505aabd0-6652-11e7-9011-98b03538a88e.PNG)

> Bonus question: What is the difference between a timeboard and a screenboard?

**A timeboard and a screenboard are both types of dashboards.  A timeboard is focused on a particular slice of time for all its graphs and is excellent for event correlation.  A screenboard allows the user to customize the graphs with any timeslice and is great for getting a general overview of your system health.**

> Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Dashboards allow users to instantly collaborate on events that need attention.  By simply using markdown you can send emails and notify colleagues to take a look at events.

![l2 snapshot](https://user-images.githubusercontent.com/29982897/28101194-78ceda20-668c-11e7-9067-f67aa984a10e.PNG)


## Level 3 - Alerting on your Data
> Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

Alerting is critical to effective monitoring as it's impossible to watch all of the data coming in.  Setting up thresholds and trends to understand when deviations occur above or below the expected norm provide real-time notifications to look at possible issues.  I created a monitor to alert when the random number is above 0.9.

![monitor status](https://user-images.githubusercontent.com/29982897/27966658-9e78711c-6305-11e7-9d37-87c002bf414d.PNG)

> Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

![monitor](https://user-images.githubusercontent.com/29982897/28090551-5059f082-6652-11e7-9fda-a2bc59f8d2a4.PNG)

> Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

![monitor 2](https://user-images.githubusercontent.com/29982897/28090556-506e2750-6652-11e7-85d8-2119d01e3afb.PNG)

> This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

![alert email](https://user-images.githubusercontent.com/29982897/27966728-f6804ec0-6305-11e7-9352-cf50ef2bf282.PNG)

> Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Scheduling blackouts is critical to effective monitoring.  Noise is generated from routine maintenance of applications through things like patching of servers, application releases, system refreshes, etc.  The ability to suppress the noise is critical for operations to focus on what's actually affecting the environment.

![downtime](https://user-images.githubusercontent.com/29982897/27966792-24767656-6306-11e7-8db7-0d5a7c194d0a.PNG)

![blackout](https://user-images.githubusercontent.com/29982897/28090558-5083a648-6652-11e7-884a-4e7fc82d8675.PNG)

# Conclusion
This was a fun excercise that exposed me to some new technologies and took me back to my development days.  I really enjoyed exploring the potential of the Datadog product.  The possibilities seems endless and the setup was remarkably simple.  Thank you for the opportunity, and I look forward to hearing from you.

## Links
[Dashboard]https://app.datadoghq.com/dash/317271/postgres---level-2?live=true&page=0&is_auto=false&from_ts=1499441575500&to_ts=1499445175500&tile_size=m
