In order to demonstrate some of the main features of DataDog, here is a quick run-through of how to get started on a few of them.

I assume you've already got a machine to explore the functionality on but if you don't you can spin up a VM through vagrant pretty quickly. [Instructions for that are here.](https://www.vagrantup.com/intro/getting-started/).

I'm running Ubuntu on my VM, but you can find your operating system [here](https://app.datadoghq.com/account/settings#agent) and install the agent that way.

Now that that's out of the way, let's dive in!

First and foremost, Datadog is a metrics collection tool. Everything else flows from the data that you've collected. So let's start by collecting some data.

# Collecting Metrics


Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
> See ./HostMap.png

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.


Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?
