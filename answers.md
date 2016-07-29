Your answers to the questions go here.

Level 1 - Collecting your Data
Here is initial Agent Install
Screenshot 1 

Here's my laptop on Datadog :)
Screenshot 2 

Adding my first tags 
Screenshot 3

Postgresql reporting locally
Screenshot 4

Postgresql integration installed 
Screenshot 5




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
Screenshot 6

Alerting over 0.9 
Screenshot 7

Bonus: Difference between a timeboard and a Screenboard?

Timeboard is where everything is displayed relative to time - good for realtime, troubleshooting... "why is database crashing?"
Screenboard is more flexible and custamizible.. more high level - good for seeing trends, general performance..etc


Level 3 

Email Alert!
Screenshot 8



Bonus: 
Downtime
Screenshot 9

Extra:

Experimenting with CPU load
