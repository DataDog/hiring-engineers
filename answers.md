# The Beginner's Guide to Datadog

Learning datadog for the first time? Building a demo environment? Planning an evaluation guide for a client? Completing the datadog hiring exercise?

If you answered 'yes' to any of those questions then you've come to the right place. This handy guide will help you in understanding the key components and setup steps for datadog! This will bring you one step closer to improving collaboration and visibility across teams. 

## Prerequisites - Setting up the environment

*Download and install vagrant with ubuntu image

*Download and install Datadog Ubuntu agent using bash command provided
![alt text](screenshots/1_Prereq_1.png)
![alt text](screenshots/1_Prereq_2.png)

## Collecting Metrics:

This section focuses on collecting infrastructure metrics from your host

*Modify the agent config file to add your own tag mytag:bbdemo

![alt text](screenshots/2_Collect_1.png)

*Go to the host Map page in data dog. Filter by the tag created

![alt text](screenshots/2_Collect_2.png)

*Install Mongodb on your machine with "sudo apt-get -y mongodb-org
![alt text](screenshots/2_Collect_3.png)

*Create a new user for Datadog in Mongo using db.createUser 
![alt text](screenshots/2_Collect_4.png)
*Validate user with db.auth command

![alt text](screenshots/2_Collect_5.png)

*create a mongo.yaml config file in conf.d directory
![alt text](screenshots/2_Collect_6.png)

*restart the agent

*You should now see mongodb on the hostmap

![alt text](screenshots/2_Collect_7.png)


*Create a custom agent check my_metric that submits random value between 0 and 1000 via python script in checks.d. Implement the AgentCheck interface and "random" library. Use randint function as 2nd param in self.gauge call
![alt text](screenshots/2_Collect_8.png)

*Create check config yaml file in conf.d directory. **Bonus Tip** You can specify collection interval here without needing to modify the python script

![alt text](screenshots/2_Collect_9.png)

Lastly, run the dd-agent check command to validate things are working okay.

![alt text](screenshots/2_Collect_10.png)

## Visualizing Data

This section focuses on taking that data and visualizing it in a useful way.

First, validate that datadog is receiving the metric by checking the metric explorer.

![alt text](screenshots/3_Visualize_1.png)

Next, manually create a timeboard that shows my_metric scoped over the host, mongodb.network.bytesinps metric from mongo, and a rollup sum of my_metric over the last hour

To automate the timeboard creation for simply future deployment, use the datadog API dash resource via python script https://docs.datadoghq.com/api/?lang=python#create-a-timeboard

You will first need an api key and app key which can be created in Datadog

![alt text](screenshots/3_Visualize_2.png)

Below is a screenshot of the script (see createtimeboards.py) **Hint** For the graph array JSON objects: copy the JSON from the timeboard graph setting screen that you made earlier

![alt text](screenshots/3_Visualize_3.png)

![alt text](screenshots/3_Visualize_4.png)

Once the script runs you should now see the timeboard in datadog:

![alt text](screenshots/3_Visualize_5.png)

Change the timeboard to only show last 5 minutes then create an annotated snapshot and inform yourself.

![alt text](screenshots/3_Visualize_7.png)

**Bonus Tip** The anomaly graph for the mongodb metric is showing where Datadog expects the behavior of the metric to be based on past performance. This is useful for letting you know when your metrics are performing out of the ordinary.

