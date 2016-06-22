# Level 0
**Set up an xubuntu virtual machine for this challenge.**

<img src="http://i.imgur.com/Zr3nj6i.png" width="500" height="332" >


# Level 1
Bonus question: In your own words, what is the Agent?: **The Agent is a program that collects metrics and events from the system and its apps. This is then sent to Datadog.**

**Added the tag Algorithm:three and Algorithm:four.**


<img src="http://i.imgur.com/013yado.png" width="500" height="332" >


**Installed PostgreSQL.**


<img src="http://i.imgur.com/36FHAnu.png" width="500" height="332" >


**Wrote the custom Agent Check and stored it in the correct directory.**

**The Python file and directory**


<img src="http://i.imgur.com/IohQjlF.png" width="500" height="332" >


**The YAML file and directory.**


<img src="http://i.imgur.com/scTP90Y.png" width="500" height="332" >


# Level 2
**Cloned the database integration and added the `test.support.random` metric to it.**


<img src="http://i.imgur.com/7Gmim4c.png width="500" height="332">


Bonus question: What is the difference between a timeboard and a screenboard? **Timeboards have their graphs scoped to the same time, whereas Screenboards are flexible can be shared live, and can be created with drag and drop widgets which can each have a different time frame.**

**Snapshotted the `test.support.random` graph and drew a box where it surpasses 0.90.**


<img src="http://i.imgur.com/DNj4yy1.png width="500" height="332" >


# Level 3
**Added a monitor to alert when it surpasses 0.90 at least once every 5 minutes.**


<img src="http://i.imgur.com/zq6dW4m.png width="500" height="332" >


Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.: **Shown in the screenshot above.**

**An alert sent to an email.**


<img src="http://i.imgur.com/zNaaguY.png width="500" height="332" >


**The downtime information on the host.**


<img src="http://i.imgur.com/Z6eS4S8.png" width="500" height="332" >



