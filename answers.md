# Application as 'Senior Sales Engineer' at Datadog

Who is 'The Logfather'

This nickname was given to me by former colleagues at Splunk. Although my focus goes far beyond simple log files, I still carry this name with a certain pride.

I am now 54 years old and have been working for almost 20 years as presales in various companies, but ALWAYS for start-up companies.
Where, if not in such young, agile and open companies, does the own acting and thinking have so much positive influence on the prosperity, the growth and the coming events of ingenious ideas, products and companies.

Before I started in the IT industry, I worked as a roofer, plumber, steel constructor and a lot more.
I also worked as a full-time paramedic for almost ten years.
I gained a foothold in IT about twenty years ago after training as a Java programmer.
However, I am not the code nerd who loves to sit between undefinable amounts of cold pizza boxes and let his genius run free to create incredibly good lines of code.
I'm rather the type of nerd who loves to successfully bring the ingenious ideas of others to the table. For me there is nothing more pleasing than to see how a great idea first becomes a convincing product, and in the next step a brilliant business idea becomes a successful company for everyone involved.

My personal thanks go to _**Lee Farrar**_ and Datadog for their interest in me and for giving me the opportunity to apply as a Senior Sales Engineer.

# Following now all my answers. 


## Starting with Datadog - Setup the environment

### Step 1: Download

First things first I created a new user account on https://www.datadoghq.com/.

![datadog_account.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_account.png)

From there on I decided to download and run a standalone agent on my macos system, instead of using a VM or Docker approach.   

![datadog_install_1.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_1.png)   

Instead of downloading and running a DMG file on MAC you can simply download and start the installation of the agent buy the use of a simple command line in your terminal:

DD_API_KEY=719d714d7132af72ce6e1f2d8b67b618 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"  

### Step 2: Install

I ran the DMG package and updated the datadog.yaml file with the API key provided on the download page of Datadog!
datadog.yaml config file refers to the path: /opt/datadog-agent/etc/  

![datadog_install_3.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_3.png)

After installing the Datadog agent you can always check the actual status by running following command:

`datadog-agent status`

After successfully installing your agent you will see a message within the Datadog webpage!

![datadog_install_4.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_4.png)

### Step 3: See the results

And from now on you will be able to see first results in the Datadog App!

![datadog_install_5.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_5.png)

## Tagging

Tags are key to Datadog because they allow you to aggregate metrics across your infrastructure at any level you choose while they decouple collection and reporting. Tags can be used to dynamically add additional dimensions to monitoring and analysis. The more unknown levels, areas and entities there are in a monitored environment, the more unmanageable a naming scheme becomes.

Hostnames i.e. can be automatically or manually tagged.  

![datadog_tagging_2.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_tagging_2.png)

Tagging different assets helps you to sort which hosts are located in a specific federal state.  

![datadog_tagging_3.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_tagging_3.png)  

### Create a new tag  
Tagging is made very easy within Datadog by the ability to create new tags or assign tags to different assets.  

