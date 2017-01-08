# DevOps_Evangelist Challenge Answers for Don Darwin

**Level 1:**
  * **What is the Agent:**
      The Datadog agent is a lightweight service or daemon that provides out-of-the-box host monitoring of resources including CPU, Memory, Disk, and Network I/O. The Agent includes 3 components: the collector, which collects the metrics; Dogstatsd, a statsd server for sending custom metrics; and the forwarder that collects the metrics from the collector and Dogstatsd and forwards them to Datadog. 

  * **Creating a simple Event:**
      Here is [a screenshot of the email notification](https://github.com/ddarwin/hiring-engineers/blob/master/images/_Monitor_Alert__Triggered__We_received_a_Farce_Event_%E2%80%94_Inbox_and_Events___Datadog.png) from a simple Event I generated through the Event API.
      Here is [a screenshot of a Slack channel notification](https://github.com/ddarwin/hiring-engineers/blob/master/images/API_Event_Slack_notification.png) from the same Event.
 
**Level 2:**
  * [Link to the timeseries graph of Web PageView Rate per second](https://app.datadoghq.com/dash/231347/ddarwinlevel1dashboard?live=true&page=0&is_auto=false&from_ts=1483808200587&to_ts=1483811800587&tile_size=l&fullscreen=173546301)
  * [Link to histogram data graph of Web Page Average Latency (response time)](https://app.datadoghq.com/dash/231347/ddarwinlevel1dashboard?live=true&page=0&is_auto=false&from_ts=1483808317076&to_ts=1483811917076&tile_size=l&fullscreen=173571706)
  
**Level 3:**
  * [Link to the timeseries graph of Web Page Latency Stacked Are Chart](https://app.datadoghq.com/dash/231371/ddarwinlevel3dashboard?live=true&page=0&is_auto=false&from_ts=1483825223896&to_ts=1483828823896&tile_size=m&fullscreen=173575187)
   
**Level 4:**
 * [Link to Total Web Requests over Time graph](https://app.datadoghq.com/dash/231372/ddarwinlevel4dashboard?live=true&page=0&is_auto=false&from_ts=1483825530684&to_ts=1483829130684&tile_size=l&fullscreen=173577937)
 * [Link to Page Requests per Second, by Page graph](https://app.datadoghq.com/dash/231372/ddarwinlevel4dashboard?live=true&page=0&is_auto=false&from_ts=1483825630308&to_ts=1483829230308&tile_size=l&fullscreen=173592246)
 * [Link to Total Page Requests, by Page graph](https://app.datadoghq.com/dash/231372/ddarwinlevel4dashboard?live=true&page=0&is_auto=false&from_ts=1483825739731&to_ts=1483829339731&tile_size=l&fullscreen=173603528)
 * [Link to Python Web App used for these challenges](https://github.com/ddarwin/hiring-engineers/blob/master/source/datadog_web_example.py)
 * **Bonus Question: Why are the graphs so spikey?** The spikey nature of the graphs is due to the short reporting interval, 1 second in this example. Because the request rate and the reporting rate are different, the value reported each interval varies, creating the spikes. Using a rolling average over a longer interval would smooth out the graph.

**Level 5:**
  * [Link to the Agent Check Random Value over Time graph](https://app.datadoghq.com/dash/231358/ddarwinlevel5dashboard-agent-check-example?live=true&page=0&is_auto=false&from_ts=1483826305890&to_ts=1483829905890&tile_size=xl&fullscreen=false)
  * [Link to Agent Check file, mycheck.py, used for this challenge](https://github.com/ddarwin/hiring-engineers/blob/master/source/mycheck.py)
 
**Level 6:**
  * As you suggested, this was a fun exercise that helped me learn more about the features and capabilties of the Datadog solution. My initial impressions were very good. I particularly liked the AWS Integration and dashboarding capabilities. 
