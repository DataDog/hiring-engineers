## Prerequisites
Initially, I tried completing the exercise on Ubuntu using Bash on Windows, but I ran into issues getting the agent properly reporting metrics, so I decided to try using a Vagrant VM with VirtualBox. After installing Vagrant and VirtualBox, typing `vagrant up` then `vagrant ssh` in the command line was all I needed to do to get a working Ubuntu virtual machine running on my computer.

![vm](https://dl.dropboxusercontent.com/s/ovuuhbbbjtcgfxm/cmd_2017-10-26_16-34-26.png)

After I got my virtual machine up and running, I signed up for Datadog and installed the Agent for Ubuntu using the one step install:
```
DD_API_KEY=<API key> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```
On Datadog's [infrastructure page](https://app.datadoghq.com/infrastructure), I could see that the Agent was reporting live metrics from my machine:

![infrastructure](https://dl.dropboxusercontent.com/s/pgwvp74rygkg28y/firefox_2017-10-26_16-42-43.png)

## Collecting Metrics
From the [Agent guide for Ubuntu](https://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/), I found that the Agent configuration file for Ubuntu was located at `/etc/dd-agent/datadog.conf`. I kept two of the example tags 'env:prod' and 'role:database', and added my own tag 'banana':
```
# Set the host's tags (optional)unt/settings
tags: banana, env:prod, role:database
```

After restarting the agent with `sudo /etc/init.d/datadog-agent restart`, I could see my tags when inspecting the host on the infrastructure page:

![tags](https://dl.dropboxusercontent.com/s/yo1046yzdlhrohv/firefox_2017-10-26_16-57-18.png)

I decided to install the Postgres database on my machine and install the its integration for the agent. After I installed Postgres on my machine, I navigated to the integrations page, selected the Postgres integration, and followed the instructions to create a `datadog` user on my Postgres server:

![postgres](https://dl.dropboxusercontent.com/s/p666mvj9azigkt3/firefox_2017-10-26_17-03-14.png)

Next, I edited `/etc/dd-agent/conf.d/postgres.yaml` to configure the Agent to connect to the Postgres server:
```yaml
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: <password>
    tags:
      - optional_tag1
      - optional_tag2
```

After I restarted the agent and ran `sudo /etc/init.d/datadog-agent info`, I could see that the Postgres integration was working properly:
```
 postgres (5.17.2)
    -----------------
      - instance #0 [OK]
      - Collected 10 metrics, 0 events & 1 service check
```
'postgresql' also appeared under the list of apps attached to my agent on the Infrastructure page:

![apps](https://dl.dropboxusercontent.com/s/cm993j7lppn9ly6/firefox_2017-10-26_17-09-10.png)

To create a custom agent check, I followed the guide at http://docs.datadoghq.com/guides/agent_checks/. First, I created a python file `/etc/dd-agent/checks.d/random.py` that sends a random value between 0 and 1000 as a metric called 'my_metric' from a check called 'random':
```python
from checks import AgentCheck
import random
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('random.my_metric', random.randint(0, 1000))
```

To change the collection interval for the check, I had to create a new configuration file for my check, saved as `/etc/dd-agent/conf.d/random.yaml`:
```yaml
init_config:
    min_collection_interval: 45

instances:
    [{}]
```
This set my check to submit the metric once every 45 seconds. After I restarted the agent, my custom check appeared as one of the agent's apps in the Infrastructure page:

![random](https://dl.dropboxusercontent.com/s/boholra9x4k06cl/firefox_2017-10-26_20-36-14.png)

## Visualizing Data
To use Datadog's API to create a timeboard, I first had to add an application key to my account:

![app](https://dl.dropboxusercontent.com/s/kcan4nmfo2eo8yz/firefox_2017-10-26_18-52-22.png)

Next, using an example from the [API reference](https://docs.datadoghq.com/api/?lang=console#timeboards), I created a timeboard by running a shell script that made a POST request to Datadog's API:
```sh
#!/bin/sh
# Make sure you replace the API and/or APP key below
# with the ones for your account

api_key=my_api_key
app_key=my_app_key

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [
        {
          "definition": {
            "events": []
            "requests": [
              {"q": "avg:random.my_metric{host:precise64}", "type": "line"}
            ],
            "viz": "timeseries"
          },
          "title": "my_metric"
        },
        {
          "definition": {
            "events": []
            "requests": [
              {"q": "avg:random.my_metric{host:precise64}.rollup(sum, 60)", "type": "line"},
            ],
            "viz": "timeseries"
          },
          "title": "my_metric rollup"
        },
        {
          "definition": {
            "events": []
            "requests": [
              {"q": "anomalies(avg:postgresql.percent_usage_connections{host:precise64}, 'basic', 2)",
      "type": "line"},
            ],
            "viz": "timeseries"
          },
          "title": "postgresql.percent_usage_connections anomaly"
        },
      ],
      "title": "Adisa\'s Timeboard",
      "description": "A timeboard for agent data."
      "read_only": "True"
    }' \
"https://app.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
```

This code creates a timeboard with three graphs:
* The values of the 'random.my_metric' metric I created earlier as a line graph
* The sum of the values the metric had over the past hour (using the `rollup` function)
* An anomaly graph for the `percent_usage_connections` metric from the Postgres integration.
    * The anomaly graph displays when the metric's value is outside of where it's expected to be based on past behavior.

After I created the timeboard, I accessed my dashboard online through the Dashboard List in the 'Dashboards' menu, [changed the rollup graph to 'Query Value' to display a single value](https://dl.dropboxusercontent.com/s/aopo00mn0j0urug/firefox_2017-10-26_20-31-25.png), and adjusted the board to only display the last 5 minutes by dragging on one of the graphs:

![dashboard](https://dl.dropboxusercontent.com/s/cnj6vm5msjbym7a/firefox_2017-10-26_20-16-53.png)
![dashboard](https://dl.dropboxusercontent.com/s/uptdzqj2ygn17mh/firefox_2017-10-26_19-30-12.png)

Next, I created a snapshot of one of the graphs by clicking on the camera icon above the graph:

![cam](https://dl.dropboxusercontent.com/s/wq6szp8tcw9bbwk/firefox_2017-10-26_20-33-20.png)

and sent it to myself using the @ notation:

![snapshot](https://dl.dropboxusercontent.com/s/rn30nua5jeb0xc9/firefox_2017-10-26_19-32-11.png)

## Monitoring Data

To monitor the data from my custom metric, I created a new monitor using the option in the 'Monitors' menu. Using the options available, I had the monitor track the average value of the metric over the last 5 minutes, and send an alert if the average goes over the warning threshold of 500, or the alert threshold of 800. I also had the monitor notify me if no data was received over the past 10 minutes.

![monitor](https://dl.dropboxusercontent.com/s/362nf15jy5eiuue/firefox_2017-10-26_19-39-46.png)

Next, I customized the monitor's message using the available templating options, and created different messages depending on the conditions that triggered the alert. If the monitor was triggered by the value going above the alert threshold, I had the message include the trigger value and host IP address. I also had the monitor send me an email message whenever it triggered by tagging myself with the @ notation.

![format](https://dl.dropboxusercontent.com/s/v89x012k0omtuv9/firefox_2017-10-03_17-06-23.png)

A few minutes after I created the monitor, I received my first message:

![alert](https://dl.dropboxusercontent.com/s/e4gqzwonmuahe0z/firefox_2017-10-03_17-04-53.png)

Soon, I was receiving emails from the monitor on a regular basis. To prevent my email inbox from being flooded, I used the 'Manage Downtime' menu to schedule two downtime periods for my monitor, one for every weekday from 7pm to 9am the next day, and one that silenced my monitor completely during the weekend.

![downtime](https://dl.dropboxusercontent.com/s/n86t3r7qzbwg856/firefox_2017-10-26_20-05-38.png)
![downtime](https://dl.dropboxusercontent.com/s/ycoawrvu4eqi8gf/firefox_2017-10-03_17-04-22.png)

![downtime](https://dl.dropboxusercontent.com/s/94glumzfzkyh9g6/firefox_2017-10-26_20-06-08.png)
![downtime](https://dl.dropboxusercontent.com/s/twif2p44nqfbagb/firefox_2017-10-03_17-04-12.png)

Once my monitor entered downtime, I received an email in my inbox:

![notification](https://dl.dropboxusercontent.com/s/b6jvb14ho889bwa/firefox_2017-10-03_19-40-50.png)

## Final Question
I think a potentially cool application for Datadog would be monitoring a restaurant's activity/occupancy. Depending on how much data a restaurant's systems are collecting, a restaurant could create a public board that displays how full the restaurant is, available tables, average wait time, etc. Additionally, a user could create a board that displays information about occupancy from multiple restaurants using publically available data from Foursquare, Google Maps, etc.
