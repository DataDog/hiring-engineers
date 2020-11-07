### Answering all the technical exercise by Kazutoshi Shimazu ###

## Prerequisites - Setup the environment ##

Installing Ubuntu/xenial64 OS with MySQL on My MAC laptop with Vagrant file

## Collecting Metrics: ##

# Installing mysql on ubuntu VM #
```vb
sudo apt install mysql-server
```

# Creating the MySQL DB user for datadog agent instead of using root user #
```vb

mysql> create user datadog@localhost identified by 'datadog';
Query OK, 0 rows affected (0.00 sec)

mysql> grant replication client on *.* to 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> grant process on *.* to 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

```

# Creating the `conf.yaml` under the `/etc/datadog-agent/conf.d/mysql.d/`

