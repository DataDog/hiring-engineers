# Welcome
Welcome to the Datadog product demonstration!
# Agenda
- Prerequisites - Setup the environment
   - Installing and Configuring VirtualBox
   - Installing and Configuring Vagrant
   - Installing the Datadog Agent
- Collecting Metrics
- Visualizing Data
- Monitoring Data
- Collecting APM Data
- Final Question
# Prerequisites - Setup the environment
NOTE: This section is intended to assist with setting up an environment to run Datadog.  This section can be skipped if you already have an environment with the Datadog Agent installed

The Datadog agent can be installed on a variety of operating systems.  For this demo, we will be utilizing a Linux VM, courtesy of Vagrant, and viewing it through VirtualBox.  We will install the Datadog Agent to the Linux VM that we deploy in this section.
## Installing and Configuring VirtualBox
You can download VirtualBox here:

[https://www.virtualbox.org/wiki/Downloads](url)

For this demo, we will download the VirtualBox 5.2.12 platform package for OS X hosts
![virtualbox](https://user-images.githubusercontent.com/39865915/41008653-f89df63a-68e0-11e8-9e1c-475b2a53c7d9.png)
Execute the VirtualBox.pkg and take all defaults through the installation
![virtualbox2](https://user-images.githubusercontent.com/39865915/41008714-5562d502-68e1-11e8-933b-0582ade8bef0.png)
## Installing and Configuring Vagrant
The "getting started" guide for Vagrant can be found here:

[https://www.vagrantup.com/intro/getting-started/index.html](url)

You can download Vagrant here:

[https://www.vagrantup.com/downloads.html](url)

For this demo, we will download the Mac OS 64-bit package
![vagrant](https://user-images.githubusercontent.com/39865915/41007786-5ba3f946-68dc-11e8-9f4f-135d38ede7b9.png)
Execute vagrant.pkg and take all defaults through the installation
![vagrant2](https://user-images.githubusercontent.com/39865915/41007954-30768710-68dd-11e8-94f4-fc8888c58ee3.png)
Now that we have Vagrant installed, we can create a directory for our Vagrant project by opening a terminal window and entering the following commands:
- mkdir vagrant_dd_demo
- cd vagrant_dd_demo

For this demo, we will use the official Ubuntu 16.04 LTS provided by VirtualBox, from Vagrant's cloud box catalog found here:

[https://app.vagrantup.com/boxes/search](url)

In the terminal, enter the command to add the VM box:
- vagrant box add ubuntu/xenial64

To create and initialize the Vagrant configuration file to use the box we just added, enter the following command in the terminal:
- vagrant init ubuntu/xenial64

![vagrant3](https://user-images.githubusercontent.com/39865915/41010123-96679d18-68ea-11e8-8f02-f5933a79b6cf.png)

Finally, to launch our Vagrant VM via virtual box, enter the following command into the terminal:
- vagrant up --provider=virtualbox

Launch VirtualBox and you will see the Vagrant VM running
![virtualbox3](https://user-images.githubusercontent.com/39865915/41123326-235a2ace-6a53-11e8-8609-1c1cc9a06a04.png)

Login to the VM with the following:
- User: _vagrant_
- Password: _vagrant_
![virtualbox4](https://user-images.githubusercontent.com/39865915/41125387-2c7e557a-6a59-11e8-8742-97363391faad.png)
## Installing the Datadog Agent
Go to the Datadog website ([https://www.datadoghq.com](url)), click on the "FREE TRIAL" icon, and enter your information to begin your trial:
![datadog](https://user-images.githubusercontent.com/39865915/41126910-f92fa9bc-6a5d-11e8-8f36-93fc2330958f.png)

Since we are installing the agent to our VM that we just setup/configured, we will select "Ubuntu" from the menu run the installation script command from our VM command line interface.  The result should be as follows:
![virtualbox5](https://user-images.githubusercontent.com/39865915/41126935-0aacfc9e-6a5e-11e8-921f-cdddf2e0b3c0.png)


# Collecting Metrics
# Visualizing Data
# Monitoring Data
# Collecting APM Data
# Final Question
