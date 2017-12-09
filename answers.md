**Collecting Metrics:**

***Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.***

![image](./screenshots/host_tags.png)

***Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.***

In the postgres.yaml file:
```
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: HwUFx2fFVefYm9yc2osaEEoE
    dbname: postgres
    tags:
      - role:db
      - region:east
      - app:backend
```

Bonus: Question Can you change the collection interval without modifying the Python check file you created?

Yes, we can modify the my_metric.yaml file that will be situated in /etc/dd-agent/conf.d

```python
init_config:
    min_collection_interval: 45

instances:
    [{}]
```
