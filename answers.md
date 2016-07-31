Your answers to the questions go here.
Level -1 Collecting Data 

To start off, here is the initial Agent Install

 
![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%201.png)

Here's my laptop on Datadog, well..., my girlfriend's laptop. :)

![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%202.png)

Now, lets add my first tags 
![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%203.png)

Postgresql reporting locally
![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%204.png)


Look! Postgresql integration installed 
![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%205.png)




Bonus: In your own words, what is the Agent?

The Datadog Agent is piece of software that runs on the bqckground of your hosts. It collects events and metrics and bring them to Datadog so you can do something useful with your monitoring and performance data.

```PYTHON
import random

from checks import AgentCheck

class HTTPCheck(AgentCheck):
    def check(self, instance):
        random_number = random.random()
        self.gauge('test.support.random', random_number, tags=['test'])
```
After adding a matching config file called `random.yaml` to the `conf.d` folder, my check is ready to test!

Level 2


Random Value succesfully reporting!
![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%206.png)


Alerting over 0.9 
![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%207.png)


Bonus: Difference between a timeboard and a Screenboard?

Timeboard is where everything is displayed relative to time - good for realtime, troubleshooting... "why is database crashing?"
Screenboard is more flexible and custamizible.. more high level - good for seeing trends, general performance..etc


Level 3 

There you have it, an Email Alert!
![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%208.png)




Bonus: 
After many email alerts, looks like I'm in need of some Downtime
![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%209.png)


Extra:

Experimenting with CPU load. After experimenting with a few applications to stress test the CPU, I found this command ```yes > /dev/null``` - which simply prints out the letter 'y' as fast as possible until the CPU is at 100% usage. Datadog really makes it easy to understand the performance of our stack!

![ScreenShot](https://github.com/jramon1/hiring-engineers/blob/master/Screenshot%2010.png)
