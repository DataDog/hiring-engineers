## Below is the answers provided by Hanting ZHANG in response to the `Solutions Engineer` recruitment exercises 

## Prerequisites - Setup the environment

First, I created a trial account on Datadog, And I followed the instructions to install an agent on Windows 10.
The installation file can be found at [Datadog App Page](https://app.datadoghq.com/account/settings#agent/windows).<br>
The API key required for installation can be found via the menu at [Integration->APIs](https://app.datadoghq.com/account/settings#api) 

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

*Solution:*<br> Add the tag 'HantingPC' in the configuration file (for Windows 10, the file can be found at C:\ProgramData\Datadog\datadog.yaml) under the option 'tags'.
<br>
The configuration file is also attached in the pull request [datadog.yaml](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/conf/datadog.yaml)
<br>
Screenshot : <br>
![SCREENSHOT 1](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/1.agentTag.PNG)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.


*Solution:* <br>
1.Install PostgreSql on the local machine, Screenshot : ![SCREENSHOT 2](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/2.postgreSql_local_installation.PNG) <br>
2.Install integration for PostgreSql by following the configuration instruction on the Integration Tab <br>
	-Create user 'datadog' who has the right to query the database stats <br>
	-Create a configuration file at C:\ProgramData\Datadog\conf.d\postgres.d\postgres.yaml stating the database ip, username, password and tags <br>

   The postgres configuration file is attached at	[postgres.yaml](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/conf/postgres.yaml) <br>
3.Restart the datadog agent<br>
4.We can now see the database metrics via the dashboard tab. <br> 
Screenshot: ![SCREENSHOT 3](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/3.postgreSql_dashBoard.PNG) 

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

*Soulution:*<br>
In order to configure a custom metric, we need to put 2 files in datadog folders (C:\ProgramData\Datadog\checks.d for the check and C:\ProgramData\Datadog\conf.d for its configuration) <br>
1.The .yaml configuration file [*mycheck.yaml*](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/conf/mycheck.yaml) <br>
2.The class file [*mycheck.py*](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/src/mycheck.py) <br> 
The are both included in the pull request

After the 2 files are added, restart the datadog agent, we can see the check in the tab 'Metrics'. By click on 'explore' and search for 'mycheck'. Screenshot: ![SCREENSHOT 4](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/4.myMertric.PNG)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

*Solution:*<br>To configure the submission interval of the metric, simply add `min_collection_interval: 45` in the configuration file of the check 

* **Bonus Question** 

The bonus question is answered in the section above.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.

*Solution:* <br>
I found a way to use datadog API with PostMan [here](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs). With the [datadog API doc](https://docs.datadoghq.com/api/?lang=python#create-a-timeboard), I was able to come up with the following script : <br>
[myTimeboard.py](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/src/myTimeBoard.py "myTimeboard.py") <br> 
I also downloaded datadog Python library in order to run and test the script via this [link](https://github.com/DataDog/datadogpy). <br> 
The following screenshot shows the timeboard created by the script: <br>
![SCREENSHOT 5](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/5.TimeBoard.PNG "SCREENSHOT 5") <br>

The anomaly detection for the postgreSql database is based on the number of connections <br>


Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

*Solution:* <br>
Select a 5 minute interval on one of the graphs on the timeboard, the timeboard will 'zoom'. <br>
![SCREENSHOT 6](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/6.TimeBoardWith5MinTimeRange.PNG)
<br>

* Take a snapshot of this graph and use the @ notation to send it to yourself.

*Solution:* <br>
Click the camera icon to take a picture of the graph and use the @ annotation in the comment section <br>
![SCREENSHOT 7](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/7.TimeBoardGraphWithNotification.PNG) 
<br>
Enter the comment and I received a mail <br>
![SCREENSHOT 8](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/8.TimeBoardGraphWithNotificationMail.PNG)

* **Bonus Question**: What is the Anomaly graph displaying? <br> 
*Solution:* <br>
According to datadog documentation about anomaly detection, it distinguishes between normal and abnormal metric trends by analyzing a metric’s historical behavior. It shows the actual value and whether it is normal by using different colors based on the algorithm we chose for the metric. 


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

*Solution:* <br>
Click on the monitor tab and select New Monitor, configure the monitor to fit it to the requirement.<br>
The configurations are demonstrated in the following screenshots: 

![SCREENSHOT 9](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/9.MonitorThresholdConfiguration.PNG)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

*Solution:* <br>
Configure the notification message in the 'See What's Happening' section. The syntax can be found by clicking the 'Use message template variables ' button <br>
![SCREENSHOT 10](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/10.MonitorMessageConfiguration.PNG) <br>
![SCREENSHOT 11](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/11.WarningEmail.PNG)  <br>

I had trouble seeing the host name and its ip in the email, didn't find any document about that. Perhaps should have used another variable or a tag name? 

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    * One that silences it from 7pm to 9am daily on M-F,
    * And one that silences it all day on Sat-Sun.
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

*Solution:* <br>
Click on the Monitor tab then select 'Manage Downtime' <br> 
Then click 'Schedule Downtime' on the top right corner. The configurations are demonstrated through screenshots below : <br>
![SCREENSHOT 12](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/12.DownTimeSchedule1.PNG) <br>
![SCREENSHOT 13](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/13.DownTimeSchedule2.PNG) <br>
![SCREENSHOT 14](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/14.DownTimeSettings1.PNG) <br>
![SCREENSHOT 15](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/15.DownTimeSettings2.PNG) <br>


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```    

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

*Solution:* <br>
I had trouble running the python app via `ddtrace-run` command because it looks for a folder with a space in its name, so I added the middleware in the application instead. The source code is added in the pull request [my_app.py](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/src/my_app.py) <br>

After running the flask app, the button 'traces' became available in the APM tab of the Datadog UI. Click on it, we can now see the traces of our application: 
<br>
![Screenshot 16](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/16.APM_Trace.PNG) <br>
![Screenshot 17](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/17.APM_Trace2.PNG)

I created a dashboard combining the check 'mymetric' and python app we just created ![Screenshot 18](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/18.CustomedDashBoard.PNG). Then I made it public using the options button on the top right corner, ![ScreenShot 19](https://github.com/HantingZHANG/hiring-engineers/blob/solutions-engineer/images/19.GeneratePublicURL.PNG). <br> 
The link to the dashboard is [here](https://p.datadoghq.com/sb/bc0f6093b-7b584e455cb564b634c85f1d4e90804b). 

* **Bonus Question**: What is the difference between a Service and a Resource?

*Solution:* <br>
A "Service" is the name of a set of processes that work together to provide a feature set. Such as a functional module of a website.<br> 
A 'Resource' is a particular query to a service. For a web application, for example, it can be a canonical URL like /user/home or a handler function like web.user.home (often referred to as "routes" in MVC frameworks).

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

*Solution:* <br>
One thing I see Datadog would fit into is the credit card manufacturing system. Inspired by my previous internship at a credit card personalization solution company, I believe that if we install Datadog in the host machine that sends credit card manufacturing order to the card printers, we can collect multiple kinds of interesting data such as number of cards manufactured within a given period of time, system malfunction logs, origins of orders, etc.
