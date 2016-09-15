##Level 1 – Collect your data


**Bonus question: In your own words, what is the Agent?**
The Datadog agent is a program that runs on your host machine and monitors performance (CPU and memory usage) as well as events. The user can also specify custom metrics to allow the agent to keep track of. This is then all sent over by the agent to the Datadoghq site where the metrics are put to use.

Add tags in the Agent config file:
![tags](https://cloud.githubusercontent.com/assets/4193161/18540832/5feb86cc-7aef-11e6-89cf-7ff555504933.png)


Screenshot of host and its tags on the Host Map page in Datadog:
![hostmap](https://cloud.githubusercontent.com/assets/4193161/18540876/a9c80cf2-7aef-11e6-975d-130b34fabf13.png)


Install a database on your machine (MySQL) and then install the respective Datadog integration for that database.
![datintegration](https://cloud.githubusercontent.com/assets/4193161/18540896/c93aaf0e-7aef-11e6-8c86-b995020ac30a.png)
#### I ran into some problems with the MySQL database integration, I followed the steps accordingly and edited the necessary files but the agentkept returning this erorr in the checks
![mysql error](https://cloud.githubusercontent.com/assets/4193161/18567020/4564a958-7b64-11e6-8c51-1ceff5128781.PNG

Write a custom Agent check that samples a random value. Call this new metric: test.support.random
random.py code that will send a random number to agent:
```python
import random
from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
#built using hello.world example on http://docs.datadoghq.com/guides/agent_checks/
```

random.yaml put in config folder conf.d:
```yaml
init_config:
min_collection_interval: 30

instances:
    [{}]
```




##Level 2 – Visualize your Data 
Attached is an image showing a timeboard with the cloned information fom the database metrics as well as other metrics including the random test. Also attached is an image of a Screenboard test. 
![timeboard](https://cloud.githubusercontent.com/assets/4193161/18540986/49b7499e-7af0-11e6-8c6b-9c4ffbdfa792.png)
![screenboard](https://cloud.githubusercontent.com/assets/4193161/18540990/4f92370c-7af0-11e6-933e-9aa1425f6a63.png)


**Bonus question: What is the difference between a timeboard and a screenboard?**
>TimeBoards and ScreenBoards are two different ways that Datadog allows the user to visualize and encapsulate their data. With a TimeBoard the metrics are all synchronized and showing their data for the same time. This is useful for getting a look at all the relevant information of a system and the grid like representation of the data makes this a strong troubleshooting and correlations board. A ScreenBoard is much freer and more customizeable than a TimeBoard. With a ScreenBoard you get the feeling of having a pushboard where you can pin relevant information and keep track of everything on a much higher level. While ScreenBoards can be shared as a whole, TimeBoards can only share individual graphs.

snapshot of test.support.random graph / draw a box around a section that shows it going above 0.90:
![snapshot](https://cloud.githubusercontent.com/assets/4193161/18541013/7b1d681a-7af0-11e6-895f-c4c34a6438f2.png)

Make sure this snapshot is sent to your email by using the @notification
![notification](https://cloud.githubusercontent.com/assets/4193161/18541017/7d75e8bc-7af0-11e6-895a-ec04f258dad7.png)


##Level 3 – Alerting on your Data

Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes. This is a multi-alert by host. (had to change the average to at least once)
![monitor](https://cloud.githubusercontent.com/assets/4193161/18541037/ac4cf22a-7af0-11e6-9dfd-8aa4a722d428.png)

Email alert from monitor:
![alert](https://cloud.githubusercontent.com/assets/4193161/18541040/afbfb14a-7af0-11e6-816d-e7e85b2972f0.png)
**Bonus: Scheduled Downtime on Monitor**
![downtime](https://cloud.githubusercontent.com/assets/4193161/18541046/b579477c-7af0-11e6-9ede-3586a536f400.png)

##Links
[Michael ScreenBoard](https://app.datadoghq.com/screen/119081/michaels-screenboard-15-sep-2016-0108 "Michael ScreenBoard")
[Visualizing Data TimeBoard](https://app.datadoghq.com/dash/183841/visualizing-data?live=true&page=0&is_auto=false&from_ts=1473920203653&to_ts=1473923803653&tile_size=l "Visualizing Data TimeBoard")

###Thank you for taking the time to look over my submission. I'm available to be contacted at any time at MichaelSRodriguezz@outlook.com | 914-602-3603


