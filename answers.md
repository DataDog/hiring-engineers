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





# Monitoring Data

# Collecting APM Data

# Final Question
