##Level 1 – Collect your data


**Bonus question: In your own words, what is the Agent?**
The Datadog agent is a program that runs on your host machine and monitors performance (CPU and memory usage) as well as events. The user can also specify custom metrics to allow the agent to keep track of. This is then all sent over by the agent to the Datadoghq site where the metrics are put to use.

Add tags in the Agent config file:
![tags](https://cloud.githubusercontent.com/assets/4193161/18540832/5feb86cc-7aef-11e6-89cf-7ff555504933.png)


Screenshot of host and its tags on the Host Map page in Datadog:
![hostmap](https://cloud.githubusercontent.com/assets/4193161/18540876/a9c80cf2-7aef-11e6-975d-130b34fabf13.png)


Install a database on your machine (MySQL) and then install the respective Datadog integration for that database.
![datintegration](https://cloud.githubusercontent.com/assets/4193161/18540896/c93aaf0e-7aef-11e6-8c86-b995020ac30a.png)

Write a custom Agent check that samples a random value. Call this new metric: test.support.random
random.py code that will send a random number to agent:
![random](https://cloud.githubusercontent.com/assets/4193161/18540916/ec409e8c-7aef-11e6-9d42-f1081dc34814.png)

random.yaml put in config folder conf.d:
![yaml](https://cloud.githubusercontent.com/assets/4193161/18540920/ef89d8ba-7aef-11e6-8c00-3f82f76cd7be.png)






##Level 2 – Visualize your Data 
Attached is an image showing a timeboard with the cloned information fom the database metrics as well as other metrics including the random test. Also attached is an image of a Screenboard test. 
![timeboard](https://cloud.githubusercontent.com/assets/4193161/18540986/49b7499e-7af0-11e6-8c6b-9c4ffbdfa792.png)
![screenboard](https://cloud.githubusercontent.com/assets/4193161/18540990/4f92370c-7af0-11e6-933e-9aa1425f6a63.png)


**Bonus question: What is the difference between a timeboard and a screenboard?**
>TimeBoards and ScreenBoards are two different ways that Datadog allows the user to visualize and encapsulate their data. >With a TimeBoard the metrics are all synchronized and showing their data for the same time. This is useful for getting a >look at all the relevant information of a system and the grid like representation of the data makes this a strong >troubleshooting and correlations board. A ScreenBoard is much freer and more customizeable than a TimeBoard. With a >ScreenBoard you get the feeling of having a pushboard where you can pin relevant information and keep track of everything on >a much higher level. While ScreenBoards can be shared as a whole, TimeBoards can only share individual graphs.

snapshot of test.support.random graph / draw a box around a section that shows it going above 0.90:
![snapshot](https://cloud.githubusercontent.com/assets/4193161/18541013/7b1d681a-7af0-11e6-895f-c4c34a6438f2.png)

Make sure this snapshot is sent to your email by using the @notification
![notification](https://cloud.githubusercontent.com/assets/4193161/18541017/7d75e8bc-7af0-11e6-895a-ec04f258dad7.png)


##Level 3 – Alerting on your Data

Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes. This is a multi-alert by host. (had to change the average to at least once)
![monitor](https://cloud.githubusercontent.com/assets/4193161/18541037/ac4cf22a-7af0-11e6-9dfd-8aa4a722d428.png)

Email alert from monitor:
![alert](https://cloud.githubusercontent.com/assets/4193161/18541040/afbfb14a-7af0-11e6-816d-e7e85b2972f0.png)
Scheduled Downtime on Monitor:
![downtime](https://cloud.githubusercontent.com/assets/4193161/18541046/b579477c-7af0-11e6-9ede-3586a536f400.png)


