## Tiffany Monroe
Solutions Engineer Applicant

## The Exercise

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setting up the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.

<img src="img/vagrant.png" />

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

<img src="img/network.png" />


## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

<img src="img/tags.png" />

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

```
create user datadog with password '(generated password)';

grant SELECT ON pg_stat_database to datadog;

psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" &&
echo -e "\e[0;32mPostgres connection - OK\e[0m" ||
echo -e "\e[0;31mCannot connect to Postgres\e[0m"

~.datadog-agent/conf.d/postgres.d/conf.yaml.example

mv conf.yaml.example conf.yaml
```
<img src="img/postgres.png" />

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

<img src="img/metric.png" />

Sources: [Agent Check](https://docs.datadoghq.com/developers/agent_checks/),  [Random Value](https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/).


```
touch ~.datadog-agent/conf.d/my_metric.yaml ~.datadog-agent/checks.d/my_metric.py
datadog-agent check my_metric
```

<img src="img/metric_check.png" />


* Change your check's collection interval so that it only submits the metric once every 45 seconds.

See image above.


* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

You change the .yaml file.


## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:


* Your custom metric scoped over your host.

Sources: [Timeboards](https://docs.datadoghq.com/graphing/dashboards/timeboard/),
[API](https://docs.datadoghq.com/api/?lang=python#timeboards)

<img src="img/timeboard.png" />


* Any metric from the Integration on your Database with the anomaly function applied.

Source: [Anomaly Detection](https://docs.datadoghq.com/api/?lang=python#create-a-monitor)
https://docs.datadoghq.com/graphing/functions/algorithms/


* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Source: [Rollup Function](https://docs.datadoghq.com/graphing/functions/rollup/)



Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?
