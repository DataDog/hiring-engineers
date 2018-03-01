# **DATADOG TUTORIAL**
In this tutorial we will be installing Datadog and exploring some of the great features it has to offer while using Mac OS X.  Throughout this tutorial there will be links, screenshots and documentation to help you get through each step.  If you have any questions along the way please go to our help center for further support. <https://help.datadoghq.com/hc/en-us>

## SETTING UP YOUR ENVIRONMENT
------------------------------

We will be using a linux virtual machine during this tutorial.  This will keep you from running into any operating system or dependency issues and help get you up and running quickly.  To begin lets go ahead and get the necessary programs installed on our computer.  If you are new to virtual machines check out these resources to get more acquainted with what they do:
1. <https://en.wikipedia.org/wiki/Virtual_machine>
2. <https://www.youtube.com/watch?v=yIVXjl4SwVo>

### Installing VirtualBox
You will need to download and install VirtualBox to use Vagrant.  Click on the link below to begin downloading the OS X version of VirtualBox for your computer.
<https://www.virtualbox.org/wiki/Downloads>  
Make sure that your computer allows VirtualBox to install.  You can look to see if your computer is blocking any installations under the security and privacy page in your settings.

### Installing Vagrant
Vagrant is a tool for building and managing virtual machine environments.  Click on the link below and click on the OS X version to begin downloading.
<https://www.vagrantup.com/downloads.html>
#{show vagrant_download_page screen shot}

After downloading the appropriate version follow the instructions for installation on your local computer.  Like VirtualBox make sure your computer allows for installation.

Once finished installing head over to the getting started page for Vagrant here: <https://www.vagrantup.com/intro/getting-started/>.  Since you've already installed vagrant you only need to verify that the installation was successful.  Follow the instructions on verifying the installation was successful.

Next go to the project setup page.  <https://www.vagrantup.com/intro/getting-started/project_setup.html> You have the option of either creating a new directory or incorporating Vagrant in a pre-existing directory.  Please choose the appropriate option for your needs and then follow the instructions on the page.
#{show vagrant_project_setup}

Lets now head over to the Boxes page.
<https://www.vagrantup.com/intro/getting-started/boxes.html>
Follow the instructions to create a Ubuntu 12.04 LTS 64-bit box by using the command in your terminal or command-line:
```
$ vagrant box add hashicorp/precise64
```
In the terminal please choose VirtualBox for the choices of providers.  
#{show terminal_creating_box}

You should see a similar terminal indicating the creation was successful.
#{show successful_box_creation}

Now open up the vagrantfile in your project.
#{show project_config}  

Follow the instructions to set the box you just created as the base box you will be working with.

Good job on creating your own virtual machine!  Go through the instructions on this page to get comfortable with the virtual machine and its commands.
<https://www.vagrantup.com/intro/getting-started/up.html>

### Signing up for Datadog

Head over to Datadog's website <https://www.datadoghq.com/> and click on 'GET STARTED FREE'.  Fill out the appropriate fields to set up your account.
#{show datadog_signup}

On the Agent Setup page download the OS X agent for your local machine then follow the installation instructions.
#{show agent_setup}

After the agent is done installing run it in the command line using this command:
```
$ datadog-agent start
```

If it started successfully the agent setup page will tell you so and you can go on to the next step!

To learn more about what the Agent does and how to better us it you can look through the documentation here <https://docs.datadoghq.com/agent/>.

## Collecting Metrics
---------------------

Read through the documentation for learning about tags. <https://docs.datadoghq.com/getting_started/tagging/>

Lets start by adding tags to our config file by going into our console and typing the command:
```
$ open /opt/datadog-agent/etc/datadog.yaml
```
Scroll down until you find the "Set the hosts tags" section.  Remove the hashes to uncomment the area and add any tags you want using the key value format.  
#{show assigning_tags_config}

#{IMPORTANT! SHOW host_map_tags}

Next we will install PostgreSQL to use as our server.  We will install it using homebrew and the command line.  You can follow the instructions from here to install homebrew and PostgreSQL: <https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb>

Now create a database on the command line:
```
$ createdb [your database name here]
```

Next we need to integrate PostgreSQL with Datadog using Datadog's provided integration.  We'll start by first adding a postgres.yaml file in the agent's conf.d directory.  To do so follow these commands in the command-line:
```
$ open ~/.datadog-agent/conf.d/
touch postgres.yaml
```

You can read about this step and more regarding integrations here: <https://docs.datadoghq.com/integrations/postgres/>

Now lets go to
<https://app.datadoghq.com/account/settings#integrations/postgres> to create the integration. Follow the instructions to install the integration. 
#{show postgres_integration}
