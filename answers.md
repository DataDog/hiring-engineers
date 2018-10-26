#Intro:

I’m approaching this challenge the same way I would approach integrating any third party provider; as a developer that has decided to use Datadog, is on that 15 day trial, and trying to get up and running as quick as possible.

With that said, kudos to the team member(s) that wrote this challenge. I felt like each todo was a perfect balance of just enough information of what you wanted me to look for in the docs but not enough to give me the answer.

Setup and Installing the Agent:
I used Vagrant (Ubuntu) to complete the exercise. My Datadog host map also includes a docker instance because I was curious about installing the agent on a Docker container. The setup after creating an account was pretty straight forward.

#1) Collecting Metrics

	Everything in this section was self-explainable and found the docs easy to understand.

	Note: The dd-agent status command helped me out A LOT through this particular exercise.

	a) Adding Tags
	Used the docs here: https://docs.datadoghq.com/tagging/assigning_tags/?tab=hostmap

	Editing the the datadog.yaml, I found the tag dictionaries, saved the file, and restarted the dd agent:

	![Alt text](images/1/1/1.png?raw=true "Title")

	I confirmed that the tags showed up by looking at the UI of my host map instance:


	b) Install Datadog integration for my DB
	Used the docs here: https://docs.datadoghq.com/integrations/postgres/

	I installed Postgres on my machine and went through the steps of setting up the Postgres user for datadog and edited the Postgres.d/conf.yaml.

	After restarting the dd-agent, I ran the agent status and received an “ok” from the status check:

	(screenshot)

	After confirming confirming an “ok” from my status check, I went back to the UI to confirm it was showing up:

	(screenshot)


	c) Custom Agent called “my_metric”
	Used the docs here: https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6

	Created a file called my_metric.py and my_metric.yaml. Confirmed that the metric was showing up as well:

	(screenshot)

	(screenshot)

	Note: I have to admit that this was the first time writing Python and I used the library “random” to generate the random number to send. I hadn’t downloaded the necessary library to use that (your docs told me to but I was just being lazy).

Again, this is where the dd-agent status command helped me out. Running the command let me know that that library wasn’t there and I needed to pull it in.

	d) Send the metric every 45 seconds

	I used my my_metric.yaml to set the min_collection_interval to 45, looked at my map in the UI and looked like it was sending every 45 seconds

	(screenshot)

2) Visualizing Data

	Using the API
	a) created my custom metric
	b) anomoly function with my db metric (I used “postgresql.max_connections”)
	c) roll up from with my custom metric

	I used these docs:
		API Timeboards: https://docs.datadoghq.com/api/?lang=python#timeboards
		Anomaly: https://docs.datadoghq.com/monitors/monitor_types/anomaly/
		Rollup: https://docs.datadoghq.com/graphing/functions/rollup/

Note: Used a ruby script

require 'dogapi'
require 'byebug'

api_key = '' # left these out bc the repo is public
app_key = ''

dog = Dogapi::Client.new(api_key, app_key)

# Create a timeboard.
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

	d) Accessing in the UI and sending to myself using @ notation

	(screenshot)

	Bonus: Noticed that my anomaly function was pretty dead, so it’s technically not detecting anything. I a real working db, it would be displaying an algorithmic function to detect an unusual amount of max connections

3) Monitoring Data

	I used the UI: https://app.datadoghq.com/monitors#create/metric

	a) Create warning, alerting, no data thresholds
	(screenshot)

	b) Different messages
	(screenshot)

	c) Send an email
	(screenshot)

	Bonus:
	(screenshot)

4) Collecting APM Data:

	I used the flask app example and the docs for the APM setup:

	(screenshot)

	Dashboard: https://app.datadoghq.com/dash/959266/my-metric-4

5) Final Question:

My wife and I just had a baby and he sleeps in another room. We use a baby monitor at night to listen to see if we wakes up. One of the problems is trying to figure out if he’s actually awake and needs to be fed or he’s a little upset and will go back to sleep. I’ve thought a lot of about frequency within monitors and measuring the consistency/frequency height to figure out if he’s actually awake. There’s many circumstances where he starts crying, I walk across the house to get him, and right before I open his door, he quits crying and falls back asleep.

My solution involving Datadog would be to send this frequency data, monitor it, and use an alert that could tell if he’s awake or not. Bye bye baby monitor!
