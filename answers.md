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

I am here to apply for the support engineer at [Datadog](http://datadog.com) Sydney.


# The Challenge

## Questions

### Level 0 (optional) - Setup an Ubuntu VM

* While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. [Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.](https://www.vagrantup.com/docs/getting-started/)
>Answer: I am using macOS Sierra Version 10.12.6 for this Challenge.


### Level 1 - Collecting your Data

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

>Answer: [Sign up here](https://www.datadoghq.com/#), get a datadog account for free for 14 days.

>login, click on [_integration-Agent_](https://app.datadoghq.com/account/settings#agent/mac) in DataDog on the left column and follow the installation instructions for Mac OS X to install the Agent.

> The datadog can be installed on OS X as easily as:
```
DD_API_KEY=63ab065b2982aed65fff538ba18a93ba bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)"
```
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/Agent%20instalation%20and%20config.png" />

* Bonus question: In your own words, what is the Agent?

>Answer: The Datadog agent is a full stack data monitoring platform/software which brings data from servers, databases, tools, and services to the Datadog web interface.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

>Answer: Change direction by type _cd ~/.datadog-agent_ in terminal, then type _emacs datadog.conf_ to open and edit the configuration file. 
reference: https://docs.datadoghq.com/guides/tagging/

<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/tagging%20in%20conf%20file.png" />

After a few minutes refresh the Datadog, go to [Infrastructure - Host Map_](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false), the tags are now shown in there.


<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/tagging%20in%20host%20map.png" />


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

>Answer: I am using PostgreSQL for this part, for how to download and install the software PostgreSQL please refer to -> [Download PostgreSQL here](https://www.postgresql.org/download/)

>Find the PostgreSQL API under [_Integrations-Integrations_](https://app.datadoghq.com/account/settings), click _install_, then click on _Configuration_ tab.
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/integration.png" />

>Create a read-only datadog user with proper access to your PostgreSQL Server.
```
create user datadog with password 'password_for_datadog';
grant SELECT ON pg_stat_database to datadog;
```
>Configure the Agent to connect to the PostgreSQL server 
>Edit _conf.d/postgres.yaml_
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/postgres_yaml.png" />

>Restart the Agent

>Type _datadog-agent info_ in Terminal to check states.
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/postgreschecks.png" />

>Can also go to [_Dashboard-Dashboard List_](https://app.datadoghq.com/dash/list) to check whether it is working or not.

* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

>Answer:

_~/.datadog-agent/checks.d/randomcheck.py_

```
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

_~/.datadog-agent/conf.d/randomcheck.yaml_

```
init_config:
instances:
    [{}]
```

reference: https://docs.datadoghq.com/guides/agent_checks/

Here is a snippet that prints a random value in python:

```python
import random
print(random.random())
```

### Level 2 - Visualizing your Data

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.

>Answer: Go to [_Dashboard-Dashboard List_](https://app.datadoghq.com/dash/list), select [_Postgres_](https://app.datadoghq.com/dash/integration/postgresql?live=true&page=0&is_auto=false&from_ts=1508633477863&to_ts=1508637077863&tile_size=m) under _Integration Dashboards_, then click on _Clone Dashboard_ on the top right corner.
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/clone%20dashboard.png" />

>Click on add new graph and type _test.support.random_ in the Get then click Save.
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/new%20graph%20test_%20support_random.png" />

reference: https://docs.datadoghq.com/guides/templating/

* Bonus question: What is the difference between a timeboard and a screenboard?

>Answer: all graphs are always scoped to the same time in timeboard, but screenboard is flexible and more customisable, it can be created by drag and drop widgets.

reference: https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-

* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

>Answer: click on the camera icon on the top right of the graph and type @person
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/notification.png" />


### Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.
* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

>Answer: click on the [_setting icon - create Monitor_](https://app.datadoghq.com/monitors#create/metric?aggregator=avg&metric=test.support.random) on the top right of the graph
<img src="hhttps://github.com/jinmei612/datadog_screenshots/blob/master/upload/create%20monitor.png" />

<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/alert.png" />

reference: https://docs.datadoghq.com/guides/monitors/

* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

>Answer: select _Multi Alert_ under 2-Define the metric, has been done in the previous step.

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/alert2.png" />


* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/email%20notif.png" />


* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

>Answer: [_Monitors - Manage Downtime - Schedule Downtime_](https://app.datadoghq.com/monitors#downtime)
<img src="https://github.com/jinmei612/datadog_screenshots/blob/master/upload/downtime.png" />



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

### About Me
Mathematician, Computer Scientist, Barista, World Explorer

[My Linkedin](https://www.linkedin.com/in/mei-jin/)
