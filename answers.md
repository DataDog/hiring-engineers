Your answers to the questions go here.

## Prerequisites:
I configured a fresh Linux Ubuntu 17.04 VM via the Oracle Virtual Box tool so I would have no OS or dependency issues and I could type my way out of almost anything using the terminal.
I then signed up for a Datadog free account and downloaded everything I needed: the dd-agent, a MySQL cluster, the latest Python and Node.js versions.
Once everything was settled and clean, I started working on the Datadog application. 

## Collecting Metrics:
 * Tags: I modified the datadog.conf.yaml file, uncommented the Tags option and added three tags I thought meaningful for this host.
![Vim interface of the .conf.yaml file](00_ASSETS/01_SCREENSHOTS/METRICS_Tags_conf.png)
![DD's Host Map page](00_ASSETS/01_SCREENSHOTS/METRICS_Tags.png)

 * Custom Check: To create a Custom Agent check we need two files.
One in the datadog-agent/checks.d and one in the datadog-agent/conf.d. We'll see about the later at the next question. 
The first one is a .py document and is a small Python Program just to check a random number between 0 and 1000.
![.py Check](00_ASSETS/01_SCREENSHOTS/METRICS_my_metric_Random.png)

 * Collection interval: The second file is a .yaml configuration file for the check we have previously written. Here we will only tell the Agent to change the default collection_interval to 45 thus changing the rate of submition of the metric.
![.yaml Config](00_ASSETS/01_SCREENSHOTS/METRICS_Interval_yaml.png)

 * **Bonus**:
Elsewhere on the app.datadoghq.com/metric/summary, we have access to the metadata of our metrics therefore we can modify the interval. It also does not modify __neither__ our Python Check File nor our Yaml Config File!
![Web App Metadata](00_ASSETS/01_SCREENSHOTS/METRICS_Interval_web.png)


## Visualizing Data:
 * Timeboard: I created a Timeboard on the Web Application with three graphs:
![My custom metric scoped](00_ASSETS/01_SCREENSHOTS/VISUAL_Timeboard_my_metric_scoped.png)
![The CPU Time from the mysql.performance](00_ASSETS/01_SCREENSHOTS/VISUAL_Timeboard_mysql_perf.png)
![My custom metric with a rollup function](00_ASSETS/01_SCREENSHOTS/VISUAL_Timeboard_my_metric_rollup.png)
As for the script, since I did not use the API but the UI, I wrote a script to fetch my Timeboard which could be used to save it. The Curl request was:
> curl "https://api.dash/883660?api_key=c2a059719d8ed637828c38c8d5699d44&application_key=f291ca2d769bbda165f427a823f004980a00ffeb"
I stored the JSon result in my **00_ASSETS/02_SCRIPTS** folder as **Script_Timeboard_Get**
![Curl GET request](00_ASSETS/01_SCREENSHOTS/Visual_Script_Get_Timeboard.png)

 * Timeboard's timeframe: I unfortunately didn't find how to modify the timeframe to __less than 1h__.

 * Snapshot: 
![Snapshot sent to my account](00_ASSETS/01_SCREENSHOTS/VISUAL_Snapshot.png)

 * Bonus:
The MySql Performance CPU with Anomaly Detection graph is displaying what is normal - the __greyed area__ - and what is not - the __red flagged points__ outside of this greyed area. The greyed area shows a trend of what should be next and by such detects what should not be: strange checks that are way too high or way too low.


## Monitoring Data:
 - Screens of the Monitoring Window

 * Send an email

 * Script 

 * Script

 * Screenshots time!

 * Bonus: Manage Downtime


## Collecting APM Data:
 - Screen of the dd-trace working

 * 

 * Bonus:
From what I understood, a service is a process or a set of processes like a database and a resource is an action for a service like a query to a database. Therefore, a service can have multiple resources.
