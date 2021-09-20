**Prerequisites - Setup The Environment**

Deciding on what environment for this technical test was an interesting one as I had not heard much of Vagrant and did want to explore this route but ulitmately after sometime with this I decided to go with Virtual box and run Ubuntu as there was some familiarity from my days in college and througout my own projects.

I obtained the image "Ubuntu 21.04" straight from Ubuntu.com. The reason for not using the image from Virtual box was so I could create a customised image for my own specifications.

Once the image was installed and configured the first command that needed to be run was "sudo apt-get update". This command is used to download package information from all configured sources. When this was completed it was time to setup my DataDog account and install the agent which is detailed in the next section.

**Collecting Metrics**

Installing DataDog Agent
Once the Ubuntu machine was operational I setup a Datadog account, logged onto the datadog site and installed the agent through the first inital account setup phase.

A big help was to go onto DataDog site and use the tips and notes illustrated below:
https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7

I copied the API that was informed on the Datadog 
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=96817c29cbbbde53f1825089e3716712 DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)" 

![image](https://user-images.githubusercontent.com/90416145/134027968-b8f26a6a-2254-4a9e-9bc4-409bb72b6bad.png)

Below is a photo of the host that was created along with the tags that I established for this task:
![image](https://user-images.githubusercontent.com/90416145/133288893-bf3652f8-7f41-4793-937b-76acdf12ae11.png)

To create these Tags I opened up the terminal in my Ubuntu VM and entered the command "sudo vi /etc/datadog-agent/datadog.yaml"

Sudo vi - enters into another terminal to edit the datadog.yaml file from the path /etc/datadog-agent/.

Once opened, I changed the hostname and inserted some tags into the datadog.yaml file by removing the comment # and inserting the new tags.

![image](https://user-images.githubusercontent.com/90416145/133290532-5beffd84-8545-4636-b2d9-cbeaaee7c366.png)

Used the command :wq to save changes and leave.
If anything that was written by accident or removed could enter :q! to exit the .yaml file without saving these changes

_Installing  PostGresDB_
I decieded on adding Postgres DB to as it is perhaps not as well known as MySQL and the fact that it is an open source tool has me interested to use as I am a fan of open sourced tools/applications as I think many people can learn and get into without having time restraints  

To install run the command "sudo apt-get install postgressql"
To check it is installed and operational run the command service postgresql status where active entry should be active link in the screenshot below:
![image](https://user-images.githubusercontent.com/90416145/133295300-a2625237-9bdb-45d5-89b3-a5c7e51daec9.png)

To integrate DataDog into PostGres I followed the steps detailed on the datadog site link below:
https://www.datadoghq.com/blog/collect-postgresql-data-with-datadog/

To create the datadog user I followed the commands listed onto DataDog site noted above:
First thing is to enter into the postgres domain. To do this you must perform the command sudo -su postgres. When in the terminal I created the account with the following credentials 

  -create user datadog with password 'Eagles';
  -grant pg_monitor to datadog;
  -grant SELECT ON pg_stat_database to datadog;

To confirm if you are connected to PostgreSQL and want to see details of the connection, use the command: 
To verify if the user and their access was graned can type the command \du to view the users in postgresql
![image](https://user-images.githubusercontent.com/90416145/134029594-9253779b-94f0-4825-9621-01ca24e8e875.png)

Subsequently I logged onto Datadog gui and installed the PostGres integration
![image](https://user-images.githubusercontent.com/90416145/133296005-ee828608-4724-40f1-bdf7-0163cab1f339.png)

_Custom Checks_

Tasks to create a custom metric named custom_SimonCheck.yaml / py

Followed the example on DataDog site link below:
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

Changed directory by using the command cd /etc/datadog-agent/checks.d

vim custom_SimonCheck.py
![image](https://user-images.githubusercontent.com/90416145/133300229-e52eae46-7e50-4f27-9061-a7e0bf25bb3e.png)

Side note:
Later on came across an issue that my graphs were not populating.
This was due to the "hello.world"


Confirmation that the file was present

![image](https://user-images.githubusercontent.com/90416145/133300546-350e2964-656e-4939-bb26-182a8b353518.png)

Changed directory to conf.d to create the .yaml file
sudo vim custom_Simon_Check.yaml to edit the yaml file to add instances

In the image below I have the instance that can now use up to 45 seconds in the custom_Simon_Check.yaml
![image](https://user-images.githubusercontent.com/90416145/133298909-3c557e41-c88d-4019-9f59-27b817e886c3.png)

Confirmed custom_SimonCheck/yaml was present:
![image](https://user-images.githubusercontent.com/90416145/133300765-e6cfa3d7-fc12-48da-95c8-47e4877e3650.png)

To verify check run command sudo -u dd-agent -- datadog-agent check custom_SimonCheck

![image](https://user-images.githubusercontent.com/90416145/133299153-a6317b23-2e22-43a0-b136-09c1b7899bda.png)

_Bonus Question_
The  min_collection_interval is set to a number i.e 45, this means that it could be collected every 45seconds not that it will collect every 45seconds. The collector will try to run the checker every 45 seconds but it maybe late as another task/check is being performed prior to this custom check. If the check takes longer than the allotted time then the Agent will skip the execution until the next interval

**Visualizing Data**

I used the applications Postman that was documneted on the DataDog site:
https://docs.datadoghq.com/getting_started/api/

To obtain the API's needed for Postman I logged onto Datadog, selected Integrations > APIs
![image](https://user-images.githubusercontent.com/90416145/134031726-3cc42809-e19b-4d42-9f59-1c5c3e44e9cb.png)

Expanded the Data Api Collection > selected Post a check status > Inserted the api keys into the Query Params filed.
Saved the changes and clicked on send to confirm communication was established
![image](https://user-images.githubusercontent.com/90416145/134031917-3d030ec0-6a4f-4e13-b3c9-a79ca50e20b5.png)

To create a Dashboard with Postman click on the Dashboard entry within DataDog API Collection.
Went to the Body tab and inserted the following code to create the follow dashborad entries:

_Custom Metric Name: custom_SimonCheck
Postgres Metric: postgresql.connections
Rollup Metric: SimonCheck_

    {"title": "<Simon Dashboard>",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:SimonCheck{host:SimonDataDog}"
                    }
                ],
                "title": "SimonCheck scoped on myhost"
            }
        },
    {
            "definition" : {
                "type" : "timeseries",
                "requests": [
                        {
                                "q": "anomalies( avg:postgresql.connections{*}, 'basic', 2 )"

                        }

                ],
                "title" : "Postgres Connection with anomalies factor"
                         }
    },
    {
            "definition": {

                    "type": "timeseries",
                    "requests": [
                                 {
                                     "q": "avg:SimonCheck{*}.rollup(sum,3600)"
                                 }

                                ],
                "title": "SimonCheck with Rollup Function Applied"

                            } }
    
    ],
    "layout_type": "ordered",
    "description": "<Simons Visualizing Data Dashbaord >",
    "is_read_only": true,
    "notify_list": [
        "test@datadoghq.eu"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "<HOSTNAME_1>"
        }
    ],
    "template_variable_presets": [
        {
            "name": "Saved views for hostname 2",
            "template_variables": [
                {
                    "name": "host",
                    "value": "<HOSTNAME_2>"
                }
            ]
        }
    ]
}

Confirmed Dashboard was imported into DataDog:
![image](https://user-images.githubusercontent.com/90416145/134032788-c2c7bc6a-c640-47be-b215-95bf691649e7.png)
  ![image](https://user-images.githubusercontent.com/90416145/134033133-156a91d1-d87b-40a2-9ba0-2104404db0de.png)

Set the TimeFrame to the past 5mins for the timeboard:
When in the Timeboards can adjust the timeframe in the top right corner of the timeboard you wish to edit and and choose the desired time. This being past 5 minutes.

![image](https://user-images.githubusercontent.com/90416145/134034428-d736ce52-54f5-4aa8-974a-dda5292be3ca.png)
![image](https://user-images.githubusercontent.com/90416145/134034497-83773f48-7a28-49fe-813b-00b633259130.png)

Can also create a graph to set the display preferences to show past 5 minutes:
![image](https://user-images.githubusercontent.com/90416145/134034267-6f6450d7-8d9d-448f-953a-8eed352bf749.png)

Taking a snapshot is a great tool that can be used to show spikes and quickly illustrate a potential issue or any area that may need some attention to by you team
 ![image](https://user-images.githubusercontent.com/90416145/134035056-7280d4d7-ff4d-431a-918e-17ee004e1286.png)
 
_Bonus Question_

Anomaly functions inform us if a metric has an abnormal behaviour. Datadog has implemented this anomaly detection feature. Anomaly detection distinguishes between normal and abnormal metric trends by analysing a metric’s historical behaviour. These values are represented in an overlaying grey stripe/band and are deemed as potential results.

![image](https://user-images.githubusercontent.com/90416145/134035265-5e4e3b0d-9343-4040-b9c9-36ddf519b493.png)

The anomalies function uses the past to predict what is expected in the future, so using it on a new metric may yield poor results
An example of this would be if there is a sudden spike of the values for a type of metric (i.e CPU usage) this would soar higher than the grey line in the dashboard

**Monitoring Data**

To create a new Monitor - I logged into Datadog and hovered Monitors and clicked the new monitor option. Below in the screenshot lists the chosen metric selected from which host and any additional tags that can be added to gather a more detailed field of view.

Set the Alert threshold to > 800
Set the Warning threshold to > 500
Selected to Notify if data is missing for more than 10 minutes

![image](https://user-images.githubusercontent.com/90416145/134035592-5014261a-4729-48db-a93d-34744c94bb82.png)

_Configuring the Monitor Message_

Using the Message Template Variables I was able to write my Monitor Message
{{#is_warning}}
**WARNING**: The average value of `system.cpu.user` has been **slightly high** over the past **5 minutes**.
{{/is_warning}} 

{{#is_alert}}
**ALERT!** `system.cpu.user` has been **high** over the past **5 minutes** at {{value}}  for {{host.name}} with IP {{host.ip}}.
{{/is_alert}}

{{#is_no_data}}
There has been **no** data for the  average value of `system.cpu.user` over the past **10 minutes**.
{{/is_no_data}} @kav92is@gmail.com

_Bonus Question _

Schedule downtimes:
To create a Schedule Downtime. Click Montiors > Manage Downtime and select yellow Schedule Downtime icon on the right side of the page

![image](https://user-images.githubusercontent.com/90416145/134038566-be4ce49c-2db3-4e10-ae3b-affea2441048.png)

Upon clicking the Schedule Downtime you are prompted with the fields to insert to specificy what would like to silence, the schedule and a optional message:
![image](https://user-images.githubusercontent.com/90416145/134036633-e7223891-2c26-4f75-96cd-3dacad327659.png)

Email Alert notification:
![image](https://user-images.githubusercontent.com/90416145/134038957-6744e3e1-906c-42e4-a3da-48d1672cdba2.png)

**Collecting APM Data**

I was having some issues as I was unable to install the ddtrace on my VM.

pip install flask
pip install ddtrace

when creating a python file it would not allow me to do so.
![image](https://user-images.githubusercontent.com/90416145/134039210-f92465ec-6f8b-4f3b-9656-095703752ab6.png)

I followed the steps on the Datadog site (link below) but unfortunately I could not find a solution to my issue.
https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers

However what needs to be done is set apm_non_local_traffic: true in the apm_config
![image](https://user-images.githubusercontent.com/90416145/134041020-47a343d2-b66a-4211-be18-e78334845d17.png)

Define DD_SERVICE and DD_ENV 
DD_SERVICE="flask_apm_app" DD_ENV="dev" DD_LOGS_INJECTION=true ddtrace-run python3 flask_apm.py.

_Bonus Question is the difference between a Service and a Resource?_

A service are grouped together endpoints, queries, or jobs for the purposes of scaling instances. An example of this would be a group of DB queries that are grouped together within one database service. They aren’t uncommon and are pillars in microservices architectures
Resources : are particular actions for your service. Resources represent a specific domain of an application such as a background job. It allows services to do their role.

**Final Question**

The thing about Datadog is there is no limits as to what it cant be applied to.
One aspect of my life that I could see a big gap in which Datadog can be used for is with gym training sessions/programs.
Information that I think that are vital to monitor to benefit multiple people would be:

-Gym/Machines/Equipment - Busy or Not? What equipment is popular at certain times of the day.

-Heart rate - is it too high or too low? Is our heartbeat too high?

-Rest time between sets or repetions - too long or too short?

-Hydration levels - Are we at optimal levels for peak performance?

-Max force output generated - Can we go one more repition/set or increase the weight?

Having this information would be great to understand not only an optimal time to go training to work on specific exercises but also are we operating at peak conditional levels.
If my resting periods are too short or not drinking enough water, what affect does that have on my maximum force output?
If the gym is busy does it affect my reset time which can have a knock on affect.
