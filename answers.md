
# DataDog Hiring Exercise - William Karges Answers

*Disclaimer: All code is linked in this doc, it can also be found in the config files folder.*

## Section 1 - Collecting Metrics

### Tags

Installed DataDog agent on my local Windows machine and added tags in the datadog.yaml.  It took me longer than it should've as I'm admitedly not great at coming up with naming conventions.

*tags: - "availability-zone:us-west" - "machine:local" - "env:test"*
	
[HostMap](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)
![HostMap_Tags.png](assets/HostMap_Tags.png)

### Relational Database Integration

Installed MySQL and HeidiSQL (so I could have a UI) on my local Windows machine.  Added the datadog user to the MySQL DB to grant access for the DD Agent.  Configured the MySQL conf.yaml file to pass the appropriate database credentials.

This process is almost identical to a typical OLE DB integration but the DataDog agent gives you the ability for far more detailed machine & database monitoring as opposed to a simple SELECT query that you see in most relational DB integrations.

[conf.yaml](configfiles/conf.yaml)

![mySQL_integration.png](assets/mySQL_integration.png)

### Custom Agent

Created a custom agent by placing a python file in the checks.d repository and a matching .yaml file in the config.d repository.

Uses the python [random](https://docs.python.org/3/library/random.html) library (specifically the **randint** function) with data dog [gauge](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=gauge) metric submission to submit my_metric with a random integer value between 0 and 1000.

Used the **min_collection_interval** function in the yaml file to set the collection to every 45 seconds without modifying the python check file.

[PythonFile](configfiles/custom_ac1.py)
[YamlFile](configfiles/custom_ac1.yaml)

![my_metric.png](assets/my_metric.png)

## Section 2 - Visualizing Data

Imported the DataDog API collection into Postman.  Customized the create dashboard POST requet to track my_metric averages and sum over the past hour as well as MySQL CPU usage anomalies.  See [WK_CustomTimeBoard JSON file](configfiles/WK_CustomTimeBoard.json)

### Create Dashboard API

[WK Timeboard](https://app.datadoghq.com/dashboard/ysn-u6q-tmg/williams-timeboard-20-jan-2020-1735?from_ts=1579721318547&to_ts=1579722218547&live=true&tile_size=m)

![PostmanAPI_Success.png](assets/PostmanAPI_Success.png)

![TimeTable_1-21-2020.png](assets/TimeTable_1-21-2020.png)

Unfortunately I wasn't able to, "Set the Timeboard's timeframe to the past 5 minutes" (see screenshot below).  While I can adjust individual graphs to 5 minutes, the timeboard itself seems to be restricted to 15 minute intervals.  Not sure if this is just a limitation of the trial version or maybe this was just a trick question.

### 5 Minute Snapshot

[TimeBoard Notification e-mail](assets/TimeBoard_Notification.eml)

##### Error
![Error_5min.png](assets/Error_5min.png)

##### 5 Minute Graph
![5mGraph.png](assets/5mGraph.png)

##### Notifications
![Notifications.png](assets/Notifications.png)

### Bonus Question - What is the Anomaly graph displaying?

The Anomaly graph compiles historical performance of a specific metric to flag truly "abnormal" activity.  

For example a game developer may have an alert set for when their autoscaling servers eclipse a specified threshold.  If the alert gets triggered on a Friday night it's likely redundant as the majority of their users are active weekend nights and there's probably an existing process to provision more servers.  

The more relevant information might actually be the opposite, if the server count stays unchanged or low through the Friday night.  The alert wouldn't go off since the threshold wasn't eclipsed but the anomaly graph would call out the unusually low server usage.  This in turn may motivate the game company to boost their marketing and/or run an in-game promotion the next weekend to recooperate that user base or, at the very least, scale down server usage to save costs.

## Section 3 - Monitoring Data

Used the DataDog monitoring tool to create a monitor that tracked my_metric on my host machine and sent notifications to my e-mail if specific criteria was met:

	* Warning if my_metric eclipsed the threshold of 500
	* Alert if my_metric eclipsed the threshold of 800
	* Notification if my_metric has missing data over 10 minutes

Tested the threshold both on average and at least once during the last five minutes.  Used conditional statements to adjust the body of the e-mail notification based on the relevant alert type.  Then immediately deleted the monitor to prevent my phone from vibrating off my desk.

[Monitor JSON](configfiles/Monitor.json)

[Monitor E-mails](assets/Monitors/)

![Warn.png](assets/Monitors/Warn.png)

### Bonus Question - Deactivate Out of Office notifications

Monitor alerts can be turned ad hoc via the mute button in the monitor dashboard or have scheduled deactivation by using the scheduled downtime feature.

[Scheduled Downtime](https://app.datadoghq.com/monitors#downtime?)

#### Mute
![mute.png](assets/Monitors/mute.png)

#### Scheduled Downtime configuration
![SilenceScope.png](assets/Monitors/SilenceScope.png)

#### Scheduled Downtime test e-mail
![scheduled_downtime_email.png](assets/Montiors/scheduled_downtime_email.png)

## Section 4 - Collecting APM Data


