## Setup:

Setup and Installing the Agent:
I used Vagrant (Ubuntu) to complete the exercise. My Datadog host map also includes a docker instance because I was curious about installing the agent on a Docker container. The setup after creating an account was pretty straight forward.

## 1) Collecting Metrics

Everything in this section was self-explainable and found the docs easy to understand.

Note: The dd-agent status command helped me out A LOT through this particular exercise.

### a) Adding Tags
Used the docs here: <a href="https://docs.datadoghq.com/tagging/assigning_tags/?tab=hostmap">https://docs.datadoghq.com/tagging/assigning_tags/?tab=hostmap</a>

Editing the the datadog.yaml, I found the tag dictionaries, saved the file, and restarted the dd agent:

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/1/1/1.png" />

I confirmed that the tags showed up by looking at the UI of my host map instance:

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/1/1/1.png" />

### b) Install Datadog integration for my DB
Used the docs here: <a href="https://docs.datadoghq.com/integrations/postgres/">https://docs.datadoghq.com/integrations/postgres/</a>

I installed Postgres on my machine and went through the steps of setting up the Postgres user for datadog and edited the Postgres.d/conf.yaml.

After restarting the dd-agent, I ran the agent status and received an “ok” from the status check:

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/1/2/1.png" />

After confirming confirming an “ok” from my status check, I went back to the UI to confirm it was showing up:

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/1/2/2.png" />


### c) Custom Agent called “my_metric”
Used the docs here: <a href="https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6">https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6</a>

Created a file called my_metric.py and my_metric.yaml. Confirmed that the metric was showing up as well:

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/1/3/1.png" />

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/1/3/2.png" />

Note: I have to admit that this was the first time writing Python and I used the library “random” to generate the random number to send. I hadn’t downloaded the necessary library to use that (your docs told me to but I was just being lazy).

Again, this is where the dd-agent status command helped me out. Running the command let me know that that library wasn’t there and I needed to pull it in.

### d) Send the metric every 45 seconds

I used my my_metric.yaml to set the min_collection_interval to 45, looked at my map in the UI and looked like it was sending every 45 seconds

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/1/4/1.png" />

## 2) Visualizing Data

Completed Dashboard: <a href="https://app.datadoghq.com/dash/959266/my-metric-4">https://app.datadoghq.com/dash/959266/my-metric-4</a>

### Using the API
a) created my custom metric
b) anomoly function with my db metric (I used “postgresql.max_connections”)
c) roll up from with my custom metric

I used these docs:

API Timeboards: <a href="https://docs.datadoghq.com/api/?lang=python#timeboards">https://docs.datadoghq.com/api/?lang=python#timeboards</a>

Anomaly: <a href="https://docs.datadoghq.com/monitors/monitor_types/anomaly/">https://docs.datadoghq.com/monitors/monitor_types/anomaly/</a>

Rollup: <a href="https://docs.datadoghq.com/graphing/functions/rollup/">https://docs.datadoghq.com/graphing/functions/rollup/</a>

Note: I used a ruby script
```
  require 'dogapi'
  require 'byebug'

  api_key = '' # left these out bc the repo is public
  app_key = ''

  dog = Dogapi::Client.new(api_key, app_key)

  title = 'My Metric 4'
  description = 'Scope over my host'
  graphs = [{
    "definition" => {
        "events" => [],
        "requests" => [
          {"q" => "avg:my_metric{*}"},
          {"q": "avg:my_metric{*}.rollup(sum, 60)" },
          {"q" => "anomalies(avg:postgresql.max_connections{*}, 'basic', 2)"}
        ],
        "viz" => "timeseries"
    },
    "title" => "My Metric Scoped over Ubuntu Xenial"
  }]
  template_variables = [{
    "name" => "ubuntu-xenial",
    "prefix" => "ubuntu-xenial",
    "default" => "host:ubuntu-xenial"
  }]

  dog.create_dashboard(title, description, graphs, template_variables)
```

### d) Accessing in the UI and sending to myself using @ notation

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/2/snapshot email.png" />

Bonus: Noticed that my anomaly function was pretty empty, so it’s technically not detecting anything. I a real working db, it would be displaying an algorithmic function to detect an unusual amount of max connections

## 3) Monitoring Data

I used the UI: <a href="https://app.datadoghq.com/monitors#create/metric">https://app.datadoghq.com/monitors#create/metric</a>

### a) Create warning, alerting, no data thresholds

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/3/1.png" />

### b) Different messages

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/3/2.png" />

### c) Send an email

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/3/3.png" />

Bonus:

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/3/bonus/Screen Shot 2018-10-24 at 11.13.13 PM.png" />

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/3/bonus/Screen Shot 2018-10-24 at 11.13.38 PM.png" />


## 4) Collecting APM Data:

I used the flask app example and the docs for the APM setup:

#### (screenshot)
<img src="https://github.com/kfike/hiring-engineers/blob/solutions-engineer/images/3/bonus/Screen Shot 2018-10-25 at 5.11.05 PM" />

Dashboard: <a href="https://app.datadoghq.com/dash/959266/my-metric-4">https://app.datadoghq.com/dash/959266/my-metric-4</a>

## 5) Final Question:

My wife and I just had a baby and he sleeps in another room. We use a baby monitor at night to listen to see if we wakes up. One of the problems is trying to figure out if he’s actually awake and needs to be fed or he’s a little upset and will go back to sleep. I’ve thought a lot of about frequency within monitors and measuring the consistency/frequency height to figure out if he’s actually awake. There’s many circumstances where he starts crying, I walk across the house to get him, and right before I open his door, he quits crying and falls back asleep.

My solution involving Datadog would be to send frequency data, monitor it, and use an alert that could tell if he’s awake or not.
