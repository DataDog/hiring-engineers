---

[![Datadog Rocks!](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/datadoglogo.png)](https://www.datadoghq.com/ "Datadog Rocks!")
</br>

# Technical Assignment Submission
## M Herring - Solutions Engineer Candidate

[![Mal Herring](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/headshot_rounded+200x200.gif)](https://www.linkedin.com/in/malherring/ "Find me on LinkedIn")
</br>

### Date: 15th June 2018


---
</br>

# Introduction
Hello,
My name is Mal Herring and may I take the pleasure in submitting my technical assessment for your review.  

I have provided my answers as best as I can and supplied the associated screenshots, each section is contained within its own block, and of course, I used the Datadog knowledge base extensively.

As I would with any PoV I run, I've given my "Working Notes" at the bottom of this document. I use these in a Nutshell document to keep a record of significant issues, situations, interventions with people (training etc.) and the thinking behind the process if required. This information dump can often be useful in the sales process along with the working notes that Sales will use, but also valuable for win/loss reviews as a reminder of the actions and steps taken. I've approached with this task with the same mindset as a PoV.

I look forward to the feedback; I enjoyed the process. I found it challenging; however, I like to be stretched and love to learn new skills.

Please feel free to click on my profile on LinkedIn, just click my profile picture.

Yours Sincerely

Mal Herring

</br>

---


# Collecting Metrics

Please find below the response to each of the questions in the technical assignment.

I've added notes, inserted the screenshot and linked the image to the relevant page in the documentation that I used.

### Q. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I found this task pretty easy, and it also highlighted on a very simple level the power of tags, I was blown away by the host map, that was a big WOW moment when I say it's capability.
</br>

[![Host Tags](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/host_tags.png)](https://docs.datadoghq.com/getting_started/tagging/#tags-best-practices "Open: Getting started with tags")

</br>

### Q. Install a database on your machine (Used MySQL) and then install the respective Datadog integration for that database.

I opted for MySQL as I have experience of using this in a past life, installation went smoothly and configuring the check was a breeze, again, the ease and simplicity of configuring Datadog shone through again.

</br>

### Q. Create a custom Agent check that submits a metric named my_metric with a random 

Originally I set a value of 40 but then realised this gave me a flatline graph and then figured this was not going to represent a real-world metric well so after some research I discovered the randomNumber function and set this to give me a better view.
</br>

[![My Custom Check](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/custom_check.png)](https://docs.datadoghq.com/developers/agent_checks/ "Open: Writing an Agent check")

</br>

### Q. Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes, by adding min_collection_interval under instances to the YAML file, not the PY file. Originally this was not working as I misread the syntax on the documentation page [**here**](https://docs.datadoghq.com/developers/agent_checks/#configuration), I saw that it could be added in the init_config section, but this is relevant for V5, so I needed to ensure this worked for V6, which I believe it now does.
</br>

---

# Visualising Data

Full Disclosure: The tasked called for the Datadog API to be used to create a Timeboard, I used the GUI as my scripting is a little rusty.


### Q. Your custom metric scoped over your host.
I found this easy to setup and also saw the options for visualising the data compelling, one of the things I love about Datadog is its ability to highlight the same point across multiple graphs, being able to establish potential correlations between data sources in this way is incredible. 

</br>

[![My Metric Dashboard](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/my_metric_dashboard.png)](https://docs.datadoghq.com/graphing/ "Open: Graphing")

</br>

### Q. Any metric from the Integration on your Database with the anomaly function applied.
I performed this via the GUI, will work on my API skills as I get back into scripting. :smile:

[![Anomaly Function](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/anomaly_function.png)](https://docs.datadoghq.com/monitors/monitor_types/anomaly/ "Open: Anomaly monitor")

</br>

### Q. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Here you can see how I applied the rollup over an hour followed by the resulting graph.

[![Rollup Function](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/rollup_function.png)](https://docs.datadoghq.com/graphing/#aggregate-and-rollup "Open: Aggregate & Rollup")

</br>

![Custom Metric Rollup](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/custom_metric_rollup.png "Graph of Rollup")


### Q. Set the Timeboard's timeframe to the past 5 minutes

Using the key combination ALT + [ & ] I was able to adjust the timeframe as you can see in the screenshot below

![Timeboard 5m Timeframe](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/timeboard_timeframe_5m.png "Timeboard over 5m timeframe")

</br>

### Q. Take a snapshot of this graph and use the @ notation to send it to yourself.

Here is a snapshot of the email I received when I annotated my graph, very powerful and easy for users to share data with others, very impressive.

![Snapshot Received](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/snapshot_received.jpeg "Graph Annotation")

</br>

### Q. What is the Anomaly graph displaying?
The anomaly monitor can give you a view of its behaviour that differs from how it has behaved in the past. This is very useful to assist in understanding if your environment is acting as it has done traditionally or if the behaviour is different from what is expected. 

This can often serve as an early warning to something not being as it should and allows for questions to be asked or investigations to be run. As an example, this could serve as an early indicator of data leakage (more data sent by a device or more activity than usual)
</br>

---

# Monitoring Data
Below you'll find the code I used in the status notification along with a screenshot of the alert conditions.

I had originally made an error but caught this during testing and corrected it. I had selected the wrong variable for one of the recovery lines, and this highlights the importance of testing everything! :wink:

#### Code for Notification
```
Subject: {{host.name}} STATUS NOTIFICATION
Body:
Aloha!

HOST: {{host.name}}
HOST IP: {{host.ip}}

{{#is_alert}}Host has breached ALERT threshold by exceeding {{threshold}} for the past 5 minutes, it hit {{value}}. {{/is_alert}} 
{{#is_warning}}Host has breached WARN threshold by exceeding {{warn_threshold}} for the past 5 minutes, it hit {{value}}. {{/is_warning}} 
{{#is_no_data}}Host has not sent any data for the past 10 minutes, please investigate.{{/is_no_data}} 
{{#is_alert_recovery}}Host has recovered and is no longer in an ALERT condition, phew!{{/is_alert_recovery}} 
{{#is_warning_recovery}}Host has recovered and is no longer in a WARN condition, you dodged a bullet!{{/is_warning_recovery}} 
{{^is_no_data_recovery}}Host is now sending data again, hold sending the A-Team for now.{{/is_no_data_recovery}} 

Yours Sincerely,
Your friendly Datadog

```

#### Screenshot of Notification Settings
[![My Monitor](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/my_monitor.png)](https://docs.datadoghq.com/monitors/monitor_types/metric/ "Open: Metric Monitor")
</br>

#### Alert Email Received

![Alert Email](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/alert_email.JPG)
</br>

#### Recovery Email

![Recovery Email](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/recover_email.JPG)
</br>

# Q. Bonus Question
Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
</br></br>

As per my working notes, while setting downtime periods, I noted that the question called for "two" scheduled downtimes and when using the GUI I found that setting an all day Sat/Sun was simple as was doing a Mon>Fri evening but this would leave a gap on Monday 00:00 > 19:00 so I extended my evening downtime period over the weekend also to cover the Monday morning gap, this assumes my logic is correct. 



#### Weekend Downtime Schedule

![Weekend Downtime Configuration](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/weekend_downtime.png "Weekend Downtime Configuration")
</br>

#### Email Received

![Weekend Notification Received](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/weekend_notification.JPG "Weekend Notification Received")
</br>

### Weekday Downtime Schedule

![Evening Downtime Configuration](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/evening_downtime.png "Evening Downtime Configuration")
</br>

#### Email Received

![Evening Notification Received](https://s3-eu-west-1.amazonaws.com/malherring/datadog_screenshots/evening_notification.JPG "Evening Notification Received")
</br>

---

# Collecting APM Data
I'm afraid I have to admit defeat on this section. 

I had considerable issues getting things to install/run and tried Google as best as I could, but at this stage, I'd be looking to utilise internal knowledge base articles if there is one, internal communication channels or a mentor/senior member of the team.

 I'm not above asking for help and not only enjoy helping others with my knowledge, but I also enjoy when others share their knowledge with me.
</br>

---

# Final Question Response
Having better understood Datadog and it's power to bring in information from diverse systems, I feel it would be groundbreaking if we were able to query data sources to understand the mood of the nation better. 

Imagine being able to bring in data from smartphones, IoT devices and Facebook, for example, and view a city, county or country in a host map. Datadog could create a fun "Mood App" in the App Stores that allow users to rate, by colour, how they feel and this could then be used as data, with consent, to build the national view.

Green people would be those that are happy and go about their daily life with a smile on their face, but using the colour coding system; we could be alerted to those not feeling so happy and possibly may need an intervention before they harm themselves or another.

Being able to have an early warning could save health providers millions by intervening earlier rather than waiting until the situation is dire, we could see nation productivity skyrocket as people feel happier and more engaged.

If the person is using wearable tech, we could monitor their health stats and view this, but more importantly, perhaps we can "monitor and alert" to potential situations, for example, a construction site worker who is tired and whose levels suggest he may not be safe to be working on a site or consider a lone worker that has a fall or 

Sounds a bit "Minority Report" but this is the power of data, that said, data regulations may stop this from ever happening...

---
### Working Notes


#### ** Saturday 19th May ** 
[20:57] Downloading Ubuntu and also installing agent into Windows machine & MacOS - GitHub desktop installed, Repo forked - Reading Overview.

[21:26] Fighting with bandwidth, currently away and have a 2mb line, causing pain downloading agent to MacOS, Windows and ubuntu download causing issues, may need to postpone efforts.

[21:34] Windows Installed, MacOS stalled, restarting...  Bandwidth still causing issues and tethering on a low 3G proving troublesome also...

[21:46] Pushing ahead with Windows...  Agent Setup page confirmed first agent installed.

Your Agent is running properly. It will continue to run in the
background and submit metrics to Datadog.

You can check the agent status using the "datadog-agent status" command
or by opening the webui using the "datadog-agent launch-gui" command.

If you ever want to stop the Agent, please use the Datadog Agent App or
the launchctl command. It will start automatically at login.

[21:52] Both agents available in Infra list - painful to install but that was due to local bandwidth; otherwise this would have flow. Agents reboot-less which is nice.

[22:08] Playing with Infra View and enabled process_config - process view very impressive and it unwraps svchost

[23:04] Documentation consumed, been playing with the dashboard.  Feel more confident attacking answers.md, resuming tomorrow.

#### ** Sunday 20th May ** 
[13:48] Back home, ubuntu downloading in minutes now, ahh, to have bandwidth...  Also installing Vagrant to have an additional host to play with and to complete questions...

[13:58] Running vagrant up, waiting...  Configured host to have bridge networking, SSH working from OSX terminal.

[14:09] Curl installed - Datadog agent installed to host, MySQL installed - Datadog MySQL integration also being done.

[14:29] MySQL looking ok and Collector is running MySQL checks.

```
=========
Collector
=========

  Running Checks
  ==============
    mysql
    -----
      Total Runs: 1
      Metrics: 63, Total Metrics: 63
      Events: 0, Total Events: 0
      Service Checks: 1, Total Service Checks: 1
      Average Execution Time : 14ms
```

[14:30] Will continue later.

#### ** Monday 21st **
[22:29] Picking up again...  Checking the status of agents in DG, MySQL not showing so have rebooted ubuntu box as it was paused, may have confused things. (Playing with tags in mysql.yaml caused the issue, have fixed this...)

```
  Config Errors
  ==============
    mysql
    -----
      yaml: line 8: found a tab character that violate indentation
```

[23:01] DogStatsd enabled after reading up on custom metrics, limits of metrics etc.cd

[23:25] Check Created and seems ok, amending collection interval...

```
sudo -u dd-agent -- datadog-agent check mycheck

=========
Collector
=========

  Running Checks
  ==============
    mycheck
    -------
      Total Runs: 1
      Metrics: 1, Total Metrics: 1
      Events: 0, Total Events: 0
      Service Checks: 0, Total Service Checks: 0
      Average Execution Time : 0ms
```

[00:19] Kept seeing following error when I added the min_collection_interval -

```
    Error: invalid config for mycheck: yaml: unmarshal errors:
        line 4: cannot unmarshal !!map into []check.ConfigRawMap
    Error: no valid check found
```

Seems to work under the init_config section, although this doesn't work on the V6 Collector (according to the knowledge base, this is not how it's configured in the V6 Collector) so I am not happy with this - will come back to it.

#### ** Wednesday 23rd **
[17:08] resolved invalid configuration issue, checks are reporting into the dashboard and seems good. Missed "-" in the yaml file.  Bonus question answered as I've been thinking about something not technical that Datadog could make a real difference in. Reading about dashboards...

[17:15] Creating anomaly metric...  reading first.

[21:04] Metric was created, monitor setup and test emails have been received, found the error and corrected this - used the wrong variable (^ not #) 

[21:36] Setting downtime periods, email notifications received.  Scheduled evening notification over weekend otherwise, as far as my logic goes, just by setting weekends, then a M > F alert, you'd miss the period that ends 00:01 Sunday Evening/Monday morning to 08:59 Monday morning, the tasks asked for two, and so this is how I figured this would achieve the requirement.

[22:28] Having issues with "pip install trace" - Will have to leave for now and come back with a fresh pair of eyes.  Error below:

```
vagrant@precise64:/etc/datadog-agent/checks.d$ sudo pip install ddtrace
Downloading/unpacking ddtrace
  Cannot fetch index base URL http://pypi.python.org/simple/
  Could not find any downloads that satisfy the requirement ddtrace
No distributions at all found for ddtrace
Storing complete log in /home/vagrant/.pip/pip.log
```

[23:59] back again, Maybe I'm reading this wrong, and I don't need the Python trace if I am using the given Flask app - playing with this a little more.
Installing Flask to the virtual env setup still failed, found article suggesting that older versions distribute to an old URL - used command "pip install -i https://pypi.python.org/simple -U pip distribute" and this cleaned up the issue and allowed me to then "pip install Flask" without issue.

#### ** Thursday 24th **
[21:30] Checking all answers and ensuring images are all correct

[01:00] Have still been struggling to get APM running...  The error I am seeing is, which suggests something else is on that port: 

```
Flask uses port 5000 and dd-agent is on this port.  Hence error "socket.error: [Errno 98] Address already in use"  Considering options... 
```

[01:32] Cannot run ddtrace - error:

```
vagrant@precise64:~/ddproject$ sudo ddtrace-run myapp.py
Traceback (most recent call last):
  File "/usr/local/bin/ddtrace-run", line 11, in <module>
    load_entry_point('ddtrace==0.12.0', 'console_scripts', 'ddtrace-run')()
  File "/usr/local/lib/python2.7/dist-packages/ddtrace/commands/ddtrace_run.py", line 78, in main
    os.execl(executable, executable, *sys.argv[2:])
  File "/usr/lib/python2.7/os.py", line 312, in execl
    execv(file, args)
OSError: [Errno 8] Exec format error
```
Can run script: 

```
vagrant@precise64:~/ddproject$ python myapp.py
 * Serving Flask app "myapp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
2018-05-24 00:33:23,071 - werkzeug - INFO -  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
I'm able to run the script if I stopped the Datadog agent, it seems that there is a component within the agent that uses port 5000.  Clearly, I am missing something here, but I cannot seem to find the answer so at this point I'd need to reach out to another member of the team for guidance.