<img align="center" src="https://image.ibb.co/iudGGa/datadog_logo.png">
<h1 align="center">DATADOG TEST</h1>
<p align="center">by Morsalin Billah</p>
<p><br><br><br><br><br><br><br><br></p>

  
# Level 0 (optional) - Setup an Ubuntu VM

I followed the instructions in the link ([Here are instructions for
setting up a Vagrant Ubuntu 12.04
VM](https://www.vagrantup.com/docs/getting-started/)) and setup an
Ubuntu VM.

1. Download Virtual Box from the official link below:
<https://www.virtualbox.org/wiki/Downloads>

2. Download the correct Virtual Box host for your Operating System

<img align="center" src="https://image.ibb.co/ewYK2F/VB_Download.png">

3. Install Virtual Box using following your Operating System standard
procedure.

4. Download and install Vagrant from the link below:
<https://www.vagrantup.com/downloads.html>

5. I find it difficult to find the username and password to Ubuntu system installed in Virtual Box. I searched online and found the
username and password to be ‘vagrant’.

<img align="center" src="https://image.ibb.co/fWNhpv/Task0_vagrant_Login.png">

6. I have followed the step-by-step instruction provided ‘Getting Started Page’. It is very helpful and described each steps elaborately.

7. Vagrant Networking: I have entered the URL <http://127.0.0.1:4567> and I can see a web page
that is being served from the virtual machine that was automatically setup by Vagrant.

<img align="center" src="https://image.ibb.co/fyUWGa/Task0_Networking.png">

8. While executing vagrant share I have encountered the following error:

<img align="center" src="https://image.ibb.co/eryYwa/Task0_share_Error.png">

9. I install ‘ngrok’ from <https://ngrok.com/download> and execute the
command in terminal.

<img align="center" src="https://image.ibb.co/dQR8Uv/Task0_ngrok.png">

10. I copy over ‘ngrok’ to my test project folder
‘vagrant\_getting\_started’ and run `./ngrok help` command.

11. I could not run vagrant share as it was giving me the following error:

<img align="center" src="https://image.ibb.co/bZP6Ga/Task0_share_Error2.png">

12. I read Internet articles from different source and found that I just realized I didn't need to use vagrant share I can run ngrok and share
any port with no problem. So I use the command `./ngrok http 4567`

<img align="center" src="https://image.ibb.co/i44j2F/Task0_ngrok_Http.png">

13. I used the URL <https://bab2212d.ngrok.io/> to view the page.

<img align="center" src="https://image.ibb.co/k0VrhF/Task0_http_Page.png">

  
# Level 1 - Collecting your Data

## Installing Agent:

1. At first I went to Datadog home page and signed up myself with company name as ‘Datadog Recruiting Candidate’.

2. Then I downloaded the agent by following the instruction on the screen.

<img align="center" src="https://image.ibb.co/hdZ6Ga/Task1_agent_Download.png">

3. Then I downloaded agent, copied the following code snippet and pasted it to MacOSX terminal.
`DD\_API\_KEY=0668e689f28ba3418c76ee8f62e7f5f9 bash -c "$(curl -L
https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)"`
While installing the agent in terminal I encountered the following
error:

<img align="center" src="https://image.ibb.co/e4hRGa/Task1_download_Agent_Error.png">

4. As a workaround, I manually downloaded the ‘datadogagent.dmg’ and
installed it.

5. I have executed ‘vi /opt/datadog-agent/etc/datadog.conf’ command to
read the ‘datadog.conf’ file and my API Key was already installed.

<img align="center" src="https://image.ibb.co/kjqrhF/Task1_APIKey.png">

6. After that I clicked finish button and received a welcome email from
Datadog that has my username and login URL.

7. Then I started the datadog agent and it was working fine without
error.

<img align="center" src="https://image.ibb.co/dsZv9v/Task1_agent_Start.png">

## What is an Agent?

An agent is a software installed in user’s computer that collects and
delivers the metrics and events from the computer to Datadog server.
User can see more information of the agent installed in computer by
executing the command

`$ datadog-agent info`.

<img align="center" src="https://image.ibb.co/bR9j2F/Task1_agent_Info.png">

  
## Add tags in the Agent config file

1. I have searched Datadog Docs and found a help document ‘Guide to
Tagging’.

<img align="center" src="https://image.ibb.co/jK0cpv/Task1_tagging_Doc.png">

2. I have used ‘Configuration File’. I have tried to add ‘HTTP\_Check’
and successfully get the information in ‘datadog-agent info’

<img align="center" src="https://image.ibb.co/d6vrhF/Task1_http.png">

3. I have downloaded and installed ‘MongoDB’. I have followed the
instruction from the following site:
<https://www.mongodb.com/download-center#community>

4. I installed Homebrew using the following command:
`/usr/bin/ruby -e "$(curl -fsSL
https://raw.githubusercontent.com/Homebrew/install/master/install)"`

5. Then installed MongoDB by the instructions of the following page:
<https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/>

<img align="center" src="https://image.ibb.co/njW6hF/Task1_install_Mongo_DB.png">

6. I have found the following Youtube video handy to create data/db
directory for MongoDB:
<https://www.youtube.com/watch?v=Hh-bLCP6jVI>

7. Then I have created the following user (datadogMorsalin) in MongoDB
according to the manual installation process:
`db.createUser({"user":"datadogMorsalin", "pwd":
"YG0Z80l4bHizR3ayEoLplg0Y", "roles" : \[ {role: 'read', db: 'admin' },
{role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }\]})`

8. After creating the user successfully into MongoDB, I modified the
‘mongo.yaml’ file in conf.d directory:
`init\_config:`
`instances:`
`- server:`
`mongodb://datadogMorsalin:YG0Z80l4bHizR3ayEoLplg0Y@localhost:27016`
`tags:`
`- mytag1`
`- mytag2`
`- server:`
`mongodb://datadogMorsalin:YG0Z80l4bHizR3ayEoLplg0Y@localhost:27017`
`tags:`
`- mytag1`
`- mytag2`

9. Further following the instructions, I went into the Integrations tab
on Datadog-web app and installed MongoDB begin configuration for the
same. This is where I changed the User and followed the steps to
configure the MongoDB integration with Datadog-agent.

<img align="center" src="https://image.ibb.co/bNqz2F/Task1_integration.png">

<img align="center" src="https://image.ibb.co/m61vba/Task1_integration1.png">

10. I went to Infrastructure Host Map Click on mongodb. This is where I
found the tags which I have added using the Configuration File.

<img align="center" src="https://image.ibb.co/mtCOUv/Task1_tags.png">

11. Once I got it working and installed properly I ran ‘Datadog-agent
info’ in terminal to verify Mongo was up and running. However, instance
\#0 was not running properly due to the local host either being
incorrect or due to me not having permission rights to access the local
host of 27016 (found a couple of references on Datadog—GitHub stating
that one instance running would be sufficient for the time being.)

<img align="center" src="https://image.ibb.co/dCwxNF/Task1_datagog_Agent_Info_Mongo_DB.png">

  
## Write a custom Agent check that samples a random value

1. First of all I searched Datadog site to found instruction on ‘How to
a Custom Agent Check’ and I found it under the guides.
<https://docs.datadoghq.com/guides/agent_checks/>

2. In ‘Writing an Agent Check’ page I found the section ‘Your First
Check’

<img align="center" src="https://image.ibb.co/gegWhF/Task1_first_Check.png">

3. I have used `Finder` of Mac OS X to navigate to `conf.d` and `checks.d` directories.

<img align="center" src="https://image.ibb.co/bxzj2F/Task1_directory.png">

4. Then I have created `test.support.random.py` and
`test.support.random.yaml` files in `/opt/datadog-agent/agent/checks.d/`
and `/opt/datadog-agent/etc/conf.d/` respectively using text editor
application (Sublime Text).

5. I have added an `import random` line as the first line and modified the code snippet in `test.support.random.py` file. I have changed the
class `HelloCheck` to `TestCheck` and edited `hello.world` to `test.support.random`.

<img align="center" src="https://image.ibb.co/cOs1Ga/Task1_py_File.png">

6. I have copied over the code for `test.support.random.yaml` file and
left it untouched.

<img align="center" src="https://image.ibb.co/k2MTwa/Task1_yaml_File.png">

7. I ran `datadog-agent info` in terminal and can see the `test.support.random` check has been integrated successfully.

<img align="center" src="https://image.ibb.co/ebn1Ga/Task1_test_Check_Agent_Info.png">

8. Now I can see the custom agent check in my Host Map:

<img align="center" src="https://image.ibb.co/ez02pv/Task1_custom_Agent.png">

# Level 2 - Visualizing Data

## Database Dashboard:

1. To visualize data, I went to ‘Dashboards’ menu and selected ‘Dashboard List’. Found the ‘Integration Dashboards’ list and selected the proper integration dashboard (MongoDB here) shown below.

<img align="center" src="https://image.ibb.co/mEyDUv/Task2_integration_Dashboard.png">

2. Then I have selected MongoDB dashboard and opened it. On the top-right corner of the screen there is a setting icon where I found ‘Clone Dashboard’ option.

<img align="center" src="https://image.ibb.co/b4Unpv/Task2_mongo_Dashboard.png">

3. After cloning the dashboard I went to Dashboard List again and can see ‘MongoDB(cloned)’ dashboard in the list on the left hand side of the screen. After that, I opened the ‘MongoDB(cloned)’ dashboard and add custom metric `test.support.random` to the dashboard.

<img align="center" src="https://image.ibb.co/bOrdwa/Task2_custom_Metric.png">

**Link to the Dashboard:** <https://app.datadoghq.com/screen/208410/mongodb-cloned>

  
## Difference between Timeboard and Screenboard?

**Timeboard:** For a timeboard, all the graphs are scoped within the same time and appear in a grid-like fashion. A timeboard has utility for
correlation of data and troubleshooting.

**Screenboard:** Screenboard is for getting a high level look into the functioning of the system. It is much more flexible and customizable. The widgets may have different time frames.

<img align="center" src="https://image.ibb.co/dDQtUv/Task2_Timevs_Screen.png">

## Snapshot of `test.support.random` graph:

<img align="center" src="https://image.ibb.co/kFUywa/Task2_snapshot1.png">

After that, I have cloned this Custom Metrics – test dashboard and turned on the notification. I have then taken snapshot and could not manage to send that snapshot to my email address. Then I used the annotation process to send the snapshot to my other email address:

Link: <https://www.datadoghq.com/blog/real-time-graph-annotations/>

The email I received:

<img align="center" src="https://image.ibb.co/n7bdwa/Task2_snapshot2.png">

# Level 3 - Alerting on your Data

1. I went to ‘Monitors’ drop down menu and selected ‘New Monitor’. After that I selected the option ‘Metric’ and continued to define the metric
‘test.support.random’ according to the requirements of test.

2. I set the alert threshold at 0.9 and warning threshold at 0.8. I also selected Multi Alerts via hosts.

<img align="center" src="https://image.ibb.co/eiCOUv/Task3_monitor.png">

3. Then I named monitor ‘Threshold Monitor, wrote a message body and added recipients to notify.

<img align="center" src="https://image.ibb.co/jMKRhF/Task3_monitor_Notify.png">

4. Then I created email notifications by selecting my own name/email in the ‘Notify your team’ section.

<img align="center" src="https://image.ibb.co/isWiUv/Task3_monitor_Alert_Message.png">

5. After a while I received the following warning emails followed by recovered emails from monitor I have created.

**Warning Email (1):**

<img align="center" src="https://image.ibb.co/iMkhNF/Task3_email_W1.png">

**Recovered Email (1):**

<img align="center" src="https://image.ibb.co/cq9WGa/Task3_email_R1.png">

**Warning Email (2):**

<img align="center" src="https://image.ibb.co/cfSe2F/Task3_email_W2.png">

**Recovered Email (2):**

<img align="center" src="https://image.ibb.co/nOx7pv/Task3_email_R2.png">

**Recent Activity under Threshold Monitor:**

<img align="center" src="https://image.ibb.co/b00GhF/Task3_downtime_Recent_Activities.png">

6. Setting up Downtime: I went to Monitors then selected ‘Manage Downtime’. On Manage Downtime page I clicked ‘Schedule Downtime’ button located on top-right corner of the screen. After clicking on the button a pop up window opened to setup schedule downtime. I setup schedule downtime and received an error message saying ‘Schedule downtime start
cannot be in the past’

7. Then I changed the date to start from tomorrow and it allowed me to save the Schedule Downtime.

Email from Monitor:

<img align="center" src="https://image.ibb.co/fTiTxF/Task3_downtime_Alert_Email.png">
