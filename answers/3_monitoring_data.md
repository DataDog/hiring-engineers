# Monitoring Data

### Define thresholds on metrics to monitor and send corresponding email alerts.

1. Navigate the Datadog interface: Monitors > New Monitor
2. Select Metric on the side menu.
3. Choose Threshold Alert as the detection method.
4. Define the metric as follows:
    - Metric = **my_check**
    - from = **host:vagrant**
    - **Simple Alert**
5. Set alert conditions as follows:
    - Alert threshold = **800**
    - Warning threshold = **500**
    - **Notify** if data is missing for more than **10** minutes.
6. Say what's happening by copy-pasting the following configuration:

    ```
    {
    	"name": "Random number is high at {{host.name}}",
    	"type": "metric alert",
    	"query": "avg(last_5m):avg:my_check{host:vagrant} >= 800",
    	"message": "{{#is_alert}}\nAlert: Random number have exceeded an average of 800 over the past 5 minutes.\nValue: {{value}}\nHost: {{host.name}}\n{{/is_alert}}\n\n{{#is_warning}}\nWarning: Random number have exceeded have exceeded an average of 500 over the past 5 minutes.\nValue: {{value}}\nHost: {{host.name}}\n{{/is_warning}}\n\n{{#is_no_data}}\nAlert: No data for random number over the past 10 minutes.\nValue: Unknown\nHost: {{host.name}}\n{{/is_no_data}}\n\nContact @marc.santos083@gmail.com",
    	"tags": [],
    	"options": {
    		"timeout_h": 0,
    		"notify_no_data": true,
    		"no_data_timeframe": 10,
    		"notify_audit": false,
    		"require_full_window": true,
    		"new_host_delay": 300,
    		"include_tags": false,
    		"escalation_message": "",
    		"locked": false,
    		"renotify_interval": "0",
    		"thresholds": {
    			"critical": 800,
    			"warning": 500
    		}
    	}
    }
    ```
    JSON config [here](../scripts/monitor.json).
    
    **Note:** Different messages are sent based on whether the monitor is in an Alert, Warning, or No Data state.
    
    Sample Notification:

    ![Alt text](../images/3_alert_sample.png?raw=true "Sample Notification")

    **Note:** Metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state are indicated.

### Set up two scheduled downtimes

1. Downtime from 7pm to 9am daily on Mondays-Fridays

    a. Navigate to Monitors > Manage Downtime.

    b. Choose what to silence:

        - By monitor name
        - Monitor = <INSERT MONITOR NAME>
        - Group scope = host:vagrant

    c. Specify the schedule:

        - Recurring
        - Start Date = 2018/10/06
        - Time Zone = Asia/Tokyo
        - Repeat Every = 1 days
        - Beginning = 19:00
        - Duration = 14 hours
        - Repeat Until = No end date

    d. Add a message:

        - Hi @marc*****@gmail.com, This is a scheduled downtime. FYI.

2. Downtime on Saturday and Sunday

    a. Navigate to Monitors > Manage Downtime.

    b. Choose what to silence:

        - By monitor name
        - Monitor = <INSERT MONITOR NAME>
        - Group scope = host:vagrant

    c. Specify a schedule:

        - Recurring
        - Start Date = 2018/10/06
        - Time Zone = Asia/Tokyo
        - Repeat Every = 1 weeks
        - Repeat On = Sun, Sat
        - Beginning = 00:00
        - Duration = 24 hours
        - Repeat Until = No end date

    d. Add a message:

        - Hi @marc*****@gmail.com, This is a scheduled downtime. FYI.

3. Sample Notification:

    ![Alt text](../images/3_downtime.png?raw=true "Sample Notification")

[Next: Collecting APM Data](./4_collecting_apm_data.md)

[Back to Index](../answers.md)
