Your answers to the questions go here.

Level 1

1) Instead of downloading it locally, I downloaded and installed remotely on my VPS which hosts my website.

2) "The Datadog Agent is piece of software that runs on your hosts. Its job is to faithfully collect events and metrics and bring them to Datadog on your behalf so that you can do something useful with your monitoring and performance data." Source:"http://docs.datadoghq.com/guides/basic_agent_usage/"

3) I initially was checking out the different APIs. I ended up submitting events via Ruby, Python, and lastly PHP. The PHP section took me the longest because of the installation troubleshooting I had to go through. It's pretty specific and only work's with "PECL http version 1.7.6"

4)Image link to "submit an event via the API" = "http://i.imgur.com/ew6kN4Q.png?1"

5)Image link to "get an event to appear in your email inbox" = "http://i.imgur.com/P8nE80h.png?1"


Level 2

1)Created simple web app via PHP script. 
```
"<?php

require '/var/www/html/php-datadogstatsd/libraries/datadogstatsd.php';

$apiKey = '0f32b85e17d89512cfae1dd0b54aebb7';
$appKey = 'c8c5dee8457aa27e939485d83298c191a439bab7';

DataDogStatsD::increment('web.page_viewsphp');


?>"
```

2) Called the metrics.php file via Apache Benchmark. "ab -n 999 -c 20 http://firasimus.com/metrics.php"
After a couple of minutes of testing with different variations this is the following result : "http://i.imgur.com/j2aTPB4.png?1"

3) Made another simple php file :
```
<?php

require '/var/www/html/php-datadogstatsd/libraries/datadogstatsd.php';

$apiKey = '0f32b85e17d89512cfae1dd0b54aebb7';
$appKey = 'c8c5dee8457aa27e939485d83298c191a439bab7';

DataDogStatsD::histogram('web.render_time', 15);DataDogStatsD::histogram('web.render_time', 15);

BatchedDatadogStatsD::histogram('web.render_time', 15);
?>
```
I used this to php file with the load tester once again to gauge the latency of the server.

The link to the latency graph = "http://i.imgur.com/ALeLxmY.png?1"

Level 3

1) Added ```"DataDogStatsD::increment('web.page_viewsphp', array('tagname' => 'support'));"```

2) Added ```"DataDogStatsD::histogram('web.render_time', 15, array('tagname' => 'support'));"```

3) Added the "support" tag to the infrustructure on datadog of the VPS being used. This could be utilized across multiple VPS via the "support" tag.


4) Added "page" to webpage view metric. 
```"DataDogStatsD::increment('web.page_viewsphppg1', array('tagname' => 'page:pageview1','tagname' => 'support'));"```

5) Created similar "page" for easier comparison via page tags.
```"DataDogStatsD::increment('web.page_viewsphp', array('tagname' => 'page:pageview2','tagname' => 'support'));"```

**Added the tags via infrustructure once again**

6) Latency comparison between pages "http://i.imgur.com/xqC64ZC.png?1"



Level 4)

```"DataDogStatsD::increment('web.page_viewsphppg1', array('tagname' => 'page:pageview1','tagname' => 'support'));"``` is a perfect example of a page counter. It incremently counts the web page views as the php is called.

It's already setup to be compared to it's counterpart ```"DataDogStatsD::increment('web.page_viewsphp', array('tagname' => 'page:pageview2','tagname' => 'support'));"``` for easy page splitting.

Results of page splitting for web page view comparison can be seen here "http://i.imgur.com/lXSPxjk.png?1"

Bonus - I believe the graph is spiky because of the inactivity with a surge of activity being created by the load tester.

Level 5)

Using "http://docs.datadoghq.com/guides/agent_checks/" the first thing I did was create the files in the appropriate locations.

"test.support.random.yaml" and "test.support.random.py" were created with the yaml file going to the /etc/dd-agent folder and the py file going to /etc/dd-agent/checks.d directory.

The yaml file contained 
```
init_config:

instances:
    [{}]  
```    

with the py file containing
```    
import random

class testsupportrandom(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random.random())
   ``` 
