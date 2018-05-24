Dear Reviewer,
Thank you for taking the time to read this.  I've provided my answers as best as I can and provided links to the relevant screenshots.

As I would with any PoV I run, I've given my "Working Notes" at the bottom of this document, I use these in the Nutshell document to list the steps taken, actions performed, interventions with people etc and the thinking behind the process as this dump can often be used in the sales process but in the win/loss reviews as a reminder of the actions and steps we took. I've taken the same approach with this task and you can see my steps and thoughts.

I look forward to the feedback, I enjoyed the process but did find it a challenge, however, I like being stretched and learning new skills.

Many Thanks

Mal Herring



- Collecting Metrics -
Q. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
R. Completed (https://www.dropbox.com/s/ytyj4eyan0fecwy/host_tags.png?dl=0)

Q. Install a database on your machine (Used MySQL) and then install the respective Datadog integration for that database.
R. Completed, See working notes below, Sunday 20th

Q. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
R. Created my_metric with a value of 40 then realised this needed to be random so corrected. (https://www.dropbox.com/s/2jhtkem17glz7bv/custom_check.png?dl=0)

Q. Bonus Question Can you change the collection interval without modifying the Python check file you created?
R. Yes, by adding min_collection_interval under instances to the YAML file, not the PY file, see above screenshot.



- Visualising Data - 
Utilise the Datadog API to create a Timeboard that contains (Used GUI I'm afraid as found API scripting a challenge)

Q. Your custom metric scoped over your host.
R. Completed (https://www.dropbox.com/s/7afg553jhznu8zp/my_metric_dashboard.png?dl=0)

Q. Any metric from the Integration on your Database with the anomaly function applied.
R. Completed via GUI - Will examine API and come back to this (https://www.dropbox.com/s/v67edp64hltyzhd/anomaly_function.png?dl=0)

Q. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
R. Completed via GUI - (https://www.dropbox.com/s/ic84bfk50oq3bc5/custom_metric_rollup.png?dl=0)

Q. Set the Timeboard's timeframe to the past 5 minutes
R. Completed (https://www.dropbox.com/s/9q8q2wmlqaer7js/timeboard_timeframe_5m.png?dl=0)

Q. Take a snapshot of this graph and use the @ notation to send it to yourself.
R. Completed (https://www.dropbox.com/s/8jin94n0dazh15v/snapshot_received.jpeg?dl=0)

Q. What is the Anomaly graph displaying?
R. The anomaly monitor is able to give you a view of its behaviour that differs from how it has behaved in the past. This is very useful to assist in understanding if your environment is behaving as it has done traditionally or if behaviour is different from what is expected, this can often serve as an early warning to something not being as it should and allows for questions to be asked or investigations to be run. As an example, this could serve as an early indicator to data leakage (more data sent by a device or more activity than usual)



- Monitoring Data -
Alert Email example: (https://www.dropbox.com/s/r5kxyykm42lth08/my_monitor.png?dl=0)

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

Found that I selected the wrong variable when the emails came through, replaced this to correct issue with email format.

Alert Email (https://www.dropbox.com/s/kz4eofm32v6ay9w/alert_email.JPG?dl=0)
Recover Email (https://www.dropbox.com/s/jcd9l310bv6b9z2/recover_email.JPG?dl=0)

Q. Bonus Question
R. Completed, see below:
Weekend downtime setup (https://www.dropbox.com/s/x0j4hbgpiuej14w/weekend_downtime.png?dl=0)
Weekend downtime email (https://www.dropbox.com/s/9zrkmvo321j6nql/weekend_notification.JPG?dl=0)
Evening downtime setup (https://www.dropbox.com/s/i9jm5nlu0yix33h/evening_downtime.png?dl=0)
Evening downtime email (https://www.dropbox.com/s/0fwzmr68yg457cw/evening_notification.JPG?dl=0)

See thoughts on downtime logic below under Wednesday 23rd [21:36]



- Collecting APM Data -
I'm afraid I have has to admit defeat on this section. I had considerable issues getting things to install/run and tried Google as best as I could but at this stage I'd be looking to utilise internal knowledge base articles if there is one, internal communication channels and/or a mentor/senior member of the team. I'm not above asking for help and not only enjoy helping others with my knowledge but I also enjoy when others share their knowledge with me. It's only by sharing our knowledge that we can all become stronger and advance together. 



- Final Question Response -
Having better understood Datadog and it's power to bring in information from diverse systems, wouldn't it be amazing if it were able to query data sources to better understand the mood of the nation. Imagine being able to bring in data from smart phones, IoT devices and Facebook, for example, and view a city, county or country in a host map. Datadog could create a fun "Mood App" in the App Stores that allow users to rate, by colour, how they feel and this could then be used as data, with consent, to build the national view.

Green people would be those that are happy and go about their daily life with a smile on their face, but using the colour coding system we could be alerted to those not feeling so happy and possibly may need an intervention before they harm themselves or another.  Being able to have an early wanting could save health providers millions by intervening early rather than waiting till the situation is much more dire and we may see nation productivity sky rocket as people feel happier and more engaged.
If the person is using wearable tech, we could monitor their health stats and view this, but more importantly, perhaps we can "monitor and alert" to issues, for example, a site worker who is tired or whose levels suggest he may not be safe to be working on a building site...

Sounds a bit "Minority Report" but this is the power of data, that said, data regulations may stop this from ever happening...




*** Working Notes ***

~~ Thursday 24th ~~
[01:32] Cannot run ddtrace - error:
vagrant@precise64:~/ddproject$ sudo ddtrace-run myapp.py
Traceback (most recent call last):
  File "/usr/local/bin/ddtrace-run", line 11, in <module>
    load_entry_point('ddtrace==0.12.0', 'console_scripts', 'ddtrace-run')()
  File "/usr/local/lib/python2.7/dist-packages/ddtrace/commands/ddtrace_run.py", line 78, in main
    os.execl(executable, executable, *sys.argv[2:])
  File "/usr/lib/python2.7/os.py", line 312, in execl
    execv(file, args)
OSError: [Errno 8] Exec format error

Can run script: 

vagrant@precise64:~/ddproject$ python myapp.py
 * Serving Flask app "myapp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
2018-05-24 00:33:23,071 - werkzeug - INFO -  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

[01:00] Still struggling to get this running... 
Flask uses port 5000 and dd-agent is on this port.  Hence error "socket.error: [Errno 98] Address already in use"  Considering options... 


~~ Wednesday 23rd ~~
[23:59] back again, Maybe I'm reading this wrong and I don't need the Python trace if I am using the given Flask app - playing with this a little more.
Installing Flask to the virtual env setup still failed, found article suggesting that older versions distribute to an old URL - used command "pip install -i https://pypi.python.org/simple -U pip distribute" and this cleaned up the issue and allowed me to then "pip install Flask" without issue.

[22:28] Having issues with "pip install trace" - Will have to leave for now and come back with fresh pair of eyes.  Error below:

vagrant@precise64:/etc/datadog-agent/checks.d$ sudo pip install ddtrace
Downloading/unpacking ddtrace
  Cannot fetch index base URL http://pypi.python.org/simple/
  Could not find any downloads that satisfy the requirement ddtrace
No distributions at all found for ddtrace
Storing complete log in /home/vagrant/.pip/pip.log

[21:36] Setting downtime periods, email notifications received.  Scheduled evening notification over weekend otherwise, as far as my logic goes, just by setting weekends, then a M > F alert, you'd miss the period that ends 00:01 Sunday Evening/Monday morning to 08:59 Monday morning, the tasks asked for two and so this is how I figured this would achieve the requirement.
[21:04] Metric was created, monitor setup and test emails have been received, found error and corrected this - used the wrong variable (^ not #) 
[17:15] Creating anomaly metric...  reading first.



~~ Tuesday 22nd ~~
[17:08] resolved invalid config issue, check reporting into dashboard and seems good. Missed "-" in the yaml file.  Bonus question answered. Reading about dashboards...



~~ Monday 21st ~~
[22:29] Picking up again...  Checking status of agents in DG, MySQL not showing so have rebooted ubuntu box as it was paused, may have upset things. (Playing with tags in mysql.yaml caused issue, have fixed this...)

  Config Errors
  ==============
    mysql
    -----
      yaml: line 8: found a tab character that violate indentation

[23:01] DogStatsd enabled after reading up on custom metrics, limits of metrics etc.cd
[23:25] Check Created and seems ok, amending collection interval...
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

[00:19] Kept seeing following error when I added the min_collection_interval -

Error: invalid config for mycheck: yaml: unmarshal errors:
  line 4: cannot unmarshal !!map into []check.ConfigRawMap
Error: no valid check found

Seems to work under the init_config section, although this doesn't work on the V6 Collector - Not happy with this - will come back to it.



~~ Sunday 20th May ~~
[13:48] Back home, ubuntu downloading in minutes now, ahh, to have bandwidth...  Also installing Vagrant to have an additional host to play with and to complete questions...
[13:58] Running vagrant up, waiting...  Configured host to have bridge networking, SSH working from OSX terminal.
[14:09] Curl installed - Datadog agent installed to host, MySQL installed - Datadog MySQL integration also being done.
[14:29] MySQL looking ok and Collector is running mysql checks.

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

[14:30] Will continue later.



~~ Saturday 19th May ~~
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

[21:52] Both agents available in Infra list - painful to install but that was due to local bandwidth, otherwise this would have flow. Agents reboot-less which is nice.
[22:08] Playing with Infra View and enabled process_config - process view very impressive and it unwraps svchost
[23:04] Documentation consumed, been playing with dashboard.  Feel more confident attacking answers.md, resuming tomorrow.
