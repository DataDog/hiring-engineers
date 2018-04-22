# Datadog Solutions Engineer Exercise
The responses to all questions in this exercise are based off of the original document:
https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md

# Prerequisites - Setup the environment:

Items used to complete this exercise:
- Macbook Pro
- *Vagrant*
- *Virtualbox*
- *Ubuntu Trusty 64*
- *Various Linux utilities*
- Datadog trial account

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Vagrant%20install%20Ubuntu.png)

Once the Ubuntu server is installed, the next task is to install the Datadog Ubuntu agent. The agent deployment information can be found on the Integrations -> Agents -> Ubuntu page.

`sudo DD_API_KEY=76919a606a574952a97b6faf68987b49 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/DD%20Agent%20Install.png)

The Datadog agent can be stopped or started using the following commands:
`sudo stop datadog-agent`
`sudo start datadog-agent`

# Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog

Tags can be created either in the Datadog GUI or by editing the mysql.yaml file.

`sudo nano /etc/datadog-agent/datadog.yaml`

Look for the section in the file that starts with “Set the host’s tags (optional)", remove the comment (#) in front of tags, edit them with the relevant information and place them on a single line. The entry should show the following:

`tags: host:dwlinux, env:lab, role:engineering`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Edit%20datadog.yaml%20to%20input%20tags.png)

After restarting the Datadog agent, the tags will show up in the GUI.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Restart%20dd%20agent%20after%20tags%20inserted.png)

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Host%20map%20with%20tags.png)


### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database

To install MySQL, execute the following command:

`sudo apt-get install mysql-server`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Install%20MySQL.png)

Once MySQL has been installed, a Datadog user account, password and permissions must be created. 

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/DD%20MySQL%20Integration%20Commands.png)

Be sure to include the -p flag when running the commands shown on the Integration page, or you will get an error stating "Access denied for user 'root'@'localhost' (using password: No)".

`sudo mysql -p -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'dYDtGrBz8Dmx/BbXrFctnkV2';"`
`sudo mysql -p -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"`
`sudo mysql -p -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"`
`sudo mysql -p -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Install%20MySQL%20Integration.png)

To verify that the grants were successfully completed, follow the instructions on the Integration page.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Check%20MySQL%20Permissions.png)

When the grant verification process has been completed, you are ready to continue configuring the Datadog MySQL integration. The next step is to edit the mysql.yaml file. An example file can be found at /etc/datadog-agent/conf.d/mysql.d/conf.yaml.example. Copy this file into a new directory and edit it.

`sudo cp /etc/datadog-agent/conf.d/mysql.d/conf.yaml.example /etc/datadog-agent/conf.d/mysql.yaml`
`sudo nano /etc/datadog-agent/conf.d/mysql.yaml`

Scroll down to the entry below and remove the comment marks from the following lines. You will need to include the password provided from the MySQL integration page.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Edited%20mysql.yaml%20file.png)

Once the file has been modified and saved, restart the Datadog agent. To verify that that the MySQL check is running, issue the following command and look for the heading "mysql":

`Sudo datadog-agent status`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/MySQL%20integration%20check.png)


### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000

To create a custom Agent check, create and edit a mycheck.yaml file in the /etc/datadog-agent/conf.d/ folder.

`sudo touch /etc/datadog-agent/conf.d/mycheck.yaml`
`sudo nano /etc/datadog-agent/conf.d/mycheck.yaml`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Edit%20mycheck%20yaml%20file.png)

Next create and edit mycheck.py file in the /etc/datadog-agent/checks.d/ folder.

`sudo touch /etc/datadog-agent/checks.d/mycheck.py`
`sudo nano /etc/datadog-agent/checks.d/mycheck.py`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Edit%20mycheck%20py%20file.png)

To verify that the custom check is working, issue the following command:

`sudo datatog-agent check mycheck`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Custom%20agent%20check.png)

In a few minutes the new custom check will start appearing in the Metrics Explorer page of the Datadog GUI.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Metrics%20Explorer%20showing%20test%20metric.png)



### Change your check's collection interval so that it only submits the metric once every 45 seconds

To make this change, the mycheck.yaml file will need to be updated. The min_collection_interval will need to change from 15 to 45.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Change%20mycheck%20yaml%20collection%20time.png)


### Bonus Question: Can you change the collection interval without modifying the Python check file you created?

Yes, in this instance it it can be accomplished by modifying the mycheck.yaml file. Adding a section to the file entitled "min_collection_interval" will allow you to modify the default frequency of the check. 15 seconds is the minimum supported interval check by the agent.


# Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

### Your custom metric scoped over your host
### Any metric from the Integration on your Database with the anomaly function applied
### Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Before you can create a custom metric using the Datadog API, you need to retrieve a couple of API keys. These can by obtained by going to the Integrations -> API section of the Datadog GUI. 

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/API%20Keys.png)

An API key is automatically created when the Datadog user account is activated. An application key must also be created in order to make full use of the Datadog API. Copy both the API key and the Application key as they both will be needed to create a Timeboard via the Datadog REST API.

If you are unsure of the correct syntax to create a Timeboard with the custom metric or the database metric with the anomaly function applied, you can get it from the Datadog GUI by doing the following: 
* Open the dashboard that was previously created which has both the custom metric and database with anomay function
* Click the pencil icon on either graph. (In this case it is the anomalous database traffic graph)
* Click on the JSON tab and you will see the relevant information to include in the POST

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/JSON%20Code%20for%20Anomaly%20Metric.png)

In addition to needing the code to insert into the body of the POST, a correcly formed URL will also need to be created using both the API key and the Application key. In this case, the URL will be the following:

`https://api.datadoghq.com/api/v1/dash?api_key=76919a606a574952a97b6faf68987b49&application_key=1f6afbaffe7d1208708084d70a1b9fde8023514d`

