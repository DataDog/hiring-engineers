Your answers to the questions go here.

Prerequisites - Setup the environment
=================================

I created an ec2 instance in my account, for now I will use a t2.micro, if I find that later steps demand more, I will resize the instance.

I installed the datadog client, and 
![image](images/installed-agent.PNG?raw=true "Installed Agent")

during the startup processs, I saw the filename  "/etc/datadog-agent" so I would assume this is the config file, a quick google search confirmed this.


*Collecting Metrics:*
**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

running a "grep" command, allowed me to find that there was infact a direct mention of "tags" within this file, and as such, I have created 3 tags as follows:


![image](images/tags.PNG?raw=true "Tags")

**one thing to note, I had to stop here for 2 days to move house, I am currently trying to troubleshoot getting the client to publish metrics once again as my instance was stop-started, these steps may give some insight into the troubleshooting steps I have followed**

I checked the outbound SG on my instance, and could see that all outbound traffic was allowed. As SGs are stateful,I do not need to open inbound traffic (unlike ACLs).

I searched online and found the doc:

https://docs.datadoghq.com/agent/troubleshooting/

when first thing to check per the doc was my API-key. When checking the datadog config file, the API key was the same. 

I restarted the datadog client to ensure it was up and sending traffic (should have checked top before hand to confirm if it was running).

this did not work^^ as such, I am trying to find the status of the agent on the instance.

I found the doc here https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7 outlining how to check the status
running the command :

sudo service datadog-agent status

and see the following information:

![image](images/broken.PNG?raw=true "Broken")