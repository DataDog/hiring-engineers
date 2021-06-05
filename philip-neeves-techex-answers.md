**Prerequisites - Setup the environment**

I decided to go with the recommendation of setting up a Vagrant Ubuntu VM via VirtualBox.  It was quick to set up and I was able to easily SSH into it via Powershell.

![image](https://user-images.githubusercontent.com/22836380/120678648-3ba5fa00-c490-11eb-82b9-36f3ae4d21d9.png)

I registered for the free Datadog trial and initially installed the Agent for my local Windows machine as a test and launched the Agent Manager on localhost:

![image](https://user-images.githubusercontent.com/22836380/120678794-66904e00-c490-11eb-8d2c-1b78db489a6a.png)

I then installed the Agent on my Vagrant Host and from hereon I focused only on this Host.

Got it running, checked the Agent status, and everything seemed to be working as expected:

![image](https://user-images.githubusercontent.com/22836380/120679015-9b040a00-c490-11eb-9d09-2856d0ddb0aa.png)

**Collecting Metrics:**

•	Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog

I added additional Host Tags in the datadog.yaml file and decided to go with Unified Service Tagging ‘service’, ‘env’ and ‘version’ tags as per the Datadog suggestions, to form a single point of configuration for all telemetry emitted.

Host Map showing additional Host tags:

![image](https://user-images.githubusercontent.com/22836380/120679157-c5ee5e00-c490-11eb-9e6b-a722b3f608be.png)

Link to my Host Map:

https://app.datadoghq.eu/infrastructure/map?host=78171197&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host 

•	Install a database on your machine (MongoDB, MySQL, or PostgreSQL):

I decided to install MongoDB onto my vagrant Ubuntu Host
Start MongoDB and confirm it's working:

![image](https://user-images.githubusercontent.com/22836380/120679485-22ea1400-c491-11eb-95ff-85c3ba5d36ea.png)

Launched the Mongo shell and set up a myNewDB database and inserted 2 small ‘Collections’:

![image](https://user-images.githubusercontent.com/22836380/120679647-50cf5880-c491-11eb-987f-e56708420cff.png)

Integrate MongoDB:

Set up Admin user and Datadog as a User:

![image](https://user-images.githubusercontent.com/22836380/120680540-55484100-c492-11eb-98ed-29d25e38cdef.png)

Enabled Log Collection in the datadog.yaml file:

![image](https://user-images.githubusercontent.com/22836380/120683991-2338de00-c496-11eb-9af4-50acca70fe46.png)

Add config block for logs conf.yaml:

![image](https://user-images.githubusercontent.com/22836380/120684111-3d72bc00-c496-11eb-8d6e-2efef85de559.png)

MongoDB integration installed and ‘working properly’:

![image](https://user-images.githubusercontent.com/22836380/120684207-54b1a980-c496-11eb-82f6-7fcd7bed191f.png)

However, MongoDB errors showing on metrics tab on UI:

![image](https://user-images.githubusercontent.com/22836380/120684289-6dba5a80-c496-11eb-95d9-bf4f5aef2fd1.png)

Also 'permission denied' to mongod.log errors showing following 'mongo' check in terminal.  So ran a 'mongo service' check and everything seemed fine:

![image](https://user-images.githubusercontent.com/22836380/120684616-d1dd1e80-c496-11eb-89d0-0b32278510b7.png)

So ran a full Agent check and there is an error reported under the 'Collector' section:

![image](https://user-images.githubusercontent.com/22836380/120684739-f6d19180-c496-11eb-91bf-3ac8c2647029.png)

Issue seems to be the host:27017 connection refused.

Checked mongod.conf file and bindIp is 127.0.0.1

[image](https://user-images.githubusercontent.com/22836380/120883948-2cca5f00-c5d8-11eb-88e6-012a755640a8.png)

Updated conf.yaml host from ‘vagrant’ to 127.0.01 (my mistake originally)

This seemed to resolve the issue:

![image](https://user-images.githubusercontent.com/22836380/120684963-38fad300-c497-11eb-821e-dbffa6751a80.png)

Also shows up on the UI now as 'OK':

![image](https://user-images.githubusercontent.com/22836380/120685034-50d25700-c497-11eb-84a2-f0121d78f9de.png)

But...still getting errors on the Host Map Metrics for MongoDB:

![image](https://user-images.githubusercontent.com/22836380/120685166-73fd0680-c497-11eb-973f-910ca05e10ca.png)

Plus, still getting permission denied errors on mongod.log...

![image](https://user-images.githubusercontent.com/22836380/120884012-787d0880-c5d8-11eb-94b8-c9b7ff3034b7.png)

Did some research and changed the permissions on the file and directory from mongodb to dd-agent which did seem to work:

![image](https://user-images.githubusercontent.com/22836380/120685312-9f7ff100-c497-11eb-92b1-119c4ffb5ef2.png)

This resolved errors on the UI also:

![image](https://user-images.githubusercontent.com/22836380/120685399-b292c100-c497-11eb-9fe5-6e226d05ebc3.png)

The Dashboard looking good:

![image](https://user-images.githubusercontent.com/22836380/120685468-c3433700-c497-11eb-8b36-dcc9d43c4d88.png)

**Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000**

First of all, I set up a test custom ‘hello world’ metric taken from Datadog guide - tested it and it worked.

![image](https://user-images.githubusercontent.com/22836380/120884044-a2cec600-c5d8-11eb-88b0-de08460dfcbf.png)

**Set up custom_my_check metric:**

Created the yaml file under conf.d:

![image](https://user-images.githubusercontent.com/22836380/120685645-f5ed2f80-c497-11eb-9c13-82329d6de253.png)

Created custom_my_check.py file, which modified the hello test metric python code to include the use of random for the generation of a random integer between 1 – 1000 and also time.sleep for 45 seconds, so the collection interval is set to every 45 seconds:

![image](https://user-images.githubusercontent.com/22836380/120685703-09989600-c498-11eb-994a-d9e2aefd588d.png)

Check the check – seems to be working – integer = 627

Tried again and integer = 60

Tested the check and timed execution against a stopwatch and was bang on 45 seconds.

Restarted the Service

Appears on the host map and dashboard as expected, however, collection rate is still the default 15 seconds.  This implies delaying the code execution does not change the collection rate:

![image](https://user-images.githubusercontent.com/22836380/120685757-1e752980-c498-11eb-9e2a-849e32049143.png)

Link to my_check custom metric display:

https://app.datadoghq.eu/dash/integration/custom%3Amy_check?from_ts=1622728920682&live=true&to_ts=1622732520682&tpl_var_scope=host%3Avagrant

So, after consulting the Datadog docs I removed the time delay from the python code:

<code>import random</code>

<code>try:</code>

    from datadog_checks.base import AgentCheck
    
<code>except ImportError:</code>

    from checks import AgentCheck
    
<code>__version__ = "1.0.0"</code>

<code>class my_check(AgentCheck):</code>

    def check(self, instance):
    
        while(True):
        
        time.sleep(45)
        
        self.gauge(
        
            'my_check.gauge',
            
            random.randint(0, 1000),
            
            tags=['TAG_KEY:TAG_VALUE'] + self.instance.get('tags', []))
            
and added the min_collection_interval to the custom_my_check.yaml file:

![image](https://user-images.githubusercontent.com/22836380/120685976-6431f200-c498-11eb-9c48-57b35b061ad3.png)

Tested it and all good so restarted the service to include it again and report data to DD.  

You can see the intervals widen to the right side of the graph below after this was implemented:

![image](https://user-images.githubusercontent.com/22836380/120686468-e5898480-c498-11eb-80a0-f45e1e5ebb34.png)

**Bonus Question Can you change the collection interval without modifying the Python check file you created?**

Add the min_collection_interval in the .yaml file.  This in fact is what I did originally before I put the time delay in the python code.

**Visualising Data:**

Utilize the Datadog API to create a Timeboard that contains:

•	Your custom metric scoped over your host.
•	Any metric from the Integration on your Database with the anomaly function applied.
•	Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Screenshot below showing my Timeboard (Phil's Timeboard API Test Creation 2) displaying 3 graphs:

1. My custom metric scoped over my Host showing the generated random integers between 0 - 1000.
2. A MongoDB Collection Locks per second with an Anomaly detection overlay to identify any movement out of the expected variation
3. A simple rollup display of the average my_check integer per Hour

created using a script to POST to the Datadog API using Postman (see attached script ‘phils_timeboard_api_script.json’):

![image](https://user-images.githubusercontent.com/22836380/120686556-018d2600-c499-11eb-8a90-9f3a001b7eb8.png)

And as it appears on the Dashboard:

![image](https://user-images.githubusercontent.com/22836380/120686611-15388c80-c499-11eb-9b1c-770f862181dc.png)

Link to my custom Timeboard:

https://app.datadoghq.eu/dashboard/xd8-es7-597/phils-timeboard-api-test-creation-2?from_ts=1622729300712&live=true&to_ts=1622732900712

Once this is created, access the Dashboard from your Dashboard List in the UI:

**Set the Timeboard's timeframe to the past 5 minutes**

**Take a snapshot of this graph and use the @ notation to send it to yourself.**

![image](https://user-images.githubusercontent.com/22836380/120686758-3dc08680-c499-11eb-980f-d26952b99663.png)

![image](https://user-images.githubusercontent.com/22836380/120686810-49ac4880-c499-11eb-9d13-64050f3beccc.png)

**Bonus Question: What is the Anomaly graph displaying?**

There are 2 main features to the anomaly graph:

1. **The Anamolous Grey Band** 

The overlying grey band shows the scope of the expected variation in the data.  Any variation of the line above or below the grey band could indicate an issue with with this particular part of the system.

3. **The Graph**

This particular graph is showing the Intent Shared Collection locks, it was chosen for demonstration purposes of anomaly detection, as it provides some consistent variation of data for a database that is not in constant use.

What are Intent Share Collection locks?

Locking is a mechanism used to maintain concurrency in the databases. MongoDB uses multi-granularity locking in different levels and modes of locking to achieve this.

There are four different levels of locking in MongoDB: Global, Database, Collection, Document

Intent Shared?

•	Intent locks are higher level locks acquired before lower level locks. 
•	It indicates that the lock holder will read the resource at a granular level.
•	If an Intent Shared lock is applied to a database, then it means that lock holder is willing to apply a Shared lock on Collection or Document level.

**Monitoring Data**

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

•	Warning threshold of 500
•	Alerting threshold of 800
•	And also ensure that it will notify you if there is No Data for this query over the past 10m.

**Please configure the monitor’s message so that it will:**

1.	Send you an email whenever the monitor triggers.
2.	Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
3.	Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
4.	When this monitor sends you an email notification, take a screenshot of the email that it sends you.

**Alert email received:**

![image](https://user-images.githubusercontent.com/22836380/120686994-7ceed780-c499-11eb-812e-756deaf81c1b.png)

**Warning:**

![image](https://user-images.githubusercontent.com/22836380/120687076-9001a780-c499-11eb-9cfe-448cb68d1010.png)

**No Data:**

![image](https://user-images.githubusercontent.com/22836380/120687161-a60f6800-c499-11eb-8235-ae91bdc86bdd.png)

**
[phils_timeboard_API_script.txt](https://github.com/Philneeves/hiring-engineers/files/6593469/phils_timeboard_API_script.txt)
[phils_timeboard_API_script.txt](https://github.com/Philneeves/hiring-engineers/files/6593470/phils_timeboard_API_script.txt)
Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:**

One that silences it from 7pm to 9am daily on M-F:

(Shows UTC in the email but as per screenshot below, setting is for BST in Datadog)

![image](https://user-images.githubusercontent.com/22836380/120687255-bde6ec00-c499-11eb-87d2-1b713478bdf6.png)

And one that silences it all day on Sat-Sun.

(Again email below shows UTC but system is showing Europe/London or BST.  Tried to set to Europe/Dublin but saved as IST (Indian Summer Time) for some reason)

![image](https://user-images.githubusercontent.com/22836380/120687326-d0612580-c499-11eb-8229-191a92273150.png)

Collecting APM Data:

The plan here was to demonstrate the ability to monitor the level of a product's performance and to diagnose errors of an instrumented application. 

Installed Flask in a virtual env, saved the provided App code as app.py, installed ddtrace and had to update PIP as didn't work at first.
Seemed to work when launched it:

![image](https://user-images.githubusercontent.com/22836380/120687620-1322fd80-c49a-11eb-98d8-1af45cab7818.png)

However quit this as needed to add Tag Configs
Entered in tag configs:

![image](https://user-images.githubusercontent.com/22836380/120687688-23d37380-c49a-11eb-9718-092a5c978d85.png)

Restart the service
Launched app again with full tag configs:

DD_SERVICE="ubuntu_host" DD_ENV="sandbox" DD_LOGS_INJECTION=true ddtrace=run flask run --port 5050

Opened up a second terminal connection and called the URL, response is as expected ‘Entrypoint to the Application’:

![image](https://user-images.githubusercontent.com/22836380/120687896-62692e00-c49a-11eb-9e32-39aaff2c10fd.png)

Stream of data giving informative messages about the execution of the application at run time can be seen in the other terminal:

![image](https://user-images.githubusercontent.com/22836380/120687944-70b74a00-c49a-11eb-9c8f-2fd31ca7dff1.png)

Called api/apm:

![image](https://user-images.githubusercontent.com/22836380/120688020-875da100-c49a-11eb-8280-616718463a69.png)

Again a stream of trace data can be seen:

![image](https://user-images.githubusercontent.com/22836380/120688095-9d6b6180-c49a-11eb-80e5-5851b235c21f.png)

Called the /api/trace as well:

![image](https://user-images.githubusercontent.com/22836380/120688216-be33b700-c49a-11eb-833e-7458ccc28aa3.png)

Services results can be viewed in the APM Datadog UI APM section:

![image](https://user-images.githubusercontent.com/22836380/120688281-ce4b9680-c49a-11eb-8695-66527d0cbf79.png)

Expand Services for ubuntu_host:

![image](https://user-images.githubusercontent.com/22836380/120688350-e02d3980-c49a-11eb-9456-07f4417e44e0.png)

![image](https://user-images.githubusercontent.com/22836380/120688402-ee7b5580-c49a-11eb-9c88-aa9faa1e46bc.png)

Link to APM Services:

https://app.datadoghq.eu/apm/service/ubuntu_host/flask.request?start=1622731004820&end=1622734604820&paused=false&env=sandbox

Results in the Traces section of the APM:

![image](https://user-images.githubusercontent.com/22836380/120688506-0c48ba80-c49b-11eb-8817-5c03c62bffad.png)

Link to APM Traces:

https://app.datadoghq.eu/apm/traces?end=1622734669861&paused=false&query=service%3Aubuntu_host%20env%3Asandbox%20operation_name%3Aflask.request&start=1622733769861&streamTraces=true

Phil's Infrastructure and APM Dashboard:

![image](https://user-images.githubusercontent.com/22836380/120688962-7feac780-c49b-11eb-8801-416941d519e0.png)

Link to Infrastructure and APM Dashboard:

https://app.datadoghq.eu/dashboard/mph-cb4-tum?from_ts=1622731610456&live=true&to_ts=1622735210456

**Bonus Question: What is the difference between a Service and a Resource?**

Services are the building blocks of microservice architectures.  A service groups together endpoints, queries, or jobs for the purposes of building your application
Resources represent a particular domain of a customer application.  They are typically an instrumented web endpoint, database query or background job.

**Final Question:**

Is there anything creative you would use Datadog for?

If I did own a Casino I think it would be useful to be able to monitor all of the various machines through a 'single pane of glass'.  It could tell you a if a machine is paying out too much or too little.  Does that correlate with the machine’s performance?  You could get good analytics on the use of machines: which ones are used more than others.  If so, why? Is it the location of the machine, the look, the feel, the programming?  Are certain machines more popular at certain times of the day? It would give you a good understanding then of their profitability.  You could look for anomalies in performance that might highlight an unknown hack on the machines for cheating.  You could also get real time feedback on the cashflow of individual machines through to groups of machines through to the entire Casino.
