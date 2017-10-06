### Level 1 - Collecting Data

* **Task:** Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from local machine.
  - [Link to Host Dashboard](https://app.datadoghq.com/dash/host/349301929?live=true&page=0&is_auto=false&from_ts=1507061300792&to_ts=1507064900792&tile_size=m)
  - This image shows initial metrics gathered from a virtual Linux system by the Datadog agent:
  <br><br>
  ![Initial Host Dashboard After Setup](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/initial_host_dashboard.JPG?raw=true)


* **Bonus Question:** In your own words, what is the Agent?
  - The agent is software installed to run on a host and collect events and metrics about an application or overall infrastructure.
  - It is composed of three main parts each with different tasks.
    - The collector captures system metrics like memory and CPU usage from the current machine and/or the host integrations.
    - To send custom metrics from an application the agent uses a statsd backend server called Dogstatsd
    - The forwarder interacts with the collector and Dogstatsd to retrieve data from both and queue it for transfer to Datadog.
  - Click [here](https://docs.datadoghq.com/guides/basic_agent_usage/) for more information and a full description of the Datadog Agent.


* **Task:** Add tags in the Agent config file and show a screenshot of host and its tags on the Host Map page in Datadog.
  - Here is a screenshot of the Agent config file (`datadog.conf`), opened with the built in Nano editor, showing two custom tags added (on a line near the middle of the image):
  <br><br>
  ![Custom tags in Agent config file.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/dd_agent_config_tags.JPG?raw=true)

  - *Note:* The `datadog.conf` file location was not specified directly in the [Guide to Tagging](https://docs.datadoghq.com/guides/tagging/) and the link provided in the first paragraph of the "Assigning tags using the configuration files" section led me back to my getting started section rather than an article guiding me toward the file. I was able to find the location from this [article](https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-).
  - This is an image of the Host Map page displaying the tags entered on the datadog.conf file:
  <br><br>
  ![Host Map page screenshot with tags displayed.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/initial_host_map_tags.JPG?raw=true)


* **Task:** Install a database on the virtual machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

  - This image displays successful check of the Postgres integration via the agent `info` command (second from the bottom):
  <br><br>
  ![Agent info command checking Postgres integration.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/pg_agent_info_check.JPG?raw=true)

  - Display of Posgres integration in Host Map page:
  <br><br>
  ![Display of Posgres integration in Host Map.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/pg_host_map.JPG?raw=true)

  - Basic use of Postgres integration metric in a [custom dashboard](https://app.datadoghq.com/dash/373118/miket---support-engineer-applicant-assignment?live=true&page=0&is_auto=false&from_ts=1507149351527&to_ts=1507152951527&tile_size=m):
  <br><br>
  ![Posgres on custom dashboard](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/pg_on_dashboard.JPG?raw=true)


* **Task:** Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

  - The `random_check.yaml` configuration file for the custom check returning a random integer:
  <br><br>
  ![Configuration code in random_check.yaml file for test.support.random custom Agent check.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/random_check_config.JPG?raw=true)

  - The corresponding `random_check.py` file contains the following:
  <br><br>
  ![Image of code in python file for test.support.random custom Agent check.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/random_check_python.JPG?raw=true)


### Level 2 - Visualizing Data

* **Task:** Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.
* **Task:** Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

  - This image displays completion of the two tasks above:
  <br><br>
  ![Screenshot of cloned Postgres dashboard with added metric from test.support.random](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/random_check_pg_dashboard.JPG?raw=true)


* **Bonus Question:** What is the difference between a timeboard and a screenboard?
  - They are both dashboard types but their primary difference is that in a timeboard all graphs are scoped to the same time frame set while the screenboard is more flexible allowing for greater customization, deeper analysis of a system, and graphs displayed with varying time scopes.

  - A control of the timeboard time scope:
  <br><br>
  ![Timeboard scope setting in dashboard](https://help.datadoghq.com/hc/en-us/article_attachments/202547215/TimeControl.jpg?raw=true)

  - In a timeboard, graphs appear in a grid-like layout making them great for finding correlation patterns or troubleshooting issues.  With a time board you can share individual graphs.

  - By contrast, a screenboard has a more customizable widget layout and can be shared as an entire single read-only live entity.


### Level 3 - Alerting on Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  

* **Task:** Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

* **Bonus Task:**  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
  - The following image demonstrates completion of the two tasks above, displaying a multi-alert monitor tracking two hosts starting at roughly 13:13.  Both hosts have the same `project:miket_interview_challenge` tag through which the grouping has been made, and they share the same custom check yielding a random value. The monitor is set to trigger when either of these hosts exceeds a threshold of 0.90.
  <br><br>
  ![](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/multi_alert_monitor.JPG?raw=true)


* **Task:** Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.

 - The message sent when this monitor is triggered handles dynamic insertion of the `host.name` variable and reminds the recipient of the conditions prompting the alert.
 <br><br>
 ![Monitor message settings, title, and body.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/monitor_message.JPG?raw=true)


* **Bonus Task:** This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
  <br><br>
  - Email notification of the monitor alert being triggered:
  ![Email of monitor alert message.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/monitor_response_email.JPG?raw=true)

* **Bonus Task:** Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  - A display of the scheduled downtime settings:
  <br><br>
  ![Downtime settings.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/monitor_silent_hours.JPG?raw=true)

  - The following is an email confirmation of downtime (*Note*: The time interval in the message refers to 3:15pm to but that was only to force the email to be sent right away instead of waiting until 7pm to take a screenshot ):
  <br><br>
  ![](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/monitor_silence_conf_email.JPG?raw=true)
