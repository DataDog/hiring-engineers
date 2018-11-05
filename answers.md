Your answers to the questions go here.
### Solution Engineer Answers
## by John Meagher

# Prerequisites - Setup the environment
I started the project by spinning up a ubuntu 16.04 linux box using vagrant. The specific box that I used was "https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-vagrant.box" which I found on vagrantbox.es. Originally I tried to create my own vm using virtualbox but I was having trouble with the datadog agent integration. Once I switched over to the vagrant box the datadog agent integration went smoothly. 

# Collecting Metrics
Once the datadog agent was running. I didnt realize that the agent config file was the /etc/datadog-agent/datadog.yaml file initially. I was able to add tags via the gui. While working on the APM section I realized where I was supposed to initially do the tags so I went back and changed them in the datadog.yaml file. 
![tagged host](https://github.com/jmeagheriv/hiring-engineers/blob/master/HostTagged.JPG)

I installed mongodb community edition using the instructions for ubuntu xenial 16.04 from [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/). I configured a datadog user based on the  integration for mongodb, configuration tab in the datadoghq. Upon restarting the agent, the mongodb metrics started to report in. [CheckConfig Output](https://github.com/jmeagheriv/hiring-engineers/blob/master/checkconfig.txt)

To create my_metric I created a checkvalue.d directory in the /etc/datadog-agent/conf.d directory. This is where I created a checkvalue.yaml. I created the checkvalue.py in the /etc/datadog-agent/checks.d directory. I followed along with the instructions [here](https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6) and changed the files to fit this metric.
checkvalue.yaml
`
init_config:

instances:
  - username: john
    password: te5tus3r
    min_collection_interval: 45
    tags:  env:testing, proj:solutioneng`
    
checkvalue.py
`
from checks import AgentCheck
import random
import time
class MetricCheckk(AgentCheck):
  def check(self, instance):
	self.gauge('my_metric', random.randint(0,1001))`



