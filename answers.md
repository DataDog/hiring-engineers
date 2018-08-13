Your answers to the questions go here.

##Collecting Metrics:


1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog:
    * After trying to open the config file, I was met with "permission denied"
    several times. 


![yaml](screencaptures/datadog-yaml.png "Yaml Permission Denied")

Shortly after, I managed to open the yaml file.
Here are my edits to the yaml file and the tags on the Host Map page

![yaml tags](screencaptures/yamledit.png "Yaml Tags")
![host map tags](screencaptures/tags.png "Host Map tags")


##Question 1 Roadblocks - 
    I downloaded the virtual box that was recommended, but I'm getting 
    an error when I try to run it. I've attached a screen shot of the error below.
    I've read the Vargrant documentation that was provided in the reference links
    to get the Virtual Box up and running, but I can't progress pass this error.

    Because of that, I downloaded a Datadog Agent for my Mac OS, which is OS 10.12.6.
    As mentioned above, I had some issues opening the yaml file but eventually was able to.
    I followed a few YouTube tutorials on the matter.

    One thing I am confused on, though, is when I make edits to the yaml file,
    am I suppose to be seeing changes to the host map in real time? I put the same
    tags I put for the yaml file in the host map area but one did not happen because of the other.
    I'm not sure where the connection between these two parts are, as stated by the question for 
    #1. 



2.  Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I'm using PostgreSQL on my Mac with the corresponding Datadog integration.

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.


4. Change your check's collection interval so that it only submits the metric once every 45 seconds.



##Visualizing Data, Utilize the Datadog API to create a Timeboard that contains::

1. Your custom metric scoped over your host.

2. Any metric from the Integration on your Database with the anomaly function applied.

3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket   
    <img src="screencaptures/timeboardpasthour.png" alt="timeboard">
    
    Unsure why the line is flat

4. I included my email and a 5 minute time notfication with the timeboard
posted above

##Monitoring Data

The following are screenshots showing the Warning and Alerting thresholds
and the corresponding emails that were sent to me. The alert email is from
a few days ago when I was working with these settings

<img src="screencaptures/monitor.png" alt="monitor email">
<img src="screencaptures/alert.png" alt="alert">
<img src="screencaptures/threshold.png" alt="threshold settings">

##Collecting APM Data
    answer in .py file

##Final question
    I would use Datadog to monitor for any available parking spaces
    around the city. Specifically in crowded areas like Times Square 
    and especially within parking garages.



