Your answers to the questions go here.
# Prerequisites - Setup the environment:
I am using a [Vagrant](https://learn.hashicorp.com/collections/vagrant/getting-started) VM with an Ubuntu 18.04 server.

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  - To add tags into the host, I used the [following guide](https://docs.datadoghq.com/getting_started/tagging/assigning_tags?tab=noncontainerizedenvironments)
  Here are the images of the code from the host and the Host Map.
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
  - I choose MySql for this example, if you don't have MySql installed on your machine, please use the following [guide](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04)
  - Once you have installed MySql on your machine please use the following [guide](https://docs.datadoghq.com/integrations/mysql/?tab=host#pagetitle) to install the Datadog integration for MySql.
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
  - To be able to s (https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/)
  here's the pic for the code, and the yaml file and from the  ui 
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
  - submit a pic
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
  - Yes, you can. Please see the [following](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval)
