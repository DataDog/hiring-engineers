
## Environment Setup

For the purpose of this exercise, I am using an AWS EC2 (machine is Ubuntu 18.04.4 LTS)
Server is installed with latest packages




![Image of EC2](EC2-UP.JPG)


I have signed up for Datadog with email jgdesanti@yahoo.com, copied my API key and installed the latest agent



![Agent](2-DDagent.JPG)


Agent is installed


![Agent](3-DDagent.JPG)

Now lets check the Datadog UI to verify that the agent is reporting correctly and data is being collected


![Agent](4-DDagent.JPG)

First step is complete


## Collecting Metrics
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.


I am adding tags to the agent configuration file and restarting the agent

` sudo vi /etc/datadog-agent/datadog.yaml`
` sudo service datadog-agent restart`

![Agent](5-TagsConfig.JPG)

Then checking in the UI that my new tags are displayed

![Agent](6-TagsCheck.JPG)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I am installing MongoDB 4.2.6 on my machine

![MongoDB](7-MongoDB.JPG)

Check the Mongo logs

![MongoDB](8-MongoDB.JPG)

Configure the MongoDB integration in /etc/datadog-agent/conf.d/mongo.d

![MongoDB](9-MongoDB.JPG)

Check Datadog Log File
`cat /var/log/datadog/agent.log`

![MongoDB](11-MongoDB.JPG)

Finally Check that integration is working properly and MongoDB is detected

![MongoDB](10-MongoDB.JPG)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.


