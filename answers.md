# Datadog Solutions Engineer Technical Exercise - answers

## Prerequisites - Setup the environment

My environment for completing the exercises consisted of a 64-bit Linux Ubuntu 16.04 since I use it on a daily basis. No OS or dependency issues were encountered while completing the exercises.

![](/prerequisites/agent_installation.png)

## Collecting Metrics

1. I have added 4 tags to my Agent: #awesome_tag, #env:test, #nice_tag, #host:slazien-ThinkPad-W530

![](/collecting_metrics/host_map.png)

2. Already having PostgreSQL installed on my OS, I have then installed the relevant Datadog integration using the instructions provided here: https://docs.datadoghq.com/integrations/postgres/.

![](/collecting_metrics/postgres_datadog_user.png)

3. I have then created a custom Agent check that submits a metric named *my_metric* with a random value between 0 and 1000 (inclusive):
```python
import random

try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

__version__ = "1.0.0"

class CustomCheck(AgentCheck):
    def check(self, instance):
        self.gauge("my_metric", random.randint(0, 1000))
```

4. **Bonus question:** Can you change the collection interval without modifying the Python check file you created?
Yes! This can be done by adding a *min_collection_interval* as instance parameter to the check's .yaml configuration file ![](/collecting_metrics/bonus_min_collection_interval.png)


## Visualizing Data
1. Using the Datadog API I have created a Timeboard that contained:
- My custom metric (*my_metric* scoped over my host: *slazien-ThinkPad-W530*)
- *rows_fetched* metric from the PostgreSQL Datadog integration which measures the number of fetched rows per second. I have also applied the Anomaly function using the *basic* algorithm and set 1.2 for the number of standard deviations for the algorithm to detect anomalies
- I have also included a graph of *my_metric* and applied the rollup function to sum up all the points for the past hour:
![](/visualizing_data/timeboard_graphs.png)

2. Since the PostgreSQL graph was rather boring (oscillating between two values repeatedly), I ran an expensive query to create a spike in the *rows_fetched* graph and sent a 5-minute snapshot to my email:
![](/visualizing_data/timeboard_graph_snapshot.png)

3. **Bonus question:** What is the anomaly graph displaying?
- In the screenshot above, the timeseries graph is displaying that around 18:03 a spike i rows fetched occurred, which surpassed the set standard deviation of 1.2. Graphs like this one are very useful since they allow us to detect events which we would not normally expect to happen (based on historical data). In this particular scenario, a sudden increase in the number of rows fetched could indicate that someone has just run an read-intensive query such as *SELECT * FROM table_name;*, where the table contained a large number of rows.
- In general, an Anomaly graph allows to, quite simply, detect anomalous values of metrics, based on historical context.t Examples of very valuable, yet also very variable metrics include application throughput, web requests or user logins. Such metrics might exhibit seasonal patterns (e.g. increased login rate in the evenings) or show a trend (e.g. monotonically increasing number of web requests due to a rapidly growing user base of a high-growth startup)

## Monitoring Data
1. I have created a Metric Monitor which monitors the average of my_metric and has the following states:
- Alert threshold of 800
- Warning threshold of 500
- Notification when No Data over the past 10 minutes

2. The message has been configured as follows:
- Send an email upon a Monitor trigger
- Send a different message depending on monitor state (Alert, Warning, No Data)
- Report metric value and host IP when in Alert state

Here is a screenshot of my Monitor's configuration:
![](/monitoring_data/monitor_config.png)

... of one of the emails I received from the Monitor after it was triggered:
![](/monitoring_data/monitor_trigger_email.png)

... of daily 7pm-9am silencing:
![](/monitoring_data/downtime_7pm.png)
![](/monitoring_data/downtime_9am.png)

.. and, finally, of weekend silencing:
![](/monitoring_data/downtime_weekend.png)

## Collecting APM data
1. 
