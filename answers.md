# Prerequisites - Setup the environment

The operating system used to complete this exercise was MacOS High Sierra Version 10.13.4.

After signing up for an account, I navigated to the Integrations Tab --> Agent Tab --> Mac OS X Tab.
<img MacOS X/>


I used the one-line installation given to install the DataDog Agent.

Installation Complete!  
<img Installation/>


# Collecting Metrics

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.*

Using the DataDog Agent GUI, I configured the hostname and tags in the Settings Tab.

<img Tags/>

After saving the configurations and restarting the DataDog Agent GUI, I navigated to the Infrastructure Tab --> Host Map Tab in the DataDog Application in my browser.

<img HostMap/>

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose PostgreSQL for my database. I navigated to the Integrations Tab, found the PostgreSQL integration, and followed the configuration steps.

I edited the conf.d/postgres.yaml file.

<img configurations/>

I added the postgreSQL check to my Checks --> Manage Checks Tab in the GUI for future configurations.

I ran a status check and PostgreSQL integration check was successful.

<img PostgreSQL integration check />

After configuration, I proceeded to install the integration onto the DataDog platform

<img PostgreSQL download />  


## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Writing an Agent check requires the creation of two files:
1) A Check file
2) A YAML configuration file

I created a my_metric.py and my_metric.yaml file and placed them in the checks.d and conf.d folders respectively.

<img Checkfile/>
<img YAML file/>

I restarted the DataDog Agent GUI and my_metric check is successfully being executed and ran.

<img mymetriccheck running/> 
