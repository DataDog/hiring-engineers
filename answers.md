# Prerequisites - Setup the environment

My approach was to spin up a Debian 10 Linux Server running on a Public Cloud Provider

The DataDog Agent installed with the following command:

```
$ DD_API_KEY=<MY_API_KEY> DD_SITE="datadoghq.eu" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

# Collecting Metrics:

**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

I added the following tags on the /etc/datadog-agent/datadog.yaml file:

```
tags:
   - env_test:testing_datadog_tags
   - test:succeeded
```

Screenshots: [screenshots/debian-dd-box_extra_tags.png]


**Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

I installed Mysql Database and took the following steps for datadog integration collects metrics:

1) Added datadog user on Mysql Database with right privileges;
2) create the datadog-agent/conf.d/mysql.d/conf.yaml as follow to get metrics collected:

```
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: '<DATADOG_MYSQL_PASS>' 
    port: 3306 
    options:
        replication: 0
        galera_cluster: true
        extra_status_metrics: true
        extra_innodb_metrics: true
        extra_performance_metrics: true
        schema_size_metrics: false
        disable_innodb_metrics: false
```

3) Restart the datadog Agent;
4) Install datadog mysql integration on the datadog dashboard.

Screenshot: [screenshots/debian-dd-box_mysql_integration.png] [screenshots/debian-dd-box_mysql_metrics.png]
Screenshot: [screenshots/debian-dd-box_mysql_metrics.png]
