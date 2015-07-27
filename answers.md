
Your answers to the questions go here.


############ LEVEL 1 #################################################################################################################

  # "Sign up for Datadog, get the agent reporting metrics from your local machine."

    - Local metrics: Matthews-MacBook-Pro.local
      * Host Dashboard screenshot => https://flic.kr/p/w2cDKb
      * System Overview - Integration Dashboard Screenshot => https://flic.kr/p/wf4uM7


  # "Bonus question: what is the agent?"

    - The agent is a lightweight piece of open-source software that is responsible for collecting events and metrics on behalf of the host user and delivering them to Datadog. Its architecture comprises four main components, each running as a separate process. They are as follows: 

      - Collector - Checks the current machine for integrations and captures standard system metrics (i.e., CPU, memory usage, etc.) every fifteen seconds.
      - Dogstatsd - Aggregates local metrics via code from the host. This is a StatD backend server implemented in Python.
      - Forwarder - Cues data pushed from both the Collector and Dogstatsd by listening for requests over HTTP. This cued data is buffered and forwarded to Datadog via HTTPS, after which it can be used to create visual graphs.
      - SupervisorD - This is the master process that essentially supervises the other three main components. 


  # "Submit an event via the API."

    - First things first... I set up an API key.
      * screenshot => https://flic.kr/p/wgw4pb
      
  ![Matthew-MBP](https://farm1.staticflickr.com/540/20014020236_039e1afc20.jpg" width="500" height="268" alt="Screen Shot")
  
    - Next, I downloaded the 'dogapi' gem and add it to my gemfile.
      * screenshot => https://flic.kr/p/wiSigX
      
  ![API-download](https://farm1.staticflickr.com/532/19892897185_0ba1f22594_n.jpg)
      
    - Then I fired up shotgun, added a binding and reloaded the app. Once I hit the binding a created a new event object in the pry. The following JSON event response was the output.
      * screenshot => https://flic.kr/p/wwKDkM
      
  ![API-response](https://farm1.staticflickr.com/519/20038713351_33e1f34b2d.jpg)
  
  [url=https://flic.kr/p/wwKDkM][img]https://farm1.staticflickr.com/519/20038713351_33e1f34b2d.jpg[/img][/url][url=https://flic.kr/p/wwKDkM]Screen Shot[/url] by [url=https://www.flickr.com/photos/manybeverages/]Matthew Stines[/url], on Flickr
  
  
  # "Get an event to appear in your email inbox (the email address you signed up for the account with)"

    - I added my email in the event message text section of the API request via a "@" notification.
      * screenshot => https://flic.kr/p/vzhKLu
    - The event notification email then arrived in my inbox.
      * screenshot => https://flic.kr/p/wj1Tpa



############ LEVEL 2 ################################################################################################################

  # "Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics."

    - I made a simple Sinatra app based on an example I'd recently built for the Intro to Software Engineering Course I taught at the Flatiron school. It uses the Giphy and Twilio APIs the fire off an animated gif MMS based on keyword search parameters. I provided the 'application-controller.rb' file, the'metric.rb' file and both view files ('home.erb' and 'result.erb') in this commit. Note: I created a Metric class ('metric.rb') to handle all dogstatsd metrics. 

    For metric testing purposes I ran the app locally. I actually spent a fair amount of time trying to re-deploy the app to Heroku using the Datadog Heroku Buildpack. Unfortunately I was having issues getting the app the work correctly. I believe I've narrowed the problem down to a few possible causes (no thanks to Heroku's woefully uninformative logs!) but I didn't want to get too far off track while working on this challenge. I'll continue looking into the problem after I complete this assessment. I could use the API to submit metrics, or course, but I'm determined to install a working agent in the Heroku build using your buildpack. I'll happily send the link when it's up and running correctly!

    For stress testing I used Tsung, per the references provided. I'm new to Tsung but after spending lots of time with it I can say that I'm a fan. It's an awesome piece of software that I plan to continue using going forward. Setup was not particularly intuitive (See image => http://memegenerator.net/instance/53090695) but the program worked very well when all was said and done. Tsung runs an XML file that I configured using the Tsung recorder to create a session. I accomplished this by configuring a proxy in Firefox to listen on port 8090 and then by mimcking typical user behavior in my app on the local server. Tsung records this session as a log file. Adding this session log code to the XML file (in addition to setting the client, server, and load params) completed my testing script (please see included 'tsung.xml' for code implementation.)

    - Here are two (partial) screenshots of the main Tsung report. The first is a summary. The second shows some visual graphs.
      * screenshot(summary) => https://flic.kr/p/vwnqRU
      * screenshot(graphs) => https://flic.kr/p/wr5mfY


  # "While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!"

    - Here is a link my real-time Datadog graph that displays average views per second (timeframe: past week.)
      * link => http://bit.ly/1IpePTP

    - Here is a screenshot of my Datadog views-per-second graph captured just after running the Tsung load test.
      * screenshot => https://flic.kr/p/wtSjFg

  
  # "Create a histogram to see the latency; also give us the link to the graph"

    - I included four metrics on this latency histogram: 'page_view_latency.median', 'page_view_latency.95percentile', 'page_view_latency.avg', and 'page_view_latency.count'. 
      * Latency Histogram link (timeframe: past week) => http://bit.ly/1KsWE1O
      * Latency Histogram screenshot => https://flic.kr/p/wsY8kf

    
  # "Bonus points for putting together more creative dashboards."

      * My Dashboard link => https://app.datadoghq.com/dash/60254/matt?live=true&page=0&is_auto=false&from_ts=1437354976014&to_ts=1437959776014&tile_size=m



############### LEVEL 3 ###############################################################################################################

  # "tag your metrics with support (one tag for all metrics)"

    * Plaese see included metric.rb for 'support' tag implementations.


  # "tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1 with page:page1)"

    * Please see included metric.rb for 'page' tag implementations.
    

  # "visualize the latency by page on a graph (using stacked areas, with one color per page)"

    - I included three metrics for each page on this graph: 'page_view_latency.median', 'page_view_latency.95percentile', and 'page_view_latency.avg'. Links and screenshots below (included support-by-page-avg.-views as well).

      * Latency graph tagged with "support" and pages link (timeframe: past week) => http://bit.ly/1VHWibe
      * Latency graph tagged with "support" and pages screenshot => https://flic.kr/p/wt7mQA

      * Average page views graph tagged with "support" and pages link (timeframe: past week) => http://bit.ly/1D0yzwY
      * Average page views graph tagged with "support" and pages screenshot => https://flic.kr/p/wuz5Wq


   
################# LEVEL 4 #############################################################################################################

  # "count the overall number of page views using dogstatsd counters."

    - Here is a toplist visualization displaying the total number of page hits.
      * Total Page hits graph link => http://bit.ly/1GPiyoc


  # "count the number of page views, split by page (hint: use tags)"
  # "visualize the results on a graph"

    - Here is a toplist visualization displaying total hits by page. Note that 'N/A' represents hits before the page tags were implemented. The 'home' tag was originally 'index' before I changed it, hence the 'index' count. 

      * Total views by page graph link => http://bit.ly/1IoUTR8
      * Total views by page graph screenshot => https://flic.kr/p/wrHmoE


  # "Bonus question: do you know why the graphs are very spiky?"

    - That graphs appear 'spikey' because of the time value increments represented by the x-axis. My tests generally lasted for a few minutes each so the wider the time range on the x-axis, the more 'spikey' the graphs will appear. Selecting 'The Past Hour' range smooths out the graphs somewhat. Also, because dogstatsd flushes data in ten-second intervals, exact point-in-time metrics are unknown. Instead dogstatsd plots metrics to each interval and normalizes them over the graph.



################ LEVEL 5 ##############################################################################################################

  # "Write an agent check that samples a random value. Call this new metric: test.support.random"

    - For the agent check I basically followed the Datadog Docs. I created a simple 'matt.yaml' configuration file and placed it in the 'conf.d' directory. Then, I added the check script, 'matt.py', to the 'checks.d' directory in the Agent root. (see included 'matt.py' and 'matt.yaml' files for code implementation.) After implementing my agent check the 'test.support.random' metric began reporting to Datadog. 


  # "Visualize this new metric on Datadog, send us the link."

      * test.support.random graph link => http://bit.ly/1fx7NBb
      * test.support.random graph screenshot => https://flic.kr/p/webxAq



########## Finished!!.. Fini!!.. 完了!!.. Terminado!!.. Hotovo!!.. Fertig!!.. Klar!!.. 完成!!.. Свершилось!!.. lokið!!..  ##############
