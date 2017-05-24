Table of contents
=================

- [Level 0 - (optional) Setup an Ubuntu VM](#level-0)
- [Level 1 - Collecting your Data](#level-1)
	* [Task 1](#task-1)
	* [Task 2](#task-2)
	* [Task 3](#task-3)
	* [Task 4](#task-4)
- [Level 2 - Visualizing your Data](#level-2)
	* [Task 1](#task-1)
	* [Task 1](#task-2)
	* [Task 1](#task-3)
- [Level 3 - Alerting on your Data](#level-3)
	* [Task 1](#task-1)
	* [Task 1](#task-2)
	* [Task 1](#task-3)
	* [Task 1](#task-4)
	* [Task 1](#task-5)



## Level 0 - (optional) Setup an Ubuntu VM

I oppted to use the windows agent and not the Ubuntu VM using Vagrant for a few reasons. Firstly i was curious to see how well the cross compatability of Datadog agent was. 
Secondly there were some teething issues with setting up Vagrant, as Vagrant requires virtual box to operate and for the virtual box to operate it requires that virtualisatoin on the cpu be turned on which is done through the bios as not all machine have it turned on by default. I did an initial attempt but I was unable to access the bios as the documentation for my laptop was incorrect so i left it and proceeded with the rest of the tasks as this task was only optional.

## Level 1 - Collecting your Data
1. Signing up for Datadog was quite simple. once i filled out the form
2. An agent is a program which is installed on a host and has 3 functions, the collector, dogstatd, and the forwarder.
    - The collector is responsible for gathering various system metrics from the host machine it is installed on, as well as running the checks for each integrations installed for that host.
    - Dogstatd is local api server that allows you to send custom metrics from your applications to Datadog.
    - The forwarder is responsible for gathering all the collected data from both the colloctor and dogstatd and then queueing it to be sent to Datadog.
3.  Custom tags setup in the agent config ![custom_host_tags](images/custom_host_tags.png). 
    Custom tags in the hostmap in Datadog ![Custom_tags_from_agent](Custom_tags_from_agent.png) 
4. I installed the database integration for Microsoft SQL Server as I had it already installed on my machine. The documentation [here](https://app.datadoghq.com/account/settings#integrations/sql_server) was very helpful, it provided sql scripts for creating a Datadog sql account and granting persmission to the account. Configuring the agent was simple, though I had a minor issue with the yaml configuration file initially but after removing the comments to make sure the formating was correct i was left with the below and it worked fine.
![sql_server_agent_config](images/sql_server_agent_config.png)
5. I found writing a agent check

## Level 2 - Visualizing your Data
1.
https://app.datadoghq.com/dash/292968/sqlserver--test-agent--overview?live=false&page=0&is_auto=false&from_ts=1495582671070&to_ts=1495582971070&tile_size=s
2. 
   - TimeBoards have all their graphs scoped to the time selected in the show drop down box. Also all graphs a displayed in a grid-like fashion and each graph can be share individually.
   - ScreenBoards are more flexable and are made up of widgets which can be drag and dropped in. Each graph can be set to a different time frame. ScreenbBoards can also can be share as a whole and\or as a read only entity.
3.
https://app.datadoghq.com/event/stream?tags_execution=and&show_private=true&per_page=30&aggregate_up=true&use_date_happened=false&display_timeline=true&from_ts=1494990000000&priority=normal&is_zoomed=false&status=all&to_ts=1495594800000&is_auto=false&incident=true&only_discussed=false&no_user=false&page=0&live=true&bucket_size=10800000#

 https://help.datadoghq.com/hc/en-us/articles/203038119-What-do-notifications-do-in-Datadog-

## Level 3 - Alerting on your Data

https://app.datadoghq.com/monitors#2123423/edit
1.
2.
3.
4.
5.

