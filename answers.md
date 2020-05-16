# Prerequisites

To begin this exercise, I assesed the options for a development environment to effectively model Datadog’s functionality that's also feasible within the confines of my Chromebook running Chrome OS. I opted to dual-boot my machine to run [GalliumOS](https://galliumos.org/), a lightweight Linux distribution based on Xubuntu, partitioned alongside the Chrome OS. From my new VM, I was easily able to sign up for Datadog and begin running the agent.  

# Collecting Metrics 
Next, I added the below tags into the `tags` block of my agent configuration file to add some more details on my machine.

```
## @param tags  - list of key:value elements - optional
#
tags:
   - environment:dev
   - chassis:desktop
   - os:galliumos3.1
   - kernel:linux4.16.18
```

Here is my host, named `katelyn.localhost`, and its tags, shown bottom right, on the Host Map page in Datadog.

![My host with tags](screenshots/host_with_tags.png)


I opted to download a PostgreSQL database on my machine and install the corresponding Datadog integration to begin collecting those metrics and logs.  After creating user `datadog` and granting the role `pg_monitor` to that user,  here is a verification of the correct permissioning on my PostgreSQL database:

![Postgres connection OK](screenshots/postgres_connection_ok.png)

To make this integration more meaningful, I wanted to allow for metric collection and log integration.  To do so, I altered my `postgres.d/conf.yaml` [configuration file](https://github.com/kmglassman/hiring-engineers/blob/kmglassman-answers-test/conf-files/postgres.d_conf.yaml) to point to my host/port and to configure logging, shown here: 
```
instances:

    ## @param host - string - required
    ## The hostname to connect to.
    #
  - host: katelyn.localhost

    ## @param port - integer - required
    ## Port to use when connecting to PostgreSQL.
    #
    port: 5432

    ## @param user - string - required
    ## Datadog Username created to connect to PostgreSQL.
    #
    username: datadog

    ## @param pass - string - required
    ## Password associated with the Datadog user.
    #
    password: *******

    ## @param dbname - string - optional - default: postgres
    ## Name of the PostgresSQL database to monitor.
    #
    dbname: datadog
```
```
logs:
 - type: file
   path: "/etc/postgresql/12/main/pg_log.log"
   source: postgresql
   service: pslogservice
```

and altered my machine's `postgresql.conf` [configuration file](https://github.com/kmglassman/hiring-engineers/blob/kmglassman-answers-test/conf-files/postgresql.conf) to configure logging, shown here:

```
logging_collector = on                          # Enable capturing of stderr and csvlog
                                                # into log files. Required to be on for
                                                # csvlogs.
                                                # (change requires restart)

# These are only used if logging_collector is on:
log_directory = 'pg_log'                        # directory where log files are written,
                                                # can be absolute or relative to PGDATA
log_filename = 'pg.log'                         # log file name pattern,
                                                # can include strftime() escapes
log_file_mode = 0644                            # creation mode for log files
```

After a quick change to `logs_enabled: true` in my Datadog agent configuration file, my setup was ready to begin log collection. 

The output of a call to `sudo datadog-agent status`, shown below, verifies that the PostgreSQL integration and logging is functioning.  

![Postgres status](screenshots/postgres_status.png)

![Logs status](screenshots/logs_status.png)


I then introduced my own metric to begin tracking on my host.  I created a new check called `custom_check` using the script `custom_check.py`, which can be found [here](https://github.com/kmglassman/hiring-engineers/blob/kmglassman-answers-test/scripts/custom_check.py).  

**Bonus question**: To change the check's collection interval without modifing this Python file, I altered the check [configuration file](https://github.com/kmglassman/hiring-engineers/blob/kmglassman-answers-test/conf-files/custom_check.yaml), `custom_check.yaml`, as shown below:
```
init_config:

instances:
  - min_collection_interval: 45
```

Now, my check is up and running as expected, submitting a random value between 0 and 1000 every 45 seconds.  

# Visualizing Data

Next, I used the Datadog API to generate some visualizations in the form of a Timeboard.  The script I used can be found [here](https://github.com/kmglassman/hiring-engineers/blob/kmglassman-answers-test/scripts/timeboard.py).  Some highlights of the script:
* I set the parameters for my three timeseries visualizations each within the `widgets` parameter.
* I prompt for a title and a description of the Timeboard to be created.
* I then pass my API key and app key and make the connection.

Here is the view of my new timeboard, [Katelyn's Timeboard](https://app.datadoghq.com/dashboard/vas-prc-xq8/katelyns-timeboard?from_ts=1589597791299&live=true&to_ts=1589612191299), upon creation with my script:

![My Timeboard](screenshots/my_timeboard.png)

Here are each of my visuals after I set the timeframe to the last 5 minutes.

My custom metric scoped over katelyn.localhost:
![My metric](screenshots/my_metric_5m.png)
My Postgres buffer hit:
![Postgres anomaly](screenshots/postgres_anomaly_5m.png)
And the sum of my custom metric in buckets of one hour, which does not appear to be an informative visual at this 5 minute timeframe:
![Sum of my metric](screenshots/my_metric_sum_5m.png)

I took a snapshot of my first graph  and wrote a notification for myself:

![Snapshot](screenshots/snapshot.png)

and confirmed receipt to my Gmail:
![Email notif](screenshots/email_notif.png)


**Bonus Question**: My anomaly graph shows when the buffer hit count to my PostgreSQL database is greater than 2 standard deviations from the average buffer hit count over the given 5 minute timeframe. 


# Monitoring Data
After making my Timeboard, I initialized a monitor to watch the average value of `my_metric` over the past 5 minutes.  Below are the configurations I used to set up this monitor:

![Monitor](screenshots/monitor1.png)


![Monitor](screenshots/monitor2.png)


These configurations allowed my email notifications to be customized depending on the condition of the monitor trigger - Warning, Alert, or No Data.  Here is an example of the Alert notification, as received by email:

![Monitor alert](screenshots/monitor_alert.png)

**Bonus Question**: I set up two recurring downtimes for my monitor.  One for 7pm-9am ET Mondays to Fridays:

![Downtime](screenshots/schedule_downtime1.png)

and one all day Saturdays and Sundays, also in ET:

![Downtime](screenshots/schedule_downtime2.png)

Below are the email notifications of the upcoming downtimes.  The notifications express the downtimes in UTC, not ET, so there is a 4-hour offset.

![Downtime email](screenshots/downtime_email.png)

![Downtime email](screenshots/downtime_email2.png)


## Collecting APM Data
