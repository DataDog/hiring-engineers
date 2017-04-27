
# Overview

* [Datadog Agent](#Datadog-Agent)
  * [Example Ubuntu Installation](#Example-Ubuntu-Installation)
* [Collecting Data](#Collecting-Data)
  * [Tags](#Tags)
* [Integrations](#Integrations)
  * [Example MongoDB](#Example-MongoDB)
* [Custom Checks](#Custom-Checks)
  * [Example Agent Check](#Example-Agent-Check)
* [Timeboards](#Timeboards)
* [Screenboards](#Screenboards)
* [Notifications](#Notifications)
* [Monitors](#Monitors)
  * [Example Monitor](#Example-Monitor)
* [Downtime](#Downtime)
  * [Example Downtime](#Example-Downtime)
* [Links](#Links)
  * [Agent](#Agent)
  * [KBA](#KBA)
  * [Example Configs](#Example-Configs)
  * [Custom Tools](#Custom-Tools)


# Datadog Agent 

An open source customizable application that lives on each host relaying various events and time-series data to datadog for visualization; such as system and application performace metrics, aggregated log parsing and custom user created checks.

* Agent Source Code: https://github.com/DataDog/dd-agent

## Example Ubuntu Installation
* https://app.datadoghq.com/account/settings#agent

```
$ DD_API_KEY=[secret] bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```

# Collecting Data

Basic system metrics begin flowing into your Datadog account after setup. Several features are available to provide further meaning into your environment.

## Tags

Use the power of tags for locating and grouping metrics.

* Added automatically through integrations
* Created using the API
* Configured in the agent configuration

![alt text](images/tags_agent.png "Tags agent config")

* Editable in the UI for hosts

![alt text](images/tags_ui.png "Tags host UI")

# Integrations

Datadog comes with several [Integrations](https://www.datadoghq.com/product/integrations/) that make installation a snap and add dashboards out of the box so you can visualize meaningful data instantly. 

## Example MongoDB

* Add the Datadog integration
![alt text](images/integrations_menu.png "Integrations Menu")
![alt text](images/integrations_setup.png "Integrations Setup")

* Install MongoDB on an instance
  * [Ansible MongoDB](ansible/mongo.yaml) 

```
$ ansible-playbook -i [ip_address], mongo.yaml
```

* Check for successful installation

![alt text](images/info_mongo.png "Info mongodb check")

# Custom Checks

You may find use cases that require the collection of metrics not already provided by Datadog's many functions and Integrations. Custom [Agent Checks]( http://docs.datadoghq.com/guides/agent_checks/) have the ability to run personalized scripts to meet these requirements.

## Example Agent Check

* Create the script `/etc/dd-agent/checks.d/random.py`

```python
from random import random

from checks import AgentCheck

class RandomMetric(AgentCheck):
    """sends a random number > 0 < 1"""

    def check(self, instance):
        self.gauge('test.support.random', random())
```

* Each check requires a config with the same name `/etc/dd-agent/conf.d/random.yaml`

```yaml
init_config:

instances:
    [{}]

```

* Restart the agent and confirm the installation

```
$ sudo /etc/init.d/datadog-agent restart && sudo dd-agent info
```

![alt text](images/info_check.png "Info random check")

# Timeboards

* Are laid out in a grid and good for analysing events during a specific window of time
* Graphs and widgets share a common time frame
![alt text](images/timeboard_show.png "Timeboard Time Selector")

* Available widgets: Timeseries, Query Value, Heat Map, Distribution, Top List, Change, Hostmap
![alt text](images/timeboard_widgets.png "Timeboard Widgets")

# Screenboards

* Screenboards allow widgets to specify different time frames 
* providing flexibility of placement and widget size.
* Available widgets: Free Text, Graph, Query Value, Toplist, Change, Event Timeline, Event Stream, Image, Note, Alert Graph, Alert Value, IFrame, Check Status, Hostmap

![alt text](images/screenboard_widgets.png "Screenboard Widgets")

# Notifications

* Share findings from graphs in Timeboards and Metrics Explorer

![alt text](images/annotate_icon.png "Annotation Icon") 
![alt text](images/annotation.png "Annotation") 

* Use @name to send an email notification

![alt text](images/snapshot_comment.png "Snapshot Comment")

# Monitors

Datadog provides Monitors for alerting on metrics

## Example Monitor

![alt text](images/monitors_menu.png "Snapshot Comment")
![alt text](images/monitor_metric.png "Snapshot Comment")

* Simple Alerts fire once when the conditions you set match while Multi Alerts will alert for each member of the provided grouping tag

![alt text](images/bonus_multi_alert.png "Multi Alert")

* Provide a meaningful message so receipients can understand the event and take action if needed

![alt text](images/alert_config_message.png "Alert Message Config")

# Downtime

Downtime allows for the suppresion of alerts while performing maintenance and deployments or to remove noise and mitigate alert fatigue.

## Example Downtime

* Alerts from a POC environment are not required outside normal business hours, let the team get some sleep

![alt text](images/downtime_config.png "Downtime configuration")

* By using @name again you can send notifications when a Downtime is configured
![alt text](images/alert_downtime.png "Alert Suppression/Downtime")

# Questions?


# Links

## Agent
* https://github.com/DataDog/dd-agent

## KBA
* [Agent Settings](https://app.datadoghq.com/account/settings#agent)
* [Guide to Tagging](http://docs.datadoghq.com/guides/tagging/)
* [Integrations](http://docs.datadoghq.com/integrations/)
* [Writing an Agent Check](http://docs.datadoghq.com/guides/agent_checks/)
* [Guide to Monitors](http://docs.datadoghq.com/guides/monitors/)
* [Downtime](https://www.datadoghq.com/blog/mute-datadog-alerts-planned-downtime/)
* [Screenboard vs Timeboard](https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-)
* [Converting Dashboards](https://help.datadoghq.com/hc/en-us/articles/211244183-How-to-Transform-a-Timeboard-to-a-Screenboard-or-vice-versa)

## Example Configs
* [Terraform Instance](terraform/)
* [Ansible Resources](ansible/)

## Custom Tools
* https://github.com/DataDog/Miscellany
* https://github.com/DataDog/Miscellany/pull/12


```python

```
