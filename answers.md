Your answers to the questions go here.
## Part 01: Collecting Metrics
- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in datadog
Excerpt from datadog.yaml file
```
# Set the host's tags (optional)
tags:
  - env_type:test
  - env_from:home
```
<a href="img/01-CollMetrics-002.png">
     <img src="img/01-CollMetrics-002.png" width="500"/>
</a>

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

<a href="img/01-CollMetrics-004.png">
     <img src="img/01-CollMetrics-004.png" width="500"/>
</a>

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
1. Go to and open the folder that holds the configuration files for datadog.
```
cd ~/.datadog-agent/ && code .
```
 

- Change your check's collection interval so that it only submits the metric once every 45 seconds.
     - Answer:
          - G

- Bonus Question Can you change the collection interval without modifying the Python check file you created?
- Answer: Yes, you do it by changing the 