Your answers to the questions go here.
# Datadog Hiring Challenege - Support Engineer
### *Completed by Justin Dizon*

## Level 1 - Collecting Your Data

To begin this challenge, I first initiated a [Vagrant](Screenshots/Initiating vagrant environment.png) environment, as suggested, to prevent OS or dependency issues. I then followed the steps initiating an [agent](Screenshots/Initiate Datadog agent.png).

**BONUS QUESTION:** *In your own words, what is the Agent?*

The Agent is a program that runs in the background; collecting metrics and event-data on your hosts and giving that information back to Datadog to be presented to you.

The next step was to configure my `~/.datadog-agent/datadog.conf` file to create [tags](Screenshots/Set Tags - .datadog-agent.conf.png) and set the `hostname` to my local machine. After this, I was able to see my tags when viewing my [Host Map](Screenshots/Host Map - Tags.png).

Since I've previously installed [PostgreSQL](Screenshots/PostgreSQL.png) on my machine, I decided to use the corresponding integration with Datadog. I followed the docs to integrate PostgreSQL with Datadog; I first created a user named [datadog](Screenshots/Create Datadog user.png), then I [grant](Screenshots/GRANT Datadog user.png) the proper access to `datadog`, then I configured the Agent to connect to PostgreSQL with a new file, [.datadog-agent/conf.d/postgres.yaml](Screenshots/PostgreSQL YAML.png), and lastly, I verified that everything was properly [connected](Screenshots/Integration Check Passing.png)!

Next up, was writing a custom Agent Check called `test.support.random`. I read through the docs, created two new files, [.datadog-agent/checks.d/randomvalue.py](Screenshots/Random Value python.png) and its corresponding configuration file, [.datadog-agent/cond.d/randomvalue.yaml](Screenshots/Random Value YAML.png).

## Level 2 - Visualizing Your Data

Since I had just finished created my custom Agent Check, `test.support.random`, it was now time to see it in action! I cloned my Datadog dashboard and added a new Timeseries [graph](Screenshots/Dashboard showing custom metric.png).

*NOTE: I had used the* `randint()` *method from the* `random` *Python library when I first created the Agent Check. I configured the method to output a random value between 0 and 100, that is why the initial values are so high. I later adjusted* `test.support.random` *to use the* `random()` *method with no arguments to produce results within the desired range.*

**BONUS QUESTION:** *What is the difference between a timeboard and a screenboard?*

From reading through the docs, a timeboard is a dashboard where all the graphs are processing data within the same time period. Screenboards, on the other hand, can be configured differently and give more in-depth information. It also seems that timeboards are great for troubleshooting problem areas whereas screenboards are better for presenting the bigger picture of your infrastructure/metrics.

After reconfigured `test.support.random` to output values within the desired range, I was able to take a [screenshot](Screenshots/>.90.png) and `@notify` that event to my [email](Screenshots/Notify myself.png).

## Level 3 - Alerting Your Data

Now, it was time to write a monitor on `test.support.random` to automatically email me when we would get a value that is [greater than 0.90](Screenshots/Create monitor.png) at least once, within a 5 minute interval. It was really excited to receive the first email [notification](Screenshots/Email notification.png)! After receiving a few more emails, I understood why [Downtime](Screenshots/Configure Downtime.png) was such an important [feature](Screenshots/Downtime set.png).
