In order to demonstrate some of the main features of DataDog, here is a quick run-through of how to get started on a few of them.

To get started you'll need a couple of things.

First, you'll need a machine to work on. You can [install a VM with vagrant](https://www.vagrantup.com/intro/getting-started/) pretty quickly if you don't want to get your personal machine too messy.

Next, sign up for a trial at the [Datadog website.](https://app.datadoghq.com/signup)

Finally you'll have to install a datdog agent onto the machine you're working with. I'm running Ubuntu on my VM, but you can find your operating system [here](https://app.datadoghq.com/account/settings#agent) and install the agent that way. This agent will report the metrics you configure to the Datadog website and you'll be able to view the data there after logging in. 

If you have any trouble with that last step you can refer to [the excellent datadog docs and guides.](https://docs.datadoghq.com/getting_started/agent/?tab=datadogussite)


Now that that's out of the way, let's dive in!

# Collecting Metrics

First and foremost, Datadog is a metrics collection tool. Everything else flows from the data that you've collected. So let's start by collecting some data!

Let's have a look at what your agent is already reporting out of the box. You can view that here:
![default tags](./tags.png)

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
> See ./HostMap.png

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.


Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?
