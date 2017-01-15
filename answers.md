Below you will find the answers for Victor Gonzalez.  Thank you in advance for taking the time to read my answers.  If you have any questions, issues or concerns please do not hesitate to contact me (victorg1001@gmail.com).  

  <a href="https://dl.dropboxusercontent.com/u/6427521/haha.jpg" title="New Hire Hazing">
  <img src="https://dl.dropboxusercontent.com/u/6427521/haha.jpg" width="300" height="332" alt="Issue with Dropbox"></a>

## Answers

### Level 0 (optional) - Setup an Ubuntu VM

* Although not required, followed the recommendations to spin up a fresh linux VM via Vagrant.  Very straight forward and had a fresh linux VM up in short order. 

  <a href="https://j.gifs.com/y8z6k6.gif" title="Vagrant Up">
  <img src="https://j.gifs.com/y8z6k6.gif" width="500" height="332" alt="Issue with Dropbox"></a>

### Level 1 - Collecting your Data

* Signed up for a Datadog trial.  Was very impressed with the smooth onboarding process without the extra step of needing to have a conversation with a sales representative before the trial is approved.  Installed the datadog agent on a macOS(CLI), Win10(wizard) and Ubuntu(CLI) system.  Within minutes, I had system metrics being gathered right out of the box...REALLY COOL! 

  <a href="https://dl.dropboxusercontent.com/u/6427521/infrastructure_list.jpg" title="Infrastructure List">
  <img src="https://dl.dropboxusercontent.com/u/6427521/infrastructure_list.jpg"  alt="Issue with Dropbox"></a>
  
  #### Bonus question: What is the Agent

    The Datadog Agent is an open source software solution that will collect, store and forward performance metrics and checks against its     host.  The agent leverages 3 components to complete its tasks:
    
     * Collector - runs checks and gathers performance metrics against host and any integrations in place.
     * Dogstatsd - backend service that can store check results and performance metrics.  
     * Forwarder - responsible for sending checks and metrics from both the collector and dogstatsd.

  #### Tags
  
  Adding tags was not entirely obvious at first but with some quick searching (Datadog blogs, knowledgebase, etc) my understanding of this  concept became clear.  Found the Datadog agent config files and was able to uncomment out the appropriate section and follow some best practices (XXX:XXX) for creating a few tags.
  
  <a href="https://dl.dropboxusercontent.com/u/6427521/tags.jpg" title="Tags1">
  <img src="https://dl.dropboxusercontent.com/u/6427521/tags.jpg" alt="Issue with Dropbox"></a>
  
  Restarting the agent also allowed these tags to be visible in the console.
  
  <a href="https://dl.dropboxusercontent.com/u/6427521/tags2.jpg" title="Tags2">
  <img src="https://dl.dropboxusercontent.com/u/6427521/tags2.jpg" alt="Issue with Dropbox"></a>
  
  #### Integrations
  
  For my integration exercise, I went with installing a MySQL database.  Installed and configured MySQL.  Began the integration process by following the nicely laid out instructions for MySQL.  In just a few minutes, I was able to verify that the agent was collecting MySQL specific metrics by running the following:

  ```
  sudo /etc/init.d/datadog-agent info  
  ```

  Querying the agent returned the following where I could look in the Checks section to validate the integration
  
  <a href="https://dl.dropboxusercontent.com/u/6427521/integration.jpg" title="MySQL">
  <img src="https://dl.dropboxusercontent.com/u/6427521/integration.jpg" alt="Issue with Dropbox"></a>

  #### Custom Agent Check
  
  I understood that I needed to get one of my agents to report a custom metric.  This metric would need to be a random number produced programmatically.  After some searching and reading, I had a few strategies to work with.  Simplest option available was to use the command line interface to send a message directly to Datadog.  While this worked, I was not happy with the results as I had to manually run the following line of code to generate some data:
  
  ```
  echo -n "test.support.random:.80|g" >/dev/udp/localhost/8125
  ```

  Continued to research and decided to try out leveraging dogstatsd for this task (http://docs.datadoghq.com/guides/metrics/).  Installed the required components and began putting together a very basic script that would assign a random number to a variable and print that number:    
 
  ```
  import random

  number = random.random()
  print (“Random number is “ + str(number))  
  ```

  After a very quick fight with python syntax, the number was being printed as expected.  I now needed to take this number and ensure it got sent to Datadog with a metric name, value and type. 

  ```
  import random

  number = random.random()
  print (“Random number is “ + str(number))  

  statsd.gauge(‘test.support.random’, number)
  ```

  Created a cronjob to run this script every minute and used the Metrics Explorer to ensure data was being delivered, logged and displayed.

  <a href="https://dl.dropboxusercontent.com/u/6427521/metric.jpg" title="Metric">
  <img src="https://dl.dropboxusercontent.com/u/6427521/metric.jpg" alt="Issue with Dropbox"></a>

  This seemed too easy so wanted to try to also create something more tightly integrated with the datadog agent.  Custom agent check reference guide was a terrific primer.  Created 2 files, test.support.random.py and test.support.random.yaml, and placed them in the /etc/dd-agent/checks.d and /etc/dd-agent/conf.d directories respectively.  Below are the contents of the test.support.random.py file:

  ```
  from checks import AgentCheck
  import random

  class RandomCheck(AgentCheck):
    def check(self, instance):
      number = random.random()
      print (“Random number is “ + str(number))
      statsd.gauge(‘test.support.random’, number)
  ```
  
  Below are the contents of the test.support.random.yaml file

  ```
  init_config:
    min_collection_interval:20
  instances:
    [{}]
  ```

### Level 2 – Visualizing your Data

* Thought the visualization components available to Datadog admins were really slick.  I’ve worked with monitoring solutions in the past where visualization and reporting capabilities were always lacking.  Looks like Datadog has so much of what I wished for with every update of previous monitoring solutions I have supported.  

  Cloning the out of the box MySQL dashboard and adding additional metrics to the dashboard was a breeze.

  <a href="https://dl.dropboxusercontent.com/u/6427521/mysql_dash.jpg" title="MySQL Dashboard">
  <img src="https://dl.dropboxusercontent.com/u/6427521/mysql_dash.jpg" alt="Issue with Dropbox"></a>

  #### Bonus question - What is the difference between a Timeboard and a Screenboard
  
  Difference between a timeboard and a screenboard.  First noticed the distinction between the two when creating a new dashboard from some collected data.  When creating a new Dashboard, I was presented with the option to create either a timeboard or a screenboard.  Both are unique ways of visualizing the data being gathered by your Datadog Agents.  After creating one of each there were some obvious differences.  

  Timeboards are a collection of graphs where the layout has been taken care of for me.  All graphs show the same timeframe and hovering over any individual graph allows me to follow along with all graphs making it easier to correlate potential issues. 

  <a href="https://dl.dropboxusercontent.com/u/6427521/timeboard.jpg" title="Timeboard">
  <img src="https://dl.dropboxusercontent.com/u/6427521/timeboard.jpg" alt="Issue with Dropbox"></a>

  Screenboards are a collection of graphs and widgets where the layout is flexible and allows the administrators creativity the opportunity to best display a high level status of a specific app / group of systems.  All widgets / graphs can show a different timeframe and are not linked to each other in any way.  Example of a screenboard below:

  <a href="https://dl.dropboxusercontent.com/u/6427521/screenboard.jpg" title="Screenboard">
  <img src="https://dl.dropboxusercontent.com/u/6427521/screenboard.jpg" alt="Issue with Dropbox"></a>
  
  Annotating and emailing a graph from a Dashboard was surprisingly easy!  

  <a href="https://j.gifs.com/2RXg6M.gif" title="Annotating">
  <img src="https://j.gifs.com/2RXg6M.gif" alt="Issue with Dropbox"></a>

  This resulted in an event in my feed as well as an email!

  <a href="https://dl.dropboxusercontent.com/u/6427521/email.jpg" title="Email">
  <img src="https://dl.dropboxusercontent.com/u/6427521/email.jpg" alt="Issue with Dropbox"></a>

### Level 3 - Alerting on your Data

* Setting up a monitor to automatically email me if the test.support.example metric was greater than .9 was very straight forward.  Gave it a descriptive name and message.  Below is a gif reviewing my created monitor for this custom metric.

  <a href="https://j.gifs.com/Q1Xg0L.gif" title="Monitor">
  <img src="https://j.gifs.com/Q1Xg0L.gif" alt="Issue with Dropbox"></a>
  
  #### Bonus - Multialert  

  Gif above shows me selecting the multi alert option to trigger on any host that reports this metric.  This is great for scaling or churn.  Less management overhead for maintaining monitors across a service or group of hosts.  
  
  Below you have a screenshot of the email notification received for this monitor with the annotation.
  
  <a href="https://dl.dropboxusercontent.com/u/6427521/alert_email.jpg" title="Alert Email">
  <img src="https://dl.dropboxusercontent.com/u/6427521/alert_email.jpg" alt="Issue with Dropbox"></a>
  
  #### Bonus - Scheduled downtime
  
  Adding scheduled downtime was easy as well.  This can be helpful and reduce the noise on distributed systems and applications that may not be running all the time.  Add the power of tags and you can easily silence notifications for a service or application instead of managing scheduled maintenance for individual servers.  

  <a href="https://j.gifs.com/xGyoq3.gif" title="Downtime">
  <img src="https://j.gifs.com/xGyoq3.gif" alt="Issue with Dropbox"></a>

### Additional information for consideration  
* I currently support a suite of products at VMware known as Workspace One.  A corner stone of this suite of products is VMware Identity Manager which competes with the likes Okta.  As we build our catalog of apps to ease integration for our customers, one common complaint is that we did not have out of the box integrations with known apps that support SSO.  Myself and a couple of other Sales Engineers took it upon ourselves to get some guides written and added to the following site (https://www.vmware.com/support/pubs/vidm_webapp_sso.html)  I have recently submitted the following document https://dl.dropboxusercontent.com/u/6427521/Datadog_vIDM_integration.docx to our marketing teams so that it may be branded and legal fine print added.  I’ve also included a gif that shows logging into the Workspace One Portal and single signing onto Datadog.  

  <a href="https://j.gifs.com/pgnRY2.gif" title="Downtime">
  <img src="https://j.gifs.com/pgnRY2.gif" alt="Issue with Dropbox"></a>

### Conclusion
  Really enjoyed this exercise.  Really excited to be able to continue this process and see if Datadog and I are a good fit!
  
  Contact information:
    Victor Gonzalez
    860.803.5785
    victorg1001@gmail.com
