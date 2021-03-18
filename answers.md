Hiring Exercise
-------------
This is [Ivair Do Carmo Jr.'s](https://github.com/Ivairjr) responses to the **Solutions Engineer's** [hiring exercise](https://github.com/DataDog/hiring-engineers/tree/solutions-engineer) at [DataDog](https://www.datadoghq.com). 


On today's exercise, the following topics will be covered in details by me in a simple and involving way to make you feel comfortable understanding as well as using Datadog's services.

- [Setup the environment](#setup-the-environment)
- [Collecting Metrics](#collecting-metrics)
- [Visualizing Data](#visualizing-data)
- [Monitoring Data](#monitoring-data)
- [Collecting APM Data](#collecting-apm-data)
- [Final Question](#final-question)
- [Dashboards and Links](#dashboards-and-links)

Setup the environment
-------------

**1.** First of all, we need to setup an environment in your machine in order to avoid any OS or dependency issues. There are many ways we can do it, but for this activity's purpose we are going to spin up a fresh Linux/Ubuntu Virtual Machine via Vagrant with a minimum version of `16.04`.
Setting up your Virtual Machine is not as hard as it sounds. You can follow Vagrant's [Getting Started](https://learn.hashicorp.com/collections/vagrant/getting-started) document which uses a very simple syntax to guide you on setting your VM easy and fast.

*IMPORTANT: **MacOS** users may run into some issues to run their VM after installation. 
**DO NOT PANIC!** it is possible that after following Vagrant's instructions, your commands still wont run your VM. An `Error` is displayed on your terminal when trying to [**Boot your Environment**](https://learn.hashicorp.com/tutorials/vagrant/getting-started-up?in=vagrant/getting-started).

The error prompted is the one bellow:

`!Kernel Driver Not Installed (RC=1908)`

Takling this issue is not a "Rocket Science" at all, and now I am going to show a very simple approach to solve it:
So, the error prompted means that "Oracle America Inc"* needs the approval to access your system.
You can easily solve this problem by going to your *System Preferences* via: 

*`System Preferences > Security & Privacy > Allow "Orable America Inc"`*

Now you can click on the Allow button and try to boot your environment again. 

Done, your VM is good to go! 

**2.** Your VM is ready, now it is time to sign up for a [DataDog 14-days free trial](https://www.datadoghq.com/) to have access to exclusive monitoring services.

*During the signing-up process, make sure you fill out  **“Datadog Recruiting Candidate”** in the [“Company”](https://a.cl.ly/wbuPdEBy) field.

**3.** Your VM is running and your Datado account is set. Now, we are going to follow the [Agent installation guide](https://app.datadoghq.com/account/settings#agent/aws) thoroughly in order to set up the DataDog Agent that reports metrics from our local machine.
Within seconds, your Datadog platform will start receiving these metrics reported by the DataDog Agent. 

As simple as that, we created a connection between our Local Machine and Datadog. Now it is the fun time: we are going to use the environment we just created to configure some files and potentialize the use of Datadog's services/ Let's go..



Collecting Metrics
-------------
**1.** Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog:

- ###### On this exercise, we are going access the Agent Main Configuration File, which is the core file for creating a bridge between our local machine and Datadog in order to add **Tasg**. Tags are custom keywords pointing to specific aspects of your config file that groups together information as you desire. We will show how to apply tags in the next steps:

    `/etc/datadog-agent/datadog.yaml`
 
*The line above represents a file path within your system. The syntax for file paths vary from OS to OS, but the line above is set for Ubuntu since the OS running in our VM is Ubuntu.
 Although, if you are running commands from a different OS, you can check the different syntax for other platforms [here](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7).
  
- The **datadog.yaml** file is large in extension, so I advise you to search for the keywords before editing anything. 
The commands we will run from now on are Linux based commands, so there are different commands to get to the same destination. You can use the commands suggested here, or your can use other commands you judge to better in order to access, read, create, remove, edit, and write on files. 
 The first command introduced for searching keywords is the command ***grep***.  Bellow you can see the syntax used to invoque the command grep that will point out the occurrences of your keyword and the exact line(s) they are located at. In this case, we are looking for the keyword *tags* located in the ***datadog.yaml*** file:

    `$sudo grep -n tags: datadog.yaml `
    
*If necessary, you can use the ***sudo*** command to have the security privileges of another user, in case you are not the root user.

- After finding the specific occurrences and the number of their respective lines, we can now access the **datadog.yaml** file in edit mode via command ***vi***: 

    `$vi datadog.yaml`

-  I found a few occurrences of the keyword *tags*, but the one we are looking for is located at around line 66. So, instead of scrolling the entire file looking for the specific line/keyword, we can jump into the exact line by typing:
 
    `:66 ` + `return`

- We are now located at line 66 of our file, which falls under the ***@param tags***. 
***@param*** *is short of parameters that are passed inside the config files*

- Almost every line is commented, which means they are not active commands. So, we need to delete the ***#*** at the beginning of the lines we want to modify/activate. 

- Add the following *tags* into the config file to get them started:
  
  ![](3tags.png)
  
  ![](3hostmap.png)
  
**2.** Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

 -  Now, we are going to follow the Ubuntu Installation Instructions for [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/), [MySQL](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04), or [PostgreSQL](https://www.postgresql.org/download/linux/ubuntu/).

- We can now install their respective [DataDog Integration](https://docs.datadoghq.com/getting_started/integrations/). Follow thoroughly every step of setting an integration. 

- SSH into your VM and run the *status* command in order to check if the if your ***Logs Agent*** report  **Status: OK**, and  **BytesRead: >= 0** as following: 

  `sudo datadog-agent status`

  ![](4logs.png)

- After installing them, we should see something like this on our DataDog Integrations tab: 

  ![](4integrations.png)

- If you run your Agent Status and it prompts the **Status: Error:** as following:

  ![](4logerror.png)

   you must run the ***chmod 755*** command in order to allow everyone in your VM to read and execute the files/directories that had limited access before: 

  `sudo chmod 755 /var/log/mysql/mysql_error.log`

- Now, run your status again, and check if the metrics of your Database Integrations return an **OK** message under ***Collector > Running Checks*** as following:

  ![](4mongo.png) 

  ![](4mysql.png)

**3.** Create a custom Agent check that submits a metric named ***my_metric**** with a random value between 0 and 1000.

- Follow the instructions to create a [Custom Agent Check](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count).

*The names of the Configuration and Check files must match. Ex: If your check is called mycheck.py, then your configuration file must be named mycheck.yaml.

- After creating your ***my_metric.py*** file, it should look like this: 

  ![](5mymetric.png)

-  Run the *status* command again and check if the metric you just created is returning an **OK** message under ***Collector > Running Checks*** as following:

  ![](5metricstatus.png)


**4.** Change your check's collection interval so that it only submits the metric once every 45 seconds.

- Access your ***my_metric.yaml*** file and modify it accordingly. It should look like this: 

  ![](645s.png)

**5.** Bonus Question Can you change the collection interval without modifying the Python check file you created?

- Yes. In order to modify the collection interval, you only need to modify the ***.yaml*** file as we did in the last picture above. The Collection Interval Default value is **15s**, but you can edit it as you wish. The ***min*** value of **30s** does not mean the metrics will be collected every **30s**, but rather it could be collected ***as often as *** **30s**.



Visualizing Data
-------------

Utilize the Datadog API to create a Timeboard that contains:

- Follow the instructions to setup [Datadog's API](https://docs.datadoghq.com/api/) properly. This step is necessary to access Datadog's platform programatically. 

- After following the package installation guide, we will get started with [PostMan](https://www.postman.com). This is an **API Development Platform** where we will try out Datadog's API and create things such as Dashboards, Graphs, and Monitors programmaticaly.  

- The 1st step is to import the [Datadog Collection](https://app.getpostman.com/run-collection/bf4ac0b68b8ff47419c1?#?env%5BDatadog%20Authentication%5D=W3sia2V5IjoiYXBwbGljYXRpb25fa2V5IiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6ImFwaV9rZXkiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWV9XQ==) into Postman. 

Then, we are going to authenticate the PostMan environment called Datadog Authentication to add our Datadog API, and apply the respective API keys. 

- Click on the manage environments gear icon in the upper right corner of Postman as following: 

  ![](19postman.png) 

- Select Datadog Authentication

- Click Edit

- Add in your Datadog [API Key](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys) as the the initial and current value for the ***api_key*** variable, and add your Datadog [Application Key](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys) as the initial value and current value for the ***application_key*** variable. Check example below:

  ![](19apikey.png)

- Now we are ready to start making API Calls via PostMan.

Click in the Dashboard Collection in the upper left corner of Postman to expand all the Methods and API Calls provided by Datadog. 

- Now we are going to follow the instructions to create a [New Dashboard](https://docs.datadoghq.com/api/latest/dashboards/) with the solutions to our next exercises.

  ![](19dash.png)


For the next steps, we will be writing into the body of our JSON file using the ***body*** tab as following: 

  ![](19body.png)


**1.** Your custom metric scoped over your host.

-  Check the following instructions in order to [Graph with JSON](https://docs.datadoghq.com/dashboards/graphing_json/widget_json/), [Widget JSON Schema](https://docs.datadoghq.com/dashboards/graphing_json/widget_json/), and [Request JSON Schema](https://docs.datadoghq.com/dashboards/graphing_json/request_json/). 

- Below we can see a short part of the Script where we scope ***my_metric*** over the ***vagrant*** host:

  ![](19mymetric.png)


**2.** Any metric from the Integration on your Database with the anomaly function applied. 

- Follow the instructions to use Database's metric with [Anomaly Function](https://docs.datadoghq.com/dashboards/functions/algorithms/) for both MongoDB & MySQL.

- Our Script to get the metrics from our databases with the ***Anomaly*** function should look as following:

  ![](20mongodb.png)

  ![](20mysql.png)


**3.** Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

- Follow the instructions to use your custom metric with [Rollup Function](https://docs.datadoghq.com/dashboards/functions/rollup/).

- Our Script using our custom metric with the ***Rollup**** function should look as following:

  ![](21rollupfunc.png)

Once this is created, access the Dashboard from your Dashboard List in the UI:

**4.** Set the Timeboard's timeframe to the past 5 minutes

- Timeboard's collecting for hours: 

  ![](22timeboard.png)

- Timeboard's collecting in the past 5min: 

  ![](22after.png)


**5.** Take a snapshot of this graph and use the @ notation to send it to yourself.

- Snapshot config: 

  ![](23snapshot.png)

- Email notification:

  ![](23email.png)


**6.** Bonus Question: What is the Anomaly graph displaying?

Anomaly Functions applied onto Graphs will use some algorithms combined with standard deviations to detect  any kind of anomaly based on a gray band overlaying the metrics displayed on the graph that shows an expected behavior of a series based 
on past.

The image bellow represents a Anomaly Monitor created to check one of our MondoDB Metrics. You can notice that there was a Anomaly Alert Triggered based on a deviation for approximately 15min:

  ![](24anomaly.png)


Monitoring Data
-------------
**1.** Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

-  Warning threshold of 500

- Alerting threshold of 800

- And also ensure that it will notify you if there is No Data for this query over the past 10m.

- Send you an email whenever the monitor triggers.

- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

So, lets get it started with this exercise by accessing Datadog's platform to create a Metric's Monitor:

- After filling out the information for your Metric's Monitor, it should look as following: 

  ![](8beg.png)

  ![](8end.png)

**2.** When this monitor sends you an email notification, take a screenshot of the email that it sends you.

  ![](8nodata.png)

- Go to ***Monitors > Manage Downtime*** and fill out 
**3.** Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

- One that silences it from 7pm to 9am daily on M-F:

  ![](10weekdays.png)

- And one that silences it all day on Sat-Sun:

  ![](10weekend.png)

- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

  ![](10email.png)

  ![](10email1.png)

*The confirmation emails are displaying the times in **UTC** format for some reason, but the Downtimes below prove that the correct times were set under **EST** format:

  ![](11email.png)

  ![](11email1.png)


- Please check the [Script](script.txt) for this exercise.

Collecting APM Data
-------------
**1.** Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

- Follow the instructions to set up [Datadog's APM](https://docs.datadoghq.com/tracing/setup_overview/).

- Make sure you config the Datadog agent for APM & add the Datadog Tracing Library to your code.

- Now let's create the Flask app provided in this exercise inside our VM. My Flask app is called ***flaskapp.py*** as following:

  ![](16flaskapp.png)

- Now, we are going to access Datadog's main config file ***datadog.yaml*** to configure the Datadog Agent for APM by enabling the ***apm_config*** under **Trace Collection Configuration** to ***true*** as following:

  ![](16datadogyaml.png)

- Now, we can start tracing our application by installing the Datadog Tracing library, ddtrace, using pip:

  `pip install ddtrace`

- Then, we are going to Instrument our Flask application by running the following command: 

  `DD_SERVICE="flaskapp" DD_ENV="prod" DD_LOGS_INJECTION=true ddtrace-run python flaskapp.py`

- If your application is successfully instrumented, you should see something like this: 

  ![](16output.png)

- Now, lets go back to our Datadog Platform and check if our tracing are being collected properly under the APM Services as following:

  ![](17servicelist.png)

  ![](17logs.png)

  ![](17map.png)

**2.** Bonus Question: What is the difference between a Service and a Resource?

- Services groups together endpoints, queries, or jobs for the purpose of scaling instances. All services are listed under **Service List** and can be visually seen as in a Micro-service format under **Service Map**.

- Resources represent a particular domain of a Customer Application.They could typically be an instrumented web endpoint, database query, or background job. Each resource has its own Resource page with trace metrics scoped to the specific endpoint.

**3.** Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

  ![](17dash.png)

Final Question
-------------
**1.** Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?

- I believe that a very creative way of using Datadog's services would be by monitoring rented bikes, scooters, and motorcycles. 
As our civilization increases exponentially, the geographical space for personal vehicles dicreases. 
So, the numbers show that people are renting each time more small vehicles for the ease of transportation, to avoid traffic, not to pay for car's financing plans, not to catch public services (mainly during pandemic times), etc. 
So, I think that it would be a great idea by monitoring these rented small vehicles to understand better where this new kind of transportation can lead us. I believe that with the right data, we can understand better if people are leaning towards a "greener" future, or even how can we use that data to solve traffic problems that only gets worse over time. 

- Another idea I had was about monitoring the different kinds of Covid 19 - Vaccines around the world. Many countries have developed their own vaccines, some have made them commercially available and some not.
But we hardly will know how efficient they are until we actually get the necessary data to study its efficiency in short and long terms. Other variants could be analyzed as well, such as time between 1st and 2nd shots, exposure to mutations of the virus, geolocation, economical accessibillity, etc. 

Dashboards And Links
-------------

- [Ivair's Dashboard](https://p.datadoghq.com/sb/wdhgfpbmapra394k-aa41aba155d6d4a1db22ce9cd2e3412f)
- [VIsualizing Data](https://p.datadoghq.com/sb/wdhgfpbmapra394k-6fc874161dca710dcb3889a04b3bafb4)
- [APM & Infrastructure Metrics](https://p.datadoghq.com/sb/wdhgfpbmapra394k-c2b6dfbfa98ea8c0663a59a82db3b11c)
- [API Script](script.txt)
