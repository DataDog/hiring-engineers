Collecting APM Data:

TASK #15:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
•	Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.
Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
Please include your fully instrumented app in your submission, as well.

ANSWER #15

Brief Explanation:
APM is the monitoring and management of performance and availability of applications. APM strives to detect and diagnose complex application performance problems to maintain high level of service. APM is commonly used for Web Application.

APM closely monitor performance metrics defines by user experience of the application like average response time under peak hours.
APM will be able to triage performance issue that related to hybrid infrastructure that runs the application.
Last, APM will be able to trace problem and find the root cause through analyzing transactions, queries and error codes.

Steps:
- PHPMYADMIN application is running on Apache Server (sg-web-01) and MySQL database (sg-db-01)
- installed datadog-php-tracer.deb on sg-web-01
-	enable APM in Datadog.yaml
-	adding PHP.ini with extension and ddtracer wrapper
-	adding the linux environment variables

Public URL:
- https://p.datadoghq.com/sb/x04kigxjnn4olmb7-4678ad177b65508402a0ec3d7ac7a322

Dashboard Explanation
I categorized my dashboard into 4 sections as follows:
- Application Performance => display high level application performance metrics like Web and Database Request / Duration
- Infrastructure => display the resource consumption on application and database server
- Problem Tracing => display high level problem like SLAO/SLA, Triggered Alarm and Log Statistic
- Anomalies and Forecasts => would be used for planning and prevention of future problem and knowing the unknown

Snapshot:
- answer-task15-pic1.png
