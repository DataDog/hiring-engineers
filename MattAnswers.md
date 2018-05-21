## Datadog Hiring Exercise **Matt Eastling** Questions and Answers

Reviewer(s),

Thank you very much for the opportunity to move forward with the hiring proecss at Datadog. Through each aspect of the process I have been able to obtain quite a bit of insight about the Datadog platform and configuration. I particularly enjoyed the hiring exercise experience as it really inspired me to get under the hood and accomplish a tangible amount of learning about Datadog technology overall.

I have completed the Technical Exercise activities and provided detailed answers, supporting documentation and screenshots for review below.

I look forward to your review and please let me know if there are any questions regarding my submission.

-Matt Eastling


## Prerequisites - Setup the environment

Environments Utilized:
* MS Windows 8.1
* Ubuntu 12 / MySQL

Ubuntu:

Vagrant Init

![Vagrant Init](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/8_Test_Vagrant_VM_Init.PNG)

Vagrant up

![Vagrant up](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/15_Install_Vagrant_Download_and_Init_VirtualBoxVM_ERROR_4-GuestKey-cannot_reconcile.PNG),

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Tag Added Event

![Tag Added](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/24_DD_Add_Tag.PNG)

Tags in Datadog UI
![Matt Tags],https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/Tags.PNG)

Host Map

https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/hostmap.PNG

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Install MySQL

![Install MySql](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/25_Install_my_sql.PNG)

SQL Installed Success

![SQL Installed Success](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/29.1_Install_DD_mysql_integration_completed_and_checked.PNG)

Datadog MySQL Integration Installed

![Datadog MySQL Integration Installed](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/29.2_Install_DD_mysql_integration_completed_and_checked_DD_UI.PNG)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

My_Metric.py

![My_Metric.py](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/A.my_metric.py)

My Metric Added

![My Metric Added](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/30.1_My_Metric_completed_and_checked_DD_Agent_Status.PNG)

My_Metric on DD Dashboard

![My_Metric on DD Dashboard](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/30.2_My_metric_01_random%2B1to1000_timeboard_completed_and_checked_DD_UI.PNG)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

My_Metric.yaml

![My_Metric.yaml](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/30.3_My_metric_yaml_45sec.PNG)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes - this is acoomplished by updating the default collection interval in the yaml file, see previous screen capture

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.

* Any metric from the Integration on your Database with the anomaly function applied.

MySQL_Anomaly

![MySQL_Anomaly](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/31_Create_Anomaly_Monitor_MySQL_User_Perf.PNG)

MySQL_Anomaly Details

![MySQL_Anomaly Details](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/32_Create_Anomaly_Monitor_MySQL_User_Perf_completed.PNG)

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

My_Metric Rollup JSON

![My_Metric Rollup JSON](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/33_Create_Rollup_My_Metric_completed-edit_JSON.PNG)

My_Metric Rollup Dash_Details
![My_Metric Rollup Dash_Details](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/33.2_Create_Rollup_My_Metric_completed-edit_DD_Dash_Properties.PNG)

* Script used to create this Timemboard:

Create Timeboard via API Script

![Create Timeboard via API Script](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/B.Matt_timeboard_api_7.py)

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes


* Take a snapshot of this graph and use the @ notation to send it to yourself.

My_Metric Sent via Comment
![My_Metric Sent via Comment](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/34_Send_Snapshot_Via_Comment_My_Metric_Graph.PNG)

* **Bonus Question**: What is the Anomaly graph displaying?

Anomaly graphs show any tracked variable of a metric that is inconsistent from what are defined as 'normal' parameters. It can be used to highlight unusually high CPU usage, traffic volumes on a website, or other important activity that may cause performance issues.

Anomalies work well for metrics that display consistent trends over time and that the one who configures it having a sense of the metrics 'normal' patterns.

I see this being particularly compelling when looking at a large pool of resources/services. By providing vast metric data of similar services/resources and applying the vetted Anomaly graphs configuration to the greater pool of resources to see which of them are not performing with prescribed parameters. Overall a deployment managing anomalies provids actional insights and valuable real time alerts for the managed resources.

## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert based on (500/800) values over the past 5 minutes:

My Metric Monitor Configuration

![Config_Metric](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/34.2_Monitoring_Alert_Email_template.PNG)

My Metric Email Alert

![My_Metric Email](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/34.3_Monitoring_Alert_Email_Sent.PNG)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    * One that silences it from 7pm to 9am daily on M-F,
    * And one that silences it all day on Sat-Sun.
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Downtime Schedule Configuration:

![My_Metric Email](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/34.5_Monitoring_Schedule_Set.PNG)

Notification Screen Shot:

Waiting for the timeframe to hit


## Collecting APM Data:

Using provided Flask app, instrument this using Datadog’s APM solution. Please include your fully instrumented app: Flask.py with code to instrument

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics:

Instrumented Flask App:

![Matt Flask App Python File Instrumented with DD](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/C.Matt_Flask_1.py)

I have completed the integration of Datadog into the provided Flask app, but was unable to get the app to send data to Datadog. I kept getting the follwing (different) connection errors from both the Ubuntu and Windows 8 environments I worked with. I did however get an app to collect metrics:

Ubuntu 12: Issue with SSL
I had a lot of issues with this environment using and installing PIP, curl, Datadog Agent, DDTrace (manual install), yet in the end was able to the point of having the components to work, but not get an app to send data. The final issue that stalled me was connecting via SSL (or any port) with the Flask App. I tried many different approaches, mainly with explicit local TCP/IP and various port parameters (5000, 5050, 80, 447) when running the Flask app.

After working for a solid amount of time on Ubuntu 12, I then tried a different version of Linux (Ubuntu 16 / Xenial) and still had envrionment setup challenges to overcome, which ultimately ended in connection errors for the Flask app. I attemtped serveral fixes/commands/test scripts within this second environment to no avail. I then moved to Windows, which also had issues, and I finally had a win in the end outlined below.

Windows 8.1: Issue with Sockets
With the Windows 8.1 environment, I was able to get everyone set up and working well (DD Agent, My_Metric, API based Timeboards). I account for this success in that the Datadog Agent UI, Datadog APM, PERL PIP, Flask/Blinker, went more smoothly in terms of configuration and straight forward installers. That said, I unfortunately wasn't able to get the flask app to actually connect to Datadog, althought it did appear to run, just with continuous Socket errors. I tried adjusting the setting in Windows Firewall, Properties of the App to run and Administrator, TCP/IP and Port parameters in the Flask run command, again all effort to no avail.

That said, I was able to get the Datadog sample-app configured and working to send APM trace data to Datadog successfully. I used the PERL sample-app.py located here https://github.com/DataDog/trace-examples/tree/master/python/flask/.

This make me believe that there is something blocking the point-to-point connection via the Port or perhaps some sort of Windows security setting that I was unable to track down. In time I am confident I would be able to sort it out as I get to know Flask a bit better in terms of how it is posting data.  In my screenshot, you will see the APM Dashboard screenshot and Dashboard link for the Datadog sample-app. Above is the Flask app (code) that I was able to run, but as I mentioned, it didn't send data to Datadog from either Linux nor Windows.

Screen Shot of APM Dashboard:

![APM_Sample_App](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/72_APM_Dashboard.PNG)

Link to APM Dashboard:

https://app.datadoghq.com/apm/service/sample-app/request?start=1526856287119&end=1526859887119&env=none&paused=false


* **Bonus Question**: What is the difference between a Service and a Resource

A service in Datadog APM is defined as "A service is a set of processes that do the same job" in relation to one's managed applications such as a web server or a database.

Datadog has the capability to monitor the performance of each service individually and provice metrics such as CPU usage, number of requests, average latency, and number of errors and their frequency.  .

A resource in Datadog APM is defined as "a particular action for a service.". The resources are the individual calls and traces that make up a service.

For a web app service, resources will be web based entry points into the application such as specific URLs that users are hitting (ex. Endpoint: /home, /api). For a database, a resource will be an individual SQL call (ex. Query: select * from datadog).

The metrics of said individual resources will make up the overall service's performance metrics and can be grouped together accordingly.


## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

