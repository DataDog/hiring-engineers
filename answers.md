Intro
This project is my demo of Datadog.  I used Docker (with compose) to set up my infrastructure.  My containers of choice were the offical Datadog agent (Alpine) container and the offical MySQL (Debian) container from dockerhub.  My repo contains everything needed to run the demo with the given pre-requisite that you will have Docker (with compose) installed already and run this on a Linux machine with bash, Ubuntu ideally.  I ran this on an Ubuntu 16.04.3 LTS VM (a.k.a worked on my machine).  A make file was written to simplify recreating the demo.  If you want to recreate it please do the following:

1.  git pull my branch
2.  cd into the ./demo/ folder
3.  make it_just_work

The one make command will take your Datadog API key, set up new MySQL creds, build and then start the containers.  Enjoy!


Level 1 - Collecting Data

What is an agent?

Agents are software programs that act on behalf of (and/or communicate with) another party, operating in a primarily autonomous manner in regards to a specific purpose or purposes. Agents are usually designed to be consume limited resources and ideally support extensible functionality.

So we've covered the definition of an agent but this will not likely bring the average user closer to understanding what an agent is.  Let’s look at some examples of agents and backtrack to the definition.  Running an antivirus is a common place to find an agent.  If you have a backup solution that pushes your data to the cloud, that will have an agent.  If you monitor your cloud infrastructure with a service like Datadog, you are running an agent.  

All of these examples are programs that are expected to do specific things like scan for viruses, check for new files or send report server metrics.  Your antivirus doesn't expect you to scan each file yourself, your backup solution doesn't expect you you to add upload each new file by hand and Datadog certainly doesn't expect you to manually push your metrics. These agents are designed to run in the autonomously in the background on your machine on behalf of your antivirus, backup provider and server monitor.

So agents are automated programs with specific purposes but having a specific purpose does not mean it can't be extensible too.  For example the Datadog agent provides several specific purposes including (but not limited to) sending your server metrics to Datadog's infrastructure.  You can write custom datadog checks and integrations to extend what you can monitor with the Datadog agent.  The agent's purpose is to monitor and report metrics but what you monitor and report on is the extensibility of the agent. Here is just some of the integrations offered by Datadog:

INTEGRATIONS SCREENSHOT HERE 

So that is what an agent is.  As a side note, a good agent should ideally be lightweight as well.  How lightweight is the Datadog agent?  Using the official Alpine datadog-agent container consumed about 78.98 MiB of RAM and less than 1% CPU at idle.  This is extremly small by today's computing standards.

ALPINE DATADOG USAGE SCREENSOT HERE


Level 2 - Visualizing your Data

Level 3 - Alerting on your Data
