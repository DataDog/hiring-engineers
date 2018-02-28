# Datadog Solutions Engineer Technical Exercise

## Prerequisites - Setup the environment

The environment used for the technical exercise consisted of an AWS EC2 instance running the amazon linux AMI. The required agent, database, and example application were generated using docker and docker-compose.

### Recreating the technical exercise
To create the required environment in an AWS account, please use the terraform docker-compose script found [here](files/terraform/)

To see the individual components check out the 
[docker-compose info](files/)

![AWS Console - Instance](https://raw.githubusercontent.com/tnoeding/hiring-engineers/solutions-engineer/files/screenshots/aws_console_ddinstance.png)

## Collecting Metrics:

The provided screenshot shows the agent with the required tags.

![Datadog Agent - displaying tags](https://raw.githubusercontent.com/tnoeding/hiring-engineers/solutions-engineer/files/screenshots/sceen1_agent_tags.png)

It also displays the MySQL integration that was added, which can be found [here](files/dd-agent/conf.d/mysql.yaml)

The custom agent check named my_metric can be found [here](files/dd-agent/checks.d/my_metric.py) and the configuration can be found [here](files/dd-agent/conf.d/my_metric.yaml)

#### Bonus Question:
By default the agent does checks every 15 seconds. By adding ```min_collection_interval``` to the init config, I was able to change the collection interval to 45 seconds. I was unable to find any way of changing the interval outside of editing the config and restarting the agent.

## Visualizing Data:

The scripts used to create and destroy the timeboard can be found [here](files/scripts/)

This screenshot shows the 5 minute snapshot mention to myself.
![Timeboard mention with anomaly](https://raw.githubusercontent.com/tnoeding/hiring-engineers/solutions-engineer/files/screenshots/timeboard_snapshot_email.png)

#### Bonus Question:
The anomaly graph shows when metrics go outside of the expected historical behavior. This allows you to distinguish between normal and abnormal trends.

## Monitoring Data

The following is a screenshot of an email alert recieved on my phone. It shows the metric was above 800 (804.2) which triggered the monitor.

![Screenshot of threshold alert](https://raw.githubusercontent.com/tnoeding/hiring-engineers/solutions-engineer/files/screenshots/datadog_alert_screenshot_phone.png)

#### Bonus Question:
This is the downtime notification sent to let me know that alerting would be suspended until tomorrow morning at 9am.

![Screenshot of downtime message](https://raw.githubusercontent.com/tnoeding/hiring-engineers/solutions-engineer/files/screenshots/phone_screenshot_downtime.png)

## Collecting APM Data:

[APM Dashboard Link](https://app.datadoghq.com/dash/595296/apm-and-infrastructure)

![Dashboard Screenshot of APM and Infrastructure Metrics](https://raw.githubusercontent.com/tnoeding/hiring-engineers/solutions-engineer/files/screenshots/apm_infra_screenshot.png)

The application and dockerfile can be found [here](files/flask-app/)


#### Bonus Question:
**Resource** - specific query to a service example: a URL or sql query

**Service** - the name of processes that provide a feature set example: my-custom-application

## Final Question:

Cryptocurrency mining has become popular recently, and I would enjoy using datadog to provide a much better window into the efficiency of the different miners. This could be used to show everything from blocks of work solved to frequency of hardware errors.