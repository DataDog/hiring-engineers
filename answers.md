### My name is Zachary Groves and I am applying for the Solutions Engineer Role.

### The links to my dashboards are included inline but also here(screenshots are inline):
 <a href="https://app.datadoghq.com/dash/907404/timeboard-of-mymetric-and-database-anomalies?live=true&page=0&is_auto=false&from_ts=1536263564164&to_ts=1536349964164&tile_size=m">Timeboard of my_metric and database anomalies</a>. <a href="https://app.datadoghq.com/dash/909618/flask-mymetric-and-database-anomalies?live=true&page=0&is_auto=false&from_ts=1536346566652&to_ts=1536350166652&tile_size=m"> Timeboard of Flask app APM data and infrastucture.</a>

 ### Project Layout
 All of my code is inside of the datadog_exercise_project.
 The vm can be started up with `vagrant up` while in the datadog_vm folder and entered with `vagrant ssh`. All of the files I used/created are there and synced through vagrant except for the datadog.yaml file, the my_metric.py check file, the my_metric.yaml config file, and the postgres.yaml config file which are in their proper places in the datadog-agent folder inside of the vm. The datadog-agent folder can be navigated to after `vagrant ssh` with the file path /etc/datadog-agent. More about the environment setup below:

# Step 1: Setting Up The Environment

## Answer: 
I chose to spin up a fresh linux VM via Vagrant. The box I used was bento/ubuntu-16.04. I used <a href="https://www.youtube.com/watch?v=4Ue1WmcHipg">this</a> quick video tutorial on installation and getting setup. Vagrant was nice because I could provision Postgresql. This is my Vagrantfile which configures how vagrant will be setup:

<img src="https://image.ibb.co/hzWqnz/Creating_vagrant_file_with_provisions.png" alt="Creating_vagrant_file_with_provisions" border="0">

The next step I took was signing up for Datadog and getting the correct agent for my machine. You can sign up for a free 14 day trial to Datadog by going <a href="https://www.datadoghq.com/product/">here</a> and clicking Get Started Free. I then selected the linux platform and ran the following code snippet to install the Datadog agent.

<img src="https://image.ibb.co/c6igAK/installing_datadog_agent_onto_ubuntu_vm.png" alt="installing_datadog_agent_onto_ubuntu_vm" border="0">



# Step 2: Collecting Metrics

## Adding Tags Answer:
Tags can be added from the Host Map page, datadog.yaml file, or through the DatadogAPI. They are very useful for selecting and grouping data to visualize and analyze. My tags were added by modifying the datadog.yaml file as shown below:

<img src="https://image.ibb.co/ceZk4e/tags_added_datadog_yaml.png" alt="tags_added_datadog_yaml" border="0">

After adding the tags they appear on the Host Map Page:

<img src="https://image.ibb.co/hSQ6cz/tags_added_shown_on_host.png" alt="tags_added_shown_on_host" border="0">


## Installing Database Answer:
The database I chose to install was PostgreSQL which I did by adding it to the provisions as shown in Step 1 and running `vagrant provision` in the terminal. Datadog has hundreds of different integrations and installing them is literally as easy as clicking a button. I simply went to the Integrations, searched for postgresql, and clicked install. 

There are however some configurations you have to add in order have the Datadog agent monitor your database. These were all shown under the configuration tab for the postgresql integration <a href=https://app.datadoghq.com/account/settings#integrations/postgres>here </a>.

I created a datadog user for postgres, granted them SELECT privileges, and ran a script to help confirm whether or not the connection was working properly with:
```
create user datadog with password
'test123'
grant SELECT ON pg_stat_database to datadog;

psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" && \
echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
echo -e "\e[0;31mCannot connect to Postgres\e[0m"
 ```

 I then configured the postgres yaml file:
 <img src="https://image.ibb.co/bZhSHz/postgres_configuation.png" alt="postgres_configuation" border="0">

and restarted the agent with: `sudo service datadog-agent restart`

## Creating Custom Agent Check Answer:

To create the my_metric custom agent check I needed to create a my_metric.py file in the checks.d directory and a my_metric.yaml file in the conf.d directory. How to do it was found <a href="https://docs.datadoghq.com/developers/agent_checks/">here</a>. 

my_metric.yaml file:
<img src="https://image.ibb.co/mcF3qK/original_check_yaml_file.png" alt="original_check_yaml_file" border="0">

my_metric.py file: <img src="https://image.ibb.co/fPzDqK/my_metric_check.png" alt="my_metric_check" border="0">

This check worked but submitted data every 15 or so seconds and I needed to make it submit every 45 seconds. To do this I modified the my_metric.yaml file:
<img src="https://image.ibb.co/fobtqK/yaml_file_for_random_number_agent_check.png" alt="yaml_file_for_random_number_agent_check" border="0">

With this change, if the agent was submitting data and it had not been more than 45 seconds since the last time it had submitted then it would not submit the my_metric check.

