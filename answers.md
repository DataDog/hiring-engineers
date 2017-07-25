Level 0 (optional) - Setup an Ubuntu VM

•While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.

Configuring the vagrantfile - screenshot 
https://user-images.githubusercontent.com/20803455/28546549-16eb05d8-7099-11e7-9b5d-bcfc372bf019.png

Starting the ubuntu VM startup - screenshot 
https://user-images.githubusercontent.com/20803455/28546550-16f28952-7099-11e7-941f-e39c27a61622.png

Level 1 - Collecting your Data

•Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

•Bonus question: In your own words, what is the Agent?

Simply put, the agent is a piece of communication software that is installed on a host. The agent is responsible for securely reporting whatever metrics is required of it to the datadog platform. The agent is fully customizable in that it can grab information from a script (in the case of the random number exercise) or from a multitude of supported integrations. In the example I used for this exercise, I setup postgresql on the server, a user for datadog within the instance and the correct grants for access. Once the yaml for that specific monitor was activated with the correct configuration, a variety of different postgresql specific metrics were available in the datadog platform.

•Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Configuring the tags in datadog - screenshot https://user-images.githubusercontent.com/20803455/28546548-16e9d5f0-7099-11e7-8fd1-30b33285f36a.png

Infrastructure host map grouped by tags - screenshot https://user-images.githubusercontent.com/20803455/28546546-16e6a86c-7099-11e7-833a-ce2dd243786c.png

•Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Installing postgresql database using apt- Level 0 (optional) - Setup an Ubuntu VM

•While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.

Configuring the vagrantfile - screenshot 
https://user-images.githubusercontent.com/20803455/28546549-16eb05d8-7099-11e7-9b5d-bcfc372bf019.png

Starting the ubuntu VM startup - screenshot 
https://user-images.githubusercontent.com/20803455/28546550-16f28952-7099-11e7-941f-e39c27a61622.png

Level 1 - Collecting your Data

•Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

•Bonus question: In your own words, what is the Agent?

Simply put, the agent is a piece of communication software that is installed on a host. The agent is responsible for securely reporting whatever metrics is required of it to the datadog platform. The agent is fully customizable in that it can grab information from a script (in the case of the random number exercise) or from a multitude of supported integrations. In the example I used for this exercise, I setup postgresql on the server, a user for datadog within the instance and the correct grants for access. Once the yaml for that specific monitor was activated with the correct configuration, a variety of different postgresql specific metrics were available in the datadog platform.

•Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Configuring the tags in datadog - screenshot 
https://user-images.githubusercontent.com/20803455/28546548-16e9d5f0-7099-11e7-8fd1-30b33285f36a.png

Infrastructure host map grouped by tags - screenshot 
https://user-images.githubusercontent.com/20803455/28546546-16e6a86c-7099-11e7-833a-ce2dd243786c.png

•Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Installing postgresql database using apt-get - screenshot 
https://user-images.githubusercontent.com/20803455/28550511-51281298-70af-11e7-9df0-13b4f760bcc5.png

Installing the datadog-agent - screenshot 
https://user-images.githubusercontent.com/20803455/28546526-16aff628-7099-11e7-9a08-19bb5247d572.png

Configuring the user for monitoring the posgresql database - screenshot 
https://user-images.githubusercontent.com/20803455/28546543-16ddc26a-7099-11e7-8fb3-727dbbb154e0.png

Configuring the postgres.yaml to monitor postgresql database - screenshot 
https://user-images.githubusercontent.com/20803455/28546542-16d96922-7099-11e7-9885-2633ebc58b2c.png

Verifying the postgres database checks are enabled after restart - screenshot
https://user-images.githubusercontent.com/20803455/28546544-16df0e2c-7099-11e7-9ab5-d0ed637e3a49.png

•Write a custom Agent check that samples a random value. Call this new metric: test.support.random

Configuring random.yaml in /etc/dd-agent/conf.d directory - screenshot 
https://user-images.githubusercontent.com/20803455/28546527-16b0c846-7099-11e7-9d89-86a980dd0016.png

