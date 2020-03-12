My answers to the questions are here !!!

# Prerequisites - Setup the environment
Prior to the interview I had already signed up for Datadog to play along the tool and interfaces with my own company name Cogitos Consulting. After the interview I have changed the company name to “Datadog Recruiting Candidate” and start to write down this document.

I've gone with the ready captive environmet of mine and used one of my linux installs with Ubuntu distrubution with version 18.04 Bionic on VirtualBox.

# Collecting Metrics:

* Adding tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

My host shown on the Datadog Inventory Hostmap page prior to adding tags

<img src="https://live.staticflickr.com/65535/49649359148_8620b9abcb_c.jpg" width="800" height="403"></a>

I remove the comment out and added three tags to my host via editing datadog.yaml file

```
## @param tags  - list of key:value elements - optional
## List of host tags. Attached in-app to every metric, event, log, trace, and service check emitted by this Agent.
##
## Learn more about tagging: https://docs.datadoghq.com/tagging/
#
tags:
         - environment:dev
         - hostdbapp:pgsql
         - hostwebapp:tomcat
```


<img src="https://live.staticflickr.com/65535/49649939656_e1a86822f6_c.jpg" width="800" height="129"></a>


