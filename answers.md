Your answers to the questions go here.

DataDog Hiring-engineers exercise
Tim Franklin

What is the agent?
Software, when configured correctly and given permissions, can collect real-time information about infrastructure and applications.  This information is generally reported into a central repository, which can be viewed on a dashboard, or setup rules to alert when certain metrics need attention.


•	Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
[Screenshot](https://drive.google.com/file/d/0BwhhPKdA0TiuVlBpd2lTR2o3R2c/view?usp=sharing).  I didn’t see a ‘public link’ option so not sure you’re able to view [my Host Map Page](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=env&filter=env%3Adev&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false).


•	Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
MongoDB is installed along with the integrations.  [Screenshot](https://drive.google.com/file/d/0BwhhPKdA0TiuZlJ2RTI4NWVEbUU/view?usp=sharing)
 
•	Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check. [Screenshot](https://drive.google.com/file/d/0BwhhPKdA0TiuZDhOM1A2OTJ3Szg/view?usp=sharing) and [Public link to MongoDBClone dashboard](https://p.datadoghq.com/sb/f4f2ef945-9092fd3843)
 
 
•	Bonus question: What is the difference between a timeboard and a screenboard?
Timeboards are always scoped to the same time, more grid-like type of view and are more useful for troubleshooting and correlation.
Screenboards are far more customizable and great for getting a high-level view into a system.  Easily created with drag-and-drop widgets, which can each have a different time frame.


•	Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification [Screenshot](https://drive.google.com/file/d/0BwhhPKdA0TiuNXE1ZUhnMGVfVEk/view?usp=sharing)
 
 
•	This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you. [Screenshot of email](https://drive.google.com/file/d/0BwhhPKdA0TiuWjZJUmcwMG45emM/view?usp=sharing) and [public link to MongoCustom dashboard inside email](https://p.datadoghq.com/sb/f4f2ef945-9092fd3843)
 
 
•	Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification. [Screenshot](https://drive.google.com/file/d/0BwhhPKdA0TiuZ2QwcTlaMTdnVWM/view?usp=sharing)
 