Authoring a random.py script to output a random value in /etc/dd-agent/checks.d - screenshot 
https://user-images.githubusercontent.com/20803455/28546525-16ae6baa-7099-11e7-9dcd-f85666d5cd49.png

Verifying that my custom agent check is enabled after agent restart - screenshot 
https://user-images.githubusercontent.com/20803455/28546528-16b3c03c-7099-11e7-9e53-537c50884f47.png

Here is a snippet that prints a random value in python:

import random print(random.random())

Level 2 - Visualizing your Data

•Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

Added custom postgresql metrics and test.support random to cloned dashboard - screenshot 
https://user-images.githubusercontent.com/20803455/28551385-b028bf80-70b5-11e7-9c77-885588915a82.png

•Bonus question: What is the difference between a timeboard and a screenboard?

Largest difference is in how much customization can be done. Timeboards are use metric graphs can be viewed for a given interval of time. The layouts of timeboards are automatic and can’t be customized that much. Usually timeboards are used for quick and dirty graphs to troubleshoot an issue. Screenboards allow for more customization, allowing for drag and drop of multiple widgets built on different metrics and time periods.

•Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Shapshot for data exceeding a threshold for random value being sent to myself - screenshot 
https://user-images.githubusercontent.com/20803455/28551385-b028bf80-70b5-11e7-9c77-885588915a82.png

Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

•Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

Configuring the monitor - screenshot 
https://user-images.githubusercontent.com/20803455/28546541-16d847cc-7099-11e7-9003-3ad5bb6b11b9.png

•Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

Configiring a multi-alert monitor - screenshot 
https://user-images.githubusercontent.com/20803455/28546540-16d7ff38-7099-11e7-9131-1f3cf2fff8c4.png

•Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

Monitor notification settings - screenshot
https://user-images.githubusercontent.com/20803455/28552592-3b5b51ba-70bd-11e7-9e34-43b80039a31c.png

•This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

Email the monitor produced - screenshot 
https://user-images.githubusercontent.com/20803455/28552888-b3bc0f40-70be-11e7-8806-f639f63e99aa.png

•Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Scheduled downtime from 7pm to 9am for the monitor - screenshot
https://user-images.githubusercontent.com/20803455/28546534-16ce5762-7099-11e7-833e-26c2bbbb1d94.png

EXTENDED Stuff - Docker Integration

Installing datadog agent on Docker Host https://user-images.githubusercontent.com/20803455/28546535-16cec58a-7099-11e7-9442-9e4a063dcd7a.png

Configuring the docker.yaml in /etc/dd-agent/conf.d https://user-images.githubusercontent.com/20803455/28546538-16d25ce0-7099-11e7-8515-6d494035e561.png

Verifying that the docker checks came up after agent restart 
https://user-images.githubusercontent.com/20803455/28546536-16cef83e-7099-11e7-8ef0-c575806ca560.png

Verifying the collection of metrics in datadog from the docker server 
https://user-images.githubusercontent.com/20803455/28546537-16cf4f3c-7099-11e7-88c2-ed5eca289ee1.png

Extended Stuff - VMWare VSphere Integration

Configuring the vsphere integration after agent install 
https://user-images.githubusercontent.com/20803455/28546554-16fa93d6-7099-11e7-896c-685a0b6fe085.png

Verifying the vshere checks came up after agent restart
https://user-images.githubusercontent.com/20803455/28546553-16f8b872-7099-11e7-9798-f80d2dd9f3bd.png

Verifying that vsphere host and managed esxi nodes appear in the infrastructure list
https://user-images.githubusercontent.com/20803455/28546552-16f793ac-7099-11e7-92eb-bb817bbcc2a7.png

Screenshot of metrics being collected from an ESXi host
https://user-images.githubusercontent.com/20803455/28546551-16f7a78e-7099-11e7-8b1d-3261d01dc518.png
