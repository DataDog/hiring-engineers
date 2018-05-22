## Introduction
Thanks for giving me the opportunity to try out this challenge. I stumbled in a few places, but in almost every case I was making the problem harder than it needed to be. I'm struck by how quickly you can instrument Datadog to show you what you want to see. 

Let me walk you through the challenge, and how I accomplished each step.

## Collecting Metrics:
 * Add tags
  The first step was to add tags to one of my hosts my modifying the Agent config file. This straightforward task eluded me for about an hour due to ntp issues. Once I got that settled, and remembered to bounce the datadog-agent, I was all set. 
  ![Alt text](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/screenshots/host_with_tags.png)
  * Install a database
  Next, I installed MySQL on my newly tagged machine, and used the Datadog GUI to find the appropriate integration. I followed the integration instructions and within minutes I had MySQL showing up as an app on my host map page. 
  * Create a custom agent check
  To create this check, I created 2 files, [mymetric.yaml](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/mymetric.yaml) and [mymetric.py](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/mymetric.py) in `conf.d` and `checks.d` respectively. `mymetric.yaml` contains the instances that I want to run through the check on every agent run, and `mymetric.py` contains the code that is executed during that run. 
  * Change the check collection interval
  To accomplish this task, and satisfy the **Bonus Question** I modified the `mymetric.yaml` file to set `min_collection_interval` to 45 seconds. This doesn't necessarily mean that the agent check will run precisely every 45 seconds. With every run of the agent, the agent check will verify how long it has been since the mymetric check has run. If it has been less than 45 seconds, it will wait to run the check on a subsequent run. If it has been more than 45 seconds, it will run the check. The result shows the custom agent check running in my environment roughly every minute.

## Visualizing Data:
  * Utilize the Datadog API to create a custom Timeboard
  I spent quite a bit of time on this portion of the exercise. I initially tried to create my script from scratch, adding in each additional component once I'd successfully created a Timeboard from my script. While I was easily able to add in standalone metrics, I struggled to find documentation examples with the correct syntax for applying functions to those metrics. Once I realized I could apply functions within the GUI, then expose the json associated with those functions, I was able to cruise through the rest. See [my_timeboard.py](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/my_timeboard.py) for the script I used to generate [the board](https://app.datadoghq.com/dash/816852/elizabeths-timeboard?live=true&page=0&is_auto=false&from_ts=1526956540982&to_ts=1526960140982&tile_size=l)

  * Access the Dashboard, adjust timeframe, take a snapshot

  ![Alt text](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/screenshots/my_timeboard_screenshot.png)
  Although the scale makes it difficult to see, the anomaly function is highlighting all of the instances where the metric I've specified (in this case the number of bytes sent to clients) deviates from the typical behavior. The anomaly function can reduce false alerts by understanding trends in metric data, and distinguishing between a normal spike in the middle of a workday versus an unusal activity spike on the weekend.

## Monitoring Data:
  In this section I used the Datadog GUI to create a new monitor for `my_metric`.  I created different thresholds for warning, alerting and no data. 
  
  ![Alt text](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/screenshots/monitor_screenshot.png)
  
  While I did not receive an alert, the average value for my_metric did not exceed 800 over any 5 minute periods, I did receive several warnings.
  
  ![Alt text](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/screenshots/high_metric_alert.png)
  
  For the **Bonus Question**, I enabled downtimes effective all day Saturday and Sunday, from 7pm - 9am M-F, and an additional downtime to cover midnight to 9am on Mondays. Here is an example of an email I recieved when scheduling these downtimes:
  
  ![Alt text](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/screenshots/downtime_set.png)
  
  and the email I received when downtime began:
  
  ![Alt text](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/screenshots/downtime_started.png)
   
## Collecting APM data:
  Using the sample code provided, I instrumented the [flask app](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/myapp.py) to send traces to Datadog. Once I generated some traffic, traces started showing up in the GUI. Drilling into the `my-app` service, I see dashboards detailing service level request and latency information, as well as the specific resources associated with this service. **Bonus Question** The difference between a resource and a service - A service represents a logical collection of processes that can fall into 1 of 4 categories - Web, DB, Cache, or Custom. For each service, there are actions you can take that produce valuable output. Those actions are called resources.

  Using the link in the upper right corner, I saved the latency and request graphs to a new [Dashboard](https://app.datadoghq.com/dash/816065/elizabeths-timeboard-for-myapp?live=true&page=0&is_auto=false&from_ts=1526872658155&to_ts=1526959058155&tile_size=l). Take a look!

  ![Alt text](https://github.com/ewplumb/hiring-engineers/blob/solutions-engineer/screenshots/apm_dashboard.png)

   ## Final Question
   There was a short period of time at Puppet when we had cold brew on tap. When they'd bought the cold brew, Puppet expected it to last for about a month. It was gone after 2.5 days. Everyone loved it, and some were convinced that it made them more productive. However, Puppet quickly realized that keeping up with this demand would have been far more expensive than they'd originally thought, so the cold brew was cut. I've heard more than a few developers wonder about the correlation between the cold brew days and employee productivity. It'd be fun to see how many code commits happened during those days, and perhaps how many bugs were associated with those commits. Coffee might make you faster, but does it make you better? Maybe we'll see!
