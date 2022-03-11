# DataDog Tech Assessment Sales Engineer
Andrew Hartzell

## Set up the Environment

Already have a version of Ubuntu installed on VirtualBox - will use that for this test.

**Install the DD agent**

<img src="/screenshots/dd_agent_install.png" alt="Ubuntu up and running" style="height: 125px; width:300px;"/>

**Appears in dashboard**

<img src="/screenshots/dd_dash.png" alt="Agent in Dash" style="height: 125px; width:300px;"/>

## Collecting Metrics


**Add tags in config file - host + tags on host map page in DD**
```
cd /etc/datadog-agent/
nano datadog.yaml (add tags)
```
<img src="/screenshots/tagsyaml.png" alt="Add tags to yaml file" style="height: 125px; width:300px;"/>


**Restart Agent so updated tags will appear in host map**
```  
sudo systemctl restart datadog-agent.service
```
<img src="/screenshots/hostmaptags.png" alt="Tags appear in hostmap" style="height: 125px; width:500px;"/>  

**Install Database**
Opted to use MySQL database for this part of the exercise.  Per the docs on https://docs.datadoghq.com/integrations/mysql/?tab=host the MySQL check is included in the DD Agent and no additional install is needed on your SQL server.

Next steps in the SQL integration detail preparing your server by adding a datadog user and password.
<img src="/screenshots/dd_sql_user.png" alt="Create DD SQL user" style="height: 80px; width:400px;"/>  

I attempted to run the commands in the MySQL docs for verifying user creation and received syntax errors.  After spending a lot of time looking for answers I was still unable to figure out what the issue was and decided to move on to the next action item.

<img src="/screenshots/sql_users.png" alt="Show all SQL users" style="height: 200px; width:250px;"/> 

**Update User Privleges**
Agent privleges updated to collect metrics
<img src="/screenshots/update_user.png" alt="Update DD privleges" style="height: 80px; width:400px;"/> 

Grant access to performance_schema
<img src="/screenshots/perf_schema.png" alt="Give DD access to performance schema" style="height: 80px; width:400px;"/> 

Add configuration to collect SQL metrics
<img src="/screenshots/conf_yaml.png" alt="Add SQL metrics config" style="height: 200px; width:250px;"/> 

Restart the user agent to sending SQL metrics back DD.  Write some data to the SQL database so metrics populate.

<img src="/screenshots/mysql_metrics.png" alt="SQL appear in metrics" style="height: 100px; width:250px;"/> 


## Create Custom Agent Check
Create a custom Agent check that submits a metric name my_metric with a random value between 0 and 1000.

Create the config file my_metric.yaml (needs to match the name of my_metric.py).

Navigate to /checks.d and create the python script.  Import the random module, use the snippet provided in the guide to import AgentCheck module.
Final step is create my_metric with random number between 1-1000.

<img src="/screenshots/my_metric.png" alt="my_metric.py script" style="height: 100px; width:250px;"/> 

Verify the check is running with: 
```
sudo -u dd-agent -- datadog-agent check my_metric
```
<img src="/screenshots/check_ok.png" alt="Check my_metric" style="height: 100px; width:225px;"/> 

My_metric appears in Metrics Dashboard:
<img src="/screenshots/metrics_dash.png" alt="Check my_metric in DD metrics dashboard" style="height: 100px; width:225px;"/> 

**Bonus Question**
Q: Can you change the the collection interval without updating the python check file created?
A: Yes! You can update the collection interval in the my_check.yaml file you created:
<img src="/screenshots/collection_interval.png" alt="Update collection interval in config file" style="height: 100px; width:225px;"/>