## Prerequisites * Setup the environment
Write about my environment and setting up my tools. Talk about background knowledge coming in
* using debian laptop
* clone repo
* install virtualbox
    * enable virtualization
* install vagrant
* create ubuntu image
* Read docs and watch Datadog 101

## Collecting Metrics
Configure the ubunutu image to set up several processes and configure agent to monitor them. Talk about why metrics are important
* install the agent directly onto ubuntu image
* learn how to use automatic provisioning with vagrant to have it install by default
* create agent config file with tags
    * screenshot of dashboard
* update vagrant provisioner to install and run mongo
* update vagrant provisioner to include a script that sends random data
* update interval, probably in python script that sends checks
* bonus: update interval outside of script, probably in some config file or through datadog site

## Visualizing Data

* create timeboard using a script
* mess around with timeboard inthe dashboard
* bonus: answer what the anomoly grpah does

## Monitoring Data
* create metric monitor
* make it send a dynamic email
    * screenshot of email
* bonus: limit emails to work hours

## Collecting APM Data
* link agent to flask api
* bonus: What is the difference between a Service and a Resource?

## Final Question
Is there anything creative you would use Datadog for? 
Abstract out what the primary purposes of Datadog are
* tracking live activities that update often
* things that have triggers that you want to know baout but not watch constantly
* difficult to see all objects in system (contrained by time, quantity, etc)

grocery stores/shopping lists, resources in libraries, meeting rooms in office