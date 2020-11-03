**Name:** Bradley Beard

**Postion:** Datadog Solutions Engineer

Hello - Below are my responses to the hiring excercise. For this exercise I set up an Ubuntu VM through Vagrant and Virtualbox and installed the agent directly onto Ubuntu. If there's any clarification I can provide please let me know. Thank you. 


#### Collecting Metrics

I started by adding a role, location, and resource_name tag to datadog.yaml file. After restarting the agent, they appeared as host tags in the dashboard. See the screenshot of the host in the hostmap below:

[![host-tags.png](https://i.postimg.cc/gj0wZTyh/host-tags.png)](https://postimg.cc/xJWTrg4j)

I then installed MySQL and set up the corresponding integration through following directions on the integrations section of the dashboard. 

[![My-SQL-Integration.png](https://i.postimg.cc/JzR55Qy5/My-SQL-Integration.png)](https://postimg.cc/fJgdwmfV)

T

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?
