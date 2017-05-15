Level 1 

Account: email

Bonus question: In your own words, what is the Agent?

The Datadog agent is a multi-use tool, deployable to hosts and enables metrics collection for the Datadog service in "on premise" environments. To support a wide variety of possible use cases, the agent contains a collector, a custom variant of statsd (a time based metrics aggregation sub-service), and forwarding state engine that securely relays data to the cloud.

Tags: line 31/259 of /etc/dd-agent/datadog.conf

tags: Test, env:test, role:candidatetest, region:west

Screenshots: *Tags* screenshots
 
 Database install: See mongo.yaml
 
 test.support.random: Code can be found in conf.d and checks.d. I used 'testcheck' to learn and 'randomcheck' to poll 'test.support.random'. 
 
Level 2


Bonus question: What is the difference between a timeboard and a screenboard?

The biggest distinction between timeboard and screenboards is that timeboards contain time or query based graphs or metrics, scoped to the same time appearing in a grid format. You can use these for time series based root cause analysis and event correlation. TimeBoards can only be shared to individuals.

Screenboards are very customizable, widget based boards. They can have checks, status, queries or any data from the Datadog system in the dashboard. Screenboards are shareable as live entities within your organization. Very modular and multifunctional. 
