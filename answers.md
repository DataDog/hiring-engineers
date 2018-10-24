# Prerequisites - Setup the environment

After skimming the overview, I downloaded Datadog onto my machine--pretty smooth, or so I thought!--used `vagrant up` and `vagrant ssh` to power up vagrant, retrieved my API key, added my tags, and installed Agent v6. After the instructions stopped being compatible with what I was seeing, I realized that I had actually installed the agent directly onto my machine instead of my virtual machine. 

After deleting the agent and reinstalling for ubuntu, I was then denied access to the files inside the agent directory. After searching online about how to change permissions, I learned that changing into the root@vagrant directory gives access to all files.

Script for fresh install of Agent v6 (minus API key):
```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
Agent status shows proper configuration:

<img width="365" alt="successful_integration" src="https://user-images.githubusercontent.com/10853262/47392866-9c62d880-d6d2-11e8-9f38-df77fbf2c7e3.png">

I also configured custom log collection for the Agent by enabling logs 
`logs_enabled: true` in **datadog.yaml** and creating a file in `/etc/datadog-agent/conf.d` called **conf.yaml**:
```
logs:

- type: file

path: /var/log/pg_log/pg.log

service: myapp

```
Agent check status:

<img width="296" alt="log_agent_conf" src="https://user-images.githubusercontent.com/10853262/47397628-0d12f080-d6e5-11e8-955f-6fcd55731e6b.png">

# Dashboard

Screenshot of host with no tags:

<img width="947" alt="host" src="https://user-images.githubusercontent.com/10853262/47334581-3461b300-d63c-11e8-9162-bed1be09124f.png">

After adding tags in the Agent config file, a screenshot of my Host Map and its tags:

<img width="1138" alt="host_with_tags" src="https://user-images.githubusercontent.com/10853262/47376532-ae7b5180-d6a7-11e8-8508-c4d5d3c0e08d.png">

# Collecting Metrics

I then installed a database on my machine (PostgreSQL) called dekker_db and followed the integration steps [here](https://docs.datadoghq.com/integrations/postgres/). Unfortunately, I copied and pasted too quickly and retained the password <PASSWORD> (not ideal!).

After creating a read-only Datadog user with access to the PostgreSQL server, I edited **postgres.d/conf.yaml** and my PostgreSQL configuration file,  **/etc/postgresql/9.5/main/postgresql.conf** to facilitate metric collection, with the following uncommented:
```
logging_collector = on
log_directory = 'pg_log'  # directory where log files are written,
                            # can be absolute or relative to PGDATA
log_filename = 'pg.log'   #log file name, can include pattern
log_statement = 'all'     #log all queries
  log_line_prefix= '%m [%p] %d %a %u %h %c '
