<!-- Your answers to the questions go here. -->

# Datadog Solutions Engineer Answers

## Introduction

Hey everybody (Hi Dr. Nick). Thanks for taking the time to go through my PR, please feel free to reach out if there's any information I can provide or any questions you may have.  I appreciate the opportunity to learn more about the Datadog team and thanks again for taking time out of your day to review my work.


### Prerequisites - Setup the environment

- 1a Vagrant + VirtualBox Setup: After installing Vagrant I spun up an Ubuntu 16 Linux VM [here](https://app.vagrantup.com/ubuntu/boxes/xenial64)  ![ubuntu xenial64](./1a_update.png)

- 1b I ssh'd into VM `vagrant ssh` and confirmed `v. 16.04` ![Ubuntu 16.04](./1b.png)

- 1c I signed up for Datadog and installed the Datadog Agent  successfully  ` DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"` ![screenshot](./1c.png)

- 1d I navigated to the [eventstream](https://app.datadoghq.com/event/stream) `https://app.datadoghq.com/event/stream` and confirmed Agent reporting from my local machine ![screenshot](./1d.png)


### Collecting Metrics

- 2a 2b Added two tags in the Agent config file `datadog.yaml` `example` and a key/value pair `env:prod` ![screenshot](./2a.png) ![screenshot](./2b.png)

- 2c 2d restarted agent `sudo service datadog-agent restart` and confirmed via that tags added to agent yaml config file were accounted for on Host Map page ![screenshot](./2c.png) ![screenshot](./2d.png)

- 2e 2f 2h 2i 2j 2k 2l I installed PostresSQL on my VM
  ```
    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib
  ```
  and then after confirming installation ![confirm installation](./2e.png) I started postgres and followed [Datadog PostgreSQL integration and configuation instructions](https://app.datadoghq.com/account/settings#integrations/postgres) ![here](./2f.png) and ![here](./2g.png) and confirmed connection ![here](./2h.png) and configured agent to connect to PostgreSQL server ![here](./2i.png) and restarted the Agent ![here](./2j.png) , checked the status `sudo datadog-agent status` ![here](./2k.png) via CLI and the [relevant Dashboard](https://app.datadoghq.com/dash/integration/17/postgres---metrics) ![here](./2l.png)

- 2m 2n 2o 2p I created a custom agent check named `my_metric` by adding both a .py file to the `checks.d` directory and also a `my_metric.d` subdirectory in the `conf.d` directory as well as a yaml config file `my_metric.yaml` . ![2m](./2m.png) ![2n](./2n.png) ![2o](./2o.png) The custom Agent check logs a random value btwn 0 and 1000 ![2p](./2p.png).

- 2q 2r 2s 2t Bonus: After confirming that my_metric custom agent check was being logged in the metrics dashboard !(2q)(./2q.png) I was able to change the the collection interval from the default 20seconds to 45 seconds by updating the yaml config file `min_collection_interval` key then restarting the agent and confirming the change in interval via the Dashboard ![2r](./2r.png) ![2s](./2s.png) ![2t](./2t.png) . I think this counts as changing the interval without changing the .py file. If I wanted to change it via the .py file via I suppose I could `time import` and invoke `time.sleep(_SOME_AMOUNT_OF_SECONDS)` or something hacky along those lines


### Visualizing Data

- 3a I chose to use the Datadog ruby library DogApi as docoumented in the [developer section of the docs](https://docs.datadoghq.com/developers/libraries/). Please note this requires rvm(ruby version manager), ruby, and rubygems to be installed on the VM (documentation for this can be found [here](https://gorails.com/setup/ubuntu/16.04) ). after installing dependancies I installed dogapi with `gem install dogapi` as can be seen  here ![3a](./3a.png).

- 3b 3c then following the documentation for creating a timeboard as noted [here](https://docs.datadoghq.com/api/?lang=ruby#create-a-timeboard) `https://docs.datadoghq.com/api/?lang=ruby#create-a-timeboard` I first created a new app key via the Datadog UI and replaced the example graph with 3 graphs, which were as requested

```
  Your custom metric scoped over your host.
  Any metric from the Integration on your Database with the anomaly function applied.
  Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
```

Script can be seen here and in `example_script.rb` The timeboard can be seen here
![3b](./3b.png)
![3c](./3c.png)

For the anomalies function and the rollup function I followed the documentation as referenced the the [misc graph section](https://docs.datadoghq.com/graphing/miscellaneous/functions/) `https://docs.datadoghq.com/graphing/miscellaneous/functions/` I chose the postgreSQL percent usage connections as that would be a relatively constant timeseries (there is only 1 connection) and so the range of 2 std deviations as specified in the arguments of the anomalies function would be easy to see.  For the Rollup of my_metric into 1 bucket over a 1hr period, since the rollup period is in seconds I passed in sum to indicate that I wanted a total of all the events, and 3600 as a parameter since there are 3600 seconds in an hour.

- 3d I selected the Timeboard from the Dashboard list and although the minimum default range options is only the past hour, in order to do 5 minutes I found that the query paramets of the URL from_ts and to_ts could be editted, so I selected a from_ts that was `to_ts - 30000` and reloaded the page in order to get a 5 minute timeframe as seen here ![3d](./3d.png).

- 3e 3f In order to take a snapshot of the graph I selected the camera icon from the Dashboard UI and in the annotation section input `@ericmustin` in order to send the snapshot to my user, and i checked my inbox to confirm reciept, both actions can be seen here
![3e](./3e.png)
![3f](./3f.png)

- Bonus: The Anomaly Graph is basically displaying a range of expected values that the metric is expected to fall within in the future a certain percentage of the time, given it's previous values.  The range it's expected to fall within is tighter or wider depending on the Param you pass in of number of standard deviations, I chose 2 standard deviations for statistical significance. Though I'm not a stats wiz the range is basically saying `95% of the time the number should fall within this range`. So, the 1 out of 20 times it is above or below that range, it probably indicative of an anamoly or underlying change in data, and is worth alerting a user on.

### Monitoring Data

- 4a 4b 4c in The Datadog UI I navigated to the [Monitor Page](https://app.datadoghq.com/monitors#/create) and selected a create new monitor, then followed the instructions to create an alert with a threshold > 800 and a warning above 500 over the previous 5 minute period, as well as a No Data alert if there's zero recorded instances of the metric over a 10 minute period.  Using Markdown and the Datadog templating language I constructed an email that has different messaging for alert, warn, and no data, and logs the my_metric value and host ip in the case of an alert.  This successfully sent me a warning alert right away as it didn't take long to go above 500, screenshots of the inputting of values into the new monitor and the email i got from this monitor can be seen here
![4a](./4a.png)
![4b](./4b.png)
![4c](./4c.png)

- Bonus: since we don't want this to alert constantly during normal business hours and on the weekend off hours, I set up two recurring scheduled downtimes via the `Manage Downtime` menu option. I selected recurring downtimes for the weekend and weekdays during Eastern Time 7:00am - 9:00pm, the emails note UTC times which, when adjusted, line up with our EST preferences.  Downtime creation forms and the emails rec'd as a result can be seen below
![4d](./4d.png)
![4e](./4e.png)
![4f](./4f.png)
![4g](./4g.png)
![4h](./4h.png)


### Collecting APM Data

 - 5a 5b 5c This one was fun. I decided not to rewrite the python app in ruby with sinatra or rails, so first I had to install pip and flask locally, and then followed the instructions in the `https://docs.datadoghq.com/tracing/setup/python/`  first installing `pip install ddtrace` then updating the example app as found here `http://pypi.datadoghq.com/trace/docs/#flask` to import the relevant ddtrace and blinker libraries and add the middleware on top of the example Flask app.  example app can be found in this repo at `my_app.py`  I ran into a few issues along the way.  First I was unable to connect to my webserver in the vm from my  browser, and after some time debugging I realized I had to setup the appropriate port forwarding which I did by editting the Vagrant file `config.vm.network "forwarded_port", guest: 5050, host: 8080` . Not a very secure approach but allowed me to make requests.  Then I remembered to update my `datadog.yaml` conf to include
```
 apm_config:
  enabled: true

```
But was still having issues with ddtrace and everytime i started up the updated flask app `python my_app.py` I got debug logs `ddtrace.writer - ERROR - cannot send span to localhost:8126: [Errno 111] Connection refused`. It turns out I just needed to restart the agent, `sudo service datadog-agent restart` and from there my flask app tracing worked great and I was able to see APM metrics in Datadog's UI, and I made a simple timeboard with both APM and Infra Metrics, as seen below. Links to APM and Infra graph here (Not sure if this is the right approach I just took the embed src link value)

[APM](https://app.datadoghq.com/graph/embed?token=d3879abb024883724beb86400b4c3d3afaf4e278d0f1065e289e6d9be497a27a&height=300&width=600&legend=true)
`https://app.datadoghq.com/graph/embed?token=d3879abb024883724beb86400b4c3d3afaf4e278d0f1065e289e6d9be497a27a&height=300&width=600&legend=true`
[Infra](https://app.datadoghq.com/graph/embed?token=22f3da6ae7ce7a1815cc1fe7cb5008e4d71e91fd430cc1d11c861e8ad8c5d237&height=300&width=600&legend=true)
`https://app.datadoghq.com/graph/embed?token=22f3da6ae7ce7a1815cc1fe7cb5008e4d71e91fd430cc1d11c861e8ad8c5d237&height=300&width=600&legend=true`

![5a](./5a.png)
![5b](./5b.png)
![5c](./5c.png)

- Bonus Surprise Question: What is a service and what is a resource? Put briefly, a service is a group of processes that are all centered around a similar job (so for example a web server could be considered a few different services, web views and database) and a resource is just one specific type of action within a service, like for example `/home` routes or just a single sql query like `SELECT users.email, users.first_name, first_orders.order_id FROM users JOIN first_orders on first_orders.user_id = users.id WHERE users.first_name LIKE "%Spartacus%"`;

### Final Question
- Datadog has a lot of interesting uses. I think an interesting service could be monitoring your expected commute time of your daily commute to and from the office.  You could write a relatively simple web scraper that could query for the Google Maps Directions estimated Commute time of your commute (say, at 6pm travelling from Grand Central NY to Astoria Queens NY). The commute time in minutes could be tracked as a custom metric in Datadog, you could set up Threshold Alerts or an Anomaly Function for when that commute time is expected to exceed it's usual amount of time, alerting you with an email ahead of time to let you know to tell your significant other you might be home late for dinner, or that you should take an alternative route in order to avoid the issue impacting your commute.




