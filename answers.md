Your answers to the questions go here.

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![Agent Tags](images/Agent_Tags.png)

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
![mysql_install](images/mysql_install_1.png)
![mysql_install](images/mysql_install_2.png)

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
my_metric.py
+ from checks import AgentCheck
+ class myCheck(AgentCheck):
+        def check(self, instance):
+                self.guage('my_metric', 223)
                
Change your check's collection interval so that it only submits the metric once every 45 seconds.
+ my_metric.yaml
+ init_config:
+ min_collection_interval: 45
+ instances:
+        [{}]

Bonus Question Can you change the collection interval without modifying the Python check file you created?
