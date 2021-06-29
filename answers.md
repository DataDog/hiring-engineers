# Prerequisites - Setup the Environment

I used the **macOS** environment to complete this exercise.

1- I created my account on https://www.datadoghq.com/
2- To install the **Agent** on my machine I chose the **Mac OS X** platform from the menu list because I'm using the macOS environment and copied the installation command: 

`DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<API KEY> DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"` 