log_file_mode = 0644
  ```

Because logs were already enabled in **datadog.yaml**, I added the log configuration block in **postgres.d/conf.yaml**.

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

Screenshots of Postgres Overview and Metric Dashboards:

<img width="566" alt="postgres_overview" src="https://user-images.githubusercontent.com/10853262/47393321-fdd77700-d6d3-11e8-93f4-03c6e10320ab.png">
<img width="1044" alt="postgres_metrics" src="https://user-images.githubusercontent.com/10853262/47393325-fdd77700-d6d3-11e8-8173-6d6e5fe7b083.png">

Datadog Agent Status Check:

<img width="368" alt="postgres_check" src="https://user-images.githubusercontent.com/10853262/47393520-94a43380-d6d4-11e8-9a76-ff67e1520f10.png">

<img width="352" alt="log_agent_2" src="https://user-images.githubusercontent.com/10853262/47397688-4ea39b80-d6e5-11e8-81d5-35d3eb8f78c9.png">


# Custom Agent Check

In order to create a custom Agent check, I read the documentation [here](https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6) and created two files: one in the `/etc/datadog-agent/checks.d` directory called **custom_check.py** and the other in `/etc/datadog-agent/conf.d` called **custom_check.yaml**. As per instructions, I wrote a Python script to run every 45 seconds; I used the sleep method imported from the time module. 

Code for custom_check.yaml:

<img width="625" alt="custom_check_yaml" src="https://user-images.githubusercontent.com/10853262/47395669-6fb3be80-d6dc-11e8-87a1-1f08d742cae2.png">

Code for custom_check.py:

<img width="625" alt="custom_check_py" src="https://user-images.githubusercontent.com/10853262/47395664-6c203780-d6dc-11e8-9cee-a634d2dd8a34.png">

From datadog-agent status check:

<img width="391" alt="custom_check" src="https://user-images.githubusercontent.com/10853262/47395722-9ffb5d00-d6dc-11e8-92ff-b370e16b6955.png">

To set the interval without modifying the custom_check.py file, the custom_check.yaml file can be modified as follows:

<img width="623" alt="custom_check_yaml_2" src="https://user-images.githubusercontent.com/10853262/47395796-ff596d00-d6dc-11e8-9cc2-64600b934db2.png">

# Visualizing Data

First, I installed the [dogshell](https://help.datadoghq.com/hc/en-us/articles/211364766-Dogshell-Quickly-Use-Datadog-s-API-from-Terminal-Shell) via pip install datadog and created my .dogrc file:
<img width="793" alt="initialize_dogrc" src="https://user-images.githubusercontent.com/10853262/47395835-329bfc00-d6dd-11e8-8745-f72ed072a476.png">
Sadly though, I wasn't able to create a Timeboard using dogshell, so in the interest of time, I moved on to create the following three metrics using the curl command:
-   Custom Metric Scoped Over Host
-   Metric from Database with the Anomaly function applied
-   Custom Metric with the Rollup function (sum , 60)

After spending a few hours trying to create a Timeboard from the API with all three metrics, I finally succeeded. With curl, I used the following script (the Anomaly function would not initially create a metric on the graph: please see below for more detail):
<img width="689" alt="curl_timeboard" src="https://user-images.githubusercontent.com/10853262/47396067-3419f400-d6de-11e8-9392-7f632dc22602.png">

Link to text file for above script:
[curl_timeboard.txt](https://github.com/dmcdekker/hiring-engineers/files/2508368/curl_timeboard.txt)

This was definitely the trickiest part of the exercise! Whenever I tried to pass in the anomalies function, I got the error message, {"errors": ["Error parsing query: unable to parse anomalies(avg:postgresql.rows_fetched{*}, basic, 2): Rule 'scope_expr' didn't match at ', 2)' (line 1, column 48)."]}. Here’s a breakdown of how I troubleshot:

1.  Double checked the parameters for the [anomalies](https://docs.datadoghq.com/graphing/functions/algorithms/) function; so far as I can tell, I wrote and passed them properly.
    
2.  Used [JSONLint](https://jsonlint.com/) to make sure my JSON was properly formatted and validated.
    
3.  As a test, I set up the Anomaly function manually and peeked at the JSON, which I tried  to copy and post into my curl script (it still didn’t work because......).
  
4.  After combing through bash formatting issues, I finally realized that the quotes around the second anomalies function parameter, 'basic', needed to be escaped. Success! It worked.

Original Timeboard created with Postgres Metrics:

<img width="547" alt="timeboard_metrics" src="https://user-images.githubusercontent.com/10853262/47396372-47798f00-d6df-11e8-8acd-de3ee0a12372.png">

Just for fun and because the above graph wasn’t as visually interesting as time progressed, I input a different metric (system.cpu.user) to show off the Anomaly function more clearly. I used this curl script to create it:

<img width="624" alt="curl_second_timeboard" src="https://user-images.githubusercontent.com/10853262/47396414-7132b600-d6df-11e8-89d8-6856bf52deb2.png">

Text file:
[curl_second_timeboard.txt](https://github.com/dmcdekker/hiring-engineers/files/2508391/curl_second_timeboard.txt)

Second Timeboard created with CPU Metrics:

<img width="548" alt="cpu_metrics" src="https://user-images.githubusercontent.com/10853262/47396490-e1413c00-d6df-11e8-9bdf-d73adad9f8ae.png">

**What’s the Anomaly function doing?** Because this graph is monitoring the system CPU usage (which is the time the operating system spends running code), the Anomaly function shows when there are spikes outside of the normal range of values (represented by red peaks and troughs on the graph, where the normal range is blue).

Once this was created, I accessed the Dashboard UI and *tried* to set the Timeboard"s timeframe to the past 5 minutes. But, from the documentation, it appears that this functionality is not available for Timeboards, only Screenboards. Screenboards possess a Global Time Selector, to set the Timeframe under 60 minutes.

I then took a snapshot of the second graph I made using @ notation and sent it to myself (cool: I also got an email!).

Screenshot of @notation sent to events page:

<img width="670" alt="timeboard_from_dash_list" src="https://user-images.githubusercontent.com/10853262/47396500-eb633a80-d6df-11e8-92c3-1496d7b582a6.png">

# Monitoring Data
I created a new, simple Metric Monitor to watch the average of my custom metric and send me alerts whenever my_metric went above a warning threshold of 500, or above an alerting threshold of 800, and when there is no data for the query over the past ten minutes.

To configure the monitor’s message so that it notified me whenever any of the above conditions were breached, I configured the message using the following markdown:

<img width="623" alt="monitor_markdown" src="https://user-images.githubusercontent.com/10853262/47396601-5c0a5700-d6e0-11e8-8574-8db75f9192ca.png">

Also, when an Alert state is triggered, I added the metric value that caused the trigger and the host IP. Here’s a screenshot of the email I received:

<img width="783" alt="alert_over_800_email" src="https://user-images.githubusercontent.com/10853262/47396636-80663380-d6e0-11e8-94ed-0b0114f84f42.png">

When I click on the host IP link, it takes me to System metrics:

<img width="1109" alt="host_ip_link" src="https://user-images.githubusercontent.com/10853262/47396710-ca4f1980-d6e0-11e8-86fa-178381acc274.png">

**Neato!**  :+1:

I then set up two scheduled downtimes for this monitor:

-   One that silences it from 7pm to 9am daily on M-F
    
-   And one that silences it all day on Saturday and Sunday.
    

Email notifications for weekend and weekly mutes:

<img width="771" alt="weekend_mute_email" src="https://user-images.githubusercontent.com/10853262/47396639-83f9ba80-d6e0-11e8-8a51-33d6a962b9ac.png">

<img width="771" alt="weekly_mute_email" src="https://user-images.githubusercontent.com/10853262/47396643-878d4180-d6e0-11e8-9577-919de84b640d.png">

# Collecting APM Data
I first enabled trace collection for the Datadog Agent in datadog.yaml:

<img width="624" alt="enable_apm" src="https://user-images.githubusercontent.com/10853262/47396818-421d4400-d6e1-11e8-948c-c2f2f35ead20.png">

Given that I’m not monitoring anything very complex on my machine, I did not modify my environment and let data default to env:none. Then, I started up virtualenv, where I already had Flask installed, and created a new Flask app called datadog_.py to instrument using Datadog’s APM solution.

After installing the Datadog Tracing library ddtrace with pip, I ran the Flask app and after a few minutes, it started submitting data!:

<img width="627" alt="dash_flask" src="https://user-images.githubusercontent.com/10853262/47396937-d7203d00-d6e1-11e8-9c1e-08f0c48bb2ca.png">

**What is the difference between a Service and a Resource?** A Service is a distinct series of processes that form a service set; users can determine services when they instrument their app with Datadog. Making a query to a service is called a Resource.

[Link](https://p.datadoghq.com/sb/58ad2a67c-c1a95aa60b3d98a02603c7b8919c9efb) and screenshot of my Dashboard with both APM and Infrastructure Metrics:

<img width="887" alt="apm_and_infrastructure_dash" src="https://user-images.githubusercontent.com/10853262/47396972-f9b25600-d6e1-11e8-82e2-2c6919f2c621.png">

# Final Question
How would I use Datadog? As a chef who obsesses over cooking things perfectly, I’d love to connect a smart thermometer to Datadog, specifically to measure the internal temperature of meat while it cooks. A few minutes of under or over cooking make a huge difference; not only is knowing the internal temperature vital to avoiding foodborne illness , but it also affects the flavor and quality of the meat. Additionally, heat is lost when the door is open and closed; having a well placed thermometer that can be monitored externally would be amazing!

> Written with [StackEdit](https://stackedit.io/).