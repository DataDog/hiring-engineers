# DataDog Technical Excercise 

#### Applicant: 
#### Date: December 12 2018

## Environment setup

I have setup and tested several environments - in Azure and locally. In Azure it was a Ubuntu Linux host, a Kubernetes based container and a Windows 10 workstation. Localy it was an Ubuntu VM host. 
<img src="01_azureoverview.jpg" width="100%">
The **DD Hostmap** then looks like:

<img src="02_ddhostoverview.jpg" width="100%">

For the sake of this assignment all tasks are beign done on the **testmachine.smit.net** host which is the local VM.I have preconfigured the environment with all necessary packages - python, pip, bench tools etc.
To have reaosnable data and events sent to the DD collector, I simulated certain situation, like high CPU usage with **stress-ng --cpu 0 --perf** and generated traffic on the simple webapp which used a local DB hosted with a simple script like: **for i in `seq 1 1000`; do curl http://0.0.0.0:9999/<name_here>; done**. App has its own randomizer inbuilt. 

**Agent info:** 
```bash
smit@ubuntu:~$ sudo datadog-agent health
Agent health: PASS
=== 11 healthy components ===
ad-configpolling, ad-servicelistening, aggregator, collector-queue, dogstatsd-main, forwarder, healthcheck, metadata-agent_checks, metadata-host, metadata-resources, tagger
````
## Collecting Metrics:

1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Tags were added to the agent yaml file */etc/datadog-agent/datadog.yaml*  : 

**# Set the host's tags (optional)
tags: mysql, env:production, role:web**

<img src="03_customtags.jpg" width="100%">

2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Installed MySQL database on the machine and installed the DD integration. Agent status is:
```bash
smit@ubuntu:~$ sudo datadog-agent status
Getting the status from the agent.

mysql (1.4.0)
    -------------
        Instance ID: mysql:c834f329c922e54c [OK]
        Total Runs: 301
        Metric Samples: 61, Total: 18,360
        Events: 0, Total: 0
        Service Checks: 1, Total: 301
        Average Execution Time : 41ms
 ```
3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.


4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

5. Bonus Question Can you change the collection interval without modifying the Python check file you created?
