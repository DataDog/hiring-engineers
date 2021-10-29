Your answers to the questions go here.
## Prerequisites - Setup the environment
  environment used: MacOS
  Set up Virtual Box and Vagrant https://github.com/hashicorp/vagrant/blob/master/README.md
  
  ** If you're using a mac you might need to enable this on "System Preferences| Security & Privacy" **
  https://medium.com/@Aenon/mac-virtualbox-kernel-driver-error-df39e7e10cd8
  
  software: DataDog "recruitment candidate" trial
  DD_AGENT_MAJOR_VERSION=7 DD_API_KEY= DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"
  Agent Report: "datadog-agent launch-gui" (add image here)
  
  build your first virtual environment:

vagrant init hashicorp/bionic64
vagrant up
  
## Collect the Metrics
### Add Tags show screenshot

### install database and install datadog integration for database

### create agent check

### change check's collection interval metric

### Bonus question Can you change the collection interval without modifying the Python check file you created?

## Visualize the Data
### Create a timeboard




  
