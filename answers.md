## Hi Datadogs! I've reached a point in the assessment where I think I just don't quite have the tools to move forward. I still thought I'd show you my work up to this point, so you can see what I've been working on.

So, I tried doing this is Linux using the Vagrant VM and made very slow progress, so I decided to start over using my good ol’ Mac OS.

Setting up the agent: ![Agent setup](http://res.cloudinary.com/emilymarro/image/upload/v1524253278/agent_running.png)

The first metrics: ![First Metrics](http://res.cloudinary.com/emilymarro/image/upload/v1524253278/first_metrics.png)

Adding tags in the config file: ![Config](http://res.cloudinary.com/emilymarro/image/upload/v1524253279/config_file_tags.png)

These tags didn't show on the host map, so for now I’m going to just add tags on the host map itself.
![host map](http://res.cloudinary.com/emilymarro/image/upload/v1524253279/Screen_Shot_2018-04-17_at_5.39.45_PM_kn73xy.png)

They disappear a few moments after I enter them! Looking into the documentation...

Stopped the agent, and on the activity monitor forced data dog to quit. When I restarted, information was sending, but I kept getting the message: "There was an error querying the ntp host: read udp 192.168.1.3:65152->45.33.84.208:123: i/o timeout”

So I did what any professional does and just left it alone for a few hours, then came back and the agent was magically working again.

Is this how the tags should be displayed on the host map? Only having one host looks terribly sad.
![hostmap](http://res.cloudinary.com/emilymarro/image/upload/v1524253280/tags_host_map.png)
![hostmap2](http://res.cloudinary.com/emilymarro/image/upload/v1524253279/Screen_Shot_2018-04-17_at_3.44.18_PM_hga4rh.png)

##POSTGRESQL

Postgresql installed. 
Configure the Agent to connect to the PostgreSQL server : waited 5 minutes, then restarted Agent. (I’m curious about whether the changes need to be pushed up before I restart, and if I can cue that somehow instead of waiting?)

As per the instructions, I’m trying to execute the info command and verify that the integration check has passed.

![Info Check Instructions](http://res.cloudinary.com/emilymarro/image/upload/v1524253762/info_check.png)

Here, the agent keeps getting stuck in a loop of running checks over and over, and only very occasionally can I interrupt this loop with a command. I also have the world's slowest terminal, so opening a new tab and running commands there isn't going much more quickly. I usually wind up closing the terminal session completely and restarting the agent. I did connect to the web GUI, and in there I tried to “add a check” since I couldn’t run an info check from the command line. This results in a message that "an error has occurred" and terminates the agent session, so I've started it up again.
![Error has occurred](http://res.cloudinary.com/emilymarro/image/upload/v1524253933/check_error.png)

My question at this point is: should I continue doing as much of this assessment as I can without being sure if I’m doing things correctly? 

So, being unable to run the info check on the Agent, I’ve decided to go with the assumption that everything is working and proceed. ![postgresql](http://res.cloudinary.com/emilymarro/image/upload/v1524254747/postgresql_installed.png)

The next step is running a custom Agent check called my_metric. On the GUI, I can’t add a check without the Agent crashing, and I’m unsure how to run one from the command line. Is this a piece of code I’m supposed to write in a Ruby file somewhere? 

I’ve been stuck here for a while, because the  rest of the assessment seems to rely on having my_metric set up.

