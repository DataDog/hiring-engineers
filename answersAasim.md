Your answers to the questions go here.
# About Datadog
Datadog is a data monitoring service for cloud-scale applications, bringing together data from servers, databases, tools, and services to present a unified view of an entire stack. These capabilities are provided on a SaaS-based data analytics platform. [Wiki](https://en.wikipedia.org/wiki/Datadog)

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

<a href="http://www.flickr.com/photos/alq666/10125225186/" title="The view from our roofdeck">
<img src="http://farm6.staticflickr.com/5497/10125225186_825bfdb929.jpg" width="500" height="332" alt="_DSC4652"></a>


# The Challenge

## Questions

### Level 0 (optional) - Setup an Ubuntu VM

* While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. [Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.](https://www.vagrantup.com/docs/getting-started/)

>Answer: I am using macOS High Sierra Version 10.13.3 for this challenge, and I have installed VM via Vagrant, as well.


### Level 1 - Collecting Metrics

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

>Answer: Website Url to create account: https://app.datadoghq.com/account/login?next=%2F

<img src="./images/Profile.png" alt="Display of profile" />

>Once you have logged in then you are prompte to install the DataDog Agent, and I utilized the macOS integration. 

> The command for installing DataDog was 
<!-- DD_API_KEY=ba43f5ff300b9342eb4d993e32500157 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)" -->

<img src="./images/display" alt="Installation and Configuration completion" />


* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

>Answer: Within the terminal change your directory to the DataDog Agent by typing _cd ~/.datadog-agent_ , then I used my text editor to make changes to the configuration file (datadog.yaml). 

<img src="./images/tags" alt="Tags being uncommented in text editor" />

Refresh your DataDog page, and use the navigation bar to go to the Infrastructure tab followed by the Host Map, and here you should be able to see your tags if you search in the "Filter By" column.


<img src="./images/display_tags" alt="All of the tags I have created" />


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

>Answer: I utilized PSQL database integration as an example for this part of the excercise. 

>Initially, I went to the Integrations tab and there I was able to see the configurations needed to integrate the DataDog Agent with PostgreSQL. 

<img src="./images/psql" alt="Terminal installing datadog as a user" />

>Create a read-only datadog user with proper access to your PostgreSQL Server.

```
create user datadog with password 'Given By DataDog';
grant SELECT ON pg_stat_database to datadog;
```
>Configure the Agent to connect to the PostgreSQL server 
>Edit _conf.d/postgres.yaml_

<img src="./images/postgresconnection" alt="PostgreSQL connection OK" />

>You need to restart the agent in order for the integration to take place. 

>I ran a test using 'datadog-agent check postgres', and it gave me confirmation that the integration was working correctly.

<img src="./images/psql_check" alt="PSQL Check" />

>Followed by this I checked on the dashboard within DataDog and was able to confirm that the PSQL metrics were displaying

<img src="./images/PSQL_metrics" alt="PSQL Metrics on DataDog Dash" />

* Write a custom Agent check that samples a random value. Call this new metric: `my_metric`

>Answer: Both of these check files will need to be placed in two directories. First, we will need to navigate into the datadog agent directory. There we will need to add a my_metric.py for our check followed by a yaml file in the conf.d. 

> First we would place a file within the Checks directory in Datadog (~/.datadog-agent/checks.d). 

```
from random import randint
random_number = randint(0,1000)
print random_number

from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random_number)

```

>Second the other directory which we would be placing the YAML file in would be the Conf.d or the configuration portion where there would also be explicit instances being described. I understood that we could add minimum intervals here but it was quite challenging. Unfortunately, my instances area often would give me an error. (~/.datadog-agent/conf.d/my_metric.yaml)

```
init_config:
instances:
    [{}]
```

<img src="./images/gui" alt="Check for Custom Metric" />
<img src="./images/bash" alt="Check within Command Line" />


Bonus Question: Can you change the collection interval without modifying the Python check file you created?

>Answer: I thought about iterating over an array within the Python portion and having a time.sleep(45) in order to only have a value display every 45 seconds but this seems to be the only solution for this. I see the min_interval within the YAML file in instances but on the docs it says that this is not necessarily utilized to have the Agent collect every 45 seconds. 

### Level 2 - Visualizing your Data

* Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket


>Answer: This part was interesting I found it quite straight forward to map the Timeboard 
over the host, and if you look in initializeTimeboard3.curl it shows the CURL commands I used to initiate the Timeboard. The next portion I tackled was the rollup function applied to the sum of allpoints I utilized the following requests within the graph. 

{
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 60)",
      },
      "conditional_formats": []
    }
  ],
}

> Finally, I applied the anonmaly function to the PSQL Row's Returned metric. I was able to do this with the following query. 

{
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 60)",
      },
      "conditional_formats": []
    }
  ],
}

<img src="./images/custom_metrics" alt="All of the custom metrics within the dashboard discovery"/>

Once this is created, access the Dashboard from your Dashboard List in the UI:
Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.

The Timeboard's timeframe is set to 5 minutes, and it is displaying the correct metrics. 
Regarding the snapshot of the graph, I have went into the share tab within the graph and created 
embedded code, as I could not find the @ notation to send it to myself. I have provided the code below:

<iframe src="https://app.datadoghq.com/graph/embed?token=259c7d8e2e1ca75617b9351f5102af8144898c8790f9e301117ff334baf3b9ea&height=300&width=600&legend=false" width="600" height="300" frameborder="0"></iframe>

<img src="./images/custom_met_5min" alt="All of the custom metrics within the dashboard discovery"/>
<img src="./images/embedded_graph" alt="All of the custom metrics within the dashboard discovery"/>

* Bonus Question: What is the Anomaly graph displaying?

>Answer: The anomaly graph is displaying the predictable patterns within the graph. Though anomaly 
detection requires a large amount of data in order to function.  If we look specifically 
at the anomalies within the graph for my_metric we can see the gray background which is beginning to display the anomalies, but as the data grows the trends could change. 

 
### Level 3 - Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.

<img src="./images/metric_monitor" alt="Made an alert based on the custom metric created by myself"/>
<img src="./images/metric_alert" alt="Email sent to me by the monitoring alert"/>

Bonus: I went on tab for Managing Downtime for Monitors and I was able to configure the alerts for the weekdays between 7:00pm and 9:00am, as well as turning the monitor off for the weekend. 

<img src="./images/downtime_monitor_week" alt="Made a downtime alert for the week"/>
<img src="./images/downtime_monitor_weekend" alt="Email sent to me by the monitoring downtime alert for the weekend"/>

### Level 4 - Collecting APM Data 




## Instructions
If you have a question, create an issue in this repository.

To submit your answers:

1. Fork this repo.
2. Answer the questions in `answers.md`
3. Commit as much code as you need to support your answers.
4. Submit a pull request.
5. Don't forget to include links to your dashboard(s), even better links *and* screenshots.  We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](http://docs.datadoghq.com/overview/)
* [Guide to graphing in Datadog](http://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](http://docs.datadoghq.com/guides/monitoring/)

### The Datadog Agent and Metrics

* [Guide to the Agent](http://docs.datadoghq.com/guides/basic_agent_usage/)
* [Writing an Agent check](http://docs.datadoghq.com/guides/agent_checks/)

### Other questions:
* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)

