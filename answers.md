## Environment Setup

Host OS: Mac OS X
Installed Vagrant
Vagrant OS: ubuntu/xenial64
  
  ## Collecting Metrics
  
##  Install Agent

```
  DD_API_KEY=<<API_KEY>> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

##  Adding Tags

The configuration files and folders for the Agent are located in:

/etc/datadog-agent/datadog.yaml

1. edit datadog.yaml
2. Add tags

```
tags:
    - env:trial
    - type:vagrant
    - role:dd_challenge
```
3. Restart datadog agent
```
$sudo service datadog-agent status
```
4. Host Map in action

![Host Map](/img/Host_Map.png)


##  Integration with Postgres

1. Install Postgres

2.Create user with proper access to your PostgreSQL server

```
sudo psql
postgres=# create user datadog with password '<PASSWORD>';
postgres=# grant pg_monitor to datadog;
```
3. Create & configure postgres.d/conf.yaml file to point to your server, port etc.
$vi /etc/datadog-agent/conf.d/postgres.d/config.yaml 
change parameters

```
    host: localhost
    port: 5432
    username: datadog
    password: <PASSWORD>
```
4. Restart Agent

```
$sudo service datadog-agent status
```
5. Postgres on Host Map

![Host Map_Postgres](/img/host_map_postgres.png)
