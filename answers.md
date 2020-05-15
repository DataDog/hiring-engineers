Dashboard link: https://app.datadoghq.com/dashboard/lists
Datadog agent installed to host running on Vagrant VM
Mysql DB installed to same host

Bonus Question Can you change the collection interval without modifying the Python check file you created?
- The collection interval can be modified at the instance level (/.datadog-agent/conf.d/<name>.yaml) by setting the following property:
  min_collection_interval 
  
Bonus Question: What is the Anomaly graph displaying?
