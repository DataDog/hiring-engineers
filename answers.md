Your answers to the questions go here.


## Level 1

#### Sign up for Datadog, get the agent reporting metrics from your local machine.

**This is what you should see in your terminal upon initial install.  You will also notice that the Data Dog Agent is automatically run upon installation.**
![Terminal](imgs/DD_initial_install.png)

**You can now go into your DataDog account and see the reporting metrics for your local machine.**
![Metric1](imgs/cpu.png)
![Metric2](imgs/disk_free.png)
![Metric3](imgs/disk_total.png)
![Metric4](imgs/memory_used.png)


#### Bonus question: what is the agent?

The DataDog Agent is software that runs on the clients host environment. It collects event data and metrics and sends it to DataDog. The client can then use that data to make adjustments to monitoring or performance optimization.  The data is presented in rich visual graphs on your Datadog account which you can customize to suit your needs.

There are three components to the Datadog agent
1. The Collector
  *  Runs checks on the current machine for current integrations you have and it will capture system metrics.

2. Dogstatsd
  * A statsd backend server that receives custom metrics from application.

3. Forwarder
  * Retrieves data from both the Collector and Dogstatsd and queues it up to send it to Datadog.

#### Submit an event via the API.
* Submit a test event via the API in Ruby.
![EventSubmission](imgs/event_submission.png)

* Run the file from the command line

* The event will then be visible in your Events feed
![Event](imgs/event_screen_shot.png)


####  Get an event to appear in your email inbox (the email address you signed up for the account with)

![EventEmail](imgs/event_email.png)

