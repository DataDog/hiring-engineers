# Links

[Events](https://app.datadoghq.com/event/stream)

[Dashboard](https://app.datadoghq.com/dashboard/lists)

[Timeboard](https://app.datadoghq.com/dash/1029490/my-datadog-technical-challenge-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1545691140000&to_ts=1545694740000&live=true)

[Metric Summary](https://app.datadoghq.com/metric/summary)

# Prerequisites - Setup the environment:

## Final Results:

DataDog successfully runs in terminal screenshot.

![DataDog successfully runs in terminal screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/6_DataDogRuns.png)

DataDog reports metrics from local machine screenshot.

![DataDog reports metrics from local machine screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/7_DataDogReportsmetricsfromlocalmachine.png)

## Steps followed:

1) Went to GitHub repo and forked it onto my local computer. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/0_github_repo_forked.png)
1.5) Virtual machine already installed on local computer
2) Installed vagrant. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/1_installingvagrant/2_successwithvagrant.png)
3) Vagrant successfully installed. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/2_successwithvagrant.png)
4) Virtual box running from terminal successfully.
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/3_virtualboxrunning.png)
5) Attempted to install DataDog but I needed curl. Installed curl. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/4_installingcurl.png)
6) Installed DataDog using prompted commands. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/5_installingdatadogonVM.png)
7) DataDog success in terminal. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/6_DataDogRuns.png)
8) DataDog reports metrics from local machine. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/pics_for_environment_setup/7_DataDogReportsmetricsfromlocalmachine.png)
9) Environment setup complete! :D

# Collecting Metrics

## Final Results:

my_metric.yaml screenshot

![my_metric.yaml screenshot](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/13_customcheckyaml.png) 

my_metric.py screenshot

![my_metric.py screenshot](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/14_customcheckpython.png) 

Time interval of metric update changed to 45 seconds between updates screenshot.

![Time interval of metric update changed to 45 seconds between updates screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/15_customcheckevery45seconds.png)

Metric tested and shows it runs screenshot screenshot.

![Metric tested and shows it runs screenshot screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/16_testmetricsuccess.png)

### Bonus: 
Yes, you can change the instance rate without editing the .py file as the instance rate is found in the .yaml not the .py file.

## Steps followed:

0) Googled how find the to agent config file.
1) Went into /etc/datadog-agent/datadog.yaml to read the .yaml file and change where needed to add tags. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/1_editedyamltoaddtags.png)
2) Got a NTP error. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/2_NTPerror.png)
3) Researched how to fix NTP error. NTP fixed itself? 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/3_NTPfixed.png)
4) Check to see if agent is running, there is a problem. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/4_Checktoseeifagentisrunning.png)
5) Found the error, went into the .yaml and fixed it. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/5_founderror.png)
6) It works!! The tags are there! 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/6_Iseetags.png)
7) Went to the host map and saw tags there. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/7_tagsshownonhostmap.png)
8) Installing MySQL server on VM. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/8_Installingmysql.png)
9) It LIVES!!! The MySQL server works. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/9_mysqlserverlives.png)
10) Give DataDog access to MySQL server. Test. Success! 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/10_giveaccesstomysqltodd.png)
11) Checked for mysql.yaml after editing. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/11_mysqlshowsuponagent.png)
12) Success 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/12_mysqladded.png)
13) my_metric.yaml 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/13_customcheckyaml.png) 
14) my_metric.py 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/14_customcheckpython.png) 
15) Changed interval of metric to 45 seconds between updates. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/15_customcheckevery45seconds.png)
16) Metric tested and shows it runs. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/collecting_metrics_pics/16_testmetricsuccess.png)

### Note: 
I started [here](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) but was confused when after following the instructions it didn't work. 

I Googled how to do it. The website that looked the most promising is [this one](https://datadog.github.io/summit-training-session/handson/customagentcheck/). Which is similar to  but not the same. In step 3 it says to go into the conf.d. Then step 4 is create the .yaml file. In step 6 says "Create a new check file in the checks.d directory. Name the file checkvalue.py." Since there wasn't a checks.d in conf.d I thought that I needed to create a checks.d in the conf.d directory. It took me quite a while to figure out that checks.d already existed and that it and conf.d are in the same directory. So I should not have created a new checks.d in conf.d. I would like to suggest that when giving instructions that the full path be utilized in all instructions to avoid this kind of error.

# Visualizing Data

## Final Results:

Here is a link to the code [datadogapigraph.py](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/datadogapigraph.py)

Here is a screenshot of the Timeboard my code created and found all three visualizations. 

![Here is a screenshot of the Timeboard my code created and found all three visualizations.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/3_Timeboard_from_code.png)

I did not find a way to successfully change the time interval to 5 minutes. See below to see what I did.

### Bonus: 

The anomaly graph is the regular graph along with a shadow of the average range for the data. If the line appears red than the data reported is outside of the normal numbers expected. 

## Steps followed:

1) For full code see work in [datadogapigraph.py](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/datadogapigraph.py) file.
	* Started by getting my DataDog API and APP keys from my account and adding them to the top of the document.
	* Followed instructions for how to create a Dashboard in the DataDog documentation.
	* Followed instructions for how to create a Timeboard in the DataDog documentation.
	* Needed 3 visualizations according to the instructions. So I added a graph for each of the challenges and changed the settings to fit each request. 
		* Note: The default setting for time period is one hour so for the third challenge I did not need to change anything.
	* Played with messages. There were two options on the messages page so labeled each response to see if one or both would work.
