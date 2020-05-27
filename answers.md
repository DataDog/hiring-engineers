Your answers to the questions go here.

## Pre-reqs:
  1. Decided to have a little fun with this and went the vagrant route, as I had a bit of experience here. I decided to install kube,     docker, and then use minikube to create a 'hello-world'-esque web application to better mimic monitoring a real world app.
 * Vagrant <img src="/pre-req-vagrant.png?raw=true" width="1000" height="332"></a>
 * Docker <img src="/docker_install.png?raw=true" width="1000" height="332"></a>
 * Minikube <img src="/minikube.png?raw=true" width="1000" height="332"></a>
 * Container monitoring in datadog after configuring docker agent conf.d yaml file: <img src="/minikube%20container%20monitoring.png?raw=true"></a>
       
## Collecting Metrics
 * Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  <img src="/tags-datadog.png?raw=true"></a>
  <img src="/Agent_tags.png?raw=true"></a>
 * Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database. Went with postgres here, install went off without a hitch. Added the datadog user and edited config file to give permissions required. Did run into an issue with the dd-agent user accessing the conf.d directory, strangely, so I _cheated_ and just gave global permissions via chmod.
  <img src="/troubleshooting-postgres.png?raw=true"></a>
  <img src="/troubleshooting-postgres-fixed.png?raw=true"></a>
 * And here it is in the UI:
  <img src="/postgres-db.png?raw=true"></a>
 * Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
  <img src="/metric_config_yaml_interval.png?raw=true"></a>
  <img src="/agentcheck_status_and_code.png?raw=true"></a>
  <img src="/my_metric_showing.png?raw=true"></a>
  <img src="my_metric_showing2.png?raw=true"></a>
 * Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?
   * For the bonus I changed the metrics_example.yaml file (what I used for the agent check) and added the line 
  ```
  - min_collection_interval: 45
  ```
  <img src="/csv_time_validation.png?raw=true"></a>
  
# Utilize the Datadog API to create a Timeboard that contains:
#  Your custom metric scoped over your host.
#  Any metric from the Integration on your Database with the anomaly function applied.
#  Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
* 
