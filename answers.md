# **DATADOG TUTORIAL**
In this tutorial we will be installing Datadog and exploring some of the great features it has to offer.  Throughout this tutorial there will be links, screenshots and documentation to help you get through each step.  If you have any questions along the way please reach out to our help center here <https://help.datadoghq.com/hc/en-us>

## SETTING UP YOUR ENVIRONMENT
------------------------------

We will be using a linux virtual machine during this tutorial.  This will keep you from running into any operating system or dependency issues and help get you up and running quickly.  To begin lets go ahead and get the necessary programs installed on our computer.  This tutorial will be going through the installation guide for Mac OS X so if you are using something other than a Mac product make sure and click on the appropriate download source in the given links.  If you are new to virtual machines check out these resources to get more acquainted with what they do:
1. <https://en.wikipedia.org/wiki/Virtual_machine>
2. <https://www.youtube.com/watch?v=yIVXjl4SwVo>

### Installing VirtualBox
You will need to download and install VirtualBox to use Vagrant.  Click on the link below to begin downloading the appropriate version of VirtualBox for your computer.
<https://www.virtualbox.org/wiki/Downloads>  
Make sure that your computer allows VirtualBox to install.  You can look to see if your computer is blocking any installations under the security and privacy page in your settings.  Next we will install Vagrant.

### Installing Vagrant
Vagrant is a tool for building and managing virtual machine environments.  Click on the link below to begin downloading the appropriate version of Vagrant for your computer.  
<https://www.vagrantup.com/downloads.html>
#{show vagrant_download_page screen shot}

After downloading the appropriate version follow the instructions for installation on your local computer.  Like VirtualBox make sure your computer allows for installation.

Once finished installing head over to the getting started page for Vagrant here <https://www.vagrantup.com/intro/getting-started/>.  Since you've already installed vagrant you only need to verify that the installation was successful.  Follow the instructions on verifying the installation was successful.

Next go to the project setup page.  <https://www.vagrantup.com/intro/getting-started/project_setup.html> You have the option of either creating a new directory or incorporating Vagrant in a pre-existing directory.  Please choose the appropriate option for your needs and then follow the instructions on the page.
#{show vagrant_project_setup}

Lets now head over to the Boxes page.
<https://www.vagrantup.com/intro/getting-started/boxes.html>
