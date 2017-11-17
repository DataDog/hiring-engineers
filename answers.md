## Collecting Metrics

### Tags
![Tags](/imgs/tags.png)
Added the tags:
- #mytag,
- #env:prod,
- #role:database

### Database Integration
![PostgreSQL Database Integration](/imgs/postgres.png =250x)

### Custom Agent Check
![Custom Agent Check](/imgs/my_metric.png =250x)

~/.datadog-agent/conf.d/my_metric.yaml
```
init_config:
  # submits metric once at most, every 45 seconds
  min_collection_interval: 45

instances:
    [{}]
```

~/.datadog-agent/checks.d/my_metric.py
```
import random
from checks import AgentCheck

class myMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1001))
```

**Bonus** -- How to change collection interval without modifying the Python check file:

In the Agent Config file, configure the `collector_profile_interval` setting.

```
collector_profile_interval: 45
```
## Visualizing Data

### Custom Metric Scoped Over Host
Using the Datadog API guides, Postman, and the Postman API Collection, I made a POST request to `https://app.datadoghq.com/api/v1/dash?api_key={MY_API_KEY}&application_key={MY_APP_KEY}` with the following payload:
```
{
    "graphs" : [{
        "title": "Custom Metric (Random Number from 1 - 1000)",
        "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:my_metric{host:Fannys-MacBook-Air.local}.rollup(sum, 3600)",
                "type": "line",
                "conditional_formats": []
            }
        ]},
        "viz": "timeseries",
        "autoscale": true
    }, {
        "title": "PostgreSQL Requests",
        "definition": {
        "events": [],
        "requests": [
            {
                "q": "anomalies(avg:postgresql.rows_inserted{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }, {
                "q": "anomalies(avg:postgresql.rows_deleted{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }, {
                "q": "anomalies(avg:postgresql.rows_fetched{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }, {
                "q": "anomalies(avg:postgresql.rows_updated{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }, {
                "q": "anomalies(avg:postgresql.rows_returned{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }]
        },
        "viz": "timeseries",
        "autoscale": true
    }],
    "title" : "Solutions Engineer",
    "description" : "Dashboard monitoring custom metrics and PostgreSQL requests",
    "read_only": "True"
}
```
In the payload of the Timeboard POST request, I made two graphs.
1. My Custom Metric, with the rollup function, `.rollup(sum, 3600`), applied to sum up all the points for the past hour. To scope the metric over my host, I added a template variable from the UI. The Timeseries graph charts the sum at each over hour, over time.
2. The Postgres Database with the anomaly function, `anomalies(avg:postgresql.rows_inserted{host:Fannys-MacBook-Air.local}, 'basic', 2)`, applied.

![5 Minute Snapshot of Timeboard](/imgs/5min_snapshot.png = 250x200)

**Bonus** What is the Anomaly graph displaying?
The Anomaly algorithm and graph identifies when a metric is behaving differently than it has in the past and takes into account seasonal day-of-week and time-of-day trends. For example, if a metric is unusually high or low during a given time period. The data points that are unusually high or low are shaded a different color from the rest of data points. I used the "Basic" anomaly function, which has a simple computation to determine the expected ranges. I also set a bound of 2, which is like the standard deviation to determine the extent of the normal points.

![PostgreSQL Database with Anomalies Function Applied](/imgs/postgres_anomalies.png =250x200)
* The top line is measuring the rows_returned metric, the yellow shaded portions represent the anomaly points and the purple portions represent the normal points.
* The bottom line is measuring the rows_fetched metric, the pink portions represent the anomaly points, and the yellow portions represent the normal points.


## Monitoring Data

Made POST request to the Create Monitor Datadog API, `https://app.datadoghq.com/api/v1/monitor?api_key={MY_API_KEY}&application_key={MY_APP_KEY}` with the following payload:

{
      "type": "metric alert",
      "query": "avg(last_5m):my_metric{host:Fannys-MacBook-Air.local} > 800",
      "name": "My Metric",
      "message": "{{#is_alert}} My metric is too high! Average over 800. @hello@fanny-jiang.com {{/is_alert}} {{#is_warning}} My metric is OK but getting high. Average over 500. @hello@fanny-jiang.com {{/is_warning}} {{#is_no_data}} My metric is not sending any data. Run status check. @hello@fanny-jiang.com {{/is_no_data}} ",
      "tags": [],
      "options": {
      	"notify_no_data": true,
      	"no_data_timeframe": 10,
      	"thresholds": {"critical": 800, "warning": 500}
      }
}

*BONUS* Scheduled Downtime
Made a POST request to the Datadog API with the following query: `https://app.datadoghq.com/api/v1/downtime?api_key=3f28739dc9067d3da8817cf5efd5859e&application_key=2e01db942359226940704dc5ec70d3676af6a669&start=1510704000&end=1510754400&type=weeks&period=1&week_days=Mon,Tue,Wed,Thu,Fri&scope=host:Fannys-MacBook-Air.local&message=Scheduled%20weekdayß%20downtime%20@hello@fanny-jiang.com`

This sets a downtime between 7pm and 9am on weekdays, repeating weekly.

For a downtime all day Saturday and Sunday, I made a POST request with the following: `https://app.datadoghq.com/api/v1/downtime?api_key=3f28739dc9067d3da8817cf5efd5859e&application_key=2e01db942359226940704dc5ec70d3676af6a669&start=1510981200&end=1511067600&type=weeks&period=1&week_days=Sat,Sun&scope=host:Fannys-MacBook-Air.local&message=Scheduled%20weekend%20downtime%20@hello@fanny-jiang.com`