![datadogs_tagging_4](https://github.com/simuvid/hiring-engineers/blob/master/images/datadogs_tagging_4.png)

Or you use the only true approach for seasoned men within the datadog.yaml file.  

Don't forget to save the file and restart the agent after the changes have been made.  

![datadog_tags_config](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_tags_config.png)

From now on you can start to group, search and filter by tags.

![hosts](https://github.com/simuvid/hiring-engineers/blob/master/images/hosts.png)

## Integrations

Datadog offers out of the box more than 200 integrations in every imaginable environment:
  
- AWS
- Azure
- Google
- Cloud
- OS & Systems
- Databases
and way more....
  
As an example for an integration I decided to build one for my PostgreSQL DB.

### Step 1: Create a user  

Thankfully we have already deployed an agent on my system that already runs a PostgreSQL DB.

So at next we have to define a new Datadog user within PostgreSQL, like shown on the left, to grant appropriate access for the agent to PSQL.

![create an user in PSQL](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_postgre_user.png)

### Step 2: Configure the Datadog agent   

In the postgres.d/conf.yaml file in the conf.d directory a few adjustments have to be made. Then restart the agent.

![config PSQL](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_postgre_conf.png)  

### Step 3: Watch the new host
The SQL DB Server now appears as a new host in our Datadog environment.

![PSQL Integration](https://github.com/simuvid/hiring-engineers/blob/master/images/postgre_host.png)  
  
  
## Custom agents
### Chicken or Egg?  

Integration vs. Agent Check

Agent checks are a great way to collect metrics from custom applications or unique systems. However, if you are trying to collect metrics from a generally available application, public service or open source project, we recommend that you write an Integration.
  
### Step 1: Create your files
<Your_Project>.py within opt⁩ ▸ ⁨datadog-agent⁩ ▸ ⁨etc⁩ ▸ ⁨checks.d⁩
<Your_Project>.yaml within opt⁩ ▸ ⁨datadog-agent⁩ ▸ ⁨etc⁩ ▸ ⁨conf.d⁩ ▸ ⁨<your_project>.d⁩  

For my example I decided to create an Agent check which simulates a CPU usage metric, means a random value between 1 and 99 percent usage.  
  
![Agent Python](https://github.com/simuvid/hiring-engineers/blob/master/images/logfather.py.png)  
    
Each check has a YAML configuration file that is placed in the conf.d directory. The file name should match the name of the check module (e.g.: logfather.py and logfather.yaml).  
    
![Agent Config](https://github.com/simuvid/hiring-engineers/blob/master/images/logfather.yaml.png)  

### Step 2: Deploy and test the files  

After copying the files into the appropriate directories like shown earlier, we can test our Agent checks before using them by running following command:  

`Logfather$ datadog-agent check logfather` 

![Agent Check](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_AgentChech_Test.png)

### Step 3: Run the Agent check  

After successfully testing the check we can restart the Agent and after a few moments we see in the Datadog App our new metric!

![CPU Metric](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_logfather_cpu_metric.png)  

Admittedly that wasn't the big challenge now, but it demonstrates how easy it is to get started with Datadog. Our self-generated agent check now creates and sends a CPU metric continuously. In order not to overload our resources in a real production case, the agent should only send the metric every 45 seconds. This again only requires a small intervention in our configuration file.  

![Collection Intervall](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_collection_intervall.png) 

## Bonus question:..

_Can you change the collection interval without modifying the Python check file you created?_  

To be honest, this question seems a bit confusing to me, as we have already shown that the collection interval is defined in the yaml configuration file.

But this answer only concerns the people who asked this question and I am always open for discussions!

## Visualizing Data  

Lets start with the visualization of our newly captured data within a new timeboard  

### Step 1: Create a timeboard  

For my example I wrote a Python script that describes a simplified timeboard.  

![Coonfig timeboard](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_timeboard_step1.png)  

### Step 2: Review the Timeboard  

After executing the python script the new Timeboard appears immediately within my Datadog App.  

![New timeboard](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_new_timeboard_1.png)  

### Step 3: Add more graphs and functions  

As the next step in evoluting my Timeboard I integrated an anomalie detection on the number of open Connections to my PostgreSQL DB

![Extended timeboard](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_timeboard_step2.png)  

### Step 3 a: Anomaly detection for CPU usage  

As a further step in evoluting my timeboard and make it more meaningful I added some anomaly detection.  

![Anomaly timeboard](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_cpu_anomalies.png)
  
  
### Step 3 b: Rollup..

Maybe it doesn't make perfect sense, but in the next step I added the sum of the CPU values to my CPU graph as another line using the rollup function.  

![Anomaly timeboard](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_rollup_function.png)  

#### Let's go back....  
#### ....way back....  
#### ....back into times!  

You will already have noticed that the user is of course able to view the individual graphs time-dependently, i.e. to define the display and analysis period.

To do so, predefined values are available in the dropdown list. Or you simply use the possibility to determine certain time periods within the graphs by dragging with the mouse.

![Dive into timeframe](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_choose_timeframe.png)  
![5 minute timeboard](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_past_5_minutes_timeboard.png)  

## Notations  

Imagine you are looking at something unusual in your monitoring and want to share this information immediately with others?

![Notation](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_notation.png)  
  
This is another outstanding feature, the possibility to forward comments and hints from current observations on the fly directly to affected colleagues, employees or customers. Datadog offers the possibility to send information directly from a graph.

### What's our anomaly graph displaying?  

In the previously seen anomaly graph we look at a time-based line of the average values of our CPU utilization on the one hand and on the other hand at a gray area that defines the min and max utilization at the same time, i.e. the area in which the CPU utilization moves in the past in a range learned as normal. As red markers the events and/or values are highlighted which are outside a range anticipated as normal.

### Why anomaly detection?  

People say "to err is human", but even machines sometimes make mistakes! In every production, controls must be carried out to detect deviations or errors early on.

For example, a carpenter will check his newly manufactured chair for grinding errors, while a manufacturer of electric cables will check whether they conduct electricity well. Both are looking for possible anomalies.

Anomaly detection is based on algorithmic models with which it can be determined when a key figure behaves differently than in the past. The key figures to be monitored are influenced by various factors, such as seasonal trends, on certain days of the week or at special times of the day. Anomaly detection is particularly effective when static alarm limits fail.

Automated anomaly detection in a dataset is a complex task involving areas such as machine learning, statistics, and data mining. The nature of the data, the information available, the nature of the anomaly and the expected result determine the choice of algorithm to be used.

Anomaly detection is defined as searching for unknown structures in a dataset that do not behave as expected.  
  
  
## Monitoring data  
  
It's time to define custom monitors to automatically monitor values and react quickly if violations of the defined limits occur during monitoring.  
  
### Step 1: Create a new Metric Monitor  

Use the UI for that task.

`https://app.datadoghq.com/monitors#create/metric` 
  
![Metric Monitor](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_create_metric_1.png)  

### Step 2: Define thresholds  

For my CPU usage I want to set thresholds for:

- Warning: If CPU usage exceeds 75%  
- Alert: If CPU usage exceeds 90%  

Additional I want to get an immediate notification if CPU data is missing for longer then past 10 minutes  
  
![Metric Monitor](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_create_metric_2.png)  
  
### Step 3: Configure the monitor’s message  

![Monitor Notification](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_monitor_notification_1.png)  

The monitor reacts as expected and from now on immediately sends email notifications about the event as desired.  

![Monitor Alert Notification](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_monitor_alert_message.png)  

Note that you can schedule downtime for your monitoring and notifications. After all, you should be able to spend your free time in peace!  

![Schedule downtime Notification](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_schedule_downtime_per_night.png)  

Maybe you just want the monitor to be silent on weekends?  

![Schedule downtime Notification](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_schedule_downtime_per_weekend.png)  

Of course you will get notified about any changes on your schedules.  

![Schedule downtime Notification](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_schedule_downtime_notification_1.png)  

## Instrumenting an application  

To illustrate the simplicity of application instrumentation, I use a relatively simple Flask web server.

What you need to do to automatically instrument the app is to add some parameters to the start of your app:

`FLASK_APP=datadog_flask.py DATADOG_ENV=flask_test ddtrace-run flask run --port=4999`

Note: I have changed the default flask port from `5000` to `4999`, as my Datadog Agent is already using Port `5000`.  

![Schedule downtime Notification](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_code_flask_sample_app.png)  

It is as easy as that!

Immediately you will see first metrics coming in!  

![Schedule downtime Notification](https://github.com/simuvid/hiring-engineers/blob/master/images/instrumented_metrics.png)  

## A final bonus question!  
  
  
### What is the difference between a Service and a Resource?  

In the past I was EMT for about ten years. From a paramedic's point of view, the answer to the bonus question is very simple:

* **Service**: Individual skills, knowledge and personal experience determine the ability of an EMT to sustain or save a person's life.  

* **Resources**: These are the technical tools available to an EMT. It makes an enormous difference whether the paramedic goes to the scene of action with an ambulance or even with a helicopter. In this case, the resource determines the time to arrival or the speed of transport to a necessary clinic.  

The difference between service and resource within Datadog can also be described clearly and simply:  

* **Service**: A service consists of a collection of different processes that are directly related to each other. Like the paramedic, a service uses different capabilities to perform a specific task. So different web applications, servers and databases can be combined to one service.  

* **Resource**: Unlike the EMT example, within Datadog a resource is not hardware, like the ambulance, but rather something like an action that is necessary to perform a service. For a web application, for example, this would be the canonical URL. Or in a connected SQL database: a certain query, like SQL statements ( SELECT * )  
  
  
## _**CONCLUSION**_: 

Datadog is different! The Logfather is different.

If I say I am different then this means I bring a lot of valuable experience with me. My skills are not limited to the classic tasks of a presales engineer. I have already proven that, to a certain extent, technical product marketing is additional one of my strengths. In the past I have worked closely with PR and marketing agencies, created my own presentations and published technical articles in various trade magazines. I would also like to bring this knowledge to my new environment.

I hope that the technical answers to this online assessment are technically correct and detailed enough to convince Datadog of me.

I look forward to a fruitful and valuable collaboration with all colleagues and divisions within Datadog.
