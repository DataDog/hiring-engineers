Hello

I will answer the questions first, then I will explain all my screenshots.

In your own words, what is the Agent?

I think of it as a data/systems observation control center. It monitors databases and systems in such a detailed way that allows users to make targeted changes when something is going wrong or want to see different results. It takes a little while to get used to, but once I learned where to look for certain controls it became almost as simple as looking at heads up displays (popular in video games where the pertinent information for the player is readily accessible by glancing around the screen). The Agent is a pretty clean way to break down monitoring all the measurable aspects of anyone trying to develop something. 

What is the difference between a timeboard and a screenboard?

They are different ways of organizing how data will be displayed on dashboards. The timeboard pulls data from a certain time frame; I really enjoyed seeing my mysql data this way. It seemed like the best way to see if at certain times the loads get too heavy or if something bad is happening right then all the information is readily available. In general, I think if less system critical data needed to be displayed, and the dashboard creator wanted to draw the eye to some pieces of data, the screenboard would be more useful. Screenboards are customizable, drag and drop dashboards.  I think screenboards are more visually interesting, since it allows for more emphasis to be put on different metrics. 


![screenshot from 2016-06-25 02 40 21](https://cloud.githubusercontent.com/assets/8127034/16355440/cb2df5ba-3a84-11e6-9dfe-f51f9a0831d8.png)

Host Map with tags 
https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false




![screenshot from 2016-06-25 02 42 00](https://cloud.githubusercontent.com/assets/8127034/16355465/588f9788-3a85-11e6-98a0-bdf627094b22.png)

The right terminal is where I entered tags that are visible in the host map. The left terminal is my custom Agent check to sample random numbers. 



![screenshot from 2016-06-25 02 32 59](https://cloud.githubusercontent.com/assets/8127034/16355513/71900a64-3a86-11e6-93c5-755fd1b5425f.png)

Database metrics with the random sampling metrics. 
https://app.datadoghq.com/dash/152147/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1466836849488&to_ts=1466840449488&tile_size=m


![screenshot from 2016-06-25 02 48 04](https://cloud.githubusercontent.com/assets/8127034/16355523/d4e2476c-3a86-11e6-959c-2129a73aab21.png)

This is the only thing I wasn't sure about. I never got this snapshot in my email, but I also think this is the way to send a notification to someone's email. Maybe the comment emails don't come in the middle of the night?



![screenshot from 2016-06-25 03 45 19](https://cloud.githubusercontent.com/assets/8127034/16355537/4cb3b2a8-3a87-11e6-9e39-8544d8075389.png)
Monitor alert triggered for the random value going above .9
https://app.datadoghq.com/monitors#/triggered





![screenshot from 2016-06-25 03 36 15](https://cloud.githubusercontent.com/assets/8127034/16355561/ee2e0070-3a87-11e6-8b36-92fe325d3987.png)

Downtime email after I set the 7pm-9am downtime. 
https://app.datadoghq.com/monitors#downtime?id=186731953

Thanks for considering me and for the assignment to play with. It was fun and interesting.

-Stefaney








