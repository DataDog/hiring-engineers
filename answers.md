Your answers to the questions go here.

Setup Environment:

Followed the instructions at https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant to configure my Vagrant VM running Ubuntu 18.04.

Familiarized myself with basic agent start/stop/restart/status, etc. https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7

Collecting Metrics:

Configured tags in Agent config file.. environment:dev, project:training, owner:tom, os:ubuntu.. utilized https://docs.datadoghq.com/tagging/

Attempted integration with MongoDB but was unable to get metrics to report.. switched to Postgresql and was able to install and pull metrics.. following the instructions from.. 

https://docs.datadoghq.com/integrations/postgres/?tab=host

Created a custom Agent check mycheck.py and a test check hello.py following the hello world example provided at https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

Configured both check intervals to be 45 seconds per the guide. Bonus Question: Changing the collection interval can be found under Metrics Summary by modifying the Metadata section of your check (see screenshot).

Visualizing Data:

I was able to create a Timeboard via the Datadog API, which included my custom metric, a checkpoint Postgresql metric (with the anomaly function) and the custom metric with rollup function. I believe I successfully configured the rollup function, but no data appears in the report so it may be configured incorrectly.

See screenshots of Dashboards and associated scripts. I created multiple scripts for testing purposes.. including a simple dashboard creation, a script to list dashboard names with their associated IDs, a script to delete a dashboard, etc. I will upload all scripts to the repo.

Monitoring Data:

Created an email alert with the thresholds defined in the readme.. warning (500), alerting (800) and no data over the past 10 minutes. (See email and alert config screenshots)

Scheduled two downtime windows as defined in the readme. From 7pm to 9am daily and over the weekend starting at 7pm Friday (see screenshots).

Collecting APM Data:

I was unable to configure APM monitoring. I believe it may be tied to using both ddtrace and middleware as mentioned in the guide, but couldn't figure out root cause.

I installed Flask and ddtrace successfully and tried to pull APM data through both the hello.py example provided at https://docs.datadoghq.com/getting_started/tracing/ and the provided Flask app (flaskapp.py), but neither service seemed to push data to Datadog. I believe this is tied to the Flask app not running properly and not the configuration, but I would need some additional assistance to find the problem.

Bonus question: A resource is a particular action asscociated with a service (such as a database query), where a service is a set of processes that provide a particular feature set (such as the database itself, and all the monitors/metrics associated with that database being up and running and available).

Final Question:

As we create better and more detailed metrics in regards to our health, I think it would be amazing to utilize Datadogs data-based analysis to monitor personal health. Like a personal health dashboard, monitoring trends in terms of calories consumed/burned, heartrate, overall weight, etc. Datadog already has the capacity to ingest mass amounts of data, visualize it, provide alerting/reporting, etc; as we develop smaller and more easily integrated health monitors (permanent heartrate monitors, calorie trackers, etc.) that data will need to be consolidated and tuned to provide value back to the person, and I think Datadog could be used to as a tool in the regard, beyond the typical IT ecosystem.

Final Thoughts:

I loved doing this exercise! While frustrating at times (what isn't?), I learned a lot feel much more familiar with the Datadog platform, thank you for your time and consideration!

Tom
