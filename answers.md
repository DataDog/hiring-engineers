# Datadog Technical Exercise Sale Engineering position
 by Jeff Hollis 2021
## Answers
Vargrant VM method. Quick install

<img width="615" alt="installing the agent Ubuntu" src="https://user-images.githubusercontent.com/87458325/155767763-6e1b9c40-2c60-4275-8f30-c673ac595a9a.PNG">

# Prerequisites - Setup the environment 

<img width="943" alt="Agent capture to API" src="https://user-images.githubusercontent.com/87458325/155801376-491cd4a9-1dcd-43f5-9528-662dacbb0447.PNG">

# Collecting Metrics

## Adding Tags

<img width="602" alt="Adding Tags" src="https://user-images.githubusercontent.com/87458325/155813006-c8193297-8abb-4745-a38d-0ae3467e20ec.PNG">

<img width="869" alt="Host map capture" src="https://user-images.githubusercontent.com/87458325/155813310-c3098ae4-dd6f-4537-9c60-2200e8970bfd.PNG">


After adding tags be sure to do a $ sudo service datadog-agent restart to apply YAML file changes.

## Installing MYSQL
sudo apt ugrade & sudo apt update
sudo apt install mysql-server
https://docs.datadoghq.com/database_monitoring/setup_mysql/selfhosted/?tab=mysql80

<img width="471" alt="Creating Datadog user and grant basic permissions" src="https://user-images.githubusercontent.com/87458325/155818635-d4541565-801c-4b46-bcb5-ed8699446bbb.PNG">

## Verify successful user creation
<img width="644" alt="verifying successful creation" src="https://user-images.githubusercontent.com/87458325/155819308-74819e2e-0a52-4cd7-8583-1d24628bc156.PNG">

## Metric Collection conf.yaml configuration

<img width="833" alt="Metric collection mysql" src="https://user-images.githubusercontent.com/87458325/155828798-530ecd4c-69e3-48f3-bf50-9a13ef407c9e.PNG">
<img width="824" alt="Metric collection mysql2" src="https://user-images.githubusercontent.com/87458325/155828804-cb220369-8af9-41c3-beb3-c3c7aabbd798.PNG">

sudo service datadog-agent restart

<img width="545" alt="installed MySQL" src="https://user-images.githubusercontent.com/87458325/155829597-af46b943-aa1a-494e-a55f-3886f4da3827.PNG">

## Creating a custom Agent check
sudo nano my_metric.yaml --- Content "instances: [{}]"

<img width="896" alt="conf d_yaml_my_metric" src="https://user-images.githubusercontent.com/87458325/155830523-f096ce1f-6f44-4094-a6fa-bd6743303635.PNG">

<img width="551" alt="check d_my_metric" src="https://user-images.githubusercontent.com/87458325/155832112-116d77d9-3028-46ff-8213-87fb3ac53384.PNG">

<img width="815" alt="change check interval" src="https://user-images.githubusercontent.com/87458325/155832850-02f90b3e-38b2-432e-b857-6f8bfd220faa.PNG">


**NOTE** The python script and yaml file must be the same name for it to pick up

<img width="693" alt="customcheck result" src="https://user-images.githubusercontent.com/87458325/155832041-04cd749b-82e7-4cb6-af1d-101f412c41d7.PNG">

# Visualizing Data


My custom Metric with the rollup function applied to sum up in the past hour
<img width="939" alt="mmgraph" src="https://user-images.githubusercontent.com/87458325/155861052-5e183fd4-e53d-4985-b484-f56a9d07cf25.PNG">


Mysql integration with the anomaly function depicting performance kernel time
<img width="936" alt="mysql metric timeboard" src="https://user-images.githubusercontent.com/87458325/155860814-95c6101d-a613-4a2a-b622-abc51c87d170.PNG">

<img width="851" alt="timeboard5minute" src="https://user-images.githubusercontent.com/87458325/155861205-dd1acc24-67d1-4f16-b1c5-09069bfa9cf1.PNG">

## snapshot

<img width="325" alt="snapshot" src="https://user-images.githubusercontent.com/87458325/155863643-c1b0e1c5-523e-45fe-8ea6-ded47ca6226a.PNG">

https://p.datadoghq.com/sb/9136907e-9663-11ec-83c8-da7ad0900002-73cac96272540807f8af3da880d08838

# Monitoring Data

<img width="773" alt="define the alert" src="https://user-images.githubusercontent.com/87458325/155863741-60224f89-0d20-4733-adba-bcea48cb1a87.PNG">


<img width="828" alt="email alert" src="https://user-images.githubusercontent.com/87458325/155864728-22c95a8a-47dc-40a5-910d-ab9aac4fc3fe.PNG">
<img width="326" alt="is no data" src="https://user-images.githubusercontent.com/87458325/155912328-711cb9a9-a0bd-4b55-bfe6-40ae761a4b08.PNG">
<img width="357" alt="email1 critical" src="https://user-images.githubusercontent.com/87458325/155864730-809392c8-e0b0-4a6f-bfbd-58c871af7703.PNG">
<img width="355" alt="email2 warning" src="https://user-images.githubusercontent.com/87458325/155864732-8812eea7-dece-4832-aa97-03a5813c5a9c.PNG">

<img width="256" alt="silence mon-friday" src="https://user-images.githubusercontent.com/87458325/155913980-8df9bdc8-773c-4ca9-a259-126d1c03a117.PNG">
<img width="300" alt="Silence weekend" src="https://user-images.githubusercontent.com/87458325/155913993-7b9199eb-65cd-4532-8c6c-b3f1221270e4.PNG">
<img width="461" alt="downtime ss" src="https://user-images.githubusercontent.com/87458325/155914130-5e13c53e-9960-4b44-86aa-d2f6be6ffc5b.PNG">

# Collecting APM Data

Install pip, flask, and ddtrace
sudo apt-get install python-pip
pip install flask
pip install ddtrace

<img width="775" alt="collect apm data python" src="https://user-images.githubusercontent.com/87458325/155917883-6fd8f063-ba8c-45bf-8a35-e1c9bc3250a0.PNG">

## Ran into an Error with pip install ddtrace, I had to upgrade pip and python to the latest versions
<img width="714" alt="diagnosing python" src="https://user-images.githubusercontent.com/87458325/155920956-ffa02325-a6c7-4f0d-842d-bc89fedc9a1b.PNG">
<img width="897" alt="ddtrace successful" src="https://user-images.githubusercontent.com/87458325/155921021-763e9df9-d73a-4c03-8b96-45a2b151944d.PNG">


ddtrace-run python hello.py

<img width="519" alt="ddtrace-run python script" src="https://user-images.githubusercontent.com/87458325/155921222-94274b3b-c8d4-443f-8c7e-49f70cd02ffd.PNG">

<img width="232" alt="0 0 0 0" src="https://user-images.githubusercontent.com/87458325/155921728-2491e10f-e00b-4be9-98dc-abc5204792ba.PNG">

<img width="954" alt="service flask" src="https://user-images.githubusercontent.com/87458325/155922180-66d4bb9f-7df0-4329-853a-8b910d0c19de.PNG">

<img width="954" alt="screenshot apm and infra" src="https://user-images.githubusercontent.com/87458325/155925383-4cbff45f-622f-47e4-a18c-fdc54369b55f.PNG">

# Shared Dashboard
https://p.datadoghq.com/sb/9136907e-9663-11ec-83c8-da7ad0900002-73cac96272540807f8af3da880d08838

