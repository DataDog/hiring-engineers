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

> Here's my host, it's a single Ubuntu instance I spun up on my MacBook with Vagrant.

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

![](images/my_metric_1hr_sum.png)

*`my_metric`'s value graphed over one hour*



### _Any metric from the Integration on your Database with the anomaly function applied._

> This ended up being more difficult than I originally expected. The `anomalies()` function requires the creation of a separate monitor, which requires a separate API request altogether. Although linked above, I've provided the contents of that request below for additional clarity.

monitor.json
```
{
      "type": "metric alert",
      "query": "avg(last_1h):anomalies(avg:mysql.performance.user_time{*}, 'basic', 3, direction='above', alert_window='last_30s', interval=30, count_default_zero='true', timezone='America/New_York') >= 1",
      "name": "MySQL CPU Anomaly Monitor",
      "message": "Unsual CPU activity by MySQL.",
      "tags": ["service:mysql", "host:ubuntu-xenial"],
      "options": {
        "notify_no_data": true,
        "no_data_timeframe": 20
      }   
}
```

> The important piece in the request above is the `"query"` value, which performs the actual check for MySQL's CPU anomaly (See below).
 

`avg(last_1h):anomalies(avg:mysql.performance.user_time{*}, 'basic', 3, direction='above', alert_window='last_30s', interval=30, count_default_zero='true', timezone='America/New_York') >= 1`


> So how did I incorporate this into the timeboard? I created a timeseries graph of the Percentage of CPU time spent in the user space by MySQL, and added a query to the `events` block that would return events triggered by the `MySQL CPU Anomaly Monitor` I created earlier. You can see this section of the timeseries API request below. 


timeseries.json
```
{
      "graphs" : [
...
        {
          "title": "MySQL CPU Time",
          "definition": {
              "events": [{"q": "MySQL CPU Anomaly"}],
              "requests": [
                  {"q":"avg:mysql.performance.user_time{*}"}
              ],
              "viz": "timeseries"
          }
        },
...
      ],
...
```

> The query below matches on the monitor's title and reports anomalies on the graph based on deviations from expected behavior. 

`"events": [{"q": "MySQL CPU Anomaly"}],`


> Here's what the anomaly graph actually looks like. I triggered MySQL anomalies by [running a script](scripts/select_abunch.sh) that spammed the DB with a large number of `SELECT` queries. You can see the anomalies highlighted in red on the graph below. 

![](images/anomalous_behavior.png)

*Anomalous MySQL events after executing `select_abunch.sh`*

### _Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket._

> To do this, I created an additional query value widget that added up all the datapoints over the past 3600s (last 1 hour). As recommended in the API docs, generating the JSON from the dashboard is far easier than attempting to to do it all manually. You can see the relevant JSON block for this graph below [as it appears in timeboard.json](scripts/timeboard.json#L14).

```
...  
      {
          "title": "Sum of my_metric Values Over One Hour",
          "description": "Adds up the value of my_metric over an hour in one bucket",
          "definition": {
              "events": [],
              "viz": "query_value",
              "requests": [
                {
                  "q": "sum:my_metric.value{host:ubuntu-xenial}.rollup(sum, 3600)",
                  "type": null,
                  "style": {
                      "palette": "dog_classic",
                      "type": "solid",
                      "width": "normal"
                  },
                  "conditional_formats": [
                      {
                        "comparator": ">",
                        "palette": "white_on_red",
                        "value": null
                      },
                      {
                        "comparator": ">=",
                        "palette": "white_on_yellow",
                        "value": null
                      },
                      {
                        "comparator": "<",
                        "palette": "white_on_green",
                        "value": null
                      }
                  ],
             "aggregator": "avg"
            }
          ],
          "autoscale": true
       }
...
```

> Here's what an averaged out value of this bucket looked like over the course of 4 hours.  

![](images/my_metric_1hr_sum.png)

*Query Value Widget Showing Average of `my_metric`'s 1 Hr Sum Over 4 Hours*

# Monitoring Data

# Collecting APM Data

# Final Question
