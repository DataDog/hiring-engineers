# Collecting Metrics

## Add tags in the Agent config file.

> Here are my host tags as they are configured in `/etc/datadog-agent/datadog.yaml`
```
...
# Set the host's tags (optional)
tags:
   - owner:mlupton
   - env:sandbox
...
```

## Show us a screenshot of your host and its tags on the Host Map page in Datadog.
### `ubuntu-xenial`

![](images/host_with_tags.png)

*Screenshot of Host from Host Map With Custom Host Tags `#env:sandbox`, and `#owner:mlupton`*


## Bonus Question - Can you change the collection interval without modifying the Python check file you created?

> Yes, it is possible to do this by creating a custom check config file for the check you've created. In my case, I created a directory at `/etc/datadog-agent/conf.d/my_check.d/`, where I stored a check file called `mycheck.yaml`. See the contents of this file below:
```
init_config:

instances:
  - min_collection_interval: 45
``` 


# Visualizing Data

## Utilize the Datadog API to create a Timeboard.

> I used the [script here](scripts/my_metric-timeboard.sh) to issue two separate `POST` requests. One [to create the timeboard](scripts/timeboard.json) itself, and the other [to create the anomaly monitor](scripts/monitor.json) for MySQL's CPU usage. Below are the details as they relate to the bullet points listed in the exercise. 


### _Your custom metric scoped over your host._

> The graph below is a screenshot of the custom metric, `my_metric`  being graphed as a timeseries. 

![](images/my_metric_timeseries.png)

*`my_metric`'s value graphed over one hour*



### _Any metric from the Integration on your Database with the anomaly function applied._

> This ended up being more difficult than I originally expected. The `anomalies()` function requires the creation of a separate monitor, which requires a separate API request altogether. Although linked above, I've provided the contents of that request below for additional clarity. The query that actually performs the anomaly check is highlighted

monitor.json
```
{
      "type": "metric alert",
      "query": `**`"avg(last_1h):anomalies(avg:mysql.performance.user_time{*}, 'basic', 2, direction='above', alert_window='last_30s', interval=1, count_default_zero='true', timezone='America/New_York') >= 1"`**`,
      "name": "MySQL CPU Anomaly Monitor",
      "message": "Unsual CPU activity by MySQL.",
      "tags": ["service:mysql", "host:ubuntu-xenial"],
      "options": {
        "notify_no_data": true,
        "no_data_timeframe": 20
      }
}
```

> So how did I incorporate this into the timeboard? Within my 

# Monitoring Data

# Collecting APM Data

# Final Question
