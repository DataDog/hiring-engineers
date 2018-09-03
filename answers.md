Submitted by: David Oslander

## Section 1: Collecting Metrics

Screenshot of my host and its tags on the Host Map page in Datadog:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-host-tags.png">

I installed a Postgres database and started it:

```
sudo service postgresql start
```

I installed the Postgres integration in Datadog:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-postgresql-installed.png">

My custom Agent check that submits a metric named my_metric with a random value between 0 and 1000:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-my_metric-py.png">

After changing my check's collection interval to submit the metric once every 45 seconds, the data points occur less frequently on the graph as expected:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-my_metric-interval-increased.png">

**Bonus Question** Can you change the collection interval without modifying the Python check file you created?

* My Custom check inherits from Agent check. Rather than modifying the interval in my file, I could edit the process interval in Datadog.yaml.

## Section 2: Visualizing Data

The script that I've used to create my Timeboard is <a href="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/scripts/create-timeboard.py">here</a>.

## Section 3: Monitoring Data

## Section 4: Collecting APM Data

## Final Question
