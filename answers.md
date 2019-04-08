# Technical Interview Round - VP


## Collecting Metrics:
### Step 1:
Instrument DataDog Infrastructure and APM Agents.
In this step, I have install the DataDog agents in Ubuntu, CentOS flavors of Linux. over the weekend, I played with various agent types and tech stacks.

##### Here is the reference of Host Map
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/hostmap.jpg" alt="Host Map">
##### Tags are added both in AWS and Agent Configuration
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/tags.jpg "Adding Tags">

APM Tag
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/apm-tag.jpg" alt= "APM Tags">

### Step 2:
I haven't installed any DB specific integration as I spent most of the time configuring APM Agents

## Visualizing Data:

### Step 3:
Custom metric scoped over Host
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/15min-story.jpg" alt= "Custom Metric">

### Step 4:
Anomaly function applied

### Step 5:
Custom metric rollup
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/5min-story.jpg" alt= "Rollup">

### Step 6:
Notebook [Link]("https://app.datadoghq.com/notebook/110047/Analysis%20Notebook)]

Analysis [[Link]("https://app.datadoghq.com/notebook/110047/Analysis-Notebook?cell=soqfsrv8)]

## Monitoring Data:

### Step 7:
Configure monitors


### Step 8:
Different thresholds

### Step 9:
Email notification

##### High Error Rate
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/high-error-rate-email.jpg" alt= "High Error Rate">

##### Recovery From Above Incident
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/recovery-email.jpg" alt= "Recovery Notification">


### Step 10:
Alert History
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/alert-history.png "Alert History">

### Step 11:
Scheduled Downtime

##### Daily downtime from 7 PM to 9 AM
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/snooze-weekday.jpg" alt= "Scheduled Downtime">

##### Weekend Snooze (Saturday and Sunday)
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/snooze-weekend.jpg">

## Collecting APM Data:
Instrumented PHP, Java, Ruby, Python applications. By far, java seems to be the fastest instrumentation from the list of applications I tried.
<img src="https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/apm-instrumentation.jpg">

## Final Question:
Screen time tracking could be awesome!!! How many hours did I spend to review metrics in DataDog UI