2) Created a virtual environment to run the code in. Then ran the code. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/1_creating_venv_install_dd_run_code.png)
3) Went to events page and found both messages present. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/4_Messages_shown.png)
4) Went to Dashboards list and found the Dashboard my code created. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/2_Dashboard_from_code.png)
5) Went to the Timeboard my code created and found all three visualizations. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/3_Timeboard_from_code.png)
6) Sending snapshot of graph to @nicholle@oboechick.com 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/5_Sending_snap_shot.png)
7) Attempt to make the time interval 5 minutes using the UI 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/6_menu_for_changing_time.png)
8) Select the only option that isn't a set time on the menu. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/7_attempt_to_change_to_5_mins.png)
9) Clicking on the date I want in hope that a time menu will show up after the date is chosen. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/8_make_it_23_to_23.png)
10) This changes it to 24 hour interval. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/9_changes_it_to_24_hrs.png)
11) Attempt to change the y-axis to make the time interval 5 minutes. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/10_attempt_to_use_yaxis_to_change_time_interval.png)
12) No change to the graph after y-axis applied 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/visualizing_data_pics/11_post_yaxis_no_change.png)
13) I did not find a way to successfully change the time interval to 5 minutes.

# Monitoring Data

## Final Results:

Email alert with datapoint screenshot.

![Email alert with datapoint screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/4_email_screenshot_of_alert_with_metric_number.png)

Email alert 2. Checking to make sure the emails are different screenshot.

![Email alert 2. Checking to make sure the emails are different screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/5_email_alert_2.png)

Email alert 3. Confirmed the emails are different screenshot.

![Email alert 3. Confirmed the emails are different screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/6_email_alert_3.png)

### Bonus Final Results:

M-F Email Confirmation Screenshot.

![M-F Email Confirmation Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/12_MF_downtime_email.png)

Saturday and Sunday Email Confirmation Screenshot.

![Saturday and Sunday Email Confirmation Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/11_SatSun_downtime_conf_email.png)

## Steps followed:

1) Created new Monitor.
2) Set warning to 500, alert to 800, and making sure that if no data no alert is sent. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/1_defining_warning_and_alert.png)
3) Create message to send depending on type of alert. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/2_Add_Message_when_alarm_engaged.png)
4) First email alert received. Realized the datapoint was not there. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/3_email_screenshot_of_alert.png)
5) Email alert with datapoint. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/4_email_screenshot_of_alert_with_metric_number.png)
6) Email alert 2. Checking to make sure the emails are different. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/5_email_alert_2.png)
7) Email alert 3. Confirmed the emails are different. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/6_email_alert_3.png)

### Bonus Steps followed:

1) Setting downtime for Monday - Friday 7:00PM-9:00AM. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/7_set_downtime_MF.png)
2) M-F Set 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/8_detailed_MF_downtime.png)
3) M-F Email Confirmation 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/12_MF_downtime_email.png)
4) Setting downtime for Saturday and Sunday all day. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/9_Downtime_SatSun.png)
5) Saturd 
![Screenshot.]y and Sunday set 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/10_SatSun_downtime.png)
6) Saturday and Sunday Email Confirmation 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/monitoring_data_pics/11_SatSun_downtime_conf_email.png)

# Collecting APM Data:

## Final Results:

I have attempted to connect to the APM using both my VM and mac and have not been able to get it to work. I am unsure what is wrong. I included everything that I attempted to try above.

### Bonus:

A service is like the MySQL server. A resource is a query to the server (MySQL).

## Steps followed:

1) Followed the instructions in changing the .yaml file so that the APM was turned on. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/1_update_ddyaml.png)
2) Attempted to install ddtrace but pip is out of date. So updated pip. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/2_attepmt_to_install_ddtrace_on_VM.png)
3) Attempted to install ddtrace again and had problems with pip. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/3_second_attempt_at_ddtrace_in_VM.png)
4) After a few more attempts to fix the problem thought about updating python to see if that fixed pip.  
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/4_update_python_and_pip_in_VM.png)
5) Pip installed! 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/5_pip_install_success.png)
6) Pip still not working. Decided to try to get the APM working in a venv. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/6_pip_still_not_working.png)
7) Check to see if the APM is working. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/6a_see_if_apm_working.png)
8) APM is not running at all. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/6b_apm_not_working.png)
9) Installed ddtrace on venv. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/8_ddtrace_successfully_installed_on_venv.png)
10) Installed flask on venv. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/9_installing_flask_on_venv.png)
11) Empty page shows up. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/11_result_from_running_code.png)
12) Installed ddagent. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/7_switched_from_VM_to_venv_install_ddagent.png)
13) Ran the files given in the challenge. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/10_run_flask_doc_given.png)
14) Fixed a few things and tried again. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/12_fixed_things_attemp_2.png)
15) Tried to fix config file in venv. 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/13_attempt_to_fix_config_file_to_connect_to_apm.png)
16) Still having problems 
![Screenshot.](https://raw.githubusercontent.com/oboechick/hiring-engineers/solutions-engineer/Collecting_APMdata_pics/14_still_not_working.png)
17) Conclusion: I have attempted to connect to the APM using both my VM and mac and have not been able to get it to work. I am unsure what is wrong.

# Final Question

**Idea 1:** I want to connect a fitbit like monitor to my cat and see if I can track how often she moves around my apartment. It would also be interesting to see if I could get the speed that she is moving. I would then use DataDog to visually look at these two things. Once I get it for my cat do the same with my friend's pets and see how different it is for dog vs cat. I could set an alert to tell me whenever the monitor stops sending data as well.

**Idea 2:** I am in the process of looking through my gmail account so see if I can find anything interesting. I've already connected it to DataDog using Zapier but I've not looked at it yet. Create tags to identify senders from Amazon, conferences, google groups, etc. What percentage of my email is from Amazon vs other. 
