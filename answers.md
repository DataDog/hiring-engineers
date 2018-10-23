Your answers to the questions go here.

# Prerequisites - Setup the environment

#### After skimming the overview, I downloaded Datadog onto my machine--pretty smooth, or so I thought!--used `vagrant up` and `vagrant ssh` to power up vagrant, retrieved my API key, added my tags, and installed Agent v6. After the instructions stopped being compatible with what I was seeing, I realized that I had actually installed the agent directly onto my machine instead of my virtual machine. 

#### After deleting the agent and reinstalling for ubuntu, I was then denied access to the files inside the agent directory. After searching online about how to change permissions, I learned that changing into the root@vagrant directory gives access to all files.

#### Script for fresh install of Agent v6 (minus API key):
```DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"```

#### **Agent status shows proper configuration:**

[[<img width="365" alt="successful_integration" src="https://user-images.githubusercontent.com/10853262/47392866-9c62d880-d6d2-11e8-9f38-df77fbf2c7e3.png">]]

# Dashboard

#### Screenshot of host with no tags:

[[<img width="947" alt="host" src="https://user-images.githubusercontent.com/10853262/47334581-3461b300-d63c-11e8-9162-bed1be09124f.png">]]

#### After adding tags in the Agent config file, a screenshot of my Host Map and its tags:

[[<img width="1138" alt="host_with_tags" src="https://user-images.githubusercontent.com/10853262/47376532-ae7b5180-d6a7-11e8-8508-c4d5d3c0e08d.png">]]

# Collecting Metrics

#### I then installed a database on my machine (PostgreSQL) called dekker_db and followed the integration steps [here](https://docs.datadoghq.com/integrations/postgres/). Unfortunately, I copied and pasted too quickly and retained the password <PASSWORD> (not ideal!).

#### After creating a read-only Datadog user with access to the PostgreSQL server, I edited **postgres.d/conf.yaml** and my PostgreSQL configuration file, **/etc/postgresql/9.5/main/postgresql.conf** to facilitate metric collection. 

### **/etc/postgresql/9.5/main/postgresql.conf** had the following uncommented:

```logging_collector = on
  log_directory = 'pg_log'  # directory where log files are written,
                            # can be absolute or relative to PGDATA
  log_filename = 'pg.log'   #log file name, can include pattern
  log_statement = 'all'     #log all queries
  log_line_prefix= '%m [%p] %d %a %u %h %c '
  log_file_mode = 0644
  ## For Windows
  #log_destination = 'eventlog'```

#### In **datadog.yaml**, I set `logs_enabled: true`  added the log configuration block in **postgres.d/conf.yaml**.

####**postgres.d/conf.yaml**

```init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: <PASSWORD>
    dbname: dekker_db
    ssl: False
    use_psycopg2: False
    tags:
    - postgres
    collect_count_metrics: False
  
logs:
  - type: file
    path: /var/log/postgres_log/postgres.log   
    source: postgresql
    sourcecategory: database
    service: myapp
    #To handle multi line that starts with yyyy-mm-dd use the following pattern
    #log_processing_rules:
    #  - type: multi_line
    #    pattern: \d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])
    #    name: new_log_start_with_date```

#### Screenshot of Postgres integration on Host Map:

[[<img width="1015" alt="host_with_postgres" src="https://user-images.githubusercontent.com/10853262/47393308-f44e0f00-d6d3-11e8-8c81-b6ab1e99110f.png">]]

#### Screenshot of Postgres Overview and Metric Dashboards:

[[<img width="566" alt="postgres_overview" src="https://user-images.githubusercontent.com/10853262/47393321-fdd77700-d6d3-11e8-93f4-03c6e10320ab.png">]]

[[<img width="1044" alt="postgres_metrics" src="https://user-images.githubusercontent.com/10853262/47393325-fdd77700-d6d3-11e8-8173-6d6e5fe7b083.png">]]

#### Datadog Agent Status Check:

[[<img width="368" alt="postgres_check" src="https://user-images.githubusercontent.com/10853262/47393520-94a43380-d6d4-11e8-9a76-ff67e1520f10.png">]]

# Visualizing Data

# Monitoring Data

# Collecting APM Data:

# Final Question