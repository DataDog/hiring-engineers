Your answers to the questions go here.

## Level 0 - Setup an Ubuntu VM
I setup the VM as outlined.  I was not familiar with Vagrant but think it is pretty freaking cool right now.  I have also always used VMware Fusion for all my virtualization and was blown away at how good VirtualBox preformed.
***Level 0 complete***


## Level 1 - Collecting your Data 
- I had previously signed up for a test Datadog account which was tied to my personal account.  When I signed up for the new DD account using "Datadog Recruiting Candidate" in the company field, there was no impact.  
- The agent is a lightweight piece of software that manages the configuration, collection and transport of data points gathered by different integration plugins on a host system to the DD servers.   
- /Users/mark/Desktop/DD-Tags.png 
- I installed mySQL on Vagrant image, no issues.  Where installing the DD integration there was a problem as I provided a root password during the DB installation and that caused some issue when trying to create the Datadog DB user.  I got to try chat support and it was spectacular!  See transcript below  /Users/mark/Desktop/DD-Support.png 
- Wrote the custom Agent check, it is not fancy but works very well: `from checks import AgentCheck
import random

class SupportTest(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())`

***Level 1 complete***

## Level 2 - Visualizing your Data
- I cloned the dashboard and added the metrics as requested and it can be viewed at  https://app.datadoghq.com/dash/169922/mysql---cloned-overview?live=true&page=0&is_auto=false&from_ts=1470855820367&to_ts=1470942220367&tile_size=m  /Users/mark/Desktop/DD-dash-clone.png 
- All graphs within a **Timeboards** are scoped to the same time and all graphs appear in  a grid layout.  Graphs from a **Timeboard** can be shared individually.  A **Screenboard** is created with widgets and each can have their own time frame or view.  An entire **Screenboard** can be shared unlike a Timeboard. 
- The snapshot can be seen in the events under the user mwheat@gmail.com and I have included a graphic as well.  /Users/mark/Desktop/DD-screenshot.png 
***Level 2 complete***

## Level 3 - Alerting on your Data
- /Users/mark/Desktop/DD-monitor.png 
- /Users/mark/Desktop/DD-monitor-email.png 
- /Users/mark/Desktop/DD-Scheduled 1.png 
- /Users/mark/Desktop/DD-Scheduled 2.png





