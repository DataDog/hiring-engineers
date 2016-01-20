#Level 1

<h2>
- Sign up for Datadog, get the agent reporting metrics.


After signing up to Datadog using *"Datadog Recruiting Candidate"* as Company Input, I installed the agent on my EC2 server hosting my Blog web application. The host is based on Ubuntu.   

I used the *easy one-step install* instruction to be found in the *Integrations>Agent* tab on Datadog personal account. System-related metrics are available on the *Metrics>Explorer* tab. 
I chose to represent three main metrics:
+ the available disk space on the host (or system.disk.in.use )
+ the CPU use ( or system.cpu.user)
+ the average available memory percentage over the past 5 minutes.

These three metrics will enable me to help me monitor my web app and make sure I constantly have enough memory, disk space available and responsive CPU.

Here are the representations of these three metrics : 
![Initial metrics](../hiring-engineers/images-challenge/Blog-initial-metrics.png)


The complete Blog Dashboard can also be found [here](https://p.datadoghq.com/sb/15d4408a4-8201f2536e)


<h2>
- Bonus question: what is the agent?

The agent is a piece of software embedded on the host to be monitored. It is composed of three main parts:

- ***The Collectors*** will collect the metrics related to the host system such as CPU or memory, and will check those related to the supported integrations.
- ***DogstatsD*** will collect metrics that the user settles according to their needs. Metrics are collected from an app. This is available in several languages to best adapt the clients’ needs in terms of applications / services to monitor.
- ***The Forwarder*** collects data from the collector and the dogstatsd , puts them on a queue then send them do Datadog for analysis and visualization capabilities.


<h2>
- Submit an event via the API.

In order to do that, I first created an API key on the personal-account Datadog *Integration>API* tab, to enable the transactions to be authenticated. I then created the Python script as follows :


```python
# Configuration of the module with the authentication required to communicate with the API
from datadog import initialize

# The API key is generated through the Integration>API part of the Datadog Website
options = { 
    'api_key':'personal_api-key'
    }

initialize(**options)

# Use Datadog REST API client
from datadog import api

title = "Something happened"
text = "This is a test creating an event through the datadog API"
tags = ['API-test']

# Create the event thanks to the elements that we have defined above
api.Event.create(title=title, text=text, tags=tags)
```

![Event](../hiring-engineers/images-challenge/event.png) 

<h2>
- Get an event to appear in your email inbox (the email address you signed up for the account with)

In order to get an event to appear in my mailbox, I created an alert thanks to the Datadog's *Monitor>New_Monitor>Event* section. 
I configured the Alert to send me a notification when at least 3 Events containing the text “Something” occurred over the past 4 Hours 

![Alert-creation](../hiring-engineers/images-challenge/Alert-creation.png) 


After launching 4 times the Event via the API, I logically received the following email : 
![Email-2](../hiring-engineers/images-challenge/mail-alert.png) 
![Email-3](../hiring-engineers/images-challenge/mail-content.png) 

I settled my alert to be triggered when 3 events happened in a timeslot of 4 hours. Therefore I received an email of recovery 4 hours after the initial alert, informing me that the alert was recovered. 