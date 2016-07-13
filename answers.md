Level 1
* Push an event with my api key with a curl in bash :
curl  -X POST -H "Content-type: application/json" \
-d '{
      "title": "Hiring test event",
      "text": "yeahhhhh!",
      "priority": "normal",
      "tags": ["environment:test"],
      "alert_type": "info"
  }' \
'https://app.datadoghq.com/api/v1/events?api_key=APIKEY'

Level 2 :

Link to my dashboard https://app.datadoghq.com/dash/160635/hiring-test?live=false&page=0&is_auto=false&from_ts=1468418940949&to_ts=1468422540949&tile_size=m

- tag your metrics with support (one tag for all metrics) :
edit /etc/dd-agent/datadog.conf and add tags: support

Level 4 :
++++@++++:/etc/dd-agent# cat /etc/dd-agent/conf.d/hiringtest.yaml
init_config:

instances:
    [{}]

++++@++++:/etc/dd-agent# cat /etc/dd-agent/checks.d/hiringtest.py
import random
from checks import AgentCheck
class HiringtestCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())