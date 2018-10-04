Hello.
Thank you for giving me the opportunity to be considered for the sales engineer role at Datadog.  By performing this exercise I have developed a deeper appreciation for your technology.  Below are my answers to the questions posed in this project.

**Collecting Metrics**.
*   Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
This could be accomplished through the web ui by going to the infrastructure list section and clicking on inspect next to your host.
(https://ibb.co/fzbcYe)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
I installed MySQL and followed the following steps to integrate with Datadog.
Create a datadog user with replication rights in your MySQL server
  sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'q7COu>Y98kQwAdzSUJVnre5l';"
  sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
  sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
  sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
After creating the datadog user and providing the appropriate privileges, I had to configure the agent to connect to MySql.

Edit conf.d/mysql.yaml
```        init_config:
          instances:
          - server: localhost
          user: datadog
          pass: 1234566
          tags:
            - optional_tag1
            - optional_tag2
           options:
            replication: 0
            galera_cluster: 1 
```
Then restart the Agent.

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
This was especially interesting and fun.  To accomplish this there needs to be a configuration file and the check script.  Naming matters and so I named my script customcheck.py and therefore the configuration file was named customcheck.yaml .  Here is the contents of customcheck.py:

```import random
   from checks import AgentCheck
   class HelloCheck(AgentCheck):
      def check(self, instance):
          x= random.randint(1,1000)
          self.gauge('Hello.CustomMetric', x)
```
In customcheck.py we import the random library for python.  This will be the source for our custom metric.  We import the AgentCheck 
object from checks and use it to create our metric.  We pick a random number between 1 and 1000 and print it.

For the configuration file, customcheck.yaml:
```
instances:
    - {}
```
This worked and produced a random number between 1 and 1000.

*  Change your check's collection interval so that it only submits the metric once every 45 seconds.
To change the collection interval, all that was needed was modifying customcheck.yaml with the following:
  ```
  instances:
    - {}
    - min_collection_interval: 45
```
**Visualizing Data:**





