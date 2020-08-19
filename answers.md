***Setting Up the Environment***

I spun up an Vagrant Ubuntu VM since I was using a Windows machine. And had little issue installing the datadog agent with the single-step command.

https://app.datadoghq.com/account/settings#agent/ubuntu

<INSERT IMAGE OF SINGLE STEP INSTALL>

***Collecting Metrics***
I installed vim and added tags to the datadog.yaml file. I had a little issue getting this to work at first because of some indentation issues.

<INSERT IMAGE OF TAGS>

I chose MySQL as my database since I had some experience with it from college and followed the instructions via this resource:
	* https://app.datadoghq.com/account/settings#integrations/mysql

<INSERT IMAGE OF SQL COMMANDS>

Creating My Metric Custom Agent Check
This was the first point of friction that I experienced in the exercise. I don't have much experience with Python so I had to utilize a few resources to feel confident editing the example.

<INSERT IMAGE OF MY_METRIC.PY>

I successfully updated the min_collection_interval to 45 seconds.

<INSERT IMAGE OF min_collection_interval>

Bonus Question Can you change the collection interval without modifying the Python check file you created?

Resources Used:

	* https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7
	* https://datadoghq.dev/summit-training-session/handson/customagentcheck/
	* https://docs.datadoghq.com/developers/metrics/types/?tab=count
  * https://stackoverflow.com/questions/710551/use-import-module-or-from-module-import
	* https://www.w3schools.com/python/numpy_random.asp

Can you change the collection interval without modifying the Python check file you created?
Yes, this can be changed in the .yaml config file.

***Visualizing Data***
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Bonus Question: What is the Anomaly graph displaying?
---
***Monitoring Data***
<INSERT IMAGES HERE>

***Collecting APM Data***
---need to finish this section--- having issues getting to the services section after running the flask app.

***Final Question***
Is there anything creative you would use Datadog for?

The worst part of being a human is having to go the DMV. I think that Dante would have made the DMV the first circle of hell if he had lived in modern times. The most altruistic application of Datadog APM would be to apply it's monitoring to DMV foot-traffic/check-ins. Leveraging Datadog's monitoring tools could help find patterns in DMV surge times, improve staffing and resource allocation, and alert community members with appointments of upticks in wait times. It could help everyone spend the smallest amount of time possible in the DMV and minimize human suffering.
