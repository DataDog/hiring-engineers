# Level 0 (optional) - Setup an Ubuntu VM
Done on a Mac with Vagrant

# Level 1 - Collecting your Data
* Check for getting metric `test.support.random`
```
from checks import AgentCheck
import random
# print(random.random())
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```
* You can find a screenshot (tag.png) showing the tags.
* **Bonus question** What is the Agent? In short, an Agent is a DataDog programme to help clients to send their metrics from their host to DataDog, should you choose not to use API to send DataDog those metrics.

# Level 2 - Visualizing your Data
* Snapshot of `test.support.random` with a box drawed for metric going above 0.90 is included in screenshot (snapshot.png)
* **Bonus question** The differences between TimeBoard and a ScreenBoard are mainly:
    * TimeBoard always scoped to the same time while ScreenBoard does not.
    * ScreenBoard is more customizable. However TimeBoard is less customizable.
    * ScreenBoard can be shared as read only, but TimeBoard cannot.
* [Link to dashboard](https://app.datadoghq.com/dash/263112/test-cloned). And you can also find a screenshot of it (dashboard.png)

# Level 3 - Alerting on your Data
* Screenshot of the alert email has been included. (alert.png)
* **Bonus question** Multi-alert done.
* **Bonus question** Screenshot of the scheduled downtime email has been included. (scheduled_downtime.png)
