**Datadog Challenge**
-- Jordan Fritz -- Support Engineer

•	Opened Github page and quickly read/skimmed through all reference pages before beginning. This helped me to establish a small level of knowledge with regards to the Datadog software, how it works, and its functions.

**Level 0 – Setup and Ubuntu VM**

•	Used the link provided on the Github page to download Vagrant and Virtualbox. Followed the directions found on https://www.vagrantup.com/intro/getting-started/. 

•	Copy and pasted the commands found in the image below to my command line in Terminal.

![alt text](http://i.imgur.com/g28bFal.png)

•	Received the following command line notifications as Virtualbox machine was booted up. (Note: became curious about “vagrant provision” so I ran that command out of curiosity and then checked the status to verify all software was up and running properly).

![alt text](http://i.imgur.com/BC3iCDM.png)

**Level 1 – Collecting your Data**

•	Downloaded the Datadog Agent via https://app.datadoghq.com/account/settings#agent/mac (macOS Sierra Version 10.12.3). Copied the code provided in the Agent Installation Instructions (shown below) and pasted this code into my command line in Terminal.

![alt text](http://i.imgur.com/0umlAqO.png)

Note: Attempted this agent installation initially when my Virtualbox machine and Vagrant were not running. In the command line table (shown below for an example) the “Time Left” column displayed more than 10 hours left to download. I halted the download and began troubleshooting. Eventually discovered that my Virtualbox machine and Vagrant were not running, simply entered “vagrant up” in the command line and re-pasted the code provided for Datadog Agent installation.

![alt text](http://i.imgur.com/b2wDaYC.png)

I initially assumed that the Datadog Agent should be installed on Ubuntu rather than Mac. This incorrect assumption was formed due to the Virtualbox machine having an Ubuntu (64-bit) operating system (shown below). However, this was not correct, and the following error occurred: “mknod: node type must be 'b' or ‘w’.”


![alt text](http://i.imgur.com/FtU2JQW.png)

•	What is the Agent?: (Refer to http://docs.datadoghq.com/guides/basic_agent_usage/) The agent is a piece of software that collects events and metrics from the current machine and passes this data to Datadog. The Agent has three main parts: the collector, dogstatd, and the forwarder.

**Add Tags in the Agent configuration file:**

• To add tags in the Agent configuration file, I read through the references provided and discovered the “Guide to Tagging” documentation.

![alt text](http://i.imgur.com/fF6gIGC.png)

•	In the “Guide to Tagging” document, there is a section titled “Assigning tags using the configuration file”.

![alt text](http://i.imgur.com/Q33CSbh.png)
Note: When I selected the link “to this article”, it brought me back to the Agent installation page rather than to an article about configuration files.

Additional Note: As the project progressed, I realized the following steps are not the correct way to add tags in the agent configuration file. My thought process is laid out below, and I eventually determined the correct process to add tags while installing the database and editing the database files.

•	The first sentence of this section prompted me to open the conf.d directory in Terminal in order to investigate the issue further.

![alt text](http://i.imgur.com/2HiNcjb.png)

•	In an effort to discover more about the configuration files, I attempted the command “open couch.yaml.example” (arbitrarily chose couch.yaml.example). This command caused an error stating there is no application that knows how to open the file. I tried again with “open auto_conf” since there was not a filename extension connected to this file. This command opened a folder on my computer (below).

![alt text](http://i.imgur.com/rZZFulr.png)

•	Arbitrarily chose couchbase.yaml to explore the files further.

![alt text](http://i.imgur.com/SpPgbz9.png)

•	The format the file was written in reminded me that one of the references referred to a very similar format. I searched the documentation until I found the reference I remembered (Writing an Agent Check: Configuration).

• Assumed I should not edit already created configurations so tried to create my own configuration (myConfig.yaml) using the structure for configuration files found in the documentation. 

![alt text](http://i.imgur.com/0eY4VI4.png)

•	Added this file to conf.d.

![alt text](http://i.imgur.com/Lrz0jUF.png)

•	Initially assumed incorrectly this file would be automatically read in to the Datadog web app, and I would be able to call the filename, and then call the particular tags I was attempting to add.

•	Tried to create a tag in Datadog using the Host Map and Edit Tags field. The following was my output when I tried to call my new_location tags from my newly created .yaml file. I did not think this was correct, as it seemed that my configuration file was not being used at all to create or edit the tags.

![alt text](http://i.imgur.com/Mip9YO7.png)

In my trial and error to attempt to create tags, I created various other invalid .yaml files (upon review, realized they are 1/2 of the agent check, missing the .py file to go along with them.)

![alt text](http://i.imgur.com/0EI5eqh.png)

Ran in to an error where the API Key was labelled as invalid. Created a new API Key from the APIs tab on the Datadog website and then reinstalled Datadog using this new API key.

![alt text](http://i.imgur.com/kYHwnKR.png)

![alt text](http://i.imgur.com/EtMFTPY.png)

•	I continued trial and error and modifying files in the conf.d drive. Eventually got the following to appear in my Datadog window, however initially could not determine how to remove the check errors.

![alt text](http://i.imgur.com/8grcluU.png)
Note: Upon review, this seems to be that I was adding checks to my configuration, rather than adding tags. 

•	Returned to the ‘Assigning tags using configuration files’ and read about datadog.conf. However, when I tried to access this file I received the following output.

![alt text](http://i.imgur.com/ei4h16A.png)

•	Determined that I could continue the rest of the project without this section completed so continued to installing the database.

NOTE: Determined how to add tags via configuration files while installing the database. See below.

**Install a Database**

•	Decided to continue the project without the tags, so began downloading MongoDB. Simply googled “MongoDB install mac” and used https://treehouse.github.io/installation-guides/mac/mongo-mac.html. As I had already had Homebrew installed on my machine, I used the following process to install MongoDB (below).

![alt text](http://i.imgur.com/coALXTf.png)

•	After a few minutes of waiting, the database was downloaded on my machine.

•	Returned to the Datadog Web App, used the ‘Integrations’ drop down menu and selected ‘Integrations’ from the menu.

![alt text](http://i.imgur.com/23eF9E7.png)

•	Searched for the proper database.

•	(In this example case, GitHub is shown. In reality, I used MongoDB.) Once the proper database was found in the list, I selected it and opened the configurations tab. On the bottom, I used the ‘Install Integration’ button to install the desired integration.

![alt text](http://i.imgur.com/rY169D8.png)

•	(Now showing MongoDB as database) I selected my newly installed MongoDB integration (shown below).

![alt text](http://i.imgur.com/BZDpQjg.png)

•	Opened the configurations tab and followed the steps to configure my database correctly for Datadog use. Used MongoDB 3.x tab as my version of MongoDB was above 3.0. 

![alt text](http://i.imgur.com/EdyPGOS.png)

Initially I added the user as shown above (datadog), however it was not compiling correctly and I kept getting check errors when I ran ‘datadog-agent info’ in the command line. I re-generated a new password and created a new user (‘Jordan’). This solved one of the two check errors.

![alt text](http://i.imgur.com/VAHodWl.png)

•	Renamed the conf.d/mongo.yaml.example file to conf.d/mongo.yaml so that my machine could properly open the file. Deleted all text in the file and copy and pasted the text shown in step 2 above (shown below). Renamed ‘datadog’ to ‘Jordan’ as I had edited my username from that in order to partially fix a bug I was receiving.

![alt text](http://i.imgur.com/I9YZAWW.png)

*NOTE: This is where I determined how to add tags using the configuration files. As shown above, I renamed the tags in instance #1 (the second instance shown) to custom tags. I then opened the Datadog web app and saw the following tags (below) after selecting mongodb from the host map and going to the status checks tab.*

![alt text](http://i.imgur.com/fpAu5Dd.png)

•	Ran ‘datadog-agent info’ to verify mongo was up and running. However, instance #0 was not running properly due to the local host either being incorrect or due to me not having permission rights to access the local host of 27016. I determined that one instance running would be sufficient for the time being while I continued with the project.

![alt text](http://i.imgur.com/lKSc3af.png)

**Write a Custom Agent Check**

•	Read the entire reference “Writing an Agent Check”

•	Copy and pasted the code found under the section titled “Your First Check” (shown below) to initially create the test.support.random .yaml file and .py file.

![alt text](http://i.imgur.com/zSRyi6e.png)

•	Edited the code in the .py file. Added an ‘import random’ line as the first line of code. Changed the ‘class HelloCheck’ to ‘class RandomCheck’ and edited ‘hello.world’ to ‘test.support.random’. 

![alt text](http://i.imgur.com/5bfW93A.png)

•	Did not edit the .yaml file.

![alt text](http://i.imgur.com/Z715MPc.png)

•	Saved my files and restarted the Datadog Agent. Opened the host map and selected the new ‘test’ metric found within the host ‘Jordans-Macbook-Air.local’.

•	After verifying that this metric did indeed record the value of 1 by graphically examining the test.support.random plot on Datadog, I assumed the argument set to ‘1’ was the value being collected for the metric. I replaced this with ‘random.random()’ in an attempt to set the value to a random number.

![alt text](http://i.imgur.com/Ai1wFv1.png)

•	Saved my files and restarted the Agent. Opened my host map, selected the ‘test’ metric, and observed the plot again. Verified a random number was indeed being plotted (below).

![alt text](http://i.imgur.com/EiQmeDP.png)

**Level 2 – Visualizing your Data**

•	Selected ‘Dashboards’ and then ‘Dashboard List’ in the drop down menu. Found the ‘Integration Dashboards’ list and selected the proper integration dashboard (MongoDB in this case) shown below.

![alt text](http://i.imgur.com/WzvyQY6.png)

•	Found the settings button in the upper right hand corner of the browser of the integration dashboard, and selected ‘Clone Dashboard’ (shown below). Named the dashboard ‘Mongo’.

![alt text](http://i.imgur.com/XqjYccm.png)

•	In my newly created integration dashboard, I selected ‘Edit Board’ and added the test.support.random metric as well as the System Load metric to the dashboard.

![alt text](http://i.imgur.com/XjtOKGT.png)

![alt text](http://i.imgur.com/X9gpDPV.png)

•	What is the difference between a timeboard and a screenboard?: (Reference https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-) 

Timeboard: All graphs are scoped to the same time and appear in a grid-like fashion. Better for troubleshooting and correlation.

Screenboard: Flexible, more customizable, and great for getting a high level look into the system. The widgets may have different time frames.

The above dashboard is a screenboard.

![alt text](http://i.imgur.com/bV45dBN.png)

•	Assumed the test.support.random test dashboard would be the best place to get a snapshot of the metric. Also assumed the camera icon represented the snapshot function. Selected the camera function, drew a box around the desired section, typed ‘@jfritz227@gmail.com’ and then hit enter. 

![alt text](http://i.imgur.com/JWRtNR1.png)
Could not get this to send to my email despite the @notification shown above.

**Level 3 – Alerting your Data**

•	Selected the monitors drop down menu and selected ‘New Monitor’. Then selected ‘Metric’ as the object I wanted to monitor as the test.support.random is a metric. The following screen appeared. Selected the desired metric in the field shown below.

![alt text](http://i.imgur.com/qIZ4pqC.png)

•	Continued to fill out the desired fields as desired from the Hiring Challenge requirements.

![alt text](http://i.imgur.com/cN8eGPx.png)

•	Multi Alert Bonus:
![alt text](http://i.imgur.com/auKUBDt.png)

•	Set up an email notification with a descriptive monitor name and message. This was done by typing desired description and title for the monitor in the ‘Say what’s happening’ section shown below. Also created email notifications by selecting my own name/email in the ‘Notify your team’ section (shown below).

![alt text](http://i.imgur.com/GVeth6w.png)

![alt text](http://i.imgur.com/0b0ltfE.png)

More Alerts:
![alt text](http://i.imgur.com/ukrbH0l.png)

•	Downtime Bonus:
Opened the ‘Monitors’ drop down menu and selected ‘Manage Downtime’. On the page that appeared, I selected ‘Schedule Downtime’ (shown below).

![alt text](http://i.imgur.com/xisa2jK.png)

Filled out the fields as required by the Hiring Challenge. I selected a scope as shown under the assumption this would then include all instances of the monitor. Scheduled the downtime from 7:00 PM of the following day (it was past 7:00 PM already in the current day) to 9:00 AM of the day following that. Repeated the downtime ‘Daily’ with ‘No end date’. Entered a quick descriptive message and entered my email address to be notified.

![alt text](http://i.imgur.com/HfpZQK5.png)

Received email notification about downtime:

Start

![alt text](http://i.imgur.com/Ao4NRjl.png)

Stop

![alt text](http://i.imgur.com/7rpNB1l.png)

Conclusion: I enjoyed becoming familiar with the Datadog software and also furthering my knowledge of command line tools and databases. This report attempts to explain the what (task), the how (process of completing the task), and the why (thought process/problem solving) of the project. I look forward to hearing back from Datadog about the support engineering role(s) available in Sydney.

Jordan Fritz

Dashboard:

https://app.datadoghq.com/screen/183285/mongo

![alt text](http://i.imgur.com/X9gpDPV.png)


