# Answers

## Prerequisites

### Setup

I chose to use Docker since containers are much more lightweight than VMs. To do this, I created a container using the `datadog/agent` image, and followed Datadog's [Docker setup documentation](https://docs.datadoghq.com/agent/basic_agent_usage/docker).

Afterwards, I installed [Datadog Agent v6](https://app.datadoghq.com/account/settings#agent/mac) on my host machine, which runs OS X.

## Collecting Metrics

### Adding tags and visualizing on the Host Map page
To add host tags, I needed to edit the config file then verify that the tags were properly added by checking the web UI. I used vim to open `~/.datadog-agent/datadog.yaml` (which is a symlink to the real location in `/opt/datadog-agent/`) and added the following lines:

```yaml
tags:
  - testtag1
  - env:prod
  - name:johanan_lai
  - role:database:mysql
```

I then checked the my Host Map page on Datadog's web UI to make sure that the tags showed up in the "Tags" section when inspecting my host machine.

![1_tags](./screenshots/1_tags.png)

### Installing a database and Datadog integration

For this part, I chose to use MySQL, since I am more familiar with it than other databases. I spun up a MySQL Docker instance with

```bash
docker run --name mysql01 -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:5.6
```

and used `telnet localhost 3306` to ensure that the Datadog Agent would be able to connect to my container, a quick "sanity check" to verify the Docker container had the port exposed correctly.

Then, I connected to my MySQL container and set up the server according to the instructions [here](https://docs.datadoghq.com/integrations/mysql/). However, the agent gave me an error saying that it "Can't connect to MySQL server". I tried:

* Using different MySQL versions/images
* Changing the `server` IP in the `conf.yaml` file from `127.0.0.1` to `localhost`, `172.17.0.1`
* Granting all privileges to the `datadog` user as a last resort

but to no avail.

After some struggling, I found out that this was an issue specific to Docker, and that I had to change all instances of `localhost` to the IP address endpoint of my MySQL container, which I got promptly using `docker inspect mysql01`.

For example, instead of

```sql
mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
```

I used

```sql
mysql> GRANT PROCESS ON *.* TO 'datadog'@'172.17.0.1';
```

To confirm that the agent was now correctly getting metrics from my MySQL container, I checked the status of the agent with `datadog-agent status | grep mysql`, double-checking by looking at whether it showed up on both the Host Map page and the agent web UI.

![2_mysql](./screenshots/2_mysql.png)

![3_mysql](./screenshots/3_mysql.png)

### Creating a custom Agent check and changing the interval

The last part of this section required me to write a custom agent check. I headed over to the [agent documentation](https://docs.datadoghq.com/developers/agent_checks/) which showed a simple example check, which I modified to send a random value between 0 and 1000. To do this, I needed to create two files, `conf.d/mymetric.yaml` and `checks.d/mymetric.py`.

For `conf.d/mymetric.yaml`:

```yaml
init_config:

instances:
    [{}]
```

For `checks.d/mymetric.py`:

```python
from checks import AgentCheck
from random import randint

class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000))
```

I quickly checked that this was working by filtering by `my_metric` in the web UI:

![4_mymetric](./screenshots/4_mymetric.png)

The graph looked fine, but I let it run a little longer to ensure that the value never went outside the range of 0 to 1000.

I also needed to change the collection interval to be at least 45 seconds, which I did by modifying `conf.d/mymetric.yaml`:

```yaml
init_config:

instances:
    - min_collection_interval 45
```

**Bonus Question:** Editing the config file allows me to avoid having to change the Python check file and hardcode it to send a metric once every 45 seconds.

Once again, I verified that the interval had correctly changed by checking the graph in the web UI:

![5_mymetric45](./screenshots/5_mymetric45.png)

The width between each value in the graph increased, so it was quite clear the minimum interval had been successfully changed to 45, since the default is 15-20 seconds.

## Visualizing Data

### Creating a Timeboard using DataDog API

I decided to use Python, the language I am the most familiar with, to create a timeboard. First, however, I had to install the [DataDog Python library](https://github.com/DataDog/datadogpy), which I did with `pip install datadog`.

Next, using the [Python API docs](https://docs.datadoghq.com/api/?lang=python#timeboards), I modified the API request example to display my custom metric on the timeboard, which I did through

* Creating an application key [here](https://app.datadoghq.com/account/settings#api) and copying both API keys to my timeboard Python file
* Getting the name of my host with `datadog-agent status | grep host` to put in `template_variables` 
* Editing the `graphs` variable to include the 3 metrics to be shown on the timeboard

To learn the syntax for requesting metrics, I played around with the JSON editor in the web UI (pictured below), which made it much easier to edit in vim.

![6_JSONeditor](./screenshots/6_JSONeditor.png)

The request for displaying `my_metric` scoped over my host was as simple as

`{"q": "avg:my_metric{host:Prestige.local}"}`.

though at first, I had unknowingly averaged by host instead of scoping it over my host machine by writing

`{"q": "avg:my_metric{*} by {host}"}`.

While the graphs looked identical on the timeboard in the web UI, I realized this subtle mistake through the JSON editor, which had two separate inputs, one for "from" and one for "avg by"; the former was what I was supposed to be using to scope the metric over my host machine.

For graphing a metric from my MySQL integration, I chose bytes sent, since it would show data without the need for me to do anything else. I then applied `anomalies` using the [anomaly documentation](https://docs.datadoghq.com/monitors/monitor_types/anomaly/), which looked like this:

`{"q": "anomalies(mysql.performance.bytes_sent{*}, 'basic', 3)"}`

Lastly, I had to sum up all of the values of `my_metric` into 1-hour buckets. I did this with the help of the [rollup function docs](https://docs.datadoghq.com/graphing/#aggregate-and-rollup), once again using the JSON editor to verify that my request was formatted correctly:

`{"q": "avg:my_metric{host:Prestige.local}.rollup(sum, 3600)"}`

I ran the file with `python timeboard1.py` and checked the timeboard in the web UI to see whether all 3 metrics were correctly displayed.

![7_timeboard1](./screenshots/7_timeboard1.png)

### Modifying my Timeboard from the web UI

At first, I could not figure out how to customize the timeframe beyond 24 hours; I tried using the "Select Range" option at the top of the timeboard, but it did not go any smaller than the same day. I also tried to edit the URL and change the timestamps manually by making `from_ts` and `to_ts` 300 seconds apart, but it did nothing.

Before long, I clicked the keyboard icon, which showed that the shortcut ALT + ] would tighten the timeframe.

![8_timeboard_shortcut](./screenshots/8_timeboard_shortcut.png)

I used this to make the timeframe of my timeboard to be the past 5 minutes:

![9_timeboard2](./screenshots/9_timeboard2.png)

While there was no option to send a snapshot of my entire timeboard (since the exercise instructions are unclear about which graph to @ myself with), I could [@ myself](https://docs.datadoghq.com/monitors/notifications/#mentions-in-slack-from-monitor-alert) with a single graph of a metric, so I chose the MySQL bytes sent anomaly graph by clicking the camera icon at the top right of the graph and @ing myself in an annotation.

![10_at_notation](./screenshots/10_at_notation.png)

As expected, I received an email with the annotation a screenshot of the graph I was tagged in.

![11_at_notation_email](./screenshots/11_at_notation_email.png)

**Bonus Question:** The anomaly graph displays a metric, with anomalous values colored red and normal values colored blue. Anomalous values are determined by previous metric values and patterns, which helps alert the owner of unusual behavior that might be difficult to notice without analyzing past metric trends.

The script for creating the timeboard is included in the project as `timeboard1.py`.

## Monitoring Data

### Creating a Metric Monitor

To create a new metric monitor, I clicked the "New Monitor" option in the web UI and created a new metric monitor.

![12_new_monitor](./screenshots/12_new_monitor.png)

There, I specified the alert and warning thresholds to be 800 and 500 respectively, and I checked the option to notify if there was no data for the past 10 minutes.

![13_monitor1](./screenshots/13_monitor1.png)

Next, I configured it to email me whenever the monitor triggered, using the `{{var}}` syntax to send me a different message in the case of an alert, a warning, or no data. In the case of an alert, I also included the metric value and the host IP. 

![14_monitor2](./screenshots/14_monitor2.png)

I received an email shortly afterwards, as `my_metric` had gone over 500, so I received the appropriate warning message.

![15_monitor_email1](./screenshots/15_monitor_email1.png)

### Scheduling downtimes for the monitor

**Bonus Question:** To avoid excess monitor notification emails, I set up 2 downtimes as described in the exercise, again doing this through the web UI with "Manage Downtime"; I scheduled both downtimes to be recurring once a week on Mon-Fri and Sat-Sun respectively.

![16_monitor_downtime1](./screenshots/16_monitor_downtime1.png)

![17_monitor_downtime2](./screenshots/17_monitor_downtime2.png)

Lastly, I checked that I was notified through email that a downtime was scheduled:

![18_downtime_email1](./screenshots/18_downtime_email1.png)

## Collecting APM Data

### Instrument a Flask app

To learn how Datadog's APM solution worked, I followed the [instructions in the web UI](https://app.datadoghq.com/apm/intro), installing `ddtrace` and `blinker`. I then ran the provided Flask app with `ddtrace-run python flaskapp1.py`.

Upon running the command, however, I got the following error:

```bash
ERROR:ddtrace.writer:cannot send services to localhost:8126: [Errno 61] Connection refused
```

From Datadog's [docs about tracing on Docker apps](https://docs.datadoghq.com/tracing/setup/docker/), I found out that I had to pass an environment variable and expose port 8126 during `docker run`, meaning I had to remove and rerun my agent container. I used

```bash
docker run -d -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -e DD_API_KEY=<YOUR_API_KEY> \
              -e DD_APM_ENABLED=true \
              -p 8126:8126/tcp
              datadog/agent:latest
```

and this time, ddtrace worked correctly:

![19_ddtrace_cmdline](./screenshots/19_ddtrace_cmdline.png)

However, for some reason, the APM page on the web UI never updated, and remained on the install page:

![20_apm_install_page](./screenshots/20_apm_install_page.png)

This may be due to

* A bug with the Dockerized agent or
* Not showing due to my Datadog trial expiring
* Me incorrectly implementing the Flask app

though I strongly believe it is a bug due to the Dockerized agent, as the command line showed that ddtrace was successfully tracing my Flask app. I was also able to graph APM metrics in [my timeboard I created](https://app.datadoghq.com/dash/855394/apm-flask-app-timeboard), which I made from cloning my agent container infrastructure timeboard and adding 2 additional APM metrics.

![21_apm_timeboard](./screenshots/21_apm_timeboard.png)

The instrumented app is included in the project as `flaskapp1.py`.

**Bonus Question:** [This help article](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-) on the Datadog site describes the differences between services and resouces.

A **service** is a set of processes that implement a feature, such as a databse. In the case of my app, ddtrace tracked 2 services.

A **resource** is a query to a service, such as the query to a SQL database.

The resources of a particular service can be seen by clicking on it in the APM section of the web UI, though I was unable to do so due to the issue described above.

## Final Question

### What would you use Datadog for?

I play a online strategy card game called **Hearthstone**, where the game's "meta" - the optimal, popular strategies and decks at the moment - to change as new cards are released. As such, to stay on top of the competition, players must react to changes in the meta quickly and adapt in order to capitalize on strong decks before the majority of players react to this meta change, lowering the effectiveness of new meta decks (as they are able to prepare better against meta decks once they are discovered).

Fortunately, a large group of the game's playerbase track their game data, allowing people to access heaps of match data and deck information. Whenever a small group of players begin experimenting with a particular deck archetype that becomes very successful, this adds to the tracked data subtly; this data can be processed and analyzed to discover trending, upcoming decks before a majority of the population can detect these soon-to-be meta decks themselves. With Datadog, I would be able to use features like the anomaly function to find decks that perform unusually well despite a low sample size much earlier than most people would be able to by looking at metrics such as winrate spikes.

