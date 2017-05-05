## Level 0

I'm using a CentOS VM where I currently host a rails app and two Sinatra apps
over a local network.

## Level 1 - Collecting Data

Installed the agent for CentOS/RedHat using:

    <DD_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

The agent is a piece of software that runs on your host machine and collects
data to send to datadog so that you can display useful metrics about your
hosts and monitor whether everything is running smoothly.

Added custom host tags in the agent config file here:

    /etc/dd-agent/datadog.conf

These are the Tags I added

    tags: location:brooklyn, role:web_app_server

The tags appear in the Host map:

![hostmap](https://s3-us-west-2.amazonaws.com/datadoghiringimages/dd_01.png)

***

My CentOS server uses PostgreSQL as a database layer for my Rails app. I
installed the integration and configured it following the instructions.

![postgreSQL instructions](https://s3-us-west-2.amazonaws.com/datadoghiringimages/dd_02.png)

***

To restart the agent I run:

    sudo /etc/init.d/datadog-agent restart

To check to see if the integration is operating I run:

    /etc/init.d/datadog-agent info

There are two files I need to create to write a custom agent check. The file
names must match.

    /etc/dd-agent/conf.d/test_support_random.yaml

```yaml
init_config:

instances:
    [{}]
```

    /etc/dd-agent/checks.d/test_support_random.py

```python
import random
from checks import AgentCheck

class TestSupportRandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

***

## Level 2 - Visualizing Data

The `test.support.random` check is now visible on my timeboard:

![test.suuport.random](https://s3-us-west-2.amazonaws.com/datadoghiringimages/dd_03.png)

***

A Time board is used more for troubleshooting. The time frames are synchronized
so that multiple metrics can be observed in real time relation to each other.

A screen board is more customizable and is used mainly to share information.
Each metric can be displayed with it's own individual timeframe.

`test.support.random` goes above 0.90 sometimes:

![test.support.random spike](https://s3-us-west-2.amazonaws.com/datadoghiringimages/dd_04.png)

***

## Level 3 - Alerting on Data

Creating a Monitor allows us to alert people who need to know then one of your
metrics crosses certain thresholds.

![monitor](https://s3-us-west-2.amazonaws.com/datadoghiringimages/dd_05.png)

***

it will generate e-mail notifications that look like this:

![alert notification](https://s3-us-west-2.amazonaws.com/datadoghiringimages/dd_06.png)

***

We can schedule downtime for Monitors so that they are not alerting in the wee
hours of the morning.

![Schedule downtime](https://s3-us-west-2.amazonaws.com/datadoghiringimages/dd_07.png)

***

When a Monitor is about to go into downtime you will get a notification that
looks like this:

![Downtime notification](https://s3-us-west-2.amazonaws.com/datadoghiringimages/dd_08.png)
