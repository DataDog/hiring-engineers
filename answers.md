# Solutions Engineer Answers

## by Jacob Feinberg

### Prerequisites - Setup the environment

- For this challenge I used my local machine as the host for the datadog agent. My OS is the macOS High Sierra Version 10.13.6
- I followed the prompt, signed up for a free trial at https://www.datadoghq.com/, and used the Mac OS installation instructions

> As a backup plan for if I ran into any OS/dependency issues I also installed a VM using Vagrant.

### Collecting Metrics

The next step was to add some custom tags to the Agent config file.

- I navigated to the agent config file at /etc/datadog-agent/datadog.yaml. Here is a screen shot of the custom tags I added to the config file:

![agentTags](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Collecting%20Metrics/Tags_Agent_Config_File.png)

- You can see that adding these tags to the config file worked by viewing them on the Host Map page in Datadog:

![hostMapTags](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Collecting%20Metrics/Tags_Host_Map_UI.png)

The next step was to set up an integration with a database on my machine. Since I was using my local machine and already had PostgreSQL installed, I then installed the specific integration for postgres.

- After creating a read-only datadog user with proper access to my PostgreSQL Server I had to configure the Agent to connect to it.

  - Since most integrations are already installed in the `conf.d` folder in the `datadog-agent`. I just had to configure the specific integration file for postgres:

    ```bash
    /etc/datadog-agent/conf.d/postgres.d/conf.yaml
    ```

  - Here I was able to add my own configuration for my PosgreSQL Server:

    ```bash
    init_config:

    instances:
    - host: localhost
    port: 5432
    username: datadog
    password: <my_password>
    tags:
        - hostname:jacobsmachine
        - env:dev
        - proj:solutinsengineer
    ```

Next I created a custom Agent check that submitted a metric name `my_metric` with a random value between 0 and 1000.

