
## Environment Setup

In this step, we are using AWS EC2 (machine is Ubuntu 18.04.4 LTS)
Server is installed.


![Image of EC2](EC2-UP.JPG)


Datadog Agent installation with API Key

![Agent](2-DDagent.JPG)

Agent is installed

![Agent](3-DDagent.JPG)

Check the Datadog UI to verify that the client is reporting correctly
![Agent](4-DDagent.JPG)

## Collecting Metrics
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![Agent](5-TagsConfig.JPG)

![Agent](6-TagsCheck.JPG)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I am installing MongoDB 4.2.6 on my machine

![MongoDB](7-MongoDB.JPG)

Check the Mongo logs

![MongoDB](8-MongoDB.JPG)

Configure the MongoDB integration in /etc/datadog-agent/conf.d/mongo.d

![MongoDB](9-MongoDB.JPG)

Check that integration is working properly and MongoDB is detected

![MongoDB](10-MongoDB.JPG)

Finally check Datadog Log File
`cat /var/log/datadog/agent.log`





![MongoDB](11-MongoDB.JPG)