Below is the code that will be included in the body of the POST

```
{
        "graphs": [{
                        "title": "My Metric Graph",
                        "definition": {
                                "events": [],
                                "requests": [{
                                        "q": "avg:test.my_metric{*}.rollup(sum,1000)"
                                }]
                        },
                        "viz": "timeseries"
                },
                {
                        "title": "Database Anomalies Graph",
                        "definition": {
                                "events": [],
                                "requests": [{
                                        "q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)",
                                        "type": "line",
                                        "style": {
                                                "palette": "dog_classic",
                                                "type": "solid",
                                                "width": "normal"
                                        },
          "conditional_formats": []
                                }]
                        },
                        "viz": "timeseries"
                }
        ],
        "title": "Dave's Timeboard",
        "description": "My test timeboard",
        "template_variables": [{
                "name": "host1",
                "prefix": "host",
                "default": "host:vagrant-ubuntu-trusty-64"
        }],
        "read_only": "True"
}
```

Using Postman (or any REST client) a POST method can be used to create the desired dashboard using the API. The screenshot below shows the URL, body of the POST (included above) and the successfully returned response.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Postman%20API%20Post.png)

I can see my new dashboard by going to Dashboards in the Datadog GUI and then looking for the dashboard with the name Dave's Timeboard.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/List%20of%20Dashboards.png)

Clicking on the entry for Dave's Timeboard will display the timeboard that was created via API call.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/New%20API%20Timeboard.png)


### Set the Timeboard's timeframe to the past 5 minutes
### Take a snapshot of this graph and use the @ notation to send it to yourself

By clicking and dragging on the end of the trend line, the current time view is changed to a 5 minute view. Hovering over the top right portion of the graph will will display a camera icon. Clicking on the camera icon allows you to create a real-time annotation. In this case I am sending an email to myself with a comment requesting a review of the past 5 minutes. In addition to email, the annotation could also have been sent to Slack, Hipchat or Pagerduty (if the Datadog integration has been created).

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/5%20minute%20graph%20on%20timeboard.png)

Below is a copy of the email that I received with the request for review of the graph.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Email%20of%20snapshot%20from%20timeboard.png)


### Bonus Question: What is the Anomaly graph displaying?

The purple line is showing the amount of time MySQL is spending in user space. The gray band surrounding the purple line is showing the predicted performance range, based on historically collected data. The red line (outside the gray band) is anomalous activity, because it is outside the predicted range.


# Monitoring Data:

### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m
* Send you an email whenever the monitor triggers
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

To set up a new metric monitor, click on Monitors -> New Monitor in the Datadog GUI. Select the metric of interest (test.my_metric) and then define the threshold values for both alert and warning. In this case the alert threshold is 800 and the warning threshold is 500. Click the dropdown box next to "if data is missing..." and select notify. Define the number of minutes to wait before a data missing alert is created. For this exercise, waiting for 10 minutes is sufficient.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Metric%20monitor.png)

In order to receive a message when one of the three events has been triggered, the syntax below can be used.

```
{{#is_alert}} The alert threshold value has been breached. Current value is {{value}}. {{/is_alert}} 

{{#is_warning}} The warning threshold value has been breached. Current value is {{value}}. {{/is_warning}} 

{{#is_no_data}} No metric data has been collected for this host in the past 10 minutes. {{/is_no_data}} 

@davidhwest14@gmail.com
```

Instead of creating three separate monitors (Alert, Warning and No Data), I combined all three in the *Say what's happening* section of the metric monitor configuration page. If any one of these events are triggered, an email will be sent to me.

Below are two examples of emails that were generated because of events that triggered a notification to be sent. Using the variables {{host.name}} and ({{host.ip}} will insert the name of the host and the host IP into the subject line or body of the monitor. The first notification (warning) only has the affected hostname in the subject line. The second email (no data) includes both the affected hostname and its IP address.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Email%20notification%20for%20metric%20alert.png)

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Email%20notification%20for%20no%20data.png)

