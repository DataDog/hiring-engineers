My Answers
==========

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat
)](https://www.python.org)
[![Module](https://img.shields.io/badge/module-pygame-brightgreen.svg?style=flat
)](http://www.pygame.org/news.html)
[![Release](https://img.shields.io/badge/release-v1.0-orange.svg?style=flat
)](http://www.leejamesrobinson.com/space-invaders.html)

About Me
--------
Add information about me here.... Love for gaming, running, reading, technology :D

<img src="http://i.imgur.com/u2mss8o.png" width="360" height="300" />
<img src="http://i.imgur.com/mR81p5O.png" width="360" height="300"/>

What I build
------------
 - I used a containerized approach as it is easy to setup and consumes less laptop resources
 - I used the following dockerfile for spining up the necessary machines for this test:
    + Postgres (Database Machine)
    + Adminer (Managing Database)
    + Datadog Agent (Monitoring Agent)
 
 If you don't have [Python](https://www.python.org/downloads/) or [Pygame](http://www.pygame.org/download.shtml) installed, you can simply double click the .exe file to play the game.
   **Note:** *The .exe file needs to stay in the same directory as the sounds, images, and font folders.*
   
 - If you have the correct version of Python and Pygame installed, you can run the program in the command prompt / terminal.
 ``` bash
cd SpaceInvaders
python spaceinvaders.py
 ```
 **Note:** If you're using Python 3, replace the command "python" with "python3"

Demo
----
[![Space Invaders](http://img.youtube.com/vi/_2yUP3WMDRc/0.jpg)](http://www.youtube.com/watch?v=_2yUP3WMDRc)

Notable Forks
----
- [AI research project where four types of agents control the ship and play the game](https://github.com/scott-pickthorn/Space_Invaders)
- [NEAT program that evolves to beat the game](https://github.com/lairsonm/neat-in-space-invaders)




Collecting Metrics:
-------------------
- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

- Change your check's collection interval so that it only submits the metric once every 45 seconds.

- Bonus Question: Can you change the collection interval without modifying the Python check file you created?
Yes, from the agent code we can see the following:

try:
                min_collection_interval = instance.get('min_collection_interval', self.min_collection_interval)

                now = time.time()
                if now - self.last_collection_time[i] < min_collection_interval:
                    self.log.debug("Not running instance #{0} of check {1} as it ran less than {2}s ago".format(i, self.name, min_collection_interval))
                    continue

If it is greater than the interval time for the Agent collector, a line is added to the log stating that collection for this script was skipped. The default is 0 which means it’s collected at the same interval as the rest of the integrations on that Agent. If the value is set to 30, it does not mean that the metric is collected every 30 seconds, but rather that it could be collected as often as every 30 seconds.

The collector runs every 15-20 seconds depending on how many integrations are enabled. If the interval on this Agent happens to be every 20 seconds, then the Agent collects and includes the Agent check. The next time it collects 20 seconds later, it sees that 20 is less than 30 and doesn’t collect the custom Agent check. The next time it sees that the time since last run was 40 which is greater than 30 and therefore the Agent check is collected.




Contact
----
Thanks for checking out my game and I hope you enjoy it! Feel free to contact me.

- Lee Robinson
- lrobinson2011@gmail.com
