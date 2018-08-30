Your answers to the questions go here.
# Prerequisites - Setup the environment
You can utilize any OS/host that you would like to complete this exercise. 
>Answer I am using both the Ubuntu via Vagrant and a Windows agent on my laptop so I can see the differences in setup and user experience.

>I am impressed how easy this is with a single command 

<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/UbuntuAgentInstall.JPG" >

   
  
>The Windows agent was also very simple with a quick setup wizard asking for the API string. I think it is great that with this API your agents report straight into the correct place. Other tools I have used have taken a lot more messing around to get the agents reporting in to the correct place. Some require DNS entries which can delay installs and need to include change control etc.

# Collecting Metrics:
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
>Answer I was having issues with the Ubuntu agent getting to the datadog.yaml to edit with permission denieds, etc so I switched to the Windows agent editor and this was much quicker and very easy to use.

<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/setting%20tagwingui.JPG" width="800" />

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

* Bonus Question Can you change the collection interval without modifying the Python check file you created?


# Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.

* Any metric from the Integration on your Database with the anomaly function applied.

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

* Take a snapshot of this graph and use the @ notation to send it to yourself.

* Bonus Question: What is the Anomaly graph displaying?

# Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.

* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up   two scheduled downtimes for this monitor:

 One that silences it from 7pm to 9am daily on M-F,
 And one that silences it all day on Sat-Sun.
 Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


