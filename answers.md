# Datadog Solutions Engineer Exercises - Matthew Tessler

## Prequisites - Setup the Environment

I am completing this exercise on a Mac OS X operating system. To avoid dependency issues, as the instructions recommended, I decided to spin up a fresh linux VM via Vagrant. I followed their [instructions](https://www.vagrantup.com/intro/getting-started/). I ran the command `vagrant init hashicorp/precise64` to create the virtual machine. 

![vagrant init hashicorp/precise64 command](images/init.png)

Then I started up the virtual machine with the command `vagrant up` and ran the command `vagrant ssh` to interface with the virtual machine.

![vagrant up and vagrant ssh command](images/up_ssh.png)

I then signed up for a Datadog account.

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

The instructions next said to "Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog."

I had to do some research to find where the Agent config file was located. I found the answer at this [resource](https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-). After moving to the `etc/datadog-agent` directory, I located the `datadog.yaml` file. I opened the file to edit it. 

I added some tags according to these instructions on this [page](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files), and then I went back to look at the host map. **I'm still not sure how to get the tags to reflect immediatedly on the host map.** I was trying to restart the service, and I don't think that worked. I couldn't figure out how to do the command to run the service check on the agent so that didn't work. It just updated after a while. Regardless, now my Agent configration file and the host map both reflect the same tags. 

The tags are visible in the configuration file at the bottom of the terminal window:

![config file](config_file.png)

And here are the tags in the host map:

![host map](host_map.png)

Next I needed to install a database on the machine and then install the respective Datadog integration for that database. I decided to go with MongoDB. First I updated my Ubuntu operating system from 12.04 to 14.04 in line with the instructions on MongoDB's [website](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) to install the Community Edition on Ubuntu.

After installing MongoDB, I began the install for the integration for Datadog. I followed these [instructions](https://docs.datadoghq.com/integrations/mongo/#setup). I set up the `conf.yaml` file, set up the user in the mongo shell, and installed the integration on Datadog. Here you can see some screenshots on Datadog that the MongoDB integration is up and running on the host. 

![host with mongo](host_with_mongo.png)
![mongo integration installed](mongo_integration_installed.png)
![mongo dashboard](mongo_dashboard.png)

Running an info status check, `sudo datadog-agent status`, the checks appear for MongoDB. Here is a screenshot:

![mongo status check](mongo_status_check.png)





