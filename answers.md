**Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.**
> RMullins407


**Bonus question: In your own words, what is the Agent?**
> The agent is a service that independently runs on each VM or Container and relays performance metrics back to the DataDog webservice for user interaction

**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**


```{r, engine='sh', count_lines}
vagrant@precise64:~$ grep -m 1 tags: /etc/dd-agent/datadog.conf 
tags: RoyMullinsExercise, env:test, role:exercise
```

> [Host Tags Screenshot](./HostTags.PNG)

**Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

```{r, engine='sh', count_lines}
vagrant@precise64:~$ mysql --version
mysql  Ver 14.14 Distrib 5.5.54, for debian-linux-gnu (x86_64) using readline 6.2
vagrant@precise64:~$ service mysql status
mysql start/running, process 10745
vagrant@precise64:~$
```

**Write a custom Agent check that samples a random value. Call this new metric: test.support.random**
```{r, engine='py', count_lines}
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random',random.random())
```

**Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.**

> [Dashboard](./DashboardClone.PNG)

**Bonus question: What is the difference between a timeboard and a screenboard?**

> Timeboards are individual performance monitoring widgets linked together with a common timestamp. Screenboards are a unified set of data metrics which can be shared as a whole, as opposed to individually as with timeboards.

**Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification**

> [Value Snapshot](./Snapshot.PNG)

**Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.**

> [Monitor Screenshot](./Monitor.PNG)

**This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.**

> Writing this .md at 1 AM, have set monitor to deliver notifications at this hour for testing purposes.

> [Email Screenshot](./Email.PNG)











