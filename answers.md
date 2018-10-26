Your answers to the questions go here.

# Prerequisites - Setup the environment

Following along with Datadog **[docs](https://docs.datadoghq.com/)**, I downloaded Datadog onto my machine using `vagrant up` and `vagrant ssh` to power up vagrant, retrieved my API key, and installed Agent v6. It was here that I realized I had actually installed the agent directly onto my machine instead of my virtual machine. 

After deleting the Agent and reinstalling for ubuntu, I was denied access to the files inside the agent directory. After searching online about how to change permissions, I learned that changing into the root@vagrant directory gives access to all files.

Agent reporting metrics from my local machine:

<img width="565" alt="agent_reporting_metric" src="https://user-images.githubusercontent.com/10853262/47467220-17e38900-d7aa-11e8-8a93-949b7262e9c2.png">




# Collecting Metrics

### Agent Tags

I added tags to the Agent configuration file via the UI.
Screenshot of host and its tags on the Host Map page:

<img width="872" alt="host_and_tags" src="https://user-images.githubusercontent.com/10853262/47468486-68f67b80-d7b0-11e8-8b45-36c55e0b8eca.png">

### Install Database

I then installed a database on my machine to monitor and visualize PostgreSQL called dekker_db and configured **postgres.d/conf.yaml** to collect logs, create a read-only Datadog user with access to the PostgreSQL server, and grant permission to query additional tables. (Side note: unfortunately, I copied and pasted the read-only access too quickly and foolishly retained the password <PASSWORD>).

I also edited the PostgreSQL configuration file,  **/etc/postgresql/9.5/main/postgresql.conf** to facilitate metric collection as per log collection directions [here](https://docs.datadoghq.com/integrations/postgres/).
  
Because logs were already enabled in **datadog.yaml** for the Agent, I added the log configuration block for PostgreSQL in **postgres.d/conf.yaml**, changing the service and path configuration. 

Code snippet for postgres.d/conf.yaml:
```
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: <PASSWORD>
    dbname: dekker_db
    ssl: False
    use_psycopg2: False
    tags:
    - postgres
    collect_count_metrics: False
  
logs:
  - type: file
    path: /var/log/postgres_log/postgres.log   
    source: postgresql
    sourcecategory: database
    service: myapp
 ```

Screenshot of Postgres integration on Host Map:

<img width="1015" alt="host_with_postgres" src="https://user-images.githubusercontent.com/10853262/47393308-f44e0f00-d6d3-11e8-8c81-b6ab1e99110f.png">

To finish, I restarted the Agent and ran the Agent status command to make sure the integration was successful: 

<img width="368" alt="postgres_check" src="https://user-images.githubusercontent.com/10853262/47393520-94a43380-d6d4-11e8-9a76-ff67e1520f10.png">

### Custom Agent Check

To create a custom Agent check, I read the documentation [here](https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6) and created two files: one in the `/etc/datadog-agent/checks.d` directory called **custom_check.py** and the other in `/etc/datadog-agent/conf.d` called **custom_check.yaml**. Initially, the .py script submitted a metric, named my_metric, of a random value between 0 and 1000, using self.gauge to sample the metric. Using the sleep method imported from the time module, I wrote a Python script to change the collection interval of my_metric every 45 seconds. Although the documentation mentioned sending events and service checks with the Agent check, I did not include them.  

Code for custom_check.yaml:

<img width="625" alt="custom_check_yaml" src="https://user-images.githubusercontent.com/10853262/47395669-6fb3be80-d6dc-11e8-87a1-1f08d742cae2.png">

Code for custom_check.py:

<img width="625" alt="custom_check_py" src="https://user-images.githubusercontent.com/10853262/47395664-6c203780-d6dc-11e8-9cee-a634d2dd8a34.png">

To test that the Agent was working, I ran `sudo -u dd-agent datadog check custom_check`:

<img width="391" alt="custom_check" src="https://user-images.githubusercontent.com/10853262/47395722-9ffb5d00-d6dc-11e8-92ff-b370e16b6955.png">

### Bonus Question
To set the interval without modifying **custom_check.py**, the **custom_check.yaml** file can be modified as follows:

<img width="623" alt="custom_check_yaml_2" src="https://user-images.githubusercontent.com/10853262/47395796-ff596d00-d6dc-11e8-9cc2-64600b934db2.png">

# Visualizing Data

### Creating the Timeboard from Datadog's API
First, I installed the [dogshell](https://help.datadoghq.com/hc/en-us/articles/211364766-Dogshell-Quickly-Use-Datadog-s-API-from-Terminal-Shell) via pip install datadog and created my .dogrc file. Sadly, I wasn't able to create a Timeboard using dogshell, so I moved on to create the following three metrics using the curl command in the API [documentation](https://docs.datadoghq.com/api/?lang=bash#screenboards):
-   Custom Metric Scoped Over Host
-   Metric from Database with the Anomaly function applied
-   Custom Metric with the Rollup function (sum , 60)

After spending an hour trying to create a Timeboard from the API with all three metrics, I finally succeeded with curl. I used the following script (the Anomaly function would not initially create a metric on the graph: please see below for more detail):

<img width="689" alt="curl_timeboard" src="https://user-images.githubusercontent.com/10853262/47396067-3419f400-d6de-11e8-9392-7f632dc22602.png">

Link to text file for above script: [curl_timeboard.txt](https://github.com/dmcdekker/hiring-engineers/files/2508368/curl_timeboard.txt)

This was definitely the trickiest part of the exercise! Whenever I tried to pass in the anomalies function, I got the error message, {"errors": ["Error parsing query: unable to parse anomalies(avg:postgresql.rows_fetched{*}, basic, 2): Rule 'scope_expr' didn't match at ', 2)' (line 1, column 48)."]}. Here’s a breakdown of how I troubleshot:

1.  Double checked the parameters for the [anomalies](https://docs.datadoghq.com/graphing/functions/algorithms/) function.
    
2.  Used [JSONLint](https://jsonlint.com/) to make sure my JSON was properly formatted and validated.
    
3.  As a test, I set up the Anomaly function manually and used the JSON inside the metric, which I then copy and pasted into my curl script.
  
4.  After combing through bash formatting issues, I finally realized that the quotes around the second anomalies function parameter, 'basic', needed to be escaped. Success! It worked.

Original Timeboard created with Postgres Metrics:

<img width="547" alt="timeboard_metrics" src="https://user-images.githubusercontent.com/10853262/47396372-47798f00-d6df-11e8-8acd-de3ee0a12372.png">

Just for fun and because the above graph wasn’t as visually interesting as time progressed, I input a different metric (system.cpu.user) to show off the Anomaly function more clearly. 
Text file: [curl_second_timeboard.txt](https://github.com/dmcdekker/hiring-engineers/files/2508391/curl_second_timeboard.txt)

Second Timeboard created with CPU Metrics:

<img width="548" alt="cpu_metrics" src="https://user-images.githubusercontent.com/10853262/47396490-e1413c00-d6df-11e8-9bdf-d73adad9f8ae.png">

### Set  Timeboard's Timeframe to the Past 5 Minutes
Once the Timeboard was successfully created, I accessed the Dashboard UI and tried to set the Timeboard"s timeframe to the past 5 minutes. But, from the documentation, it appears that this functionality is not available for Timeboards, only Screenboards. Screenboards possess a Global Time Selector, to set the Timeframe under 60 minutes, but Timeboards do not. I did try to research if I could convert the Timeboard to a Screenboard, but the [link](https://docs.datadoghq.com/graphing/faq/how-to-transform-a-timeboard-to-a-screenboard-or-vice-versa/) was broken in Datadog docs. 

### Snapshot of  Graph Using @ Notation to Send it to Me

Screenshot of @notation sent to events page:

<img width="670" alt="timeboard_from_dash_list" src="https://user-images.githubusercontent.com/10853262/47396500-eb633a80-d6df-11e8-92c3-1496d7b582a6.png">

I also received an email.

### Bonus Question
**What’s the Anomaly function doing?** 
Because this graph is monitoring the system CPU usage (which is the time the operating system spends running code), the Anomaly function shows when there are spikes outside of the normal range of values (represented by red peaks and troughs on the graph, where the normal range is represented in blue).



# Monitoring Data

### Create Metric Monitor

I created a new, simple Metric Monitor with a Threshold Alert to watch the average of my custom metric. This monitor sends me alerts when my_metric is above the following values over the past 5 minutes:
- Warning threshold > 500 
- Alert threshold > 800 
- And also when there is No Data for the query over the past ten minutes.

Using the UI, I configured the monitor’s message so that it notified me whenever any of the above conditions were breached, and configured the monitor's message to: 

- Send an email whenever the monitor triggers.
- Include the metric value that triggered the monitor and also the host ip when the Monitor triggers an Alert state.
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state using the following markdown:

<img width="623" alt="monitor_markdown" src="https://user-images.githubusercontent.com/10853262/47396601-5c0a5700-d6e0-11e8-8574-8db75f9192ca.png">

Screenshot of the email I received from the Monitor:

<img width="783" alt="alert_over_800_email" src="https://user-images.githubusercontent.com/10853262/47396636-80663380-d6e0-11e8-94ed-0b0114f84f42.png">


**Neato!**  :+1:

I then set up two scheduled downtimes for this monitor:

-   One that silences it from 7pm to 9am daily on M-F
    
-   And one that silences it all day on Saturday and Sunday.
    
### Bonus Question

Using the UI, I navigated to the Manage Downtime page of Monitors, I scheduled recurring weekly downtime to silence the Monitor for specific time periods, which were:

-   Monday to Friday, 7pm to 9am daily.
-   All day Saturday and Sunday.

Screenshot of the email notifications for weekend and weekly mutes:

<img width="771" alt="weekend_mute_email" src="https://user-images.githubusercontent.com/10853262/47396639-83f9ba80-d6e0-11e8-8a51-33d6a962b9ac.png">

<img width="771" alt="weekly_mute_email" src="https://user-images.githubusercontent.com/10853262/47396643-878d4180-d6e0-11e8-9577-919de84b640d.png">

# Collecting APM Data
In order to enable trace collection, I followed the [steps](https://docs.datadoghq.com/tracing/setup/) for tracing set up and used the given Flask app to instrument using Datadog's APM solution.

Given that I’m not monitoring anything very complex on my machine, I did not modify my environment and let data default to env:none. Then, I started up virtualenv, where I already had Flask installed, and created a new Flask app called datadog_.py to instrument using Datadog’s APM solution.

After installing the Datadog Tracing library **ddtrace** with pip, I ran the Flask app in my browser and after a few minutes, it started submitting data to the Agent. 

### Bonus Question
**What's the difference between a Service and a Resource?** 
A Service is a distinct series of processes that form a service set; users can determine services when they instrument their app with Datadog; for example, a database would be a service. Making a query to a service is called a Resource.

[Link](https://p.datadoghq.com/sb/58ad2a67c-c1a95aa60b3d98a02603c7b8919c9efb) and screenshot of my Dashboard with both APM and Infrastructure Metrics:

<img width="887" alt="apm_and_infrastructure_dash" src="https://user-images.githubusercontent.com/10853262/47396972-f9b25600-d6e1-11e8-82e2-2c6919f2c621.png">

# Final Question
**How would I use Datadog?** 
As a chef who obsesses over cooking things perfectly, I’d connect a smart thermometer to Datadog, specifically to measure the internal temperature of meat while it cooks. A few minutes of over or undercooking can make a huge difference in flavor and vital to avoid foodborne illness. Additionally, heat is lost when the door is open and closed; having a well placed thermometer that can be monitored externally would be amazing!

> Written with [StackEdit](https://stackedit.io/).