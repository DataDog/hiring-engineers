Your answers to the questions go here.
# Prerequisites - Setup the environment:
I am using a [Vagrant](https://learn.hashicorp.com/collections/vagrant/getting-started) VM with an Ubuntu 18.04 server.

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  - To add tags into the host, I used the [following guide](https://docs.datadoghq.com/getting_started/tagging/assigning_tags?tab=noncontainerizedenvironments)
  Here are the images of the code from the host and the Host Map.
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
  - I choose MySql for this example, if you don't have MySql installed on your machine, please use the following [guide](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04)
  - Once you have installed MySql on your machine please use the following [guide](https://docs.datadoghq.com/integrations/mysql/?tab=host#pagetitle) to install the Datadog integration for MySql.
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
  - To be able to s (https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/)
  here's the pic for the code, and the yaml file and from the  ui 
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
  - submit a pic
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
  - Yes, you can. Please see the [following](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval)

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
I used the following two resources to build the alerts:

(https://docs.datadoghq.com/monitors/monitor_types/metric/?tab=threshold#overview)
(https://docs.datadoghq.com/monitors/notifications/?tab=is_alert#conditional-variables)

* Warning threshold of 500
* Alerting threshold of 800
Screnshot for both ^
* And also ensure that it will notify you if there is No Data for this query over the past 10m.
Screenshot^

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.
Screen shots for the top three questions

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
I used [this](https://docs.datadoghq.com/monitors/downtimes/?tab=bymonitorname) 

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
## Collecting APM Data:
I used th give Flask application  
I ran into a couple of issues while trying to install 'ddtrace' using following [resource](https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers#follow-the-in-app-documentation-recommended). Before installing ddtrace please make sure to install the correct Cython files for Ubuntu 18.04 and install Flask using pip first. After that, install ddtrac. Now, ddtrace should be up and running and test it using ```sh ddtrace-run ```

To run the Falsk application , I used the following command: 

``` sh
DD_SERVICE="flak" DD_ENV="flask" DD_LOGS_INJECTION=true DD_TRACE_SAMPLE_RATE="1" DD_PROFILING_ENABLED=true ddtrace-run python flaskapp.py
```
insert pics{}

To view the appliction click here.


## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

- I would like to use Datadog to monitor a mall's parking lots and spaces. I can use it to see which lots are currently busy and what’s the capacity at each lot. Due to Covid-19, contactless pickups at malls has become very popular in California. I can monitor and manage which parking spaces are occupied and if there are empty spaces next to the occupied parking space( to enforce social distancing). In addition, to help prevent crowding and the virus from spreading at the pick up locations, we can alert when a lot has reached a specific capacity. In the case of that capacity being reached, we can direct shoppers to other lots that are not as busy as the one they intended to go to when they enter the mall.
