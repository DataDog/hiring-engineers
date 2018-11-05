Your answers to the questions go here.

# Prerequisites - Setup the environment
I started the project by spinning up a ubuntu 16.04 linux box using vagrant. The specific box that I used was "https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-vagrant.box" which I found on vagrantbox.es. Originally I tried to create my own vm using virtualbox but I was having trouble with the datadog agent integration. Once I switched over to the vagrant box the datadog agent integration went smoothly. 

# Collecting Metrics
Once the datadog agent was running. I didnt realize that the agent config file was the /etc/datadog-agent/datadog.yaml file initially. I was able to add tags via the gui. While working on the APM section I realized where I was supposed to initially do the tags so I went back and changed them in the datadog.yaml file. 
[tagged host](https://github.com/jmeagheriv/hiring-engineers/blob/master/HostTagged.JPG)
