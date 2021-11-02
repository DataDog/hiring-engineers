Your answers to the questions go here.
## Prerequisites - Setup the environment
  
  [Set up Virtual Box and Vagrant](https://github.com/hashicorp/vagrant/blob/master/README.md)
  
  ** If you're using a mac you might need to enable [this](https://medium.com/@Aenon/mac-virtualbox-kernel-driver-error-df39e7e10cd8) "System Preferences| Security & Privacy" **
  
1. build your first virtual environment:

``
vagrant init hashicorp/bionic64

vagrant up
``
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

  
## Collecting Metrics
### Add Tags [Getting Started with Tags](https://docs.datadoghq.com/getting_started/tagging/)
Manually added these in and restarted the agent:

![tag](https://user-images.githubusercontent.com/79612565/139706532-ec3da610-a043-4bc8-9eee-f33bb66f64ed.png)
![host](https://user-images.githubusercontent.com/79612565/139706545-862ef6a5-f91c-4fcb-86d7-7994d80b0220.png)


### install database and install datadog integration for database
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
6. create a new database by typing "use admin" in the terminal
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



### Custom Agent Check
[Datadog Documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) to create an agent check
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
6. Run this in the terminal using ``datadog-agent check my_metric`` from the documentation
7. I got an error ``AttributeError: module 'random' has no attribute 'randit'`` because I had a spelling error. Once I fixed that my_metric was running:
![metric_mispell](https://user-images.githubusercontent.com/79612565/139769636-f0102b17-5b7e-4ae3-bd90-b5b1fef91f6e.png)

**SUCESS!**
![metric_success](https://user-images.githubusercontent.com/79612565/139769661-c2ccb1f5-4c42-450c-88ad-07eaa9ed2057.png)


### change check's collection interval metric

### Bonus question Can you change the collection interval without modifying the Python check file you created?

## Visualizing Data
### Utilize the Datadog API to create a Timeboard

## Monitoring Data




  