- I did this by creating a [custom_check.py](https://github.com/JTFeinberg/hiring-engineers/tree/Jacob_Feinberg_Solutions_Engineer/Collecting%20Metrics/Custom%20Check/custom_check.py) file.
- This file was placed under the `/etc/datadog-agent/checks.d`
  folder and contained the script that the agent will run to perform the check.
- I was able to configure the check by adding a `yaml` file with the [same name](https://github.com/JTFeinberg/hiring-engineers/tree/Jacob_Feinberg_Solutions_Engineer/Collecting%20Metrics/Custom%20Check/custom_check.yaml) as the check file under `/etc/datadog-agent/conf.d`.

  - I configured the check to run every 45s with the following:

  ```bash
  init_config:

  instances:
    - min_collection_interval: 45
  ```

### Visualizing Data

To visualize some data I utilized the Datadog API an created a Timeboard that contains:

- My custom metric scoped over my host.
- Any metric from the Integration on my PostgreSQL database with the anomaly function applied.
- My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

I did this by using the folowing curl comand in my termianl:

```bash
curl -X POST \
  'https://api.datadoghq.com/api/v1/dash?api_key=<API_KEY>&application_key=<APP_KEY>' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
"graphs" : [{
"title": "Custom Metric",
"definition": {
"events": [],
"requests": [
{"q": "avg:system.mem.free{*}"}
],
"viz": "timeseries"
}
},
{
"title": "Anomalies - PostgreSQL Rows Returned",
"definition": {
"events": [],
"requests": [
    {"q": "anomalies(postgresql.rows_returned{*}, '\''basic'\'', 2)"}
    ],
"viz": "timeseries"
}
},
{
"title": "Average Custom Metric RollUp Sum last hour",
"definition": {
"events": [],
"requests": [
{"q": "avg:my_metric{*}.rollup(sum, 3600)"}
],
"viz": "query_value"
}
}
],
"title" : "My_Metric Timeboard",
"description" : "An informative timeboard about my custom metric.",
"template_variables": [{
"name": "host1",
"prefix": "host",
"default": "host:my-host"
}],
"read_only": "True"
}'
```

When I opened the Dashboard in the UI I was able to see the three graphs that were created:

![timeboards](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Visualizing%20Data/Full_Timeboard.png)

After setting the time frame for the past 5 minutes the dashboard looked like so:

![5min_timeboards](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Visualizing%20Data/5min_time_frame.png)

I then took a snapshot of the
Custom Metric graph and used the @ notation to send it to myself. The following is the notification I received:

![5min_snapshot](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Visualizing%20Data/Snapshot_%40JacobFeinberg.png)

- The Anomaly graph is displaying what the chosen algorithm expects the normal range of a metric to be at any given time. It does this by using past and current data trends.

### Monitoring Data

For setting up the monitors for `my_metric`, I used the Datadog UI which had simple and well labeled form.

- First I created a monitor that watches the avaerage of `my_metric` and alerts me if it’s above the following values over the past 5 minutes:
  - Warning threshold of 500
  - Alerting threshold of 800
  - And it will notify me if there is No Data for this query over the past 10m.
- Here is what the form in the UI looks like when those values are inputted:

![monitorForm](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Monitoring%20Data/Set_Threshold_Monitoring_Levels.png)

- I also configured a custom message to:
  - Send you an email whenever the monitor triggers.
  - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
  - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
- Here is what that configuration looks like:

![customMessage](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Monitoring%20Data/Custom_Message.png)

- Here is what the warning message looks like for my custom template:

![warning](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Monitoring%20Data/Warning_Notification.png)

- After these monitors were set up, I also scheduled downtimes for it with the following conditions:
  - One that silences it from 7pm to 9am daily on M-F
    ![weekdayDowntime](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Monitoring%20Data/Weekday_Downtime.png)
  - And one that silences it all day on Sat-Sun.
    ![weekendDowntime](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Monitoring%20Data/Weekend_Downtime.png)
  - My email is notified when I scheduled the downtime.
    ![weekdayNotification](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Monitoring%20Data/Weekday_Notification.png)
    ![weekendNotification](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Monitoring%20Data/Weekend_Notification.png)

### Collecting APM Data

- Since I was going to be using the [provided example as my application](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Collecting%20APM%20Data/app.py) I first had to install flask by running `pip install flask`
- Then to set up Datadog's APM solution I first followed the [docs](https://docs.datadoghq.com/tracing/languages/python/) and ran `pip install dd-trace`
- Since the APM agent (aka Trace Agent) isn't part of the OSX Datadog Agent yet, it needed to be run manually on the side.

  - I followed the [docs here](https://github.com/DataDog/datadog-trace-agent)
  - I also made sure that the apm_config was enabled in the `/etc/.datadog-agent/datadog.yaml`

  ![apmConfig](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Collecting%20APM%20Data/apm_config.png)

  - With the trace agent running manually on the side, and everything configured for my flask app, I was able to run `dd-trace-run python app.py` to begin collecting data on my flask app.

    - I made some requests to my running flask app and could see them in my trace list in the Datadog UI:

    ![traceList](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Collecting%20APM%20Data/Trace_List.png)

    - I was also able to create a dashboard with my traces and some infrastucture data. [Here is an example](https://app.datadoghq.com/dash/1047022/jacobs-timeboard-16-jan-2019-1525?tile_size=m&page=0&is_auto=false&from_ts=1548036000000&to_ts=1548122400000&live=true) of that:

    ![apmInDashboard](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Collecting%20APM%20Data/APM_Infrastructure_Metrics.png)

- Service vs. Resource
  - Service: A set of processes that do the same job (ex. a web application, or a database). In the case of the APM I just set up, the service is the [flask app](https://github.com/JTFeinberg/hiring-engineers/blob/Jacob_Feinberg_Solutions_Engineer/Collecting%20APM%20Data/app.py) I set up.
  - Resource: A Resource is a particular action for a service. In the case of the APM I just set up, a resource would be a api call such as GET /api/apm.

### Final Question

One idea that came to mind for a Datadog use case is for airlines to monitor their ticket pricing. Every once in a while either a computer algorithm gets something wrong, or user error causes a flight to be put up at an extreme discount. Not that I'm really advocating for this, BUT I could see airlines using datadog to monitor these anomolies and make sure that they aren't giving \$200 flights to Hawaii.