Lastly I checked to make sure my_metric check was working:
<img src="https://image.ibb.co/fiobcz/checking_if_my_metric_is_working.png" alt="checking_if_my_metric_is_working" border="0">


## Can you change the collection interval without modifying the Python check file you created? Bonus Question:

Yes. Modifying the my_metric.yaml file rather than the my_metric.py file to change the collection interval was very easy. If I were to modify the my_metric.py file I would have kept track of the time since the last collection and if it was less than 45 seconds `return`. Another option would be to change the global collection interval so that datadog submits all data every 45 seconds. 


# Step 3: Visualizing Data

## Utilizing Datadog API To Create Timeboard Answer:

To make sending requests to the API easier I installed Pip in order to install the Datadog Python library:
<img src="https://image.ibb.co/jGUf4e/installing_pip.png" alt="installing_pip" border="0">
<img src="https://image.ibb.co/e0j2Hz/Installing_datadog_python_library.png" alt="Installing_datadog_python_library" border="0">

With the Datadog Python library I could import `initialize` and `api`. I also needed to make an application key on the website.
I learned from <a href="https://docs.datadoghq.com/api/?lang=python#timeboards"> here</a> and by playing around with the graphs on the website.  Below is my script for creating a timeboard that has my_metric, my_metric rolled up with the sum of its points over the past hour, and the postgresql buffer hit metric which I chose because it would show anomalies in the graph. Here is the <a href="https://app.datadoghq.com/dash/907404/timeboard-of-mymetric-and-database-anomalies?live=true&page=0&is_auto=false&from_ts=1536263564164&to_ts=1536349964164&tile_size=m">dashboard</a>:

<img src="https://image.ibb.co/eJkbcz/script_to_create_timeboard.png" alt="script_to_create_timeboard" border="0">

Timeboard created by script:
<img src="https://image.ibb.co/iVuoPe/Graphs.png" alt="Graphs" border="0">


## Snapshot Annotation Answer:
To set the Timeboard's timeframe I simply selected the last five minutes on the graph which zoomed me in to that timeframe. To take a snapshot I clicked on the graph, selected annotate, and put @zgroves19@gmail.com (my email):
<img src="https://image.ibb.co/cH7BAK/Graph.png" alt="Graph" border="0">

 This sent me a nice little email:
 <img src="https://image.ibb.co/mwt7je/email_sent_by_annotation.png" alt="email_sent_by_annotation" border="0">

 ## What is the Anomaly graph displaying? Bonus Question:
 I used the Basic anomaly function as opposed to the Agile or Robust anomaly functions. The Basic anomaly function determines a range of expected values based on previous data with no regards for seasonal changes. If the data goes outside of the expected values range then it is considered an anomaly which is displayed in red rather than blue on the graph.

 # Step 4: Monitoring Data

## Side Note:
For the Monitoring Data section I was actually unsure if I was supposed to complete it through the Datadog API or through the UI. I ended up doing both but could not find a way to specify a single monitor downtime for only weekdays in the UI and therefore decided that it was probably meant to be done through the API which allows specific days of the week to be targeted with downtimes. Therefore I will be showing the API way.  

## Creating The Monitor Answer:
When creating the monitor I used the documentation <a href="https://docs.datadoghq.com/api/?lang=python#create-a-monitor">here</a> which said that it's easier to define monitors in the Datadog UI and then export the JSON. I followed this advice and it made creating my Datadog API request pretty simple: 

<img src="https://image.ibb.co/h2b3QK/monitor_creation_script.png" alt="monitor_creation_script" border="0">

### Side note: 
By adding the `{host:datadog-project}` part to the query I was able to use it in the messages to get the host ip and host name. I used this <a href="https://docs.datadoghq.com/monitors/notifications/?tab=is_alertis_warning"> documentation</a>.

After running this script I got an email about the monitor's creation:
<img src="https://image.ibb.co/cy9ZXz/monitor_creation_email.png" alt="monitor_creation_email" border="0">

Parts of the monitor on the UI:
<img src="https://image.ibb.co/gaPRCz/monitor_website_screenshot.png" alt="monitor_website_screenshot" border="0">

<img src="https://image.ibb.co/hAhree/monitor_website_graph.png" alt="monitor_website_graph" border="0">


Over the course of the next few hours I also received 3 different messages for my alert (goes off when the average of my_metric for the last 5 minutes is above 800), warning (goes off when the average of my_metric for the last 5 minutes is above 500), and no data (goes off when the agent has not reported data from my_metric for 10 minutes) which I received by shutting down the virtual machine and waiting 10 minutes. 

Alert email:
<img src="https://image.ibb.co/dpQ55K/alert_email.png" alt="alert_email" border="0">

Warning email:
<img src="https://image.ibb.co/kwVYsz/warning_email.png" alt="warning_email" border="0">

No data email:
<img src="https://image.ibb.co/gHvcKe/no_data_email.png" alt="no_data_email" border="0">

