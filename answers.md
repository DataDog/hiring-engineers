# Datadog Technical Exercise 


<img width="642" alt="TOC" src="https://user-images.githubusercontent.com/87458325/157798331-741af974-ac2f-4648-99e9-aa6f8f331c7d.PNG">


# Introduction
As more company’s transition from monoliths to microservices and to cloud or hybrid environments, monitoring data has become a critical aspect to all enterprises. Datadog’s infrastructure monitoring platform allows DevOps teams to track dynamic cloud environments at a high level making it easier to monitor the condition of your infrastructure on a single pane of glass. Deployment of the Agent is quick and easy. The Datadog Agent can run on cloud platforms, bare metal servers, virtual machines, containers and more. Below is an example of the agent getting deployed on a vagrant Ubuntu distribution.






<img width="615" alt="installing the agent Ubuntu" src="https://user-images.githubusercontent.com/87458325/155767763-6e1b9c40-2c60-4275-8f30-c673ac595a9a.PNG">

Prerequisites - Setup the environment 
Vargrant VM method. Quick install

<img width="943" alt="Agent capture to API" src="https://user-images.githubusercontent.com/87458325/155801376-491cd4a9-1dcd-43f5-9528-662dacbb0447.PNG">

# Collecting Metrics
Assessing the health of your environment is an important feature to all infrastructures. With Datadog, you can further customize your Host Map with tags and create custom metrics based on the data that is most important to you and your organization. Whether it’s pulling information from your current database or tracking new users, if it has a numerical value, Datadog can track it and help identify problems that arise. Datadog does this by ingesting the metric data and storing this as a data point with a "value and timestamp". Knowing exactly how to allocate your resources can help save your organization money and improve performance.

## Adding Tags
To simplify and filter queries or to find problems within your environment, Datadog allows you to configure tags to quickly identify the data you are parsing. Tags can be configured on the Agent configuration file by modifying the datadog.yaml file as seen below. This can also be configured through the Datadog UI, Datadog API or with DogStatsD.
Tags aid in identifying specific information and help keep queries organized.  

<img width="602" alt="Adding Tags" src="https://user-images.githubusercontent.com/87458325/155813006-c8193297-8abb-4745-a38d-0ae3467e20ec.PNG">

<img width="869" alt="Host map capture" src="https://user-images.githubusercontent.com/87458325/155813310-c3098ae4-dd6f-4537-9c60-2200e8970bfd.PNG">


After adding tags be sure to do a $ sudo service datadog-agent restart to apply YAML file changes.
# Database Monitoring
Deep dive into your enterprise's database to quickly determine health and performance. The Datadog Agent collects telemetry data points directly from the database by "logging in" as a Read-only user.  It’s that simple! Configure the database parameters to match Datadog perquisite settings, grant access to the agent, verify that the permissions are correct, and start visualizing efficient indexing, disk space, and other components.

## Grant access


<img width="471" alt="Creating Datadog user and grant basic permissions" src="https://user-images.githubusercontent.com/87458325/155818635-d4541565-801c-4b46-bcb5-ed8699446bbb.PNG">

## Verify successful user creation
<img width="644" alt="verifying successful creation" src="https://user-images.githubusercontent.com/87458325/155819308-74819e2e-0a52-4cd7-8583-1d24628bc156.PNG">

## Metric Collection conf.yaml configuration

<img width="833" alt="Metric collection mysql" src="https://user-images.githubusercontent.com/87458325/155828798-530ecd4c-69e3-48f3-bf50-9a13ef407c9e.PNG">
<img width="824" alt="Metric collection mysql2" src="https://user-images.githubusercontent.com/87458325/155828804-cb220369-8af9-41c3-beb3-c3c7aabbd798.PNG">

sudo service datadog-agent restart

<img width="545" alt="installed MySQL" src="https://user-images.githubusercontent.com/87458325/155829597-af46b943-aa1a-494e-a55f-3886f4da3827.PNG">

## Creating a custom Agent check
Custom Checks enable you to collect metrics from custom applications or systems suitable for your unique situations. Depending on how many custom checks created might impact cost. Unlike integrations, custom checks provide a quick solution for temperary needs. 

my_metric.yaml 

<img width="896" alt="conf d_yaml_my_metric" src="https://user-images.githubusercontent.com/87458325/155830523-f096ce1f-6f44-4094-a6fa-bd6743303635.PNG">

<img width="551" alt="check d_my_metric" src="https://user-images.githubusercontent.com/87458325/155832112-116d77d9-3028-46ff-8213-87fb3ac53384.PNG">

<img width="815" alt="change check interval" src="https://user-images.githubusercontent.com/87458325/155832850-02f90b3e-38b2-432e-b857-6f8bfd220faa.PNG">


**NOTE** The python script and yaml file must be the same name for it to pick up

<img width="693" alt="customcheck result" src="https://user-images.githubusercontent.com/87458325/155832041-04cd749b-82e7-4cb6-af1d-101f412c41d7.PNG">

# Visualizing Data
Data is the monumental key for telling a story about everything and because there is an abundant amount of data, it can easily be lost or misinterpreted without the proper tools.  Data granularity can be observed on several echelons helping aid businesses to make decisions faster and provide a clear outlook on objectives. The best way to understand data is to see it! Datadog’s centralized visualization monitoring tools helps summarize data in a clean, easily readable format. Use preconfigured or create custom dashboards, timeboards, or screenboards with a variety of objects such as timeseries, heat maps, scatter plots, geomaps and pie charts to help represent your data in an logical format. Adding query metrics, like anomalies, help to detect when datasets are deviating from their standard means and explore outliers in your data.  

