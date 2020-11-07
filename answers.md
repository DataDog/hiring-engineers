### Answering all the technical exercise by Kazutoshi Shimazu ###

## Prerequisites - Setup the environment ##

Installing Ubuntu/xenial64 OS with MySQL on My MAC laptop running Vagrant

## Collecting Metrics: ##

Installing mysql

Creating the DB user for datadog agent
```vb

root@main:/etc/datadog-agent/conf.d/mysql.d# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.7.32-0ubuntu0.16.04.1 (Ubuntu)
<snip>

mysql> create user datadog@localhost identified by 'datadog';
Query OK, 0 rows affected (0.00 sec)

mysql> grant replication client on *.* to 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> grant process on *.* to 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

```
