TASK #4: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

ANSWER #4: 

Brief Explanation:
I install mysql and integrating it to Datadog and display on Host map and Overview dashboard.
Turning on the mysql integration automatically collects 61 mysql performance metrics.
Some of them are presented automatically into the MYSQL Overview dashboard.
IMO, one of the best feature on this overview dashboard, if I hover my cursor into one particular widget to look for specific metric, the other widget is displaying the same exact point on the same time widows.
This will significantly reduce the time to correlated data based on time series on different metrics.

Steps:
- On VM sg-db-01
- Install from Ubuntu repository with “apt-get Install mysql-server”
>sudo apt-get install mysql-server

- Created datadog username and password for datadog integration. As of now, I granted all permission to datadog user but only for localhost access which will be done by the Datadog agent.
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED WITH mysql_native_password by '<UNIQUEPASSWORD>';

- Grant permission
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';

- Modified: /etc/datadog-agent/conf.d/mysql.d/conf.yaml
- Go to Host map sg-db-01

Snapshots:
- answer-task4-pic1.png
- answer-task4-pic2.png

Reference:
https://docs.datadoghq.com/integrations/mysql/
