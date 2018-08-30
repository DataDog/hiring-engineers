Your answers to the questions go here.
# Prerequisites - Setup the environment
You can utilize any OS/host that you would like to complete this exercise. 
>Answer I am using both the Ubuntu via Vagrant and a Windows agent on my laptop so I can see the differences in setup and user experience.

>I am impressed how easy this is with a single command 

<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/UbuntuAgentInstall.JPG" > 
  
>The Windows agent was also very simple with a quick setup wizard asking for the API string. I think it is great that with this API your agents report straight into the correct place. Other tools I have used have taken a lot more messing around to get the agents reporting in to the correct place. Some require DNS entries which can delay installs and need to include change control etc.

# Collecting Metrics:
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
>Answer I was having issues with the Ubuntu agent getting to the datadog.yaml to edit with permission denied and I was using a new laptop at home so a lot of settings weren't playing ball with the VM terminal, so I switched to the Windows agent editor and this was much quicker and very easy to use. This is often the best way to work around issues while onsite with customers. You can spend time and resolve the issue at a later date but getting things moving along within the time allotted is often best for the customer. 

<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/setting%20tagwingui.JPG" />

>here are the tags from the hostmap screen

<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/HostmapTags.JPG" >

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

>I have installed MongoDB on my Windows machine. I created the user on mongodb
<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/mongocreatuser.JPG" >

>I added a mongo check on the agent
<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/agentmongocheck.JPG" >

>and Mongo info is now on the host dashboard!😁
<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/mongodashboard.JPG" >

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
* Bonus Question Can you change the collection interval without modifying the Python check file you created?
>For all of the above points, I am no coder but I did find a very useful link on who all of this is done
https://docs.datadoghq.com/developers/agent_checks/
>This seems fairly straight forward for someone with coding skills but as it would take me a long time to run through it learning as I went I have left this for another time (should you give me the opportunity to get learning from within DataDog 😉)

# Visualizing Data:

>Here I can see the previous sections needs to be done and further scripting so I have instead used this time to have a play with dashboards, creating graphs, alerts and generally looking around.
>I found that the deshboards look great and can easily be edited and clone for any user or view required. One thing that my previous employers product always struggled with was making their creat dashboards so easily customisable and also work on big screen which are commonly used in NOCs and SOCs.
>I also saw how easy it was to creat alerts from items you see in graphs from dashboards. I pick one and had an alert running in no time.
<img src="https://github.com/Rusk-Hill/Datadogscreenshots/blob/master/alertsetup.JPG" >




# Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
