Your answers to the questions go here.

# Getting Started with DataDog

## Overview
This document will provide a walkthrough on how to set up a monitored host in Datadog, and from there, add a custom metric with checks and alerts. 

Each level will be broken up into 2 sections.
1. Walkthrough: This catalogues the steps you would take to accomplish the tasks in the level. It's written as though it might be used as a guide for a customer
2. Thinkthrough: This section is to give you insight into my process going through the level. I'll share what was straightforward, where I encountered problems, how I approached those problems, how I fixed them (if I did), and other insights.

## Prework
This project was started on May 3, 2017.  
Before I started the levels, I read through the reference links and took notes in order to prime myself on the material. You can find those notes in notes.md.  
I also did a quick tutorial [online](http://www.markdowntutorial.com/) (See Appendix) for writing in markdown so that I could write a good-looking answers.md. 

I had originally planned to write this all in Google docs, but after seeing the repository, 
I decided it made more sense to use markdown. Especially sense most github readme's tend to use it, 
and so do Datadog's notifications!

## Level 0 (optional) - Set up an Ubuntu VM
This step is optional but it will help you to avoid any dependency issues. You may use any VM of your
choice. We chose to use Ubuntu 12.04 run with Vagrant.

### Walkthrough

1. Install Virtualbox. Here is the [Download](https://www.virtualbox.org/wiki/Downloads)
![Running Virtualbox](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/virtualbox-installed.png)
2. Install Vagrant. Here is the [Download](https://www.vagrantup.com/)
![Vagrant Installed](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/vagrant-installed.png)
3. Launch a Ubuntu 12.04 VM using Vagrant with the following commands
```
$ vagrant init hasicorp/precise64
$ vagrant up
```
4. SSH into the new Vagrant host
``` 
$ vagrant ssh
```
Congrats! You're now ready to get started with Datadog

### Thinkthrough
I noticed initially that the instructions for Vagrant in the readme on Github had linux commands for starting vagrant.
```
$ vagrant init hasicorp/precise64
$ vagrant up
```
So I figured I should run the VM on my laptop's linux partition to make it easy for setup.

I've installed Virtualbox several times for previous jobs so I just followed the install wizard after
downloading it from the website. Since I'm running 64-bit Ubuntu 16.04, I downloaded the AMD64 version for Ubuntu 16.04.

Vagrant gave the option of a 64-bit debian installer on their website. Ubuntu is based on Debian, so I downloaded that. I avoided using my package manager with `$ sudo apt-get install` because I've had
cases in the past where the package manager version was behind the software's official download.

I checked that vagrant installed correctly with the proper version with `vagrant -v` and that was all good. But, as you can see in the screen shot below, VT-x was disabled in the bios, and that caused 
an error when vagrant attempted to use virtualbox.
![VT-x Error](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/VT-x_disabled.png)

After Enabling virtualization in the bios, vagrant worked!
![VT-x enabled](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/bios-vt.jpg)
![Vagrant is up](https://github.com/GuavaKhan/hiring-engineers/blob/parker-solutions-engineer/images/vagrant-up.png)

## Level 1 - Collecting your Data
You will create a DataDog Account, modify the Agent's configuration, install a database, add the DataDog integration for that DB, and write a custom agent check.

Bonus question: In your own words, what is the Agent?  
Reference link: http://docs.datadoghq.com/guides/basic_agent_usage/  
Idea: Draw a diagram outlining the 3 key components and how they work together

### Walkthrough

### Thinkthrough

## Level 2 - Visualizing your Data
You will clone the starting dashboard, add additional metrics, and make sure your email recieves a snapshot with @notification.

Bonus question: What is the difference between a timeboard and a screenboard?

## Level 3 - Alerting on your Data
You will set up a monitor for your metric (it should alert you within 15 minutes).

Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  
Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


## Appendix

### Software Used
- Ubuntu 16.04 LTS - Partition on my Personal Computer. This is my preferred coding environment.
- VIM - for editing Markdown files

### Online Reference Material
- [Markdown Tutorial](http://www.markdowntutorial.com/)
- [Markdown Quick Reference](https://en.support.wordpress.com/markdown-quick-reference/)
