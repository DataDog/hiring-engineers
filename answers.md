1 . Configured the Agent to connect to the PostgreSQL server by adding the code below to the conf.yaml.example file. 
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: anQaBgT9qBf8BXRyR76n9RvQ
       tags:
            - optional_tag1
            - optional_tag2
