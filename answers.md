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

### Collecting APM Data

### Final Question

```

```
