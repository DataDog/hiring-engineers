# Level 1

#### Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

#### Bonus Question: In your own words, what is the Agent?
>The Agent is software that runs on hosts and is used to bring metrics and events to the Datadog application.

#### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
>I had to dig around on the documentation to figure out which file I was specifically going to need to work with.  Once found, I searched for the section on tags and made the neccecary changes to add custom tags.  I then restarted the Datadog agent and made sure the tags were able to be seen and searched for on the Host Map.
![syntax for tags in config files](https://i.imgur.com/1WUfRdN.png "syntax for tags in config files")
![Agent tag configurataion set up](https://i.imgur.com/nmjtp8Y.png "Agent tag configuration")
![Host Map w/ Tags](https://i.imgur.com/vhHc73u.png "Host Map w/ Tags")

#### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
>I decided to use Mongodb which is an entirely new DB to me. I ran into a ton of issues however.  I used homebrew to intall Mongo but it did not have the proper permissios for me to actually create the directory that I needed to be able to use the shell.  I had to run the command shown below inorder to get the server running/create the directory/open the shell.
![Savior Command](https://i.imgur.com/GIwo5oq.png)

>Once I had the server and shell working correctly I created a user and verified that it was in the database, installed the integration and made sure the agent could see Mongo.  The agent could see Mongo because I change the name of mongo.yaml.example to just mongo.yaml, then followed the instructions on the Datadog Mongo integration page.
![Mongo configuration set up for the user created in the database](https://i.imgur.com/3TUUXkM.png)
![User I created in database](https://i.imgur.com/IKjmcAy.png)

>Before configuration:
![the agent can see Mongo even though I hadn't configured it yet](https://i.imgur.com/qRDIfCO.png)


>I then restarted the Datadog Agent and ran a status check and the agent could see the instances of Mongo!
After configureation:
![the agent status after configuration](https://i.imgur.com/N8rVtuG.png)

>I then verified that Mongo was appearing as being successfully integrated.
![verification that mongo is integrated](https://i.imgur.com/8rIFbkH.png)
![more verification on the Host Map](https://i.imgur.com/j5RW7gO.png)


>This part was challenging because I have never worked with Mongo before so I had to learn how to set everything up and then learn how to integrate it with the Datadog agent.


#### Write a custom Agent check that samples a random value. Call this new metric: ```test.support.random```

>Having never worked really worked with Python was a concern for me heading into this challenge but the documentation for building Custom Agent was very helpful along with some googling of course.  I mostly used [BUILDING A CUSTOM AGENT CHECK (HANDS ON INSTRUCTIONS)](https://datadog.github.io/summit-training-session/handson/customagentcheck/).  This gave me the methods and basic structure that the check would be in and I had to figure out what to use where.

>After much trial and error I was able to get the check to appear in ```datadog-agent info``` but it was telling me that random was not a defined and had to figure out what/how to import.
!['random' not defined error](https://i.imgur.com/OpViY4e.png "random not defined error")

>Adding ```from random import random``` allowed me to use random and the check passed. 
![Successful custom check passing](https://i.imgur.com/MbO1bmt.png "Successful custom check passing")

>The code I used for the random check looked like this(```randomCheck.py```):

```
from random import random
from checks import AgentCheck
class TestSupportRandom(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random())
```


>The code for the configuration file(```randomCheck.yaml```):

```
init_config:

instances:
    [{}]
```

>The test showed on the Host Map and on in the Metrics Summary page when searched for.
![Test working on Host Map](https://i.imgur.com/4A1EZf4.png "Test working on Host Map")
![Test metric showing up when seached for in Metric Summary](https://i.imgur.com/Qc9FTWI.png "Test metric showing up when seached for in Metric Summary")


# Level 2

#### Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

>Screenshot of the cloned dashboard.  The ```test.support.random``` check is added as well as ```systme.cpu.user``` and ```system.net.bytes_sent```.
![Cloned dashboard with custom metrics added](https://i.imgur.com/E45BDqn.png "Cloned dashboard with custom check and other metrics added")

#### Bonus question: What is the difference between a timeboard and a screenboard?
>**Timeboards** have all the data scoped to the same time and appear in a grid-like fashion for easy troubleshooting/collaberation. Graphs from a Timeboard can all be shared individually.

>**Sceenboards** are a lot more customizable and good for getting a high-level look at the system. Each widget can have a different time frame scoped and the board can be shared as a whole with live with a read-only entity unlike Timeboards which cannot. 

#### Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

>I found a tutorial in the docs for taking a snapshot and sending it to someone [here](https://www.datadoghq.com/blog/real-time-graph-annotations/)
![Snapshot of test.support.random metric](https://i.imgur.com/f6fFwqk.png)




