# A sample Heroku application with dogstatsd / ddtrace  and Ruby - nice way to trace page loads and http
It also includes the my_metric.py script for custom Metrics and Postgres Integration YAML
Started Pre-Run Script to workaround some issues that DataDog has been made aware of

**This App is an example of how to use the Heroku Buildpack]("https://docs.datadoghq.com/agent/basic_agent_usage/heroku/").**

* Heroku Variables you should have Set
* **DD_AGENT_MAJOR_VERSION:**    7
* **DD_API_KEY:**                <YOUR API DD_API_KEY>
* **DD_DYNO_HOST:**              true
* **DD_SERVICE_NAME:**           datadog-test-christ
* **DD_SITE:**                   datadoghq.eu
* **DD_TAGS:**                   env:production
