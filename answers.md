Your answers to the questions go here.
## Table of Contents
* [Setting Up the Environment](#setting-up-the-environment)
* [Collecting Metrics](#collecting-metrics)
* [Visualizing Data](#visualizing-data)
* [Monitoring Data](#monitoring-data)
* [Collecting APM Data](#collecting-apm-data)
* [Final Question](#final-question)

<a name="setting-up-the-environment"/>

## Prerequisites - Setting Up the Environment
1. First, I spinned up a fresh linux Ubuntu VM via Vagrant on Virtual Box on my Mac. I followed these steps: https://medium.com/devops-dudes/how-to-setup-vagrant-and-virtual-box-for-ubuntu-20-04-7374bf9cc3fa
2. Next, I signed up for Datadog (used “Datadog Recruiting Candidate” in the “Company” field). 
3. And installed the Datadog Agent on the  Vagrant Box by running this command for ubuntu: 
```DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=########## DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"```  
I removed the key for security purposes.
4. Finally, got the Agent reporting metrics from my local machine:
<img src='./screenshots/Agent Reporting Metrics.png'> </img>

<a name="collecting-metrics"/>

## Collecting Metrics
1. Added tags in the Agent config file and here is the screenshot of the host and its tags on the Host Map page in Datadog.
<img src='./screenshots/Datadog Agent Yaml Tags 1.png'> </img>
<img src='./screenshots/Datadog Yaml Tags 2.png'> </img>
<img src='./screenshots/Datadog Dashboard Tags.png'> </img>