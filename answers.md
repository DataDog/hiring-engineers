# Technical Interview Round - VP

## Introduction
Purpose of this document is to provide details about the steps taken to install, instrument and correlate metrics data for various integrations point.**

## Collecting Metrics:

### Step 1:
Instrument DataDog Infrastructure and APM Agents.
In this step, I have install the DataDog agents in Ubuntu, CentOS flavors of Linux. over the weekend, I played with various agent types and tech stacks.

Installation in Linux is easy with one single command: I must say this was very easy installation compared to other tools I have used.

> DD_API_KEY=a4f8c6c682be39cc35de01220c3b789d bash -c "$(curl -L
> https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

##### Here is the reference of Host Map
![Host Map](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/hostmap.jpg)

##### Tags are added both in AWS and Agent Configuration
![Adding Tags](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/tags.jpg)

![APM Tag](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/apm-tag.jpg)

### Step 2:
I installed MySQL integration. The configuration for the same is below:
**![](https://lh6.googleusercontent.com/Ji4mr2CkRplBgn22sbzkNGcivqqP3A7mG4tR4OkzQ1H-APY758dt4sXe-UNEs_XgCwG0EY3aJPFrDGZtunX6d-ExMhjdeJ2d3xbpxazrJgrGQrcYMuDE3iX5o2HhXEpaOQlNFEBg)**

### Step 3:
I created a custom agent check with the following file names
![](https://lh6.googleusercontent.com/7R5uDo4ueNYkJ2ePqiIIixjC09Vh3UsJr4y7fAP8kwff7hKybrjo2z4y7DEYRqnx-5sgiCZL618slh1UmXAmQqqdu-JKZR9saXQr_Bco4DC-9tMkKzF_Z-vYFlZJjDGm9yWpBht2)

Content of my_metric.yaml file

![](https://lh3.googleusercontent.com/HkNror1kBVCGAN9bR9mXQ5axJTPlgjDiDRO9oyM9i8tw54bFBq-oZ2nGjVVJL7xJ_SWLWns4bY9plty3zfkdk24judazFVOJnEPR2IQ1ym8NGS5zWJLsjsknZWCyHc5Mzi-sVyd9)

I further changed the check's collection interval so that it only submits the metric once every 45 seconds.

Content of my_metric.py file

![](https://lh3.googleusercontent.com/aPhYmLDGxzehdQmCQCH1NTeEdZhgw0fXCZ54i9Q1tXxLTdDeC_HHQ7A-APRpcsFwydPLmYoHBotZyNe95wmOW3TDq8xuRv8PmLADUMyQpSUxg0z5qLImaS-SU0UCLmXESqpKvg9h)


Bonus Question: I changed the interval in YAML file instead of python script as suggest in the documentation here. [https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval)

## Visualizing Data:

### Step 3:
Custom metric scoped over Host
![15 mins rollup](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/15min-story.jpg)

### Step 4:
Anomaly function applied

### Step 5:
Custom metric roll up
![5 mins rollup](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/5min-story.jpg)

### Step 6:
[Notebook Link](https://app.datadoghq.com/notebook/110047/Analysis%20Notebook)
![Custom Metrics](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/custom-metric.jpg)
<br />
![Custom Metrics](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/custom-metric1.jpg)

[Analysis Link](https://app.datadoghq.com/notebook/110047/Analysis-Notebook?cell=soqfsrv8)

## Monitoring Data:

### Step 7:
Reviewed Data
![Application Metrics](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/app-metric.jpg)

### Step 8:
Different thresholds
![Anomaly](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/anomaly.png)

### Step 9:
Email notification

##### High Error Rate
![High Error Rate](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/high-error-rate-email.jpg)

##### Recovery From Above Incident
![Recovery Notification](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/recovery-email.jpg)

### Step 10:
Alert History
![Alert Details](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/alert-history.png)

### Step 11:
Scheduled Downtime

##### Daily downtime from 7 PM to 9 AM
![During weekday](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/snooze-weekday.jpg)

##### Weekend Snooze (Saturday and Sunday)
![During weekend](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/snooze-weekend.jpg)

## Collecting APM Data:
Instrumented PHP, Java, Ruby, Python applications. By far, java seems to be the fastest instrumentation from the list of applications I tried.
![APM Instrumentation](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/apm-instrumentation.jpg)

## Final Question:
Screen time tracking could be awesome!!! How many hours did I spend to review metrics in DataDog UI

## Links
[Dashboard Link](https://app.datadoghq.com/dashboard/kne-d3n-dvn/application--server-health?tile_size=m&page=0&is_auto=false&from_ts=1554656400000&to_ts=1554742800000&live=true)
<br />
[Monitor Link](https://app.datadoghq.com/monitors/9434143)

PS: I used ec2 instances as I can run synthetics traffic using siege during random times.
