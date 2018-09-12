Your answers to the questions go here.

#Prerequisites - Setup the Environment

#Downloaded Ubuntu, Downloaded DD Agent

I used vagrant. See Vagrantfile.

#https://github.com/Stahovec29/hiring-engineers/blob/master/UbuntuDownload.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/UbuntuDownload1.png


#Added tags in the .yaml file, was able to get them up 

#Tags are christinastahovec, env:prod, mysql, role:database, host:vagrant-ubuntu-trusty64

#https://github.com/Stahovec29/hiring-engineers/blob/master/TagSetup1.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/TagSetup5.png


<code>
init_config:

instances:
    -  check_name: 'checkvalue'
       min_collection_interval: 45
</code>


#Created a custom agent check with a metric called my_metric

#Submits code every 45 seconds

Collection intervals can be specified for each instance using min_collection_interval
(in datadog prior to this release, min_collection_interval was a global)

 <code>
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
  def check(self, instance):
    instance['check_name']
    self.gauge('my_metric', random.randint(1,1000))
<code>


#Created a datadog timeboard

#https://github.com/Stahovec29/hiring-engineers/blob/master/TimeboardSetup.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/TimeboardSetup1.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/TimeboardSetup2.png

#python file 

I used the directions located here: https://docs.datadoghq.com/api/?lang=python

#Bonus: the anomaly graph is displaying the results along with the expected normal range

#Monitoring data with the custom my_metric data

#https://github.com/Stahovec29/hiring-engineers/blob/master/MetricSetup.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/MetricSetup2.png

#Configured it so it sends an email whenever monitor triggers, and based on if the monitor is an Alert, Warning, or No Data

#https://github.com/Stahovec29/hiring-engineers/blob/master/EmailMetricAlert.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/EmailMetricAlert1.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/EmailMetricAlert2.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/EmailMetricAlert3.png


#Bonus: if you click the manage downtime button in the monitor drop down menu, select my metric, choose what to silence, set the schedule for a specific time by selecting the recurring tab, set repeat every one week

#Flask and APM

#https://github.com/Stahovec29/hiring-engineers/blob/master/APM1.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/APM2.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/APM3.png

#https://github.com/Stahovec29/hiring-engineers/blob/master/APM4.png


#Bonus: Difference between a service and a resource

#A service is the name of a set of processes that work together to provide a feature set, and a resource is a particular query to a service 

#Final Question:

#I would use datadog to monitor metrics so that I could forecast my server utilization

#For example, comparing the load from black friday in a particular store from last year, to possibly see how many people came into the store, how many purchases were made, and how many items were purchased. This would be good to get ready for the sale coming up this year. Additionally, I could hook into the datadog api and trigger services to autoscale.

 