My custom Metric with the rollup function applied to sum up in the past hour
<img width="939" alt="mmgraph" src="https://user-images.githubusercontent.com/87458325/155861052-5e183fd4-e53d-4985-b484-f56a9d07cf25.PNG">


Mysql integration with the anomaly function depicting performance kernel time
<img width="936" alt="mysql metric timeboard" src="https://user-images.githubusercontent.com/87458325/155860814-95c6101d-a613-4a2a-b622-abc51c87d170.PNG">

<img width="851" alt="timeboard5minute" src="https://user-images.githubusercontent.com/87458325/155861205-dd1acc24-67d1-4f16-b1c5-09069bfa9cf1.PNG">

## snapshot
Take Graph Snapshots and use the @ annotation to quickly collaborate with team members

<img width="325" alt="snapshot" src="https://user-images.githubusercontent.com/87458325/155863643-c1b0e1c5-523e-45fe-8ea6-ded47ca6226a.PNG">

https://p.datadoghq.com/sb/9136907e-9663-11ec-83c8-da7ad0900002-73cac96272540807f8af3da880d08838

# Monitoring Data
Effective monitoring is a vital condition for observing the inner workings of your system. Being able to pinpoint problems and examine performance issues through metrics, events, logs, and traces helps capture big picture awareness and can save companies time, money, and resources. Datadog’s configurable alert conditions and collaboration tools keep urgent matters under control. These Alerts can trigger time events, thresholds, performance optimization, errors, utilization, saturation, and availability in a comprehensive overview of your infrastructure and help resolve issues quickly. 
 

<img width="773" alt="define the alert" src="https://user-images.githubusercontent.com/87458325/155863741-60224f89-0d20-4733-adba-bcea48cb1a87.PNG">


<img width="828" alt="email alert" src="https://user-images.githubusercontent.com/87458325/155864728-22c95a8a-47dc-40a5-910d-ab9aac4fc3fe.PNG">
<img width="326" alt="is no data" src="https://user-images.githubusercontent.com/87458325/155912328-711cb9a9-a0bd-4b55-bfe6-40ae761a4b08.PNG">
<img width="357" alt="email1 critical" src="https://user-images.githubusercontent.com/87458325/155864730-809392c8-e0b0-4a6f-bfbd-58c871af7703.PNG">
<img width="355" alt="email2 warning" src="https://user-images.githubusercontent.com/87458325/155864732-8812eea7-dece-4832-aa97-03a5813c5a9c.PNG">

<img width="256" alt="silence mon-friday" src="https://user-images.githubusercontent.com/87458325/155913980-8df9bdc8-773c-4ca9-a259-126d1c03a117.PNG">
<img width="300" alt="Silence weekend" src="https://user-images.githubusercontent.com/87458325/155913993-7b9199eb-65cd-4532-8c6c-b3f1221270e4.PNG">
<img width="461" alt="downtime ss" src="https://user-images.githubusercontent.com/87458325/155914130-5e13c53e-9960-4b44-86aa-d2f6be6ffc5b.PNG">

# Application Performance Monitoring

 As customer’s requirements and goals change frequently, it’s important that Datadog scale's with them on their journey. Datadog’s APM works with important programming languages (Java, go, python, Microsoft .NET, php, ruby, and node) to provide a complete package of front to backend tracing. With new features like Service maps, span summary and trace search analytics; the ability to trouble shoot faster with deep correlation is now a streamlined task. 

Install pip, flask, and ddtrace
sudo apt-get install python-pip
pip install flask
pip install ddtrace

<img width="775" alt="collect apm data python" src="https://user-images.githubusercontent.com/87458325/155917883-6fd8f063-ba8c-45bf-8a35-e1c9bc3250a0.PNG">

Ran into an Error with pip install ddtrace, I had to upgrade pip and python to the latest versions
<img width="714" alt="diagnosing python" src="https://user-images.githubusercontent.com/87458325/155920956-ffa02325-a6c7-4f0d-842d-bc89fedc9a1b.PNG">
<img width="897" alt="ddtrace successful" src="https://user-images.githubusercontent.com/87458325/155921021-763e9df9-d73a-4c03-8b96-45a2b151944d.PNG">


ddtrace-run python hello.py

<img width="519" alt="ddtrace-run python script" src="https://user-images.githubusercontent.com/87458325/155921222-94274b3b-c8d4-443f-8c7e-49f70cd02ffd.PNG">

<img width="232" alt="0 0 0 0" src="https://user-images.githubusercontent.com/87458325/155921728-2491e10f-e00b-4be9-98dc-abc5204792ba.PNG">

<img width="954" alt="service flask" src="https://user-images.githubusercontent.com/87458325/155922180-66d4bb9f-7df0-4329-853a-8b910d0c19de.PNG">

<img width="954" alt="screenshot apm and infra" src="https://user-images.githubusercontent.com/87458325/155925383-4cbff45f-622f-47e4-a18c-fdc54369b55f.PNG">

# Shared Dashboard
https://p.datadoghq.com/sb/9136907e-9663-11ec-83c8-da7ad0900002-73cac96272540807f8af3da880d08838

# Final Question

Datadog's Agent and turnkey integrations could be a useful tool that explores how companies in the telehealth industry scale, aggregate, and analyze telemetry data in preventive healthcare.  Covid-19 has opened the door on the feasibility and acceptance of remote encounters between patients and their primary care doctors which increases the bandwidth of traffic and other pain points causing extra pressure on healthcare servers. Datadog can leverage this new lifestyle by providing critical infrastructure monitoring solutions to telehealth systems. With easy scalable solutions and protective security, Datadog can ensure that availability and observability will always be a priority.

