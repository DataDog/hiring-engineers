<a href=“https://app.datadoghq.com/dash/47365/exercise?live=true&from_ts=1429716163374&to_ts=1429719763374&tile_size=m”>My dashboard</a> for all of these exercises.

# LEVEL 1
* Metrics are being reported from my machine under the “Zain Alam” name.

* The agent (“.datadog-agent”) is a kind of middleman layer responsible for handing off all of the metrics and events that you are collecting to Datadog. In the agent, the collector works at a low-level to report system metrics and figure out what integrations to collect from on your machine. Dogstatsd is the primary part of the agent that you interface with as a developer and push all of your metrics to. A forwarder collects data from both of these segments before sending them off to Datadog, and a supervisor handles all of these operations.

* Event submission to the API: 
```
curl  -X POST -H "Content-type: application/json" \
-d '{
      "title": "Posting an event to Datadog with the API!",
      "text": "Wahoo!",
      "priority": "normal",
      "tags": ["environment:test"],
      "alert_type": "info"
  }' \
'https://app.datadoghq.com/api/v1/events?api_key=d6cd967b633ff075367791b1711c1580'
```

* Event that appeared in my inbox by including @ and my email address in the text: 
```
curl  -X POST -H "Content-type: application/json" \
-d '{
      "title": "Posting an event for email notification",
      "text": "@zainalam@gmail.com to your email!",
      "priority": "normal",
      "tags": ["environment:test"],
      "alert_type": "info"
  }' \
'https://app.datadoghq.com/api/v1/events?api_key=d6cd967b633ff075367791b1711c1580'
```

# LEVEL 2
* I used php-datadogstatsd to instrument a simple PHP app with dogstatsd. 

* I ran a load-test with ab: 
```
ab -kc 75 -t 200 http://localhost:8888/?mdc_equation=creatinine-clearance-cockcroft-gault-equation. 
```
The graph can be viewed <a href=“https://app.datadoghq.com/graph/embed?token=667a147ef6bf9cf9a2892db6550d768cb5dc255b3f3fac96e5c10748aa868466&height=400&width=800&legend=true”>here</a>. Page views were counted using this code:
```
<?php
require 'libraries/datadogstatsd.php';
DataDogStatsD::increment(‘web.page_views’, 1);
// .. simple web app code here
?>
```

(pageviews.png)

* The latency histogram can be viewed <a href=“https://app.datadoghq.com/graph/embed?from_ts=1429633132178&to_ts=1429719532178&token=cef885c1e58e0e8171c3e5d4dc6cc07c483a51684cbc681429481590d755bf11&height=400&width=800&legend=true&tile_size=m&live=true”>here</a> and was measured with this code:
```
$start_time = microtime(true);
// .. simple web app code here
DataDogStatsD::timing(‘web’.latency, microtime(true) - $start_time, 1); 
```

(latency.png)

# LEVEL 3
* The latency by page chart can be viewed <a href=“https://app.datadoghq.com/graph/embed?token=c8450a10416fe501314c26191166debc979abc5c8e72a11fb04851074cc9b7b1&height=400&width=800&legend=true”>here</a>.
```
$start_time = microtime(true);

// .. simple web app code here
DataDogStatsD::timing('support.latency', microtime(true) - $start_time, 1, array('page' => $_SERVER["REQUEST_URI"])); 
```

(latency_total_page.png)

# LEVEL 4
* The graphs are spiky due to the page load that changes and remains uneven as time elapses, particularly while running a load-test with a tool like ab.
```
DataDogStatsD::increment('support.page_views', 1, array('page' => $_SERVER["REQUEST_URI"]));
```

(views_by_page.png)

# LEVEL 5
* My simple random-value agent check chart can be viewed <a href=“https://app.datadoghq.com/graph/embed?token=deddb68794269964f6389a7da26a724fb517f1817cd416e9ce05737ff161ea11&height=400&width=800&legend=true”>here</a> and was built with this code:
```
DataDogStatsD::set(‘test.support.random', rand());
```

(random.png)

