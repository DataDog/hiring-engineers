# Prerequisites - Setup the environment

I installed the Datadog Agent using the Mac/OSX instructions here: https://app.datadoghq.com/account/settings#agent/mac

![alt text] [./screenshots/1.png?raw=true "1"]

# Collecting Metrics

I added relative tags (region:northeast, env:prod, role:test) in the Agent config file and then restarted the agent. 
![alt text] [./screenshots/2.png?raw=true "1"]


PostgreSQL was already installed on my computer, so I upgraded it to the newest version. I then connected PostgreSQL with my account using these instructions: https://app.datadoghq.com/account/settings#integrations/postgres

![alt text] [./screenshots/3.png?raw=true "1"]
![alt text] [./screenshots/4.png?raw=true "1"]

Here is a copy of my YAML file. 

![alt text] [./screenshots/5.png?raw=true "1"]
![alt text] [./screenshots/7.png?raw=true "1"]

I created a custom Agent check for a random value between 0 and 1000. 
![alt text] [./screenshots/8.png?raw=true "1"]

** Can you change the collection interval without modifying the Python check file you created?

Yes, after searching I found that if you add in min_collection_interval : # of seconds (key:value pair) in the YAML file, the PY file can be left untouched. 

![alt text] [./screenshots/9.png?raw=true "1"]

# Visualizing Data

I created a timeboard that shows the timeframe over the past 5 minutes and sent it to myself using the @ notation. 
![alt text] [./screenshots/10.png?raw=true "1"]
![alt text] [./screenshots/11.png?raw=true "1"]

*What is the Anomaly graph displaying?

Anomaly graphs show any new behavior in a metric that is inconsistent from normal patterns. It can be used to highlight unusually high traffic volumes on a website or other unusual activity. It works best with metrics that display consistent trends over time.

# Monitoring Data

I set up the warning and alerting thresholds which sends an email when the monitor triggers. 
![alt text] [./screenshots/12.png?raw=true "1"]

This was then sent to my email. 
![alt text] [./screenshots/13.png?raw=true "1"]

# Collecting APM Data

Here is the Python Flask file for Datadog's APM. 
![alt text] [./screenshots/14.png?raw=true "1"] 

However, I wasn't able to connect. Go didn't want to work with the trace agent file on my computer, and I wasn't able to set up a Linux environment. I tried several times, but was unfortunately unsuccessful. 

The place where I had trouble was with installing Go. When doing `rake build` or `rake install` into the GOPATH, it did not work. This came from doing `rake restore`, yielding this error message while installing the dependencies:

`[WARN]    The name listed in the config file (github.com/DataDog/datadog-trace-agent) does not match the current location (.)`. 

Attempts to modify my GOROOT and GOPATH did not yeild the correct result. I tried to work with a Linux environment, but that did not work well on my computer. 

I hope to be able to fix it, but the trial is almost up. 

*What is the difference between a Service and a Resource?

A service in Datadog APM is defined as "a set of processes that work together to provide a feature set". In relation to your application this would normally be a web app or a database.Datadog will monitor the performance of each service individually and provice metrics such as requests, average latency, and error rate.

A resource in Datadog APM is defined as "a particular query to a service". The resources are the individual calls and traces that make up a service. For a web app service, resources will be entry points into the application such as specific URLs that users are hitting (ie. /api/apm or /user/home). For a database, a resource will be an individual SQL query (ie. select * from users). The metrics of individual resources will make up the overall service's performance metrics.


# Final Question

*Is there anything creative you would use Datadog for?

As a beer nerd, I think Datadog would be really useful for a big brewery. The brewery could track to see how many customers come in at a given time, how much time they spend in the brewery, and how much beer they order. This could allow them to keep track of their inventory, prepare new kegs more quickly for when one might kick, and know their customers actions better. 


