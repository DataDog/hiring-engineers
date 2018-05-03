This is my second (well, third) attempt. I tried doing this assessment with a Vagrant Ubuntu, but got intimidated and started over with Mac. That ran into a lot of issues (see my former pull request below) and now I’ve gotten a better understanding of how Vagrant and VirtualBox work, and am trying the original way again!

Lesson learned the hard way: install updates. Always. I kept trying to do this assignment but would get stuck and stop because my terminal was so slow and unresponsive that I could barely get anything done. I finally updated my computer to MacOSHighSierra and suddenly my computer is running twice as fast - making running commands on the CLI much easier. Rookie mistake! 

Reinstalled VirtualBox.

Was confused about the order of operations last time. Now I understand that vagrant init installs a Vagrantfile. To open up the Vagrant VM, you type "vagrant up” to start the virtual machine, and “vagrant ssh” to start the session.

when trying to use vagrant ssh, got this message: ![Timeout]()

found some help on stack overflow: {stacko_timeout} ![stacko_timeout](http://res.cloudinary.com/emilymarro/image/upload/v1525382743/stacko_timeout_fosyjj.png)

I’m hesitant to hunt down where config is because: ![scared] (http://res.cloudinary.com/emilymarro/image/upload/v1525382742/scared_because_z1hntx.png) 

So I followed some different advice, and uninstalled and reinstalled VirtualBox.

To uninstall VirtualBox, I followed the steps I found on this page (I wish everything was written as well as these directions!): https://nektony.com/how-to/uninstall-virtualbox-on-mac

Restarted Vagrant, logged into the Datadog agent. ![RESTARTEDAGENT](http://res.cloudinary.com/emilymarro/image/upload/v1525382742/restarted_agent_r51j5c.png)

Attempting the psql part of this, though sql already has a user named “data dog” and I don’t have permission to remove the user.  

Where is my config file??? there is no et/dd-agent/, but I found datadog-agent/conf.d/postgres.d, and in that is only the example file.  

I guess I’ll touch a new postgres.yaml file and copy in the contents of the example? But I don’t have permission. Where do I set my permissions for this? 

To reiterate, the problem is that I should be able to edit conf.d/postgres.yaml, but that file doesn’t exist and I don’t have permission to touch a new file. This step: doesn’t work to give me permissions!

I used sudo to touch a config file, but I can’t open it because of the MIME type. ![no_mimetype](http://res.cloudinary.com/emilymarro/image/upload/v1525382741/no_mimetype_fwj8yf.png)

Trying to edit the config file in the command line with vi, but can’t figure out if my changes are being saved. I’ve tried :i, :q, nothing really responds.

I’ve been trying to figure this out but I’m not having any luck, so I’m going to move on to the next part of the assessment.


————————
Very grateful for the dev who wrote this: https://datadog.github.io/summit-training-session/handson/customagentcheck/. I suddenly understand how to look up what I need 

agent: created my_metric. Found useful vi command line info and figured it out a little more! Hallelujah!

created my_metric.yaml: ![init_config] (http://res.cloudinary.com/emilymarro/image/upload/v1525382741/initconfig_yoj10l.png)
![initconfig] (http://res.cloudinary.com/emilymarro/image/upload/v1525382741/initconfig_myfile_gg96xg.png)

my vagrant froze, so I restarted it, and now I can’t find my datadog-agent folder. I’m reinstalling/restarting the agent, got the datadog-agent folder back, but the my_metric.yaml file is no longer there. Did it disappear when I restarted the agent?

This is probably a good thing, because I realized I didn’t insert the code correctly in the file earlier. ![my_metric](http://res.cloudinary.com/emilymarro/image/upload/v1525382742/mymetric_tyj1wg.png)

I was able to change the check by editing the my_metric.yaml file: ![45_sec](http://res.cloudinary.com/emilymarro/image/upload/v1525382740/45seconds_to7df7.png)

BONUS: I'm not sure if I did it correctly, but I changed the .yaml file, not the .py file to adjust my metric.
——————

VISUALIZING DATA

Inserted API and APP keys in datadogpostman file ![find_replace](http://res.cloudinary.com/emilymarro/image/upload/v1525383510/find_replace_jfambc.png)

Using the API in Postman seems pretty straightforward, but I can't find my_metric in the list of all active metrics. Why is this? I created a timeboard anyway.

Applying the anomaly function: ![anomaly](http://res.cloudinary.com/emilymarro/image/upload/v1525382740/anomaly_alert_p6b9ox.png)

MONITORING DATA
I'm setting up an alert for my_metric even though I can't find it on the active metric list by editing the source tab:
![source_metric](http://res.cloudinary.com/emilymarro/image/upload/v1525382740/source_metric_zpghlk.png)

Here are the downtimes: ![downtime 1](http://res.cloudinary.com/emilymarro/image/upload/v1525382740/downtime1_mqcvpi.png)
![downtime 2](http://res.cloudinary.com/emilymarro/image/upload/v1525382741/downtime2_scet66.png)

This is pretty much as far as I've gotten. I'm very unclear about what an APM is/does, and since I'm still missing some pieces up until now, I think it might be best to pause here.

As for the final question: I think we could use datadog to assist a host at a restaurant, with stats about how long a table has been seated, what course they're on, etc. It could let the host know when the table's entrees have been cleared, whether or not they're getting dessert, etc, to estimate how much longer the table will be seated and how long until people waiting for that table can expect to wait.




























_______ This is my first attempt, fo reference:_________
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

