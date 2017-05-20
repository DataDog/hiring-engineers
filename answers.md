Your answers to the questions go here.

Level 0 (optional) - Setup an Ubuntu VM

While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.

[Bruce] - Please see the two below screenshots showing the "vagrant status", along with the Ubuntu VM running within Virtual Box:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Vagrant%20Status.png)

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Virtual%20Box%20Showing%20VM%20Running%20.png)

Bonus question: In your own words, what is the Agent?  [Bruce] - The agent is a python process that runs on a given host and monitors resources, applications, etc... on that host by executing a series of "checks".  The agent then sends the collected information from these checks to the Datadog cloud to in order to monitor your entire infrastucture with an emphasis on meeting performance SLAs.

Bonus question: What is the difference between a timeboard and a screenboard? [Bruce] - With TimeBoards, all widgets/panels on a dashboard are always based on the same moment in time.  ScreenBoards provide a high-level view of a system and are very customizable, and each widget/panel can have different windows of time.

Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up. [Bruce] - Done.

Helpful Links:

https://app.datadoghq.com/dash/285620/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1494216838779&to_ts=1494220438779&tile_size=m

https://app.datadoghq.com/monitors#/downtime

https://app.datadoghq.com/metric/summary

https://app.datadoghq.com/dash/list

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/My%20host%20and%20its%20tags%20on%20the%20Host%20Map%20with%20MySQL.png)
