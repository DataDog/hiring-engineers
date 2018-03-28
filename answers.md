# Brandon's Guide to Mastering the Datadog hiring exercise

## Prerequisites - Setting up the environment

*Download and install vagrant with ubuntu image

*Download and install Datadog Ubuntu agent using bash command provided
![alt text](screenshots/1_Prereq_1.png)
![alt text](screenshots/1_Prereq_2.png)

## Collecting Metrics:

*Modify the agent config file to add your own tag mytag:bbdemo

*Go to the host Map page in data dog. Filter by the tag created

![alt text](screenshots/2_Collect_1.png)

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

*Create check config yaml file in conf.d directory. **Bonus Answer** You can specify collection interval here without needing to modify the python script

![alt text](screenshots/2_Collect_9.png)


##Visualizing Data
