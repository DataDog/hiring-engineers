## Level 0

I'm using a CentOS VM where I currently host a rails app and two Sinatra apps
over a local network.

## Level 1 - Collecting Data

Installed the agent for CentOS/RedHat using:

    <DD_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

The agent is a piece of software that runs on your host machine and collects
data to send to datadog so that you can diplay useful metrics about your
hosts and monitor whether everything is running smoothly.

Added custom host tags in the agent config file here:

    /etc/dd-agent/datadog.conf

Adding tags:

    tags: location:brooklyn, role:web_app_server

The tags appear in the Host map:



My CentOS server uses PostgreSQL as a database layer for my Rails app. I
installed the integration and configured it following the instructions.


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

##Level 2 - Visualizing Data

The test.support.random check is now visible on my timeboard:

A Time board is used more for troubleshooting. The time frames are synchonized
so that multiple metrics can be obseverd in real time relation to eachother.

A screen board is more customizable and is used mainely to share information.
Each metric can be displayed with it's own individual timeframe.

##Level 3 - Alerting on Data

    
