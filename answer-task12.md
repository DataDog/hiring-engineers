TASK #12: 
Please configure the monitor’s message so that it will:
•	Send you an email whenever the monitor triggers.
•	Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
•	Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

ANSWER #12

Brief Explanation:
After defining the right condition to monitor the threshold, I would need to make sure they come me accurately.
I configure the alert subject, which is normally, a brief description about what and where the alert from.
Then, the alert detail, to provide more information about what, where, why and when the alert gets triggered.
Last, I can use some variable to automatically match the alert condition and the detail.

Steps:
- Configure the alert message subject. 
- Configure the alert body message.
- Configure alert variable 

Snapshot:
- answer-task12-pic1.png

Reference:
https://docs.datadoghq.com/monitors/notifications/?tab=is_alertis_warning#variables
