As an introduction, I am an Enterprise SE with extensive experience evangalizing Networking, Storage and Data Protection solutions.  This has been an intriguing exercise. In my career I have been a consumer of monitoring and analytics, not necessarily involved in the  dev/ops underpinnings that enable them other than providing feedback or feature requests.

As a testament to the the clarity of the effectiveness of the online Datadog documnentation installing and enabling the Datadog agent and specific stack integration was mostly a mattter of following the instructions, which even a non-dev ops SME can do :smiley:

I created the environment for this exercise by spinning up a Centos 7 VM in a virutal machine on a local hypervisor. I installed the Datadog agent for Centos and verified it was operational (see agent_status_before_MongoDB.txt in this branch). 

I also configured my default API key, listed at https://app.datadoghq.com/account/settings#api in **datadog.yaml**, the yaml file for the Datadog agent.  

**api_key: 584df05c35575f36e17d3543d00c341d**  

Confirmed by 'datadog-agent status'  
'API Key Status'  
'=============='  
  'https://6-2-0-app.agent.datadoghq.com,*************************c341d: API Key valid'  


I next installed a single node MongoD and installed and configured Datadog integration for MongoDB.



Q: Can you change the collection interval without modifying the Python check file you created?
Y: The collection interval is changed in the yaml file for the python check, no in the python check file itself.  Also collection interval for the agent itself, via the metadata providers interval, can be changed.

