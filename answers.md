Your answers to the questions go here.
## Prerequisites - Setup the environment
  
  [Set up Virtual Box and Vagrant](https://github.com/hashicorp/vagrant/blob/master/README.md)
  
  ** If you're using a mac you might need to enable [this](https://medium.com/@Aenon/mac-virtualbox-kernel-driver-error-df39e7e10cd8)on "System Preferences| Security & Privacy" **
  
build your first virtual environment:
``
vagrant init hashicorp/bionic64
vagrant up
``
Unforutnately this wasn't working for me, so I decided to create a virutal environment on my MacOS since this would still allow me an isolated working coding environment to install different versions of software for this project:
``
$ conda create -n PythonData python=3.7 anaconda
``
  
  software: DataDog "recruitment candidate" trial
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
1. make sure the environment is active
2. [install mongo for Mac](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
3. Flask is needed for later so install it now
``
pip install Flask-PyMongo
``
4. start mongoDB
``
brew services start mongodb-community@5.0
``
5. start a new instance ``mongod``
6. create a new database by typing "use admin" in the terminal
7. create a new user:

![mongo](https://user-images.githubusercontent.com/79612565/139712008-342685c0-711b-467f-a95f-a38b2525cede.png)


### create agent check

### change check's collection interval metric

### Bonus question Can you change the collection interval without modifying the Python check file you created?

## Visualizing Data
### Utilize the Datadog API to create a Timeboard

## Monitoring Data




  
