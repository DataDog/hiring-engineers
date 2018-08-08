# Level 1: Setup the environment

1. *Setting up Ubuntu Virtual Box via Vagrant:*
First I have downloaded and installed Virtual Box and Vagrant as per the instructions in the link  <https://www.vagrantup.com/intro/getting-started/>
2. *I downloaded the virtual box as per my OS from the link* <https://www.virtualbox.org/wiki/Downloads>

![image](https://user-images.githubusercontent.com/41904992/43808052-87bcd46e-9aee-11e8-8c33-8979aaaf2636.png)

3. *Once the setup is downloaded and installed, I setup Vagrant as per the instructions in* <https://www.vagrantup.com/downloads.html>

![image](https://user-images.githubusercontent.com/41904992/43808107-b7de1f4a-9aee-11e8-8e9b-cc6b445a0bb1.png)

4. *Open Command Prompt and run the commands as per the link* <https://app.vagrantup.com/ubuntu/boxes/xenial64>

![image](https://user-images.githubusercontent.com/41904992/43808149-e92f542e-9aee-11e8-84dd-a529b9b89e2b.png)

5. *Install the DataDog agent on the Ubuntu machine as per link* <https://docs.datadoghq.com/agent/>

Sign up with the required details for a free trial

![image](https://user-images.githubusercontent.com/41904992/43809637-b4233afe-9af6-11e8-92a9-31c62bcbaab7.png)

Install the downloaded DataDog Agent as per OS, in my case, it is Ubuntu that I have created on Virtual Box:

![image](https://user-images.githubusercontent.com/41904992/43808171-1f54a932-9aef-11e8-9d29-5ddf984508bf.png)
Then SSH the Ubuntu machine from the command prompt and run the commands mentioned below.

![image](https://user-images.githubusercontent.com/41904992/43808189-384af004-9aef-11e8-98c9-9abafddb0a5f.png)

Install the DataDog agent on the Ubuntu machine mention on the link <https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/>

![image](https://user-images.githubusercontent.com/41904992/43808273-aa431e02-9aef-11e8-9ff6-9770546e1f46.png)

Run the following command to access the API Key: “sudo nano /etc/DataDog-agent/DataDog.yaml”

![image](https://user-images.githubusercontent.com/41904992/43809668-ebbb5cda-9af6-11e8-9f2f-aa5754f4dbf5.png)

![image](https://user-images.githubusercontent.com/41904992/43808295-bee352c8-9aef-11e8-928b-2d4723159adc.png)

Once the agent is installed, it starts reporting to the DataDog Console.

![image](https://user-images.githubusercontent.com/41904992/43808307-caf6e034-9aef-11e8-877b-01442cf77e9b.png)

![image](https://user-images.githubusercontent.com/41904992/43808314-d071b43a-9aef-11e8-837a-9a8347f91d50.png)

# Level 2: Collecting Metrics
1. *Add tags in the agent conf.d file. *
Add tags on the root location by following the instructions in the <https://docs.datadoghq.com/getting_started/tagging/assigning_tags/>

![image](https://user-images.githubusercontent.com/41904992/43808411-49eab26c-9af0-11e8-9703-54c9d13fc501.png)

![image](https://user-images.githubusercontent.com/41904992/43808416-50252ebe-9af0-11e8-96a2-16a7cfeb5f53.png)

Now I have assigned tags of my choice i.e. “Server” and “ENV:PROD".

![image](https://user-images.githubusercontent.com/41904992/43808444-6795e4d0-9af0-11e8-9c20-ad716563ae05.png)

Now restart the agent by running the following command: “sudo systemctl  restart DataDog-agent.service”
Tags on the host page of DataDog will come up after some time.

![image](https://user-images.githubusercontent.com/41904992/43808464-7d93b12c-9af0-11e8-9fc1-a1e6d3de8a96.png)

2. *Install MYSQL or any other Database of your choice*
Installed MySQL database on my Ubuntu machine by following the below link <https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04>

![image](https://user-images.githubusercontent.com/41904992/43808500-b0fe79fc-9af0-11e8-9132-c7a496570de6.png)

It requires a root password, once you provide the root password, My SQL starts installing.

![image](https://user-images.githubusercontent.com/41904992/43808510-bc866e06-9af0-11e8-89b2-f8067bb94de7.png)

![image](https://user-images.githubusercontent.com/41904992/43808517-c4340078-9af0-11e8-9aa1-47dcbc3c3d2d.png)

Installation completed.

3. *Now I have done the installation of the respective DataDog integration for the MySQL database.*
Go to DataDog dashboard homepage>>Integration>>Select the MySQL database integration option: 

![image](https://user-images.githubusercontent.com/41904992/43808548-e6cc0158-9af0-11e8-9987-3b804428d1a3.png)

 Follow the instructions given in the link <https://app.datadoghq.com/account/settings#integrations/mysql>
 
![image](https://user-images.githubusercontent.com/41904992/43808570-01905598-9af1-11e8-9a92-b3b06a61f625.png)

Once the password is generated, we can use this password for further configuration.

![image](https://user-images.githubusercontent.com/41904992/43808597-1cace88c-9af1-11e8-826e-def3bca6f5c7.png)

Configure the DataDog agent by making changes in the conf.d file to connect to MySQL database:

![image](https://user-images.githubusercontent.com/41904992/43808614-281ec924-9af1-11e8-9571-1765eef80450.png)

Restart the agent by following below command:“sudo systemctl  restart DataDog-agent.service”

![image](https://user-images.githubusercontent.com/41904992/43808624-32b25464-9af1-11e8-9e3f-91536f87516b.png)

The following snapshot depicts the dashboard showing the integration is working:

![image](https://user-images.githubusercontent.com/41904992/43808629-3b4a52e8-9af1-11e8-8bcb-cbed1f898cd8.png)

4. *Create a custom Agent check that submits a metric named “my_metric” as per link* <https://docs.datadoghq.com/developers/agent_checks/> 

![image](https://user-images.githubusercontent.com/41904992/43808661-60767cfe-9af1-11e8-9934-fb28b366c478.png)

![image](https://user-images.githubusercontent.com/41904992/43808664-6456b94c-9af1-11e8-93ca-63497a8fb195.png)

![image](https://user-images.githubusercontent.com/41904992/43808667-681be4a8-9af1-11e8-892c-2042935acc74.png)

Restart the agent: “sudo systemctl  restart DataDog-agent.service”
To check the current status of the agent use following command: “sudo DataDog-agent status".
![image](https://user-images.githubusercontent.com/41904992/43808687-8219c1ea-9af1-11e8-9d27-818f74741eb0.png)

5. *Changing Agent Check Interval*
I have changed the agent interval to submit the metrics to 45 seconds as per instructions on the link
<https://docs.datadoghq.com/developers/agent_checks/#configuration>

![image](https://user-images.githubusercontent.com/41904992/43808721-ac4f2f54-9af1-11e8-8946-5b9507ceb3a0.png)

![image](https://user-images.githubusercontent.com/41904992/43808728-b3781ad4-9af1-11e8-9875-8995397f811d.png)

*BONUS: Can you change the collection interval without modifying the Python check file you created?*

Answer: No. As per the online guides available and my dashboard research, I didn’t see any option other than modifying Python check.

# Level 3: Visualizing Data
1. *Create a Timeboard Using the DataDog API:*
Login to DataDog homepage and click on Integrations>> APIs.

![image](https://user-images.githubusercontent.com/41904992/43808796-05344ec4-9af2-11e8-96cf-86a6c727eb2b.png)

Then provide the name to new application key, I set it as Python-API.
Open the Command prompt and follow the instruction in the link for integration with Python.
<https://docs.datadoghq.com/integrations/python/>

![image](https://user-images.githubusercontent.com/41904992/43808824-22eb2f28-9af2-11e8-8438-d5442149e631.png)

Now make the changes in the Python script to create a Timeboard  as per the link.
<https://docs.datadoghq.com/api/?lang=python#timeboards>

I have hidden the API key for security reasons.

The script I used is:

```
from datadog import initialize, api

options = {
    'api_key':'****************************************',
    'app_key':'**********************************************'
}


initialize(**options)
title = "Python_Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q":"avg:my_metric{host:ubuntu-xenial}"}
      ],
        "viz": "timeseries"
    },
    "title": "My Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q":"avg:mysql.net.connections{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Mysql Net connections"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{host:ubuntu-xenial,env:prod}" }
        ],
        "viz": "timeseries"
    },
    "title": "Rollup funtion past 1 hr "
},

]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```

![image](https://user-images.githubusercontent.com/41904992/43808969-e9812796-9af2-11e8-97b8-044fae7d31b1.png)

![image](https://user-images.githubusercontent.com/41904992/43808994-0fb0f41e-9af3-11e8-9fcf-58ec55baf934.png)

2. *The figure below (After point 3) shows my custom metric “My Metric” scoped over my host, Metric from the Integration on MySQL Database.*

3. *The figure below shows my custom metric (My_Metric) with the roll-up function applied to sum up all the points for the past hour into one bucket.*

![image](https://user-images.githubusercontent.com/41904992/43809017-2bda1184-9af3-11e8-88ef-dcfd5c94ba5b.png)

4. *Then I set the Timeboard timeframe to the past 5 minute and used the @ notation to send it to myself.*

![image](https://user-images.githubusercontent.com/41904992/43809030-3d4cbfc0-9af3-11e8-9d88-7c01794d0b48.png)

With @notation mentioned, I received the following graph on my Email.

![image](https://user-images.githubusercontent.com/41904992/43809038-45bfef9c-9af3-11e8-8108-1a1ec0471c25.png)

*BONUS: What is the Anomaly graph displaying?*

Answer: Here, the Anomaly graph is depicting around 22:28 there is a slight increase in reported values. Anomaly graph helps us to identify any deviation from a standard or normal values. The above graph shows values for 5 minutes but generally, we can have these graphs for a longer duration to study the patterns.

# Level 4: Monitoring Data.
1. *Created a new Metric Monitor and which will alert if it’s above the following values over the past 5 minutes. By following the link*
<https://docs.datadoghq.com/monitors/>

![image](https://user-images.githubusercontent.com/41904992/43809079-80834a98-9af3-11e8-9cec-29470f03a3d1.png)

2. *Then I have set the warning threshold of 0.5, alerting threshold of 0.8 and set the alerting for no data over the past 10 minutes.*

![image](https://user-images.githubusercontent.com/41904992/43809090-8ec08eea-9af3-11e8-8e6a-08240dcf96ae.png)

3. *Then I configured the monitor’s message to send an email whenever the monitor triggers.*

![image](https://user-images.githubusercontent.com/41904992/43809107-a3766878-9af3-11e8-9f6c-add9e1a5c0c1.png)

Snapshots of the email notifications I got:

![image](https://user-images.githubusercontent.com/41904992/43809110-ab5aa388-9af3-11e8-948f-41cda915f509.png)

![image](https://user-images.githubusercontent.com/41904992/43809113-afb7cce4-9af3-11e8-84fb-d91b37833433.png)

*BONUS: Setting Up downtime*

Answer: I have set up two scheduled down times for the monitor and set up email notification for scheduling of downtime. For that I went to DataDog Homepage>>Monitors>>Manage Downtime:

![image](https://user-images.githubusercontent.com/41904992/43809140-d7c288aa-9af3-11e8-814b-e703ff9b3fb0.png)

Below is the snapshot for the monitor downtime from 7 pm to 9 am daily on M-F.

![image](https://user-images.githubusercontent.com/41904992/43809150-e541ed5e-9af3-11e8-9341-5d0630fa285e.png)

Next one is to silence it all day on Sat-Sun.

![image](https://user-images.githubusercontent.com/41904992/43809160-f0727d88-9af3-11e8-8fcd-18bdeed4957d.png)

Email received for the applied downtime:

![image](https://user-images.githubusercontent.com/41904992/43809166-f7be8ba4-9af3-11e8-9a3a-355963819a57.png)

# Level 5: Collecting APM Data

1. *I have started collecting the APM data using the flask app given on the challenge.*
 I used Python to do so and followed the instructions given in the link.
<https://docs.datadoghq.com/tracing/setup/python/>

![image](https://user-images.githubusercontent.com/41904992/43809185-1c79c292-9af4-11e8-8f37-e909d09cf6b5.png)

![image](https://user-images.githubusercontent.com/41904992/43809186-20450102-9af4-11e8-8075-bb118a41c303.png)

![image](https://user-images.githubusercontent.com/41904992/43809187-247775ca-9af4-11e8-8cda-7c6234e3e397.png)

2. *Once the configuration is done, data started reflecting on the APM Page.*

![image](https://user-images.githubusercontent.com/41904992/43809195-313d5df6-9af4-11e8-8586-6a8856dc2324.png)

URL link and screenshot below is of a Dashboard with both APM and infrastructure metrics:

Public URL- <https://p.DataDoghq.com/sb/da07b9cf6-29ce3d27775f2929ee3608ad73dc5274>

![image](https://user-images.githubusercontent.com/41904992/43809210-478dca50-9af4-11e8-8850-d760da105a51.png)

*Fully instrumented flask app*: I have made some changes in the flask app provided on DataDog challenge. Flask app I used is shown below.

![image](https://user-images.githubusercontent.com/41904992/43809216-5651a8e0-9af4-11e8-9f08-149d8e894131.png)

*BONUS: Service Vs Resource*

Answer-
*Service*: A "Service" is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two services: a single web app service and a single database service, while a more complex environment may break it out into 6 services: 3 separate web app, admin, and query services, along with a master-DB, a replica-DB, and a yelp-API external service.
These services are defined by the user when instrumenting their application with DataDog. This field is helpful to quickly distinguish between your different processes.
In the DataDog UI, this is the "Name" field in the image.  An example of setting a custom Service using Python:

![image](https://user-images.githubusercontent.com/41904992/43809240-81c179c4-9af4-11e8-9e27-ce01335d7996.png)

*Resource*: A particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like web.user.home (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like select * from users where id = ?
The Tracing backend can track thousands (not millions or billions) of unique resources per service, so resources should be grouped together under a canonical name, like /user/home rather than have /user/home?id=100 and /user/home?id=200 as separate resources.

*FINAL QUESTION: Is there anything creative you would use DataDog for?*

*Bushfires Monitoring:* It can be used to monitor bushfires by collecting data from the atmosphere around and comparing the values and studying the patterns. We can create a solution where the community can choose to opt-in, deploy the hardware to provide the environment and resource monitoring and share that information with all the State and Government services that help to protect families and homes affected by bushfires every year.

![image](https://user-images.githubusercontent.com/41904992/43809275-b4e8c42e-9af4-11e8-988c-ea42a832f01a.png)

*Water Level Monitoring:* Also, Changes in Water levels in Seas and Oceans can also be monitored by deploying a solution to monitor the effect of changes in surrounding environment on water levels in different parts of the world.

![image](https://user-images.githubusercontent.com/41904992/43809289-c59a1516-9af4-11e8-9005-e63bb3cfdf5f.png)

*Train Capacity Monitoring:* Apart from bushfires and water Level, the solution can also be implemented to check trains capacity. According to the data collected by monitoring, planning can be done by comparing the patterns of peak hours’ rush to the services and compartments available.

![image](https://user-images.githubusercontent.com/41904992/43809298-d2c3941a-9af4-11e8-9990-223418956ecf.png)
