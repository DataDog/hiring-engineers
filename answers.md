#Answer for Recuiting Challenge
I took the docker-containerized approach to complete the Challenge.  
You can reproduce the environment by docker-compose with a deploy script.  
```DD_API_KEY="<DatadogAPIKEY>" YOUR_LOCAL_IP="<LOCAL_HOST_IP>" sh deploy_local.sh```  
The script launches four containers (web, app, db, and datadog-agent) in your computer with `YOUR_LOCAL IP`.  
Following is the flow for containers to launch.
```
1. Postgres db starts with datadog user.
2. Datadog agent starts with configured yaml files inside.
3. Django app starts as backend after database migration.
4. Nginx starts http web service as frontend.
```
---
# 1. Collecting Metrics
* [x] Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

  [tags.yaml](datadog/conf.d/tags.yaml)  
```yaml
tags:
  - project:testweb
  - env:dev
```  
#### Screenshots (Host Map)
  ![Host Map](screenshots/1-hostmap.png)  
  ![Host Map 2](screenshots/1-config.png)

---
* [x] Install a database on your machine and then install the Datadog integration for that database.

  [conf.d/postgres.d/conf.yaml](datadog/conf.d/postgres.d/conf.yaml)  
```yaml
init_config:

instances:
  - host: ${DB_HOST}
    port: 5432
    username: postgres
    password: Test1Pass
    dbname: testweb
    tags:
      - project:testweb
      - role:db
      - env:dev
    custom_metrics:
    - # Active queries
      relation: false
      metrics:
        sum(CASE WHEN state='active' THEN 1 ELSE 0 END): [postgresql.active_queries, GAUGE]
        sum(CASE WHEN state='active' THEN 0 ELSE 1 END): [postgresql.inactive_queries, GAUGE]
      descriptors:
        - [ datname, db ]
      query: "select datname, %s from pg_stat_activity_allusers group by datname;"
    collect_function_metrics: True
```  
  #### PostgresQL Integration
  ![pSQL Integration](screenshots/1-install-db.png)
  ![pSQL Integration 2](screenshots/1-postgres-integration.png)
  
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