First of all, given the clear focus on quality instrumentation, extensibility, and scalability, I see so many use cases for Datadog comprehensive monitoring.  It can and will allow so many industries to focus on their monitoring configuration instead building their own. Once the data is sent, stored, and analyzed by companies, governments, and individuals the ability to understand the data and set rules.configurations themselves is limitless.  This is in stark contrast to the time and expense required to have a 'home grown' solution.

Specifically one technology sector/market that I could see having a significant opportunity for leveraging Datadog is within the 'Internet of Things' (IoT) / 'Industrial Internet of Things' (IIoT). As IoT/IIoT grows into becoming a staple in almost every merging of complex mechanical and digital components, the shear volume of IoT/IIot data is certainly going to be monitored and managed. IoT/IIoT consists of all the web-enabled devices that collect, send and act on data they acquire from their surrounding environments using embedded sensors, processors and communication hardware. This data is ripe to be sent to purpose built platforms for analysis allowing one to act on the information that is provided. I was able to find several existing IoT integrations with AWS and Azure and would like to see some compelling case studies from a large scale Datadog implemtation based IoT data collection effort.

In thinking how to creatively use Datadog, I imagine a highway where cars are able to safely navigate to their destinations without a driver because of realtime anomaly metrics of hundreds of cars within proximity and the busiest intersection of the worlds largest cities. I imagine a home where an elderly patient’s health is closely monitored by her hospital physician, with details dashboards and alerts. I imagine a city that significantly reduces waste through sensor-embedded water pipes, buildings, parking meters and more, all with precision and analytics to enable efficiency and resources.

These are no longer a part of the distant future. These scenarios are starting to happen now, through the convergence of machines and intelligent data in what is IoT and IIot. Datadog could transform many industries through providing actionable insights for intelligent, interconnected devices that dramatically improve performance, lower operating costs and increase reliability.

Some large scale enterprise examples I see as an opporuntity for Datadog to provide value are:

Energy - Optimization of business operations by understanding and affecting the minimization of unplanned downtime and the sheer maximization of operational efficiency

Healthcare - Patient-centered medical home care data from devices like an ultrasound monitor activity in the home, to detect falls and trigger automatic ambulatory services. Improved health equipment efficientcy in hospitals, clinics, and homes that eliminating could for examample, evaluate multiple device logins and perhaps adjusts user settings to help reduce risk, eliminate errors and provides a much better patient experience overall

Manufacturing - Factories having interlinked devices in the millions will need data analysis to ensure that everything runs as planned across the entire value chain. Changes in one part of the chain, automatically trigger adjustments on the factory floor.

Mining - Robotics, vehicle (remote & autonomous) monitoring & tracking. Remote conditions monitoring. Plant & machine data analytics and machine learning

Retail - Predictive equipment maintenance (store refrigeration, power efficiencies, transportation equipment etc.) will come from pooled data on any supply chain/inventory systems. Warehouse automation applications with inventory control and temperature monitoring. Supply chain optimization, including route tracking and improvement, and automated pricing adjustments. Smart stores: analyzing traffic patterns, using video analytics applications to extract actionable insights

Smart Cities - Sensor-embedded water pipes, sanitation services, traffic patterns, parking meters and more, that monitor and flag capacity issues and automatically make adjustments in traffic flow, pickup schedules and more. Improved public safety through more effective and strategic usage of policing resources for crime prevention and emergency responsiveness

Transportation - Create transportation system applications colecting IoT data that can sense and respond to changes in real time. Increase operational efficiencies & public safety, reduce fleet down time and enable preventive maintenance of faulty and soon-to-fail parts by analyzing and reacting to data created by jet engines and sensors monitoring the surrounding environment (temperature, humidity, air pressure, etc.). Identify more efficient routes and improve fuel efficiency, through capacity analytics.

In conclusion. IoT is going to grow and those in the market would be happy to focus on configuration versus development of the real focus of their solutions - data monitoring turned into insights and ultimately value for their customers.

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo. ** DONE
* Answer the questions in answers.md ** DONE
* Commit as much code as you need to support your answers. ** DONE
* Submit a pull request. ** TBD
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers. ** DONE

