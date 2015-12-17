Support Engineer Branch, Answers by Stephen Lechner


Level 1 - Answers

  A. I signed up for Datadog and got the agent reporting metrics from my local machine. For some reason, even after I manually updated the API key, the update didn't seem to take, which stopped the agent from being able to forward data to Datadog. Fortunately, as soon as I checked the forwarder logs, it became pretty clear that the agent wasn't using the correct API key. Once I restarted the agent it used the correct API key and worked correctly.

  B. The Agent is a series of processes that run regularly (a few times a minute) to collect key performance data from your system and integrated tools. It sends this performance data to Datadog so that you can graph it on your dashboards and more easily monitor your systems’ performance. It's kind of like Datadog's, well, dog--it loyally fetches everything Datadog needs to help the user understand their systems' performance. 
  
  C. I submitted an event via the API.
  
  D. I got en event notification to appear in my email inbox (the one I signed up with).
  
  
