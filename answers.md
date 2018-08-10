I experimented with using Docker for this assignment at first, but then decided to use Vagrant instead, since it offered automatically synced folders. I had a little experience with Vagrant environments from an open source project that used it for a dev environment. When I was initially trying to get the environment set up, I got this error message when I ran `vagrant up`:

```
The box you're attempting to add doesn't support the provider
you requested. Please find an alternate box or use an alternate
provider. Double-check your requested provider to verify you didn't
simply misspell it.

If you're adding a box from HashiCorp's Vagrant Cloud, make sure the box is
released.

Name: ubuntu/bionic64
Address: https://vagrantcloud.com/ubuntu/bionic64
Requested provider: [:lxc]

```

I did a bit of searching to see if other people had had a similar problem, and found that if I used the command `vagrant up --provider virtualbox`, the Vagrant box would boot without errors.

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![tags](https://user-images.githubusercontent.com/17437250/42003196-38d6eece-7a38-11e8-8559-67384f5a5faf.png)


I initially had some problems with this, since I had never dealt with a .yaml file of the length of the datadog.yaml file. My tags wouldn't display at first because I wasn't indenting the tags in the config file correctly.

If I were improving the documentation for this, I would add a troubleshooting section to the documentation that recommends using a yaml validator or linter if the tags are not appearing.

To prevent the trouble I had when initially doing this exercise, I copied the existing `datadog.yaml` file and change its name to `datadog-original.yaml`so I have the original to refer to. Large `.yaml` files can be [difficult to edit and read](https://arp242.net/weblog/yaml_probably_not_so_great_after_all.html#can-be-hard-to-edit-especially-for-large-files). Since the `datadog.yaml` file is so long, it can be hard to see if lines are indented correctly.

I created a new, empty `datadog.yaml` file, into which I copy the configuration I need:

```
sudo mv datadog.yaml datadog-original.yaml

touch datadog.yaml

```
In `datadog.yaml`, I paste in the the first 10 or so lines of the old `datadog.yaml` file, with my api key and Datadog URL.

(screenshot - datadog-yaml-first)

I restart my Agent:

```
sudo systemctl restart datadog-agent

```

And refresh my Host Map, and my agent appears.

Now I can edit my `datadog.yaml` to add some tags:

(screenshot - datadog-yaml-tags)

Now I restart the agent with `sudo systemctl restart datadog-agent` and refresh the Host Map, and the tags appear:

(screenshot tags-in-host)

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose to install MongoDB, even though I don't have that much experience with it. I have the most experience with Postgres, but setting up Postgres on a Linux machine can be time-consuming.  I read the setup documentation for MongoDB and it was more straightforward than setting up Postgres.

I ran into some installation issues with MongoDB which required me to create and then change permissions on the MongoDB `/data/db` folder, which led me to this [Stack Overflow answer](https://stackoverflow.com/questions/7948789/mongod-complains-that-there-is-no-data-db-folder). I followed the instructions, created the `data/db` folder, and changed the permissions on it, and MongoDB was up and running.

Then, I set up Datadog integration.  First, I created Datadog user:

 ( screenshot create-mongodb-user)

Then, I edited `/etc/datadog-agent/conf.d/mongo.d/conf.yaml`:

(screenshot mongodb-conf-yaml )

I restarted the agent restart agent, but didn't see the MongoDB integration on the Datadog site, because of yaml errors:

yaml errors? screenshot - mongodb-yaml-error

I resolved the yaml errors, but then the mongodb check was not running:

screenshot mongodb-check-status

I restarted `mongod` and restarted Datadog Agent with `sudo service datadog-agent restart`, MongoDB appears on host:
screenshot mongodb-on-host-map
screenshot mongodb-host-map-details


created metric called my_metric and ran it:

screenshot my_metric_running_commandln

trouble with tagging/renaming my_metric - why is namespace not explained if it appears on the Host Map? It is the first thing I search for




## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Here is `my_metric.py`:

```
from random import randint
from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric.my_metric', randint(1,1000), tags=['my_metric'])


```

I initially ran into some trouble with this, since I had mistakenly put my `my_metric.yaml` file in the `/checks.d` directory instead of in `/conf.d`. Based on this experience, I would improve the error message that occurs when people try to run checks that lack a .yaml file in the `/conf.d` directory. Instead of saying `Error: no valid check found`, I would raise an error that says that the file is missing from `/conf.d`.

The documentation could also benefit from a more fleshed-out example of a yaml config file, so users can see the syntax.

In addition, I would strongly suggest changing the name of the file used in the example for the HTTP check in the documentation [here](https://docs.datadoghq.com/developers/agent_checks/) to something like `http-check.py`(and `http-check.yaml`). This is because there is a Python module called [`http`](https://docs.python.org/3/library/http.html) that `pip` depends on. When importing modules, [Python first looks in the directory from which the script is run](https://docs.python.org/3/tutorial/modules.html#the-module-search-path) -- and returns the local `http` before it finds the correct version.

Naming the file `http` doesn't initially cause problem. Until the user later tries to do something that depends on Python's `http` module, like set up a virtual environment, or install a package with `pip` in that folder.


## Change your check's collection interval so that it only submits the metric once every 45 seconds.

I did this by editing the `my_metric.yaml` file so that it specifies the collection interval:

```
init_config:

instances:
    -   min_collection_interval: 45

```
If `min_collection_interval` is not specified, the check would run about every 15-20 seconds.

### Bonus Question: Can you change the collection interval without modifying the Python check file you created?

Yes, the collection interval can be changed by changing the `min_collection_interval` in the `.yaml` configuration file.



## Visualizing Data

### Utilize the Datadog API to create a Timeboard

[Link to Timeboard](https://app.datadoghq.com/dash/884449/lauras-timeboard?live=true&page=0&is_auto=false&from_ts=1533913657499&to_ts=1533928057499&tile_size=m&fullscreen=false)

The script is attached as `timeboard.py`.

There are a few things that could be improved in the documentation for the [Python wrapper for the Datadog API](https://datadogpy.readthedocs.io/en/latest/) -- it would be useful to know which versions of Python it supports, and a few more examples would be helpful.

Since the API documentation showed the Python API being used with a package called `datadog`, I created a virtual environment, and installed the package in it.

(dd-docs-api-package)

```
virtualenv -p `which python3.6` venv
source venv/bin/activate
pip install datadog

```

I created my application key and API key per the instructions [here](https://app.datadoghq.com/account/settings#api), and ran the example Python script in the documentation.

I ran the script and it exited without an error.

Then, I tried creating a Timeboard as in the Python example in the documentation:

screenshot timeboard_py_create_first_board

I ran the script and it exited without errors. I went and checked in my Dashboards, and a new Timeboard had appeared:

screenshot Test_timeboard

Now that my script works, I can add the graphs from assignment. Since I will be adding graphs to the Timeboard, I consulted the documentation for graphing here: https://docs.datadoghq.com/graphing/.

I noticed that Graphs can be specified with JSON objects, and that the objects in the Python API scripts that define the Graphs are Python dictionaries, which are very similar to JSON objects, so I can also rely on the [documentation on defining graphs in JSON](https://docs.datadoghq.com/graphing/miscellaneous/graphingjson/) to create my script.

First, I used the Metrics Explorer to find the correct name for my metric:

screenshot: metrics_explorer_search

Based on the syntax in the documentation, I specify that my_metric will be scoped over my host, which is named `ubuntu-bionic`:

```
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric.my_metric{host:ubuntu-bionic}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"
}]

```

I ran the new script, and it appeared in my Timeboard:

screenshot: my_metric_scoped_over_host

Since I'm working with my_metric already, I am going to work on the graph that applies the rollup function to `my_metric`.  I replicated the existing graph by copying the dictionary object, ran the script, and then I had two identical graphs:

screenshot: 2_metric_function_graphs

Two identical graphs are not that useful, so I add the rollup function as described [here](https://docs.datadoghq.com/graphing/#rollup-to-aggregate-over-time). The 3600 passed to the rollup function refers to the number of seconds in an hour.

```

{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric.my_metric{host:ubuntu-bionic}.rollup(avg, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric with Rollup Function"
}

```



Now I have my_metric displayed, along with a graph that shows my_metric with the hourly rollup function applied:

my_metric_with_rollup

(The rollup graph displays one point, because the time interval for the Timeboard is set to 1 hour.)

Finally, I look in the Metrics Explorer for something interesting to display from my database with the anomaly function applied:

I find `mongodb.connections.totalcreated`, which looks like an interesting graph:

screenshot: metrics_explorer_DB

As in the previous example, I first create the graph definition, which currently displays the MongoDB metric without an anomaly function:

```
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "mongodb.connections.totalcreated{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "MongoDB Total Connections Created"
}
```

I have been using [this JSON documentation](https://docs.datadoghq.com/graphing/miscellaneous/graphingjson/) and this [documentation on graphing](https://docs.datadoghq.com/graphing), but neither page has information about anomaly functions and how to apply them.  If I were improving the documentation, I would add a more complete description of the graphing language in the page on how to use JSON to define graphs.

Since the documentation on how to define graphs with JSON does not show me the syntax for applying an anomaly function, I am going to reverse-engineer the syntax from the JSON of a graph that I create using the GUI:

screenshot: Mongodb_GUI_graph

The GUI allows me to select the anomaly function and apply it.  Now I can look at the JSON this graph uses:

screenshot: GUI_graph_JSON

And put it into my script:

screenshot: script from RE GUI

I run the script again, and the graph with the anomaly function appeared. The Timeboard is complete:

screenshot: Timeboard_final


### Bonus Question: What is the Anomaly graph displaying?

The anomaly graph uses an algorithm that compares the past behavior of a metric to its present behavior. For instance, if the database were growing in size by a constant rate, and that rate dropped off or fell unexpectedly, the anomaly monitor would alert.

## Monitoring Data
Screenshot of timeboard:
![timeboard_5m](https://user-images.githubusercontent.com/17437250/42003362-17b571ec-7a39-11e8-8476-0d61798521e0.png)

Screenshot of email:
![my_metric_messages](https://user-images.githubusercontent.com/17437250/42003385-32ec0b74-7a39-11e8-9501-0d48c23c15c1.png)

![my_metric_alert_msg](https://user-images.githubusercontent.com/17437250/42003392-3adfb470-7a39-11e8-8285-d449461972a1.png)

I would improve this by making the "preview" section in the metric setup dialog render the tags in curly braces (like {{host.name}} or {{host.ip}}). I used the syntax to display the host IP from the documentation, and it didn't display. I tried changing the syntax a bit, but I had to wait for the alarm to trigger to see if my edits worked.

### Bonus Question: Scheduled downtime
I used the web interface to schedule downtime outside of work hours and on weekends:

![weekend-downtime](https://user-images.githubusercontent.com/17437250/42003425-58e1733c-7a39-11e8-8b9d-a29b42a0dffe.png)

## APM

Here is the [link to the Dashboard](https://app.datadoghq.com/dash/846819?live=true&page=0&is_auto=false&from_ts=1530128574143&to_ts=1530132174143&tile_size=m).

Here is the Dashboard screenshot:
![apm_dashboard](https://user-images.githubusercontent.com/17437250/42003445-7053d294-7a39-11e8-81af-cff6c353cd13.png)

Here is a screenshot of the APM:
![apm_trace](https://user-images.githubusercontent.com/17437250/42003792-1a537d5c-7a3b-11e8-83bd-0a91f4decd0b.png)

The instrumented Flask app is included as `flask_apm_app.py`.

When I tried using the APM middleware on the Flask application, I initially got an error that said the following:

```
ddtrace.writer - ERROR - cannot send services to localhost:8126: [Errno 111] Connection refused

```
I also tried using the `dd-trace run` command, but that gave the same error. I found a [GitHub issue](https://github.com/DataDog/dd-trace-py/issues/132) for the error message, but it did not have any information on how to resolve the issue.

Then I tailed the logs at `/var/log/datadog/trace-agent.log` and found it was throwing the following error from parsing the `datadog.yaml` file:

```
2018-06-27 20:17:59 CRITICAL (main.go:138) - Error reading datadog.yaml: failed to parse yaml configuration: yaml: unmarshal errors:
  line 472: cannot unmarshal !!str `enabled...` into config.traceAgent

```
I fixed the issue with the `datadog.yaml` file and then it worked.


### What is the difference between a Service and a Resource?
A service is a set of processes that all do the same job. For instance, a web application could consist of a webapp service and a database service. A resource is a particular action for a given service.

## Is there anything creative you would use Datadog for?

I am a gardener, and I think it would be very interesting to have a Datadog to visualize various environmental factors that might affect my plants. Plants are sensitive to a number of environmental factors, including:

- air temperature
- soil temperature
- intensity of light
- day length
- soil fertility
- soil moisture
- soil pH
- nutrients available in soil

It would be very interesting have a dashboard that displayed this information, especially if it could be overlaid on previous years' data. It would be really neat  to get alerts if planters need water, or if the soil is warm enough to plant spring vegetables. The dashboard would allow me to keep an eye on how all my plants were doing, even if I wasn't home.

Through monitoring of these metrics, combined with manually entered data, like how much fruit or flowers a plant produced, I could determine the best plant varieties to grow in my garden, and improve the plants' growing conditions for next year by moving them to spaces in the garden that suited them better or adjusting the amount of water or nutrients in the soil around them.

A similar sort of monitoring setup would also be useful in larger-scale growing operations, such as nursery growers, farms, and botanical gardens. The use of monitoring technology is becoming more prevalent in agriculture, and Datadog's visualizations and comparisons between various metrics would be useful to farmers as well.
