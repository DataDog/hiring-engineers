# Prerequisites - Setup the environment

The operating system used to complete this exercise was MacOS High Sierra Version 10.13.4.

After signing up for an account, I navigated to the Integrations Tab --> Agent Tab --> Mac OS X Tab.
<img MacOS X/>


I used the one-line installation given to install the DataDog Agent.

Installation Complete!  
<img Installation/>


# Collecting Metrics

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.*

Using the DataDog Agent Web UI, I configured the hostname and tags in the Settings Tab.

<img Tags/>

After saving the configurations and restarting the DataDog Agent Web UI, I navigated to the Infrastructure Tab --> Host Map Tab in the DataDog Application in my browser.

<img HostMap/>

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose PostgreSQL for my database. I navigated to the Integrations Tab, found the PostgreSQL integration, and followed the configuration steps.

I edited the conf.d/postgres.yaml file.

<img configurations/>

I added the postgreSQL check to my Checks --> Manage Checks Tab in the Web UI for future configurations.

I ran a status check and PostgreSQL integration check passed!

<img PostgreSQL integration check />

After configuration, I proceeded to install the integration onto the DataDog plaform

<img PostgreSQL download />  
