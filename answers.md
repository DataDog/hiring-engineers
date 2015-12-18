Support Engineer Branch, Answers by Stephen Lechner


Level 1 - Answers

  A. I signed up for Datadog and got the agent reporting metrics from my local machine. For some reason, even after I manually updated the API key, the update didn't seem to take, which stopped the agent from being able to forward data to Datadog. Fortunately, as soon as I checked the forwarder logs, it became pretty clear that the agent wasn't using the correct API key. Once I restarted the agent it used the correct API key and worked correctly.
  
  ![forwarder.log](https://cloud.githubusercontent.com/assets/12688271/11882907/70251712-a4dd-11e5-9a39-f76f36d1d0b2.png "Forwarder logs!")

  B. The Agent is a series of processes that run regularly (a few times a minute) to collect key performance data from your system and integrated tools. It sends this performance data to Datadog so that you can graph it on your dashboards and more easily monitor your systems’ performance. It's kind of like Datadog's, well, dog--it loyally fetches everything Datadog needs to help the user understand their systems' performance. 
  
  C. I submitted an event via the API. To do this, I wrote the following code:
  
      from datadog import initialize, api
    
      options = {
          'api_key': 'b79f2e891614183a0a6fded2c1d2301b',
          'app_key': 'test_api_key123asd145124gw5987'
      }
      
      initialize(**options)
      
      title = 'this is an event'
      text = 'but it is really just a test. in fact, nothing much happened. ' \
             '@stephenlechner@gmail.com'
      tags = ['tag:test']
      
      api.Event.create(title=title, text=text, tags=tags)
  
  Here's a screenshot of the event that it created.
  
  ![submitted event](https://cloud.githubusercontent.com/assets/12688271/11882944/9f2fbca6-a4dd-11e5-9f5e-18f68cfbe15e.png "I submitted an event via the API!")
  
  D. I got en event notification to appear in my email inbox since I used the "@" and my email.
  
  ![and I got an email for the event](https://cloud.githubusercontent.com/assets/12688271/11882947/a31c6f3a-a4dd-11e5-9577-3dbfe913a59c.png "And I got an email for the event!")
  
    
  
Level 2 - Answers
  
  A. I took a very simple web app that I wrote (an online catalog that is editable by users who login with a Google account) and added dogstatd and threadstats code to collect metrics through the agent. (See "application.py" in this repo for reference.) Some of the relevant lines of code I wrote to do this are as follows:

        from datadog import initialize, threadstats
        from datadog.dogstatsd.base import DogStatsd
        ...
        init_stuff = {
          'api_key':'b79f2e891614183a0a6fded2c1d2301b',
          'app_key':'catalog_app_key_test_1a5e2h8',
        }
        initialize(**init_stuff)
        stats = threadstats.ThreadStats(constant_tags=['category_app'])
        stad = DogStatsd()
        stats.start()
        ...
        begin = time.time()
        tags = ['support']
        ...
        if tags == ['support']:
          tags += ['catalog:home']
        stats.increment('home.page.hits', tags=tags)
        stad.increment('page.views', tags=tags)
        stats.gauge('process.runtime', time.time() - begin, tags=tags)
        stats.histogram('home.page.hits', 1, tags=tags)
        stats.histogram('user.query.seconds', time.time() - begin, tags=tags)
  
  B. I ran a load test on the catalog web app and created a graph to visualize page views per second. I used a threadstats.increment() method to do this. I ran the load test on 3 different pages within the web app, and I tagged each increment according to what page was being hit. (In this picture you can see that I played around with some different settings of the load tester before I settled on 10,000 runs with only one request at a time.) ([Here'sa link to the graph](https://app.datadoghq.com/dash/87624/testdashboard1?live=true&page=0&is_auto=false&from_ts=1450391365376&to_ts=1450394965376&tile_size=m&fullscreen=69915825).)
  
  ![page hits during a load test](https://cloud.githubusercontent.com/assets/12688271/11882962/b6b380a6-a4dd-11e5-9b54-3e19c96a4da2.png "page hit counts during a load test")
  
  C. I made a histogram to show the latency (by "latency" I assume we mean response time for each request) in seconds of the three pages I tested on the web app. (If you look at what makes up each page, it makes a lot of sense that each page had different consistent response times.) ([Here's a link to the graph](https://app.datadoghq.com/dash/87624/testdashboard1?live=true&page=0&is_auto=false&from_ts=1450390898013&to_ts=1450394498013&tile_size=m&fullscreen=69982587).)
  
  ![latency during a load test](https://cloud.githubusercontent.com/assets/12688271/11884943/49c91df8-a4eb-11e5-8443-f85a78b575a4.png "latency during a load test")
  
  D. The web app that I've been testing for this exercise is a very simple category app where users can create categories and items within those categories. Any user can then wander around the catalog and view each category's items, their descriptions, and pictures.
  
  If someone were to be using this kind of app for business purposes, they would probably want to be able to visualize what categories and items are being viewed more or less than others. Interestingly, this catelog is only shown in the home page, and what category and item appears on the home page depends on each user's inputs. By tagging each home page-view by user input, however, I was able to make a Datadog dashboard that shows the nubmer of views of each category and item. The tags themselves are made from the names that the users give to each category and item, and are preceeded by either "category:" or "item:" appropriately. As a result, there's no need to add new tags every time a user creates a new category type or item--the dashboard is already set up to display views of new categories and items, and it will identify them as categories or items appropriately. 
  ([Here's a link to the graph](https://app.datadoghq.com/dash/87624/testdashboard1?live=true&page=0&is_auto=false&from_ts=1450367730855&to_ts=1450454130855&tile_size=m&fullscreen=70053119).)
  
  ![catalog views by category and item](https://cloud.githubusercontent.com/assets/12688271/11901462/bd06eadc-a579-11e5-8c6c-22c416464a68.png "catalog views by category and item")
  
    
  
Level 3 - Answers

  A, B, C. Using the same web app, I tagged each metric I was collecting with "support", as well as the separate page tags I was already using. (Those pages were "home", "json", and "login", and they were tagged to "catalog:home", "catalog:json", and "catalog:login" respectively.) I showed the latency per page with each page's latency stacked up on top of the other in a different color. (The "login" page has very little response time, so it makes sense that it's generally hard to see.) ([Here's a link to the graph](https://app.datadoghq.com/dash/87624/testdashboard1?live=false&page=0&is_auto=false&from_ts=1450381314000&to_ts=1450381869000&tile_size=m&fullscreen=69986319).)
  
  ![latency stacked by page](https://cloud.githubusercontent.com/assets/12688271/11882988/d274563a-a4dd-11e5-9f49-828f2a2aebdc.png "latency stacked by page")
  
    

Level 4 - Answers

  A, B, C. While load testing the same web app, I counted the total number of page views using tagged dogstatd counters and visualized each page's counts stacked together on the same graph. ([Here's a link to the graph](https://app.datadoghq.com/dash/87624/testdashboard1?live=true&page=0&is_auto=false&from_ts=1450391166821&to_ts=1450394766821&tile_size=m&fullscreen=69988481).)
  
  ![page count stacked by page](https://cloud.githubusercontent.com/assets/12688271/11882993/d58ac8ea-a4dd-11e5-83d1-d03c0c5d6d30.png "page count stacked by page")
  
  D. In this case, the graph was not very spikey. But I think that's a result of the way I set up the load test. The load test was very consistent in the number of hits it was making on the app, and even in the distribution of which pages it was hitting. As a result, there was only mild change in the rate of counts per reporting period for the agent. 
  
  That being said, when I played around with the web app manually, the dashboards did register big spikes in view counts. I suspect these spikes occurred because the agent counters grouped the page views to be shown on a per-reporting-period basis. Manual activity tends to be less consistent, which would result in more jarring jumps between metric points. 
  
    

Level 5 - Answers

  A. I wrote a custom agent check that samples a random value, which I called "test.support.random". To do this, I added a "random_check.py" file to the agent's "checks.d" directory that had the following content:
  
      from random import random
      from checks import AgentCheck
      
      class RandomCheck(AgentCheck):
          def check(self, instance):
              self.gauge('test.support.random', random())
  
  I then added a "random_check.yaml" file to the agent's "conf.d" directory with the following content:
  
      init_config:
      
      instances:
          [{}]
  
  Finally, I ran the "random_check" check through the agent by sending "datadog-agent check random_check" through the command line.
  
  (I learned how to do all this from links I found in the references--specifically [this](http://docs.datadoghq.com/guides/agent_checks/) one. I got a little thrown off by differences in the directory locations of my "conf.d" and "checks.d" folders, and also by the fact that my agent's name isn't dd-agent but datadog-agent, but with a little head-tapping I figured it out.)
  
  B. I graphed the random values in a dashboard. ([Here's a link](https://app.datadoghq.com/dash/87624/testdashboard1?live=true&page=0&is_auto=false&from_ts=1450321008040&to_ts=1450407408040&tile_size=m&fullscreen=70006677).)
  
  ![test.support.random metric graphed](https://cloud.githubusercontent.com/assets/12688271/11888347/5fe30382-a50a-11e5-8d14-96d3cb577db6.png "test.support.random graphed")
  
