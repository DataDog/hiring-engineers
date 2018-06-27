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

If I were improving the documentation for this, I would add a troubleshooting section to the documentation that recommends using a yaml validator or linter if the tags are not appearing. I would also add an error message that makes it clear on startup that there is a parsing issue with the `datadog.yaml` file.

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed MongoDB and its integration and it is working:
![mongo](https://user-images.githubusercontent.com/17437250/42003230-6100e440-7a38-11e8-955e-1c0040ff6158.png)


## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Here is `my_metric.py`:

```
from random import randint
from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(1,1000))

```

I initially ran into some trouble with this, since I had mistakenly put my `my_metric.yaml` file in the `/checks.d` directory instead of in `/conf.d`. Based on this experience, I would improve the error message that occurs when people try to run checks that lack a .yaml file in the `/conf.d` directory. Instead of saying `Error: no valid check found`, I would raise an error that says that the file is missing from `/conf.d`.

The documentation could also benefit from an example of a yaml config file, so users can see the syntax.

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

[Link to Timeboard](https://app.datadoghq.com/dash/841769/lauras-timeboard?live=true&page=0&is_auto=false&from_ts=1529863991213&to_ts=1529867591213&tile_size=m)

The script is attached as `timeboard.py`.

There are a few things that could be improved in the documentation for the [Python wrapper for the Datadog API](https://datadogpy.readthedocs.io/en/latest/) -- it would be useful to know which versions of Python it supports, and a few more examples would be helpful.

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
