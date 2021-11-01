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
  ``
  DD_AGENT_MAJOR_VERSION=7 DD_API_KEY= DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"
  ``
  Agent Report: "datadog-agent launch-gui" (add image here)
  
  
## Collect the Metrics
### Add Tags show screenshot

### install database and install datadog integration for database
I decided to use MongoDB because it can handle the chaos of large unorganized data since it's not a structured database, anticipating different data strucutres and types. [Here's the documentation](https://docs.datadoghq.com/integrations/mongo/?tab=standalone)
1. make sure the environment is active
2. [install mongo for Mac](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

### create agent check

### change check's collection interval metric

### Bonus question Can you change the collection interval without modifying the Python check file you created?

## Visualize the Data
### Create a timeboard




  