## Schedule Two Downtimes For The Monitor Bonus Question:
When scheduling the downtimes from 7pm-9am on weekdays and all of the weekend I used the documentation <a href="https://docs.datadoghq.com/api/?lang=python#downtimes">here</a>. I also used <a href="https://www.epochconverter.com/">this</a> website to calculate the correct start times for the downtimes to begin. Shown when the `start_ts` variable is set.

Creating the 7pm-9am downtime on weekdays script:
<img src="https://image.ibb.co/eczq5K/weekday_downtime_monitor.png" alt="weekday_downtime_monitor" border="0">

Creating the weekend downtime script:
<img src="https://image.ibb.co/htLKze/weekend_downtime_monitor.png" alt="weekend_downtime_monitor" border="0">

When the downtimes were created I received these emails alerting me of their creation:

Weekday downtime email:
<img src="https://image.ibb.co/mjUq5K/weekday_monitor_downtime.png" alt="weekday_monitor_downtime" border="0">

Weekend downtime email:
<img src="https://image.ibb.co/e9ZOQK/weekend_monitor_downtime.png" alt="weekend_monitor_downtime" border="0">

The weekend monitor downtime in the UI:
<img src="https://image.ibb.co/bE1dQK/weekend_monitor_downtime.png" alt="weekend_monitor_downtime" border="0">

The weekday monitor downtime in the UI:
<img src="https://image.ibb.co/i4CDsz/weekday_monitor_downtime.png" alt="weekday_monitor_downtime" border="0">

## Side note:
My understanding is that datadog uses Universal time for the downtimes which makes a lot of sense since so many companies operate over many timezones. Universal time is 4 hours ahead of EST(my timezone) so they are correct. This was a bit confusing to me at first. Also I now have at least 50 datadog monitor alert emails in my inbox.

# Collecting APM Data:

## Instrumenting The Given Flask App Using Datadog's APM solution Answer:

I decided to use ddtrace-run instead of manualy inserting the Middleware. The documentation I used was: <a href="https://docs.datadoghq.com/tracing/setup/python/">tracing python applications</a>. In order to implement Datadog's APM solution on the flask app I first needed to install flask with `pip install Flask`, and ddtrace with `pip install ddtrace`. I also had to change the Vagrantfile to forward port 5050 on the VM to port 5050 on the host in order for my APM metrics to be seen since the app runs on port 5050:

<img src="https://image.ibb.co/dR2hN9/vagrant_file_added_port_5050.png" alt="vagrant_file_added_port_5050" border="0">

I also had to enable apm data to be collected by the agent in the datadog.yaml file:
<img src="https://image.ibb.co/mHLcN9/apm_enabled_config.png" alt="apm_enabled_config" border="0">

I created a new file with `sudo touch datadog_test_app.py` and pasted the app from the Readme.md into it.
Once this was done I ran the app with the ddtrace-run wrapper:
<img src="https://image.ibb.co/dpERFU/running_the_application.png" alt="running_the_application" border="0">

After that I used curl to test that it was running correctly and get some hits for the APM metrics:
<img src="https://image.ibb.co/id5V9p/curl.png" alt="curl" border="0">

This created some nice APM data, some of which I made visible on a <a href="https://app.datadoghq.com/dash/909618/flask-mymetric-and-database-anomalies?live=true&page=0&is_auto=false&from_ts=1536342253093&to_ts=1536345853093&tile_size=m">dashboard</a> along with my infrastructure data from before:
<img src="https://image.ibb.co/dZue29/dashboard_APM_And_infrastructure.png" alt="dashboard_APM_And_infrastructure" border="0">


## Difference Between Service and Resource Bonus Question:
Answer found <a href=https://docs.datadoghq.com/tracing/visualization/>here</a>. 
 A service is a set of processes that do the same job. e.g a webapp is service and a database is a service. The APM automatically assigns services one of four types: web, database, cache, or custom. 

 A resource is an action for a service. For example if you has a database service a resource would be a query e.g `SELECT * FROM godzilla_monsters WHERE name = ?` For a web application it might be url for example the flask app had `/api/apm`.  

 In addition resources and services have different naming requirements.


 # Final Question:


One possible creative use of Datadog would be for the Reddit hug of death. The <a href="https://en.wikipedia.org/wiki/Slashdot_effect">Reddit hug of death</a> is basically when a site is linked in a Reddit post that makes it to Reddit's front page and is visited so much that it overloads the smaller site. Wouldn't it be useful for the Datadog marketing team to target those website owners right as, a bit before, or a bit after their website has crashed or massively slowed down due to traffic? I would imagine other apps that reach the front page likely suffer from similar issues. Perhaps an application could be created that webscrapes the urls/applications from Reddit's front page and then dynamically monitors them through Datadog in some way. Then an email could be sent by the marketing team to the website/app owner showing the metrics and recommend trying out Datadog. I think that would be a pretty neat way to use/market for Datadog. 

Thank you so much for taking the time to review my application exercise. If you have any questions please feel free to email me at zgroves19@gmail.com. Have a great day! 