Your answers to the questions go here.

# Datadog Overview
Datadog is a monitoring service for cloud-scale applications, providing monitoring of servers, databases, tools, and services, through a SaaS-based data analytics platform. [Wiki](https://en.wikipedia.org/wiki/Datadog)

### Features
* Observability - From infrastructure to apps, in any environment
* Dashboards - Use instant, real-time boards or build your own
* Infrastructure - From overview to deep details, fast
* Analytics - Custom app metrics or business KPIs
* Collaboration - Share data, discuss in context, solve issues quickly
* Alerts - Avoid alert fatigue with smart, actionable alerts
* API - Love infrastructure as code? You'll love Datadog's API
* Machine Learning - Automatically detect outliers and temporal anomalies
* APM - Monitor, optimize, and troubleshoot app performance

I am here to apply for the support engineer at [Datadog](https://www.datadoghq.com/careers/detail/?gh_jid=1160573) Sydney.

# The Challenge

## Prerequisites - Setup the environment
* Which OS did I use for this challenge?

>Answer: I am using macOS Sierra Version 10.12.6 for this Challenge.

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

>Answer: [Sign up here](https://www.datadoghq.com/#), get a datadog account for free for 14 days.

>login, click on [_integration-Agent_](https://app.datadoghq.com/account/settings#agent/mac) in DataDog on the left column and follow the installation instructions for Mac OS X to install the Agent.

> The datadog can be installed on OS X as easily as:
```
DD_API_KEY=<you_api_key> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)"
```

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

> Answer: open ~/.datadog-agent/datadog.yaml, uncomment tag block and add your own tags to the host.  
[reference](https://docs.datadoghq.com/tagging/#applying-tags)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

> I used MongoDB to complete this section's test. The install instrcution for MongoDB can be found [here](https://docs.mongodb.com/guides/server/install/).

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

* Bonus Question Can you change the collection interval without modifying the Python check file you created?
