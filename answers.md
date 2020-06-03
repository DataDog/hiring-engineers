Your answers to the questions go here.

# These Answers by Stephen Roe

Candidate for Solution Engineer in London

*my hobby github account is p6steve, email is stephen.john.roe@gmail.com*

*link to this repo provided by Nick Elwell*

## Prerequisites

In the spirit of demonstrating thoughtfulness, here is my rationale regarding my personal setup.

1. My home laptop is OSX, could spin up Docker on that machine, but...
2. I already have a LAMP build (Ubuntu 18.04 / Apache2 / mysql / PHP, Python) live on AWS to run Wordpress - so let's instrucment that with the DataDog Agent and connect from OSX as client

### Sign Up for DataDog, Install Agent & Connect

Just used > sudo DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=7b108d7...  That was smooth!

![image1](images/image1.png)

### Get the Agent Reporting Metrics from your (local) Machine

Successful initial report from DD agent on app.datadoghq.eu webpage

![image2](images/image2.png)

## Collecting Metrics

Adding tags to the DD Agent config file...

`tags:
    - "<p6steve_build>:<1.0>"
    - "<p6steve_url>:<henleycloudconsulting.co.uk>"
    - "<p6steve-ssl>:<on>"`
