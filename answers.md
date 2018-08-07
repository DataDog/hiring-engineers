
<h2>Prerequisites - Setup the environment:</h2>

Your answers to the questions go here-


I already had few virtual machines configured and ready to use in VMWare Workstation installed locally. I decided to use Ubuntu VM for this exercise.

Signed up as Datadog Recruiting Candidate to get necessary credentials to install agent.


<h2>Collecting Metrics:</h2>

**•	Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

Added tags in agent config file datadog.yaml

![tags in yaml](https://i.imgur.com/Y7VYyfC.png)

Screenshot of HostMap page in DataDog

![tags in UI](https://i.imgur.com/eIefCI6.png)

**•	Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

Installing MySQL database
$ sudo apt-get install mysql-server-5.6
Creating the user
$ sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'syedghouri68';"

Granting necessary permissions

$ sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
$ sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"

$ sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
Creating mysql.yaml file
$ sudo vi mysql.yaml

![mysql yaml](https://i.imgur.com/qyJYIEH.png)

Verifying the integration

$ sudo datadog-agent status

![verifying integration](https://i.imgur.com/JDkCp4S.png)

**•	Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

This is achieved by creating two files - Check Module file and YAML configuration file. mycheck.yaml file is placed in conf.d directory. Python module file is placed in checks.d directory, Both the files has same name mycheck.

![mycheck python](https://imgur.com/nyE0kdo.png)

**•	Change your check's collection interval so that it only submits the metric once every 45 seconds.**

![collection interval](https://imgur.com/uU3x0PK.png)

**•	Bonus Question Can you change the collection interval without modifying the Python check file you created?**

Collection interval is changed in YAML file for the tag min_collection_interval. 
