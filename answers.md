# A Hands-on Introduction to Datadog!
## About Datadog
If you've never heard or used the Datadog monitoring tool, this is a great exercise for you to tackle. 
In this tutorial, I will spin up a VM, sign up for Datadog, and begin using their tools. 

## Setting up your environment
You can utilize any OS/host that you would like to complete this exercise. However, the Datadog team has recommend one of the following approaches:
  * You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues.
  * You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

#### I decided to spin up a VM via Vagrant. I followed the instructions from [here.](https://www.vagrantup.com/intro/getting-started)

## Signing up for Datadog
Sign up for [Datadog](https://www.datadoghq.com/) (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.
Once you sign up, you'll follow the steps to install the Datadog agent on your machine. In this case since I'm using Vagrant I'm following the CentOS/Red Hat instructions. 

## Let's collect some metrics
After you're done signing up and have the agent installed. You will now go to the Datadog Infrastructure/Host Map page. 
Here you are able to see 
