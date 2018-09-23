## Collecting Metrics:
Added tags to the agent config file:
https://s3.amazonaws.com/datadoganswers/tags_datadog.yaml.png
This was also visible from the host map page in Datadog:
https://s3.amazonaws.com/datadoganswers/tags_infra_host_map.png

I installed MySQL because that is the database that I have the most familiarity.
I ran sysbench to get some metrics, but they were barely visible. Here is a screenshot of Datadog:
https://s3.amazonaws.com/datadoganswers/MySQL_integration.png
Here is the MySQL integration config file:
https://s3.amazonaws.com/datadoganswers/MySQL_conf_yaml.png
Here is further validation via the agent config check:
https://s3.amazonaws.com/datadoganswers/MySQL_agentstatus_check.png

After the MySQL integration, I worked on the random metric. Here is the yaml file and python script for this metric:
https://s3.amazonaws.com/datadoganswers/random_check.yaml
https://s3.amazonaws.com/datadoganswers/random_check.py

Here is a screenshot of the check functioning as expected.
https://s3.amazonaws.com/datadoganswers/random_check_check.png

In order to change the custom check to only submit once every 45 seconds, I modified the random_check.yaml file. I was not sure if this counted as modifying the Python check file. Here is that file:
https://s3.amazonaws.com/datadoganswers/modified_yaml_collection_interval_45.png


## Visualizing Data:

I created a shell script and used curl to interact with Datadog API to create my custom Timeboard. Here is a copy of the script I ended up using:
https://s3.amazonaws.com/datadoganswers/timeboard.sh

Here is the snapshot that was created of a 5 minute window:
https://s3.amazonaws.com/datadoganswers/snapshot.png

## Monitoring Data

I set up a monitor for the my_metric metric. Here is the email screenshot:
https://s3.amazonaws.com/datadoganswers/datadog_alerting.png
And here is the alerting maintenance window emails received:
https://s3.amazonaws.com/datadoganswers/datadog_downtime_alert.png

## Collecting APM Data:
I did not complete this exercise. I attempted to use ddtrace with a MySQL python connector, but was unsuccessful. Here is the script I was running that was a simple connect:
https://s3.amazonaws.com/datadoganswers/APM_python_mysql.png
I am 100% sure I am missing something here, but I'd need some more time to figure it out.

## Final Question:
I think an interesting use-case for Datadog would be to actively monitor and report location data during events like concerts, festivals, or street fairs. This would help organizers identify hotspots and organize future events better and also react in real-time to open areas to alleviate crowd traffic. 
