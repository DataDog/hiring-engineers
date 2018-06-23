# Datadog Solutions Engineer Exercises - Matthew Tessler

## Prequisites - Setup the Environment

I am completing this exercise on a Mac OS X operating system. To avoid dependency issues, as the instructions recommended, I decided to spin up a fresh linux VM via Vagrant. I followed their [instructions](https://www.vagrantup.com/intro/getting-started/). I ran the command `vagrant init hashicorp/precise64` to create the virtual machine. 

![vagrant init hashicorp/precise64 command](images/init.png)

Then I started up the virtual machine with the command `vagrant up` and ran the command `vagrant ssh` to interface with the virtual machine.

![vagrant up and vagrant ssh command](images/up_ssh.png)

I then signed for a Datadog account.

![sign up](images/sign_up.png)

After that I followed the instructions in the sign up process. When I got to the "Agent Setup" step I chose the "Installing on Ubuntu" option because I was using an Ubuntu VM with Vagrant. 

![ubuntu install](images/ubuntu_install.png)

I followed the "Installing with Ubuntu" steps. I entered the one line of commands from the instructions. The installation sequence ran, and at its completion, the message from the datadog-agent informed me the Agent was running and functioning properly.

![install start](images/start_of_install.png)
...
![install end](images/end_of_install.png)

After that I was able to complete the setup process and was taken to the main dashboard. 

![main dashboard](images/main_dashboard.png)

## Collecting Metrics

The instructions next said to "Agg tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog."


