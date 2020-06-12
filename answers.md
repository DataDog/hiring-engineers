# Datadog Solutions Engineer Exercise

The intent of the exercise is to get familiar with the Datadog Platform. This document outlines the process from initial
 account setup, Agent installation, collecting metrics, visualizing and monitoring data from an array complex systems.


## Prerequisites - Setup the environment

### Read the Documentation
Before learning any new technology or platform, I start by reading through the main documentation to get a general 10k 
foot view of the technology. I found the [Datadog Platform Documentation](https://docs.datadoghq.com/) to be 
absolutely beautiful visually, easy to navigate, clear and concise. 
![datadog_docs](images/datadog_docs.png)

### Video Resources
Prior to this exercise, I utilized the [Datadog YouTube Channel](https://www.youtube.com/user/DatadogHQ) to quickly learn from the
experts/evangelists at Datadog. The [Datadog 101](https://www.youtube.com/playlist?list=PLdh-RwQzDsaOoFo0D8xSEHO0XXOKi1-5J) playlist allowed me to 
understand key concepts of the product in a short amount of time. I suggest adding this as a resource in the main [README](README.md) under the "Other questions" section. 

### Host Instances
For the exercise, I used my MacBook Pro with the following specs:
```
MacBook Pro (15-inch, Late 2016)
2.7 GHz Quad-Core Intel Core i7
16 GB 2133 MHz LPDDR3

macOS Catalina - v10.15.5
```

I also set up a Vagrant Ubuntu 18.04.4 LTS VM running with VirtualBox, to provide additional host metrics. 


### Sign up for a Datadog Account
To sign up for a Datadog account, I navigated to the main [Datadog signup page](https://app.datadoghq.com/signup) with 
my email `jeremy.daggett@gmail.com` and provided the “Datadog Recruiting Candidate” in the “Company” field as requested.


## Installing the Agent
The following links provide the commands and output for the installation of the Agent:
* [macOS Agent Installation](src/macos_agent_install.md)
* [Ubuntu Agent Installation](src/ubuntu_agent_install.md)

 
## Validate Metric Reporting
After installing the Agents on both host systems I ran a quick experiment to ensure metrics were being pushed to Datadog.

To generate load on my system, I played two YouTube videos simultaneously and watched a recorded show on Sling TV.

Additionally, I ran a duplicate finder application called [Gemini](https://macpaw.com/gemini) over my network to compare two
really large directories for duplicate files. The directories contain my various mp3 collections I've gathered over the past 30 years
and contain many duplicates.

This screenshot of the Host Dashbpard shows that metrics from the macOS host `kalachakra.local` are being reported to Datadog:
![metrics](images/macos_metric_reporting.png)

The following links provide access to the Host Dashboard and Host Map:
* [Host Dashboard](https://app.datadoghq.com/dash/host/2591983488?live=4h&page=0)
* [Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=2591983488)


## Collecting Metrics


## Visualizing Data


## Monitoring Data


## Collecting APM Data


## Final Question
