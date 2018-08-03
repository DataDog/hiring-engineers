Answers to Solution Engineering by Fernando Cremer (cremerfc@gmail.com)

## Collecting Metrics

Adding tags to configuration file and showing them in host map:

* Here is my Datadog.yaml

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/Datadogyaml.jpg" title="DataDogYamlTags">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/Datadogyaml.jpg"  alt="_DSC4652"></a>

* Here is my Host Map showing the tags for the host Unbuntu-Xenial

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/HostMapTags.png" title="DataDogYamlTags">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/HostMapTags.png"  alt="_DSC4652"></a>

* Screenshot showing mySQL metrics on host after installing mySQL and configuring the integration

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/hostwmysql.png" title="DataDogYamlTags">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/hostwmysql.png"  alt="_DSC4652"></a>

* Python file to create custom check to send my_metric a random value between of 0 and 1000:
[Python file to create custom check](https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/myCustomCheck.py)

* Tried to configure in the Python file to force it only sending the metric every 45 seconds. Was not able to properly determine the last time the metric ran. Found a couple of examples online but would not work. Thinking that checks are called every 15 - 20 seconds, I could check the last time it ran, find how long ago that was, and sleep for whatever time until we reach 45 seconds. Here is a screenshot of what I tried to do:

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/customcheck_w_sleep.png" title="Custom Check w Sleep">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/customcheck_w_sleep.png"  alt="customcheck_w_sleep"></a>


And the error received:

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/error_python_script.png" title="Error When Trying to Figure out Last Collection Time">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/error_python_script.png"  alt="error_python_script"></a>

So ended up setting the min_collection_interval in the YAML file for the custom check which can be seen here:

[Yaml file for custom check](https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/myCustomCheck.yaml)

* **Bonus Question** so as stated above I did set this up outside the Python file by using min_collection_interval in the YAML file.

## Visualizing Data:

* Python file used to create Timeboard:

[Python file to create timeboard](https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/create_timeboard.py)

* Here is a screenshot:

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/TimeboardAPI.png" title="Timeboard created by API">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/TimeboardAPI.png"  alt="TimeboardAPI"></a>

* Screenshot of email received from snapshot:

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/snapshot_email.png" title="Snapshot Email">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/snapshot_email.png"  alt="snapshot_email"></a>

* **Bonus Question** The anomaly graph shows deviation from what the expected value is based on history. This is done by comparing the obvserved value against the expected value.

## Monitoring Data

* Here is the configuration of the monitor that shows the alert and warning thresholds set accordingly abd the option to alert me if there is no data for more than 10 minutes:

<a href=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/AlertConfig.png title="Monitor Config">
<img src=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/AlertConfig.png  alt="monitorconfig"></a>

* Here is the email sent to my inbox from the monitor:

<a href=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/monitor_email.png title="Monitor Email">
<img src=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/monitor_email.png  alt="monitor_email"></a>

* Here is the downtime scheduled for Monday through Friday:

<a href=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/downtime_M_F.png title="Downtime weekdays">
<img src=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/downtime_M_F.png  alt="downtime_Weekdays"></a>

* Here is the email notifying me of the downtime:

<a https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/downtime_wd_email.png title="Downtime weekdays email">
<img src=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/downtime_wd_email.png  alt="downtime_Weekdays_email"></a>

* Here is the downtime scheduled for the weekend:
<a href=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/downtime_weekend.png title="Downtime weekdend">
<img src=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/downtime_weekend.png  alt="downtime_Weekdend"></a>

* Here is the email notifying me of the downtime:

<a href=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/downtime_we_email.png title="Downtime weekdays email">
<img src=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/downtime_we_email.png  alt="downtime_Weekdays_email"></a>

## Collecting APM Data:

* Here is a screenshot of a screen board I created to show metrics from infrastrcuture and applications showing a CPU spike around the same time that one of the application had a spike in request hits:

<a href=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/inclusive_board.png title="Inclusive Dashboard">
<img src=https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/inclusive_board.png  alt="inclusive_board"></a>

https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/inclusive_board.png

I used ddtrace for the two python apps:



