Your answers to the questions go here.
## Prerequisites - Setup the environment
  
  [Set up Virtual Box and Vagrant](https://github.com/hashicorp/vagrant/blob/master/README.md)
  
  ** If you're using a mac you might need to enable [this](https://medium.com/@Aenon/mac-virtualbox-kernel-driver-error-df39e7e10cd8) "System Preferences| Security & Privacy" **
  
1. build your first virtual environment:

````
vagrant init hashicorp/bionic64

vagrant up
````

Unforutnately this wasn't working for me, so I decided to create a virutal environment on my MacOS since this would still allow me an isolated working coding environment to install different versions of software for this project. I'll be using VSCode to edit:

``
$ conda create -n PythonData python=3.7 anaconda
``
  
  **Software:** DataDog "recruitment candidate" trial
  Plug in the API (key removed for this exercise)
  ``
  DD_AGENT_MAJOR_VERSION=7 DD_API_KEY= DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"
  ``
  Agent Report: "datadog-agent launch-gui"
  ![Screen Shot 2021-10-29 at 1 57 13 PM](https://user-images.githubusercontent.com/79612565/139704234-e461b6ee-3953-4813-934f-3c346add8fc3.png)

  ![Screen Shot 2021-10-29 at 1 57 04 PM](https://user-images.githubusercontent.com/79612565/139704323-aaf17ead-6eb3-4986-9ca2-c503bcce943d.png)

  
## Collecting Metrics:
### Add Tags [Getting Started with Tags](https://docs.datadoghq.com/getting_started/tagging/)
Manually added these in and restarted the agent:

![tag](https://user-images.githubusercontent.com/79612565/139706532-ec3da610-a043-4bc8-9eee-f33bb66f64ed.png)
![host](https://user-images.githubusercontent.com/79612565/139706545-862ef6a5-f91c-4fcb-86d7-7994d80b0220.png)


### Install a database then install datadog integration for your database
I decided to use MongoDB because it can handle the chaos of large unorganized data since it's not a structured database, anticipating different data strucutres and types. [Here's the documentation](https://docs.datadoghq.com/integrations/mongo/?tab=standalone)
1. make sure the environment is active ``$ conda activate PythonData``
2. [install mongo for Mac](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
3. Flask is needed for later so install it now
``
pip install Flask-PyMongo
``
4. start mongoDB
``
brew services start mongodb-community@5.0
``
5. in a new terminal shell start a new instance ``mongod``
6. create a new database by typing "use" and the database name you want to use in the terminal. I'm using "use admin" since it's already in the documentation.
7. create a new user:

![mongo](https://user-images.githubusercontent.com/79612565/139712008-342685c0-711b-467f-a95f-a38b2525cede.png)

8. edit conf.yaml so it reflects your new user details
![mongo_code](https://user-images.githubusercontent.com/79612565/139769209-fe7ac014-1eab-426c-be95-b90a90ca409f.png)


**Warning** mongoDB was not showing up on my integrations so I had to go back and re-do my tags and restart the agent
![mongo_wrong](https://user-images.githubusercontent.com/79612565/139769242-8b4e995d-76f1-4161-840b-04e5e2d7ced1.png)

9. I decided to update my tags in the conf.yaml file using
![tags_new](https://user-images.githubusercontent.com/79612565/139769278-cb11a2e3-1c71-4b5e-a5f0-c82078ed6681.png)

After restarting the agent I can see **mongoDB** has been integrated showing up on my hostmap and created a dashboard!
![mongo_correct](https://user-images.githubusercontent.com/79612565/139769323-92adaae7-c11f-4391-9d65-7bb100916dff.png)
![mongo_dashboard](https://user-images.githubusercontent.com/79612565/139769336-bab1fad5-f0e6-4963-a0a0-fd3ba48e0ef5.png)



### Create a Custom Agent Check
[Datadog Documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) to create an agent check
I watched [this](https://www.youtube.com/watch?v=kGKc7423744&ab_channel=Datadog) video owned by Datadog several times to better udnerstand the file structures and other important things to note such as both of the files needing the exact same name. From here I was able to navigate the directory in my terminal and create these:
1. Navigate to ``/opt/datadog-agent/check.d`` create a python file my_metric.py ``touch my_metric.py``
2. Navigate to ``/opt/datadog-agent/conf.d`` create a .yaml ``touch my_metric.yaml``
3. use random function to generate a series [found on stackoverflow](https://stackoverflow.com/questions/67694523/python-generate-random-number)
4. I copied the documentation code and used the ``randint`` function to generate a random number

````
#use random function
import random

#the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

#content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
````
6. now it's time to set up the my_metric.yaml. I used the [documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#collection-interval) and copied the code:

```
instances: [{}]
```

8. Verify by running  in the terminal using ``datadog-agent check my_metric`` from the documentation
9. I got an error ``AttributeError: module 'random' has no attribute 'randit'`` because I had a spelling error. Once I fixed that my_metric was running:
![metric_mispell](https://user-images.githubusercontent.com/79612565/139769636-f0102b17-5b7e-4ae3-bd90-b5b1fef91f6e.png)

**SUCESS!**
![metric_success](https://user-images.githubusercontent.com/79612565/139769661-c2ccb1f5-4c42-450c-88ad-07eaa9ed2057.png)


### Change the agent check's collection interval metric
Change this to submit once every 45 seconds
1. go back to my_metric.yaml
2. update the code:

````
init_config:
instances:
  - min_collection_interval: 45
 ````

**Bonus** *Can you change the collection interval without modifying the Python check file you created?* YES! amend the my_metric.yaml file to do this.

## Visualizing Data:
### Utilize the Datadog API to create a Timeboard
**First get the tools ready**:
1. install Python onto your machine (I already have this)
2. Get the Datadog library by running ``pip install datadog`` in your terminal with evnironment active
3. make sure you have your ``API_KEY`` and get an ``APP_KEY`` here:

![APP_KEY](https://user-images.githubusercontent.com/79612565/139923897-2a933996-7e2b-4b05-a2a0-f23af90ee8b7.png)

*Remember to hide your API/APP Keys!! I created a config.py file and added this to my .gitignore*

**Next build out the visualizations using JSON. I created a python file timeboard.py and tried to follow along to create the code**
*This was tough! Some resources I leveraged:*
[video](https://www.youtube.com/watch?v=KoKtlF2NShc&ab_channel=Datadog)
[Zero2Datadog](https://zero2datadog.readthedocs.io/en/latest/visualize.html#)
[Creating a Dashboard](https://docs.datadoghq.com/api/latest/dashboards/)

- A custom metric scoped over my host using ``my_metric``
- An anomoly metric using MongoDB which you can choose from [here](https://docs.datadoghq.com/integrations/mongo/?tab=standalone) or on the hostmap. I went with 
- Apply the rollup function to the custom metric ``my_metric``


**Finally take some screenshots of the dashboard in the UI**
- set the Timeboard to 5 minutes:

![timeboard](https://user-images.githubusercontent.com/79612565/139952613-28454271-5f66-4749-9e3d-522376c44376.png)

- Take a snapshot of the anomolies graph and @ yourself:
![dash_share](https://user-images.githubusercontent.com/79612565/139952754-7ffad950-7958-43f3-b0e4-50a9301985f7.png)


**What is the Anomaly graph displaying?** anOmoOOlIeSS





## Monitoring Data:
### Create a new metric:
1. From the *Menu > Monitors >New Monitors > Metric*
2. Change the metric to the custom metric ``my_metric``
3. change the warning threshold to 500
4. change the alerting threshold to 800
5. Ensure notifications for No Data past 10 minutes

![monitor](https://user-images.githubusercontent.com/79612565/139957386-ab3cf981-2498-4dcc-bf1a-1322f1c6b7b2.png)

### [Configure the monitor's message](https://docs.datadoghq.com/monitors/create/configuration/?tab=thresholdalert)
![monitors](https://user-images.githubusercontent.com/79612565/139959346-5fd64db1-4a10-47a6-a31c-28c2dcdab4e8.png)

**ALERT**
![alert](https://user-images.githubusercontent.com/79612565/139959363-8d9d8351-a58a-4757-8557-4f71226d6cae.png)

**WARNING**
![warning](https://user-images.githubusercontent.com/79612565/139959381-a3c99576-d8ce-4c4d-9d58-2b2a78c7b3c0.png)

**MISSING DATA**
![no_data](https://user-images.githubusercontent.com/79612565/139959410-fb7eff6f-b15f-4338-a286-71c76951c1b8.png)


**Bonus Question:** Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.
- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

1. *Monitor > Manage Downtime* Then click [**Schdule Downtime**](https://docs.datadoghq.com/monitors/notify/downtimes/?tab=bymonitorname)
2. Create a recurring downtime for days of the week and weekends. I assumed PDT since this is my timezone, but this couuld be based on HQ timezone.
![downtime_create](https://user-images.githubusercontent.com/79612565/139960670-fe2cecf3-bcd4-4a9e-8cc0-f1b0c2701de8.png)

![weekday](https://user-images.githubusercontent.com/79612565/139960717-d2565fea-63be-4572-b570-1de70dd55057.png)

![weekend](https://user-images.githubusercontent.com/79612565/139960731-5de73b01-62e2-4fb4-b401-020f4974643e.png)

![weekday_downtime](https://user-images.githubusercontent.com/79612565/139960751-ccea249b-b5e9-4d4b-8163-e89bb58237c3.png)

![weekend_downtime](https://user-images.githubusercontent.com/79612565/139960759-a980e593-9116-47e0-86eb-ccde0939ea9c.png)


## Collecting APM Data:

## Final Steps:
Github updated its operations on August 13, 2021 to require an access token when using command line access so I was having some trouble pushing to this repo. I followed [This Docmentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)  

## To Wrap it Up:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Something that's affected my life immensively since moving to California 3 years ago are the fires and smoke. What's more heartbreaking than a natural wildfire is one that could have been avoided. PGE can use datadog to ensure systems are functioning correctly and alert for anomolies to hopefully mitigate disasters such as the 2020 fires. Further to this Datadog can be used to monitor air quality metrics since air toxicity can be fatal and the air quality index can give a false positive, for example planning to go camping only to arrive and have high partiulate matter (PM).
 

