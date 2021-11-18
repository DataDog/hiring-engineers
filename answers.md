First off I'd like to say I really enjoyed working through this exercise and learned alot along the way about the Datadog suite.



** Setting up the environment**

1. Choosing which environment I would use for the excercise was a learning experience. I had never heard of Vagrant or Virtual box and decided to ahead and use this so I don't run to dependency issues. After reading the documentation I realized that Virtual box can not be ran on the M1 chip. I ended up using an old laptop with intel chip. I installed Vagrant and Virtual box.

2. I initialized Vagrant

```
vagrant init hashicorp/bionic64
```

3. Then started the VM
```
vagrant up
```

4. SSH to box with
```
vagrant ssh
```

## I then installed the DataDog Agent to environment 

It is important to choose the correct Agent for environment. For Ubuntu, I ran the easy one step install command

```
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=c98147090f0162434a358063a74de3a9 DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

To stop agent you can run:

```
sudo systemctl stop datadog-agent
```
To run agent:

```
sudo systemctl start datadog-agent
```

## Collecting Metrics:

#### Environment Tags

In order to add tags you can modify the /etc/datadog-agent/datadog.yaml. I ran into permission issues trying to modify the yaml file. I used documentation regarding permission issues and followed the steps.

I first ran:

```
ls -l /var/log/datadog/
```
I saw that dd-agent did not own files so I ran:

```
sudo chown -R dd-agent:dd-agent /var/log/datadog/
```
I then proceeded to restart the agent and tried to reopen the file and still ran into permission issues. I found this "https://stackoverflow.com/questions/17535428/how-to-edit-save-a-file-through-ubuntu-terminal" and realized I had to run this command to edit file:

```
sudo vi etc/datadog-agent/datadog.yaml
```
what this does is vi enters into another terminal to edit the file. I could then open the file and change the hostname and insert tags by removing the comment #.

I then used the command:
```
:wq
```
to save changes.
![Image](https://user-images.githubusercontent.com/70303700/141049686-26b9b5dd-86ee-45df-b9f3-218cb39806ad.png)


## Installing PostGres
I decided to install PostGres since I am familiar with PostGres from my bootcamp. 

to install:
```
sudo apt-get install postgressql
```
![Image](https://user-images.githubusercontent.com/70303700/141049796-3ceaef08-00d4-4a92-8733-838a36254b85.png)

I then integrated with Datadog following the steps at "https://www.datadoghq.com/blog/collect-postgresql-data-with-datadog/"

I needed to create the datadog user so I ran these commands:

```
-create user datadog with password 'Camila1234$';
-grant pg_monitor to datadog;
-grant SELECT ON pq_stat_database to datadog;
```
to check if user was created and granted access run command:

```
\du
```
![Image](https://user-images.githubusercontent.com/70303700/141049987-320f7ced-fccb-487d-a4a2-a56a45cbdfcc.png)

I then logged onto Datadog account and installed the PostGres integration.

## Create custom check
I created custom metric named my_metric.yaml/py

I used the example that was used at "https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7"

I moved to the correct directory with command:
```
cd /etc/datdog-agent/checks.d
```
then I used this command to create file:
```
sudo vim my_metric.py
```

![Image](https://user-images.githubusercontent.com/70303700/141050192-8c45f5a8-45fa-4256-9d12-df4840867b31.png)

I confirmed it was present.

![Image](https://user-images.githubusercontent.com/70303700/141050254-347b021f-5c03-4d16-b10a-16e25f2936a6.png)

I then changed directory to conf.d to create the yaml file. I then ran this command:

```
sudo vim my_metric.yaml
```
I then edited the file to have an instance that uses 45 seconds.

![Image](https://user-images.githubusercontent.com/70303700/141050107-e265fd50-ed33-4565-a2e5-844b380ea1ad.png)

I confirmed that the my_metric.yaml file was running.


I verified by running:
```
sudo -u dd-agent -- datadog-agent check my_metric
```
![Screen Shot 2021-11-07 at 11 03 25 PM](https://user-images.githubusercontent.com/70303700/141050357-95187c69-66ed-49e2-9423-b7cfdfa810dd.png)

## Bonus Question
The min_collection_interval is set to a number for example in our case 45, which means that it could collected every 45 seconds and not that it will be collected every 45 seconds. If the collector runs the check at the 45 second interval and there is another task/check that is being performed it could be late. If the check takes longer than time allotted then the Agent will skip until the next interval.

## Visualizing data 

To create dashboards via API I tried using Postman as I wanted to learn more on how to use this service. I followed the steps here "https://docs.datadoghq.com/getting_started/api/".

I obtained the API needed for Postman.

I then installed the integration on Datadog. And followed the steps to proceed in Postman.
In Postman I expanded the Data Api Collection and selected Post a new Dashboard under Dashboards.

I entered api keys into the query params fields.
![Image](https://user-images.githubusercontent.com/70303700/141050484-1473d881-d6b6-427d-acfa-0d47c8ddea0a.png)

I then proceeded to enter the code below into the body field.

Unfortunately I kept getting an forbiden response and I could not get the dashboards to be created. Due to the time constraint I was not able to figure the solution to my issue. I did want to discuss what I was looking to add. The first dashboard was to scope my_metric I had created. The second dashboard I was looking to create was a dashboard that used the anomaly function using this documentation "https://docs.datadoghq.com/monitors/create/types/anomaly/". The third dashboard I was looking to create was a dashboard with the rollup function using this documentation "https://docs.datadoghq.com/dashboards/functions/rollup/".

{
  "title": "<Luis Dashboard>",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:my_metric{host:LuisDatadog}"
          }
        ],
        "title": "My metric scoped on myhost"
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "anomalies( avg:postgresql.connections{*}, 'basic', 2 )"
          }
        ],
        "title": "Postgres Connection with anomalies factor"
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:my_metric{*}.rollup(sum,3600)"
          }
        ],
        "title": "My metric  Rollup Function Applied"
      }
    }
  ],
  "layout_type": "ordered",
  "description": "<Luis Visualizing Data Dashbaord >",
  "is_read_only": true,
  "notify_list": [
    "test@datadoghq.com"
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

I used another dashboard in the Datadog gui to set timeboards timeframe to the past 5 minutes.
  
![Image](https://user-images.githubusercontent.com/70303700/141050538-c313a4f3-23f0-4c21-9044-db8b3a8aeff4.png)

I was also able to use the snapshot feature, which is great to illustrate a potential issue and can be reviewed by the team.
  ![Image](https://user-images.githubusercontent.com/70303700/141050642-ae8f3286-e8b4-456c-aa2d-a872f9977bb1.png)


## Bonus question

An anomaly function detects abnormal behavior which takes into account the history of the metric,trends, and seasonality.
It is displayed as overlaying grey band on graph for potential results.

### Monitoring Data 

I created a new monitor by logging into Datadog and clicking the new monitor option. The screenshot below shows the thresholds set for Alert > 800, Warning > 500,  and data missing for more than 10 minutes.
  
![Image](https://user-images.githubusercontent.com/70303700/141050928-40c58e6a-6510-49d6-8450-81b8d1c72c63.png)

I used the template variables to write the monitoring message.
{{#is_warning}}
average value of `system.cpu.user` has been **slightly high** over the past **5 minutes**.
{{/is_warning}} 

{{#is_alert}}
average value of `system.cpu.user` has been **high** over the past **5 minutes**.
{{/is_alert}}

{{#is_no_data}}
There has been **no** data for the  average value of `system.cpu.user` over the past **10 minutes**.
{{/is_no_data}}
 
 I did some test runs to see what the email notification would look like and I was sent 3 emails for the different cases. I included one of the emails that were sent to me.
  
![Image](https://user-images.githubusercontent.com/70303700/141051059-92bf6484-5559-4699-8456-c7abcb0f0204.png)

  
## Bonus Schedule downtime
I created a downtime schedule by going to Monitors and click on the yellow schedule downtime icon. When I clicked the icon it prompted me to specify times and days, and to option for message to notify team. Below are the email notifications I received to my email.
  
![Image](https://user-images.githubusercontent.com/70303700/141051265-de4abbbb-1098-49c4-8327-12c548a4917b.png)

![Image](https://user-images.githubusercontent.com/70303700/141051273-84fbef41-2c29-4040-b2c3-708ac4ab5646.png)
  
![Image](https://user-images.githubusercontent.com/70303700/141051351-2de2d25f-77d3-4037-9767-724ee31c673d.png)

  
## Collecting APM data

After struggling for a while trying to run ddtrace-run, I searched online and read different documentaion and wasn't able to get it to work on my older computer using vagrant and virtualbox. I then went ahead and installed the agent to another computer. I then went ahead and created a directory called flask_app. In here I created a python file named "my_flask_app", I also installed venv which is recommended to run flask app in a virtual environment. 
  
  <img width="303" alt="flask app dir" src="https://user-images.githubusercontent.com/70303700/142482652-0fe44ac9-0fcd-4b8a-8ff8-93f39b93d0d6.png">
  
In the python file I inserted the code provided with the challenge. I then activated the virtual environment by running the following command:
  
  ```
  source venv/bin/activate
  ```
  
I ran the following command in order to install flask:

```
sudo pip install flask
```
I installed ddtrace by running:
  
```
sudo pip install ddtrace
```
I needed to update the datadog yaml file so I exited the virtual environment by running:

  ```
  deactivate
  ```
I opened the yaml file and set apm_non_local_traffic to true under apm_config, the screenshot below represents the yaml file.
  
<img width="763" alt="Datadog yaml file " src="https://user-images.githubusercontent.com/70303700/142485445-2e72dc85-886b-44a8-a563-0fe6941401a1.png">

  I saved the changes in the yaml file and went back to the virtual environment and ran the following commands DD_SERVICE="my_flask_app" DD_ENV="dev" DD_LOGS_INJECTION=true ddtrace-run python my_flask_app.py. After this I received a msg stating that my app was running.
  
  <img width="1206" alt="Terminal running flask app" src="https://user-images.githubusercontent.com/70303700/142485778-2008dc88-4c82-4870-b4b9-f962875664a0.png">

I proceeded to go to my browser and check that the app was running and indeed it was, the images below include what I saw with the different endpoints. 
  
  <img width="1357" alt="Entrypoint to application" src="https://user-images.githubusercontent.com/70303700/142486171-63ef76e1-2732-48ec-b38e-87d16443aa01.png">

  <img width="1357" alt="Getting APM started " src="https://user-images.githubusercontent.com/70303700/142486183-670a9dfa-0190-4323-870e-fa02f6abec1e.png">

  
  <img width="1381" alt="Posting Traces" src="https://user-images.githubusercontent.com/70303700/142486197-0b3112c6-1e4a-4dd9-9375-07b6431cc2e3.png">

While I was hitting the different routes on my browser I was able to see in my terminal that the traces were being sent while also seeing them on the Datadog gui.
  
  <img width="1368" alt="Terminal showing traces running" src="https://user-images.githubusercontent.com/70303700/142486479-2b7c284c-697f-4de4-a13d-38cc0469fbec.png">

  <img width="1378" alt="live traces shown" src="https://user-images.githubusercontent.com/70303700/142486571-74ef7b5c-d962-46b2-b9d4-eaa487397adf.png">
  
  I was also able to see the latency, request, and error metrics displayed under traces in APM
  
  <img width="1402" alt="Traces shown with latency, Errors, Requests" src="https://user-images.githubusercontent.com/70303700/142486820-313e4197-d788-415b-8472-8a0a4bb77bcb.png">
  
 Finally I was able to see my host infrastructure metrics displayed as well. 
  
  
<img width="1394" alt="Infrastructure metrics" src="https://user-images.githubusercontent.com/70303700/142487022-04f9232c-a302-4793-9d84-f3e909efafef.png">

  
I was able to finally after some trial and error run the flask app and also able to send traces to Datadog. Throughout this process I learned quite a bit about Datadog and how it interacts with other technologies. To stop the flask app I entered control + C and deactivate to get out of the virtual environment.
 
##Bonus Question

A service groups together endpoints, queries, or jobs for scaling. Example would be a group of URL endpoints grouped under an API service. A resource is a particular action for service. The resource represents a specific domain of your application which allows services to do their job.


##Final Question
The amazing thing regarding Datadog is that it is very dynamic and its application is limitless. Where I can see Datadog used is in peoples fitbits or applewatches that track biostats. It can check what time of the day your heart rate is elevated or not? Also what days of the weeks do you walk more or burn more calories? Monitor when your blood pressure is elevated at what times of the day? With this information the individual can make adjusstments to their daily routine in order to lower these levels, or to be aware what triggers these abnormalities. 
