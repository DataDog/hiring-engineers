## Level 1 - Collecting your Data

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

 ### Bonus question: In your own words, what is the Agent?

 The Agent is a daemon, a long-running, non-interactive background process that runs on your computer (host). The Agent's task can be broken down into three parts: collector, dogstatsd, and the forwarder. The collector runs checks and captures metrics on the current machine for your integrations, while the dogstatsd aggregates your application's metrics, and queues it up for the forwarder to send to Datadog.

 Since daemon tasks are typically denoted with a 'd' (e.g. 'sysmond', 'statsd'), you can see it running in your CPU.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I added the tags: inventory_owner: catkhuu, interactive_user: catkhuu, and role: admin. The tags did not show up until I restarted the Agent with ``` /usr/local/bin/datadog-agent restart ```

![Added Tags](https://github.com/catkhuu/hiring-engineers/blob/catkhuu-support-eng/images/dd_host_map_with_tags.png)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I already had PostgreSQL installed, so I chose the Postgres integration. After installing the integration, I added a ``` postgres.yaml ``` file to ``` conf.d ``` to hookup the integration to the Agent so it can report metrics.

![postgres.yaml](https://github.com/catkhuu/hiring-engineers/catkhuu-support-eng/images/dd_postgres_yaml.png)

I restarted the Agent again for good measure. Afterwards, my host included the recent Postgres integration.

![host post-postgres integration](https://github.com/catkhuu/hiring-engineers/catkhuu-support-eng/images/dd_postgres_yaml.png)

* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

I created a file ``` random.py ``` in ```checks.d ``` where I created my custom Agent Check ``` RandomCheck``` that will send a gauge of a randomly selected number for the metric ``` test.support.random ```. For this check, I chose self.gauge because I am sampling a metric.

![RandomCheck](https://github.com/catkhuu/hiring-engineers/catkhuu-support-eng/images/dd_random_py.png)

To configure our Agent Check, I added a ``` random.yaml ``` file to ``` conf.d ```.  

![random config](https://github.com/catkhuu/hiring-engineers/catkhuu-support-eng/images/dd_random_yaml.png)


## Level 2 - Visualizing your Data

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.

I cloned my Postgres Overview Dashboard and added a few metrics for test.support.random and system.loads 1,5, and 15.

![Cloned Database Dashboard with Metrics](https://github.com/catkhuu/hiring-engineers/catkhuu-support-eng/images/dd_updated_cloned_dashboard.png)

### Bonus question: What is the difference between a timeboard and a screenboard?

The main difference between a timeboard and a screenboard is a timeboard is...


* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

I took a few snapshots of instances when the threshold for test.support.random > 0.90. I am still waiting on my notifications, which have not come as quickly as my monitor alerts.

![Initial snapshots](https://github.com/catkhuu/hiring-engineers/blob/catkhuu-support-eng/images/dd_snapshot_test_support_random.png)

![Second snapshot](https://github.com/catkhuu/hiring-engineers/blob/catkhuu-support-eng/images/dd_second_snapshot.png)


## Level 3 - Alerting on your Data

* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

### Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

I setup a *multi-alert* monitor for test.support.random to alert me when the threshold is greater than 0.90.

![Multi-alert monitor](https://github.com/catkhuu/hiring-engineers/blob/catkhuu-support-eng/images/dd_monitor_setup_form.png)

The monitor was created successfully.

![List of Monitors](https://github.com/catkhuu/hiring-engineers/blob/catkhuu-support-eng/images/dd_monitors_listed.png))

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.

I named this monitor: ``` Threshold reached on test.support.random ```

![Monitor Description](https://github.com/catkhuu/hiring-engineers/blob/catkhuu-support-eng/images/dd_monitor_description.png)

* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

I've received over 20 alerts within the past 15 minutes. So, this monitor is definitely doing its job.

![Monitor Alert Email](https://github.com/catkhuu/hiring-engineers/blob/catkhuu-support-eng/images/dd_email_notif_threshold_reached.png)

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

I scheduled downtime for the ``` Threshold reached on test.support.random ``` monitor from 7PM - 9 AM daily.

![Downtime Setup](https://github.com/catkhuu/hiring-engineers/blob/catkhuu-support-eng/images/dd_downtime_setup.png)

(Note: I am waiting on the email notification from Datadog. It's a little over an hour until downtime.)
