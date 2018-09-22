Your answers to the questions go here.

Your answers to the questions go here.

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues.
You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.
Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.



-I chose to use both my local osx environment and a Vagrant + Virtual box envrionement to run datadog.

-osx envrionment:
	-I first downloaded datadog into my local environment envrionment and ran it using the datadog icon located in my 'Applications' folder

	-you may also lauch datadog using the following commands:
		-datadog-agent launch-gui



-Vagrant + Virtual box environment:

	-Did a fresh install into my ubuntu envrionment usind the following commands:

		- DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
		- for the command, I replaced 'YOUR_API_KEY' with the API given to me by datadog
		- API key given: b4371073b027d86e3174258d84d52b8a


![](datadog_installation_ubuntu.png)