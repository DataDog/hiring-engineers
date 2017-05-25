Table of contents
=================

- [Level 0 - (optional) Setup an Ubuntu VM](#level-0)
- [Level 1 - Collecting your Data](#level-1)
- [Level 2 - Visualizing your Data](#level-2)
- [Level 3 - Alerting on your Data](#level-3) 



## Level 0 - (optional) Setup an Ubuntu VM

I opted to use the windows agent and not the Ubuntu VM using Vagrant for a few reasons. Firstly i was curious to see how well the cross compatibility of Datadog agent was. 
Secondly there were some teething issues with setting up Vagrant, as Vagrant requires virtual box to operate and for the virtual box to operate it requires that virtualisatoin on the CPU be turned on which is done through the bios as not all machine have it turned on by default. I did an initial attempt but I was unable to access the bios as the documentation for my laptop was incorrect so I left it and proceeded with the rest of the tasks as this task was only optional.

## Level 1 - Collecting your Data

  * Signing up for Datadog was quite simple. Once I filled out the form I was taken to the agent integration page. Here I selected the agent for windows and downloaded it and then installed it. Once the agent was installed it required a api key to finish the setup and to begin sending data. Unfortunately I was unable to easily get the api key as it required going to the integration api page which was not possible until Datadog received a confirmation from the agent. I able to get the api key by typing the URL to the integration api page. Once the agent confirmation was obtained I was free to begin browsing the site. 

  * An agent is a program which is installed on a host and has 3 functions, the collector, dogstatd, and the forwarder.
    - The collector is responsible for gathering various system metrics from the host machine it is installed on, as well as running the checks for each integrations installed for that host.
    - Dogstatd is local api server that allows you to send custom metrics from your applications to Datadog.
    - The forwarder is responsible for gathering all the collected data from both the collector and dogstatd and then queueing it to be sent to Datadog.

  * Custom tags setup in the agent config ![custom_host_tags](images/custom_host_tags.png). 

    Custom tags in the hostmap in Datadog ![custom_tags_from_agent](Custom_tags_from_agent.png).

  * I installed the database integration for Microsoft SQL Server as I had it already installed on my machine. The documentation [here](https://app.datadoghq.com/account/settings#integrations/SQL_server) was very helpful, it provided SQL scripts for creating a Datadog SQL account and granting permission to the account. Configuring the agent was simple, though I had a minor issue with the yaml configuration file initially but after removing the comments to make sure the formatting was correct it began to work properly. Below is the screen shot of the final working yaml file.
  
  ![SQL_server_agent_config](images/SQL_server_agent_config.png)

  * Writing a agent check was quiet simple. The documentation on agent checks found [here](http://docs.datadoghq.com/guides/agent_checks/) was quite good. After reading it i wrote the agent check that generates a random number and sends the result as a metric as well as a custom tag.

## Level 2 - Visualizing your Data

  *
https://app.datadoghq.com/dash/292968/SQLserver--test-agent--overview?live=false&page=0&is_auto=false&from_ts=1495582671070&to_ts=1495582971070&tile_size=s

  * 
   - TimeBoards have all their graphs scoped to the time selected in the show drop down box. Also all graphs a displayed in a grid-like fashion and each graph can be share individually.
   - ScreenBoards are more flexible and are made up of widgets which can be drag and dropped in. Each graph can be set to a different time frame. ScreenbBoards can also can be share as a whole and\or as a read only entity.

  *
https://app.datadoghq.com/event/stream?tags_execution=and&show_private=true&per_page=30&aggregate_up=true&use_date_happened=false&display_timeline=true&from_ts=1494990000000&priority=normal&is_zoomed=false&status=all&to_ts=1495594800000&is_auto=false&incident=true&only_discussed=false&no_user=false&page=0&live=true&bucket_size=10800000#

 https://help.datadoghq.com/hc/en-us/articles/203038119-What-do-notifications-do-in-Datadog-

## Level 3 - Alerting on your Data


https://app.datadoghq.com/monitors#2123423/edit  - link to the metric setup

  * After reading the documentation found (here)[http://docs.datadoghq.com/guides/monitors/], I was able to setup a monitor to the specifications of the task and began receiving notifications. After a while I muted the monitor so that my email would stop receiving notifications. I then setup the down time in the as specified and after reading the portion on setting up the monitor down time. Just before 7pm I unmuted the monitor and began receiving emails again. While I received the email notification of the down time being activated and seeing that there was a mute applied to the monitor with a time to expiration I still continued to receive notification. At this point I'm not sure what I may have missed in the setup and I'm going back over the documentation and doing google searches to see what I can find. 


  * Below is a screen shot of the monitor setup
  	![monitor_setup](images/monitor_setup.png) 

  * Below is a screen shot of the monitor down time setup
  	![monitor_down_time_setup](images/monitor_down_time_setup.png)

  * Below is a screen shot of the email notification of threshold breach for the agent check I created
	![email_alert](images/email_alert.png)

  * Below is screen shot of the email notification of the scheduled down time.
	![email_notification_of_down_time](images/email_notification_of_down_time.png)

