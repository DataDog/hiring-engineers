# Datadog Answers by Michael Walker 
## [Link To My Datadog Dashboard](https://app.datadoghq.com/dashboard/3sk-vkh-d4z/mikes-new-dash)


## Prerequisites and Setup- 

1) The first thing I did for this assignment was to set up the computer environment which I chose to do in Docker. For instructions on the Docker installation, here is a quick setup guide:

      [Link to video on Docker setup](https://www.youtube.com/watch?v=lNkVxDSRo7M) 

   * Note that this is an older version of Docker in the video, but the process is still similar

2) Next, I signed up for a Datadog free trial using this web link:  https://www.datadoghq.com/
In the company input box I put "Datadog Recruiting Candidate" as I am a current applicant

3) "Your Stack" is the second tab which is where to input the tech stacks that you utilize. For example, I selected PHP, MYSQL, NodeJS, and a few others and moved onto step 3 in the Agent installation instructions. 

4) Running Datadog with Docker
For this step, I used the easy one-step install and appended the `-e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true` and the `-p 8125:8125/udp` right before `-e DD_SITE="datadoghq.com` so it looked like the following:

      `docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=(API KEY WAS HERE) -e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true -e DD_SITE="datadoghq.com" -p 8125:8125/udp gcr.io/datadoghq/agent:7`

    After running the command in your terminal, you will receive a message "Your first Datadog Agent is reporting. Congrats!" and a Finish button at the bottom of the Datadog page.  Proceed by clicking Finish then you will be directed to the Datadog Home page as seen below.

    ![HomePage](https://user-images.githubusercontent.com/54221369/123457039-c1552b00-d5a0-11eb-9d16-c43c1a26749a.png)


5) From the Datadog home screen, click the integration tab and at the top of the page, you should see Docker listed at the top. Click on the Docker icon to pull up the configuration screen that should say "This integration is working properly" as seen below. 


    ![Docker Configeration](https://user-images.githubusercontent.com/54221369/123456846-8c48d880-d5a0-11eb-8e6f-ea29fb15505d.png)



## Collecting Metrics

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
To view the Agent config file. 

I will cover two ways to reach the `datadog.yaml` file 

1) Using Vim 
  
    The first step is to open the docker program and click the button to open the terminal as seen below: 

   ![Docker GUI](https://user-images.githubusercontent.com/54221369/123457750-7982d380-d5a1-11eb-8b39-c0c0fe0e646e.png)

    This will open the terminal. Enter the following to install vim:

    ```
    apt-get update
    apt-get install vim
    ```
 

   * See additional info about installing vim and `command not found`
    error here: 
    [Stackoverflow How to edit a Docker container](https://stackoverflow.com/questions/30853247/how-do-i-edit-a-file-after-i-shell-to-a-docker-container)



   After installing Vim to the Docker file, I took the following steps to find the file path:

    ![Vim path](https://user-images.githubusercontent.com/54221369/123458924-d468fa80-d5a2-11eb-8901-994506063246.png)

      * If your path differs, refer to the Agent Configuration Files at [Datadog Docs Agent Congfiguration](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7)

2) Using VS CODE

    Open VS Code from https://code.visualstudio.com/ 
    Navigate to the Settings Gear and Extensions (or ⇧⌘X). 
    In the search bar, look up "Docker" install the application.
    
    ![Docker VSCode Path](https://user-images.githubusercontent.com/54221369/123486755-e3af6e80-d5c9-11eb-82e4-cac9e08aafe6.png)

 
    Once downloaded, the Docker logo will be added to your toolbar and you can navigate to the file path in VS Code as seen below: 

    ![DockerVSPath](https://user-images.githubusercontent.com/54221369/123459571-b3ed7000-d5a3-11eb-8ca0-f30871bc10d9.png)
    
    ![Basic configuration VS](https://user-images.githubusercontent.com/54221369/123460239-9240b880-d5a4-11eb-9294-e0398dba2899.png)

  ### Tags 
   Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

   "Tags are a way of adding dimensions to Datadog telemetries so they can be filtered, aggregated, and compared in Datadog visualizations. Using Tags enables you to observe aggregate performance across a number of hosts and (optionally) narrow the set further based on specific elements. In summary, tagging is a method to observe aggregate data points." more can be found about Tags here:
    [Datadog tag documents](https://docs.datadoghq.com/getting_started/tagging/)

   I used the Yaml Format to assign my tags. More information can be found at this link:  
  [Assigning Tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments)

   My Tags were added to the `datadog.yaml` file as seen in this photo 
  
   ![AddTags](https://user-images.githubusercontent.com/54221369/123460906-96210a80-d5a5-11eb-9352-586a72f7d611.png)

   After adding tags, restart the Docker Container 

   Verify the change by visiting the Host Map which can be found by clicking on the Infrastructure tab > Host Map.
   Click on the docker-desktop hexagon and the updated Tags will show the tags as seen below: 

   ![AddedTags](https://user-images.githubusercontent.com/54221369/123460997-b4870600-d5a5-11eb-88b4-23a6464b3d09.png)


   For more information about the Host Map, I found this documention to be rather helpful:     [Datadog Hostmap Docs](https://docs.datadoghq.com/infrastructure/hostmap/)

### Installing A Database Failed Attempt, and Tags Part 2
  * During the next step, I had some issues integrating the Datadog system with Docker for PostgresSQL. I started with the  integration and install steps recommended on Datadog and Docker [PostgresSQL Intergration Docs](https://docs.datadoghq.com/integrations/postgres/?tab=host) but
  was unable to get Datadog to show the connection despite reviewing several articles. I eventually opted to switch to my Ubuntu computer and restart the process. 

  Since Ubuntu was already installed on this computer, I decided not to set up the VM and went directly to the Ubuntu Install steps with Datadog which can be viewed on this page [Ubuntu Install](https://app.datadoghq.com/account/settings#agent/ubuntu)

   To edit the yaml file, I referred to the Agent configuration files which can be viewed here: [Agent Configuration Files](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7) 

I ran the command
`gedit vi /etc/datadog-agent/datadog.yaml`

  I then added the tags to the Ubuntu yaml file as seen below:
  
  ![Tags for Ubuntu](https://user-images.githubusercontent.com/54221369/123462351-738ff100-d5a7-11eb-9819-d3f163b89c1e.png)
  
   * I noticed that when I when to the hostmap that I did not see the updates. The edits I made failed for two reasons: I forgot to switch the `logs_enabled: true` and I found that I needed to add a `sudo -h gedit vi /etc/datadog-agent/datadog.yaml` to the command. I found the solution for this issue on [Github Forms Issues](https://github.com/DataDog/datadog-agent/issues/3596) 
  
  I then looked up a comprehensive guide on how to stop and start the Datadog Agent which can be viewed here: [Datadog Agent Commands](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7)
     ![CMD for DATADOG](https://user-images.githubusercontent.com/54221369/123462081-1a27c200-d5a7-11eb-8fb9-427fb81fe9bb.png)

  After making those adjustments, I was able to get a successful and running prompt for the Ubuntu

  ![ActiveInstall](https://user-images.githubusercontent.com/54221369/123463107-590a4780-d5a8-11eb-9376-cbb9770ac4f2.png)
  
  In addtion to seeing the tags I added to the yaml file, I also was able to add tags through the Datadog portal as seen below: 
    ![Tags Via User](https://user-images.githubusercontent.com/54221369/123464182-ba7ee600-d5a9-11eb-8e5a-69e73d93cad9.png)
    
   * Here is a link to my Hostmap Tags [Hostmap](https://app.datadoghq.com/infrastructure/map?host=4943056184&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

## Adding A Database

  Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.The first step in this process was to go to the PostgresSQL site and download the version for Ubuntu which can be found at this link [PostgreSQL for Ubuntu](https://www.postgresql.org/download/linux/ubuntu/)
  
  ```
  sudo apt-get update
  sudo apt-get -y install postgresql
  ```

  After PostgresSQL was successfully installed, I went to the Datadog integration for Postgres which can be found here [Datadog Postgres Integration](https://app.datadoghq.com/account/settings#integrations/postgres)
 
  I was able to follow the steps as seen on the integration setup. In the PostgresSQL file, I did a find command for all the values mentioned in the PostgresSQL Datadog documents and either uncommented or replaced with the suggested information depending on what the document said to do 
  
  ![File Setup PostgresSQL](https://user-images.githubusercontent.com/54221369/123466573-ba341a00-d5ac-11eb-8dca-926b4a2cddf4.jpg)
  
  ![PostgresSQL Integration Datadog Docs](https://user-images.githubusercontent.com/54221369/123482668-c75c0380-d5c2-11eb-9cf7-4f9a3cfb073a.png)
  
  ![PostgresSQL Integration Yaml File](https://user-images.githubusercontent.com/54221369/123466678-da63d900-d5ac-11eb-9fe0-966c72b7b42f.png)

  ![Postgres Install Data](https://user-images.githubusercontent.com/54221369/123466997-375f8f00-d5ad-11eb-9d44-fdf94c6d205f.png)



   * I did run into an issue with the integration as seen here: 

   ![Issue with Intergration](https://user-images.githubusercontent.com/54221369/123467123-5fe78900-d5ad-11eb-87ed-91e96ebeffb1.png)

   After tracking the issue and looking up possible solutions, I found that I had to adjust how I was storing the password in the Yaml file. After addressing this error, I ran into another issue with the database not being connected. After some digging, I found when I ran `\l` that the database was listed under Postgres and not the `datadog` user. To resolve this, I changed the owner of the database by running `ALTER DATABASEmetric OWNER TO datadog` and restarted the datadog-agent. Once restarted, the system is now connected as seen below: 

![No Error](https://user-images.githubusercontent.com/54221369/123471950-c079c480-d5b3-11eb-9f92-bb63cc3408d4.png)

![No Error Shot 2](https://user-images.githubusercontent.com/54221369/123472224-21a19800-d5b4-11eb-9fa5-c5ab24043b6f.png)

Here is my [Link to Metrics](https://app.datadoghq.com/infrastructure?hostname=mikewalker1-HP-Laptop-14-cf0xxx&text=mikewalker1-HP-Laptop-14-cf0xxx)


### Creating a Custom Agent Check
  Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
  
  I reviewed the documentation on creating a custom agent check here:
[Write A Custom Agent Datadog Docs](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) and this [Video by the Solutions Team](https://www.youtube.com/watch?v=kGKc7423744)

  Stating with the video to get a better understanding, I first ran `cd etc\datadog-agent` then installed speedtest-cli with `apt-get install speedtest-cli` 
  Once complete, I ran `speedtest-cli --simple` which produced 3 metrics: Ping, Download, and Upload. The user then used this in the checks.d to get Datadog to track the upload, and download speed with custom metrics. 

  ![Ping Download Upload](https://user-images.githubusercontent.com/54221369/123468471-0aac7700-d5af-11eb-9dc5-df1174334020.png)


  After watching the video, I started building the hello.ym check and the results of that attempt can be viewed here: 

  ![Hello World Photo](https://user-images.githubusercontent.com/54221369/123472823-e94e8980-d5b4-11eb-964b-4ead374a9a63.png)
  

  With practice building the custom agent "hello world", I moved to build "my_metric" and named the file custome_my_metrics to align with my naming convention. I then built the file out as seen below: 

![View In Terminal](https://user-images.githubusercontent.com/54221369/123474131-c0c78f00-d5b6-11eb-9ba2-e53f530b44ef.png)

![View of Yaml File](https://user-images.githubusercontent.com/54221369/123474876-d9847480-d5b7-11eb-9957-1ba5283dba30.png)


When running the custom check command `datadog-agent status` I noted that my hello was running, but I was getting a character error in the custom_my_metric file. After fixing a few typos in the file I entered in `datadog-agent status` and noted the check was running smoothly. 

![Custom_my_metric running on Ubuntu](https://user-images.githubusercontent.com/54221369/123475359-86f78800-d5b8-11eb-94e6-cbf31a7f4fa6.png)

![My_Custom_Metric](https://user-images.githubusercontent.com/54221369/123475420-9d9ddf00-d5b8-11eb-925a-ebc11f37911c.png)
 

I had some issues with getting the file to check every 45 seconds once I fixed the spacing issues and restarted the datadog-agent. I also no longer noticed the custom agent. To solve this, I went into the yaml file and set it to check every 45 seconds which resolved these issues. 

Bonus Question: 
Can you change the collection interval without modifying the Python check file you created?
Yes, you can I found that if you add the following to the yaml file: 

```
init_config:

instances:
  - min_collection_interval: 45
```

![Screenshot from 2021-06-23 15-10-24](https://user-images.githubusercontent.com/54221369/123475603-df2e8a00-d5b8-11eb-9213-201a390fa374.png)

Here is the 5 minute view of my custom entry:

![5 Min View of Custom](https://user-images.githubusercontent.com/54221369/123475672-f40b1d80-d5b8-11eb-91e1-ad2eaa8845d2.png)


## Visualizing Data
  Utilize the Datadog API to create a Timeboard that contains:
  Your custom metric scoped over your host.
  Any metric from the Integration on your Database with the anomaly function applied.
  Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
  
  To get familiar with Timeboards, I watched this youtube tutorial on [Datadog Dashboards](https://www.youtube.com/watch?v=U5RmKDmGZM4)
  To learn more about the anomaly function, I visited the Datadog link [algorithms](https://docs.datadoghq.com/dashboards/functions/algorithms/)
  and this link to learn more about the [rollup functions](https://docs.datadoghq.com/dashboards/functions/rollup/)

  For the first timeboard, I was able to use the GUI to drag and drop the Timeboard into place by clicking on Dashboards => New Dashboard (name the dashboard) and select Timeboard. Then click the widget tab and open up Timeseries. 

<img width="1409" alt="Timeboard Photo" src="https://user-images.githubusercontent.com/54221369/123476271-b78bf180-d5b9-11eb-9acf-1fbb70d95246.png">

![JSON for Graph One](https://user-images.githubusercontent.com/54221369/123476533-12bde400-d5ba-11eb-81d4-0a4caf72c48e.png)

  To add a formula, open the Timeseries again and click the drop-down for formulas or open up the JSON tab and add a `"formula": "anomalies(query1, 'basic', 2)"` by the necessary anomaly information. I was also able to achieve this by clicking the plus symbol by the "avg by" box to select formals  => anomalies => basic => bounds => 2 

<img width="1280" alt="Anomalies" src="https://user-images.githubusercontent.com/54221369/123476602-2cf7c200-d5ba-11eb-8da4-10a74877fbae.png">


It is similar when setting a rollup as seen below: 

![rollup setup](https://user-images.githubusercontent.com/54221369/123476697-4a2c9080-d5ba-11eb-9e25-24b5789daf61.png)

Here is what it looks like in the JSON file: 

![JSON Rollup](https://user-images.githubusercontent.com/54221369/123476781-64ff0500-d5ba-11eb-8619-405ac496c1fe.png)
 

I noticed that when I set the tracking to 5 minutes, I lost all my data. On further inspection, I found that my internet connection was disconnected from the computer that stored the information. Once the computer was reconnected online, I found the tables to be working perfectly.

![5 Minute View of Dashboard](https://user-images.githubusercontent.com/54221369/123477017-b4453580-d5ba-11eb-832f-c161ca61eb37.png)

Here is the email I was able to send myself:

![Location of screenshot share](https://user-images.githubusercontent.com/54221369/123477628-8dd3ca00-d5bb-11eb-83a6-58e06df1ed27.png)

<img width="1144" alt="Email Sent to myself from Dashboard" src="https://user-images.githubusercontent.com/54221369/123477294-100fbe80-d5bb-11eb-8865-8fd9404e2da7.png">

I even started to play around with the clipboard event though it was not part of the assignment: 
<img width="1429" alt="clipboard" src="https://user-images.githubusercontent.com/54221369/123477781-c4114980-d5bb-11eb-8d48-b2493ef076eb.png">

### Bonus Question: What is the Anomaly graph displaying?
  An algorithm is built to detect and highlight unusual metric values with an Anomaly graph being one of those metrics. Anomalies compare expected values to observed values to highlight anomalies.

  * algorithm: Methodology used to detect anomalies

  * bounds: Relative width of the anomaly bounds
In this section system, you will see a wider band highlighting the norm for that particular dataset. By default, this appears in a gray outline with normal data appearing in purple and not normal data in red. This can be used to detect trends over time to identify any issues.   

Here is a link to my Dashboard: [My Dash](https://app.datadoghq.com/dashboard/3sk-vkh-d4z/mikes-new-dash)

## Monitoring Data
  Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
    Warning threshold of 500
    Alerting threshold of 800
    And also ensure that it will notify you if there is No Data for this query over the past 10m.
 
   The first thing I did here was look up the Metric Monitoring articles that Datadog provides. These are some of the articles I found on threshold monitoring:

   [Metric Monitor Threshold Docs](https://docs.datadoghq.com/monitors/monitor_types/metric/?tab=threshold)

   [What are recovery thresholds?](https://docs.datadoghq.com/monitors/faq/what-are-recovery-thresholds/)

   [Monitors Types](https://docs.datadoghq.com/monitors/monitor_types/)


To start, I opened the dashboard that I created and clicked on the Settings gear icon from that screen and clicked on the Create Monitor tab. 
Note: I also found that you can open up the exclamation icon and click Monitors to open up the monitor options. 

![Threshhold Settings](https://user-images.githubusercontent.com/54221369/123478473-ba3c1600-d5bc-11eb-823f-3f5d0fbae344.png)
[link to monitors](https://app.datadoghq.com/monitors/39728989)

### SEND MESSAGE 

Please configure the monitor’s message so that it will:
Send you an email whenever the monitor triggers.
Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
When this monitor sends you an email notification, take a screenshot of the email that it sends you.
When creating an email the "Use Message Template Variables" will provide all information needed to create the variables for the email. Alternatively, you can also use this webpage as a key [Notifications](https://docs.datadoghq.com/monitors/notifications/?tab=is_alert#message-template-variables). 

This is what my markdown file looks like: 

![Threshhold Email](https://user-images.githubusercontent.com/54221369/123479261-e99f5280-d5bd-11eb-88b9-451b5bebcc2d.png)

Here is the alert for going over 800: 

![Threshhold Email Alert 800 and Over](https://user-images.githubusercontent.com/54221369/123479331-00de4000-d5be-11eb-9b42-8b705a04e80c.png)

This is the email sent for no data:

![No data Threshhold Email](https://user-images.githubusercontent.com/54221369/123479387-19e6f100-d5be-11eb-9d4f-8da7125a6f67.png)

Here is the test email for 500-800: 

![Threshhold Email Alert 500-800](https://user-images.githubusercontent.com/54221369/123479529-4d298000-d5be-11eb-91dd-dc356e59dde3.png)


### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
   One that silences it from 7pm to 9am daily on M-F, and one that silences it all day on Sat-Sun. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification. To open the Downtime menu, click the "Manage Downtime" at the top of the Monitors section. Then click on the "Schedule Downtime" button. 

Here is the documentation on the [icalendar](https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html) to add custom rules
this is the downtime set during the week:

![Downtime set for weekdays](https://user-images.githubusercontent.com/54221369/123479810-b01b1700-d5be-11eb-8742-b9206b2ed022.png)

Here is the input for the weekend: 

![Weekend message](https://user-images.githubusercontent.com/54221369/123479934-da6cd480-d5be-11eb-9a48-bec900fa5354.png)


Being since it is not the weekend, I altered the times to get an away message immediately. 
Here is the clip of the email I received: 

![Awaymessage](https://user-images.githubusercontent.com/54221369/123480026-fd978400-d5be-11eb-8d3e-5f37f5c0a214.png)

<img width="1200" alt="CustomDashMonitor" src="https://user-images.githubusercontent.com/54221369/123480106-1a33bc00-d5bf-11eb-99aa-8bc112ba6bb8.png">


## Collecting APM Data:

Here are the install steps for how to get started with Flask [How to Install Flask on Ubuntu](https://linuxize.com/post/how-to-install-flask-on-ubuntu-20-04/)
Additionally, I used these links as well: 
[Quick Start Flask](https://flask.palletsprojects.com/en/0.12.x/quickstart/) and [Tracing](https://docs.datadoghq.com/tracing/)

  I noticed that I was getting errors with permissions, so I switched out of the root file to the home directory and was able to follow the steps in the install smoothly. I still had an error with OSError: [Errno 98] Address Already in use. I already had the port filled, so I attempted to run a `kill` on the port, but was unsuccessful. I then found this article that allowed me to assign a port number. Here was the rest from the hello world sample setup: [Stackoverflow Link for Error](https://stackoverflow.com/questions/41940663/why-cant-i-change-the-host-and-port-that-my-flask-app-runs-on/41940807)

![Port error photo one](https://user-images.githubusercontent.com/54221369/123480589-cecddd80-d5bf-11eb-8acf-c309d6c5fdeb.png)

![Port error photo two](https://user-images.githubusercontent.com/54221369/123480618-d8efdc00-d5bf-11eb-9aff-e02f17ccce25.png)

Running the Flask Hello World results on Localhost: 
![Screenshot of Hello World results on Localhost](https://user-images.githubusercontent.com/54221369/123481046-73501f80-d5c0-11eb-88ef-bf7926edc3c9.png)

After I finished the tutorial on the Flask Hello World, I ran the Command `pip install ddtrace` 

I also updated the Yaml file as suggested 

![YMAL File From Ubuntu](https://user-images.githubusercontent.com/54221369/123481231-adb9bc80-d5c0-11eb-8825-5ec22af9a06c.png)


* When I ran it all up with `ddtrace-run python app.py` I found that I was getting a 404 error which was confirmed in the portal. I went back and opened port 8126 in the yaml file and re-ran the operation and now see 200s across the board. 

![Working Trace](https://user-images.githubusercontent.com/54221369/123481494-0c7f3600-d5c1-11eb-8321-9c116f8e5a0e.png)

My Link to the Trace on Datadog [My Trace](https://app.datadoghq.com/apm/traces?query=&streamTraces=true&start=1624575617650&end=1624576517650&paused=false)

Bonus Question: What is the difference between a Service and a Resource?

(Resource)(https://docs.datadoghq.com/tracing/visualization/resource/)
(Service)(https://docs.datadoghq.com/tracing/visualization/service/)
(Glossary)(https://docs.datadoghq.com/tracing/visualization/)

Services are the building blocks of modern microservice architectures - broadly a that service groups together endpoints, queries, or jobs to build your application. Some examples:
  * A group of URL endpoints may be grouped together under an API service.
  * A group of DB queries that are grouped together within one database service.
  * A group of periodic jobs configured in the crond service

All services can be found in the Service List and visually represented on the Service Map. Each service has its own Service page where trace metrics like throughput, latency, and error rates can be viewed and inspected. Use these metrics to create dashboard widgets, create monitors, and see the performance of every resource such as a web endpoint or database query belonging to the service.

Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job. In a database service, these would be database queries with the span name db.query. For example the web-store service has automatically instrumented resources - web endpoints - which handle checkouts, updating_carts, add_item, etc. Each resource has its own Resource page with trace metrics scoped to the specific endpoint. Trace metrics can be used like any other Datadog metric - they are exportable to a dashboard or can be used to create monitors. The Resource page also shows the span summary widget with an aggregate view of spans for all traces, latency distribution of requests, and traces that show requests made to this endpoint.

## Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

The first thing that comes to mind would be using it to help infrastructure such as monitoring the elastic properties of a bridge and sending an alert when the elastics change. In addition, you could also use this monitoring system to help manage energy outputs. For example, if the grid needs to divert more energy to a part of town due to a spike, it can be detected and managed. I also think that this could be used to monitor sports - let's say you plug the stats for the NHL into a database then set alerts for when a player or team hit above a particular trend by using Anomaly Tracking. 

I could also use this for whitewater kayaking, a personal hobby of mine. The data for river levels if often needed when considering a run, and it could easily be adapted to check the river levels and give kayakers the much-needed warning about flash floods or low river conditions. 

## Additional links 

[Metric Basics](https://docs.datadoghq.com/metrics/)

[Tag Video](https://www.youtube.com/watch?v=7mCxL1goRDI)

[Docker Integration](https://www.youtube.com/watch?v=VHaTdWs-gFA)

[Docker Datadog files](https://hub.docker.com/r/datadog/docker-dd-agent/)

[Nuke option](https://docs.datadoghq.com/agent/faq/how-do-i-uninstall-the-agent/?tab=agentv6v7)

[VM Setup](https://www.vagrantup.com/downloads)

[Agent Configuration Files
](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7)
