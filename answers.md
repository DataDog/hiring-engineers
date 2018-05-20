## answers.md aka "My week with Datadog in my spare time"  

As an introduction, I am an Enterprise SE with extensive experience evangalizing Networking, Storage and Data Protection solutions.  This has been an intriguing (and occasionally humbling) exercise. In my career I have been a consumer of monitoring and analytics, not necessarily involved in the  dev/ops underpinnings that enable them other than providing feedback or feature requests.

As a testament to the the clarity of the effectiveness of the online Datadog documnentation installing and enabling the Datadog agent and specific stack integration was mostly a mattter of following the instructions, which even a non-dev ops SME can do :smiley:

I created the environment for this exercise by spinning up a Centos 7 VM in a virutal machine on a local hypervisor. I installed the Datadog agent for Centos and verified it was operational (see agent_status_before_MongoDB.txt in this branch). 

### Collecting Metrics    

I configured my default API key, listed at https://app.datadoghq.com/account/settings#api in **datadog.yaml**, the yaml file for the Datadog agent.  

    api_key: 584df05c35575f36e17d3543d00c341d  

Confirmed by "datadog-agent status"     

    API Key Status    
    ==============    
    https://6-2-0-app.agent.datadoghq.com,*************************c341d: API Key valid  
    
And added tags in the agent config file, and I also configured agent yaml to report a specified host name 

    tags:
        - role:database:mongodb
    hostname: colby-exercise-machine.localdomain  





Hostnames
=========
  hostname: colby-exercise-machine.localdomain
  socket-fqdn: localhost
 socket-hostname: localhost.localdomain  

I next installed a single node MongoD and installed and configured Datadog integration for MongoDB
placing the statment in the mongo.yaml referencing the password for the datadog user I created in Mongo. 

    -   server: mongodb://datadog:kgVXlTnEFbTNSaKAdA7VYDf0@localhost:27017  
      
The collector section datadog-agent status report confirmed that the agent was successfully collecting data from the MongoDB instance

    mongo
    -----  
      Total Runs: 29444  
      Metrics: 113, Total Metrics: over 1M  
      Events: 0, Total Events: 0  
      Service Checks: 1, Total Service Checks: 29444  
      Average Execution Time : 21ms  

Per the exercise instructions I created a custom agent check to submit a metric (named "my_metric") that is a random value between 0 and 1000.  I decided to make the random "value" betweeen 0 and 1000 be an integer between 0 and 1000. 

**colbycheck.py**  

    import random
    from checks import AgentCheck
    class RandomCheck(AgentCheck):
     def check(self, instance):
      self.gauge('my_metric', random.randint(0,1000))  
 
 **colbycheck.yaml**
 
    self.init_config:

    instances:
      - name: colbyrandom
        min_collection_interval: 45  

I added a minimum collection configuration parameter for 45 seconds in the yaml file.  The exercise instructions specify changing my check's collection interval so it only submits the metric every 45 seconds. 

To be clear, however, the actual collection interval is a bit of a dance between the interval time per instance for this custom agent check and the interval time for Data Dog Agent collector (who's collection frequency is every 15-20 seconds dependent on how many integrations are enabled).  The result, per the documentation, is that this does not mean the metric is collected **every** 45 seconds but rather it **could** be collected **as often as** every 45 seconds.  


**Q: Can you change the collection interval without modifying the Python check file you created?**  
**A:** The collection interval is changed in the yaml file for the custom agent check, not in the python check file itself. 

To confirm the






