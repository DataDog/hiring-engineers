### Johannes Holger Greve, Datadog SE exercise

Hi guys :)

In the following are my all answers, screenshots and code supporting the Solutions Engineer exercise. 



# Prerequisites - Setup the environment
As you guys suggested I spun up a linux VM through Vagrant. I did not know about Vagrant before hand but it turned out to be pretty awesome. It was super easy to boot up an ubuntu 16.04 and I was ready in minutes.



# Collecting Metrics:
It did take me some time to confirm that everything was working as intended after installing the Datadog Agent on the server. Even though I changed the tags in the config file, the tags did not appear on the Host Map in the UI. It confused me a bit, but I restarted the agent and everything showed up perfectly.

Screenshots of tags in config file + Datadog Host Map.

* [Config file](https://www.flickr.com/photos/169604646@N06/47588884921/in/dateposted-public/) - datadog.yaml
* [Host Map](https://www.flickr.com/photos/169604646@N06/33711941608/in/dateposted-public/) - UI


As Javascript is my expertise, it took me no time to choose MongoDB as my database. I installed it on my ubuntu env and installed the respective MongoDB Datadog Integration. Pretty straight forward.

After this I created a custom agent check submitting a random value between 0 and 1000.
* [Custom Agent Check](https://www.flickr.com/photos/169604646@N06/32646412017/in/dateposted-public/) - bash

I opened the me_metric.yaml file and changed my checks collection interval to submit every 45 seconds.

* **Bonus question:** - *Can you change the collection interval without modifying the Python check file you created?*

Yes, absolutely. In fact it is described in the docs that the collection interval should be changed not in the Python check file, but in the configuration file - in this case: my_metric.yaml.

* [Conf file](https://www.flickr.com/photos/169604646@N06/47588884821/in/dateposted-public/) - my_metric.yaml



# Visualizing Data:
As I read through the Datadog API docs I realized that the Timeboards endpoint was outdated. I Created a Dashboard instead with the layout_type of “ordered” which will then create a Timeboard. I decided that the easiest way to utilize the API was through the CURL command. I quickly found my api_key and created an app_key in the UI and I was ready to go.


### Create Dashboard script 
```
api_key=3cec1da04a063739eaf5f07173f5467e
app_key=27d4562c55766637403a9d32a2900ece26b3d86b

curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "Johannes Dashboard created from API",
      "widgets" : [{
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "avg:my_metric{host:johannes-ubuntu}"},
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"},
                  {"q": "anomalies(avg:mongodb.dbs{*}, \"basic\", 2)"}
              ],
              "title": "Datadog Exercise Widgets",
              "yaxis": { "scale": "log"}
          }
      }],
      "layout_type": "ordered",
      "description" : "A Datadog test Dashboard Setup."
}' \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"
```

I then returned to the UI to check out my new dashboard. I was happy to see that "Johannes Dashboard created from API" was already registered and showing on my Dashboard list.

I saved my timeframe to the past 5 minutes by dragging and releasing the mouse over the graph.
* [5 minutes timeframe graph](https://www.flickr.com/photos/169604646@N06/47588885341/in/dateposted-public/)- UI

It was then super easy to click the camera icon and send a snapshot to my self like so:
* [Snapshot to user](https://www.flickr.com/photos/169604646@N06/32646411937/in/dateposted-public/) - UI
* [Received Email with snapshot](https://www.flickr.com/photos/169604646@N06/33711941588/in/dateposted-public/) - Email


* **Bonus question:** - *What is the Anomaly graph displaying?*

In genrerel the Anomaly Graph will tell you if something out of the ordinary happens on your environment. In my case I used the anomalies function to monitor the number of databases in my MongoDB document. Nothing showed up for a while (for oblivious reasons) and I then decided to create 5 new database in a row to see if my anomalies function would trigger. It surely did, indicating the sudden increase in database numbers with a read graph.

Screenshot of database anomalies:

* [Database anomalies](https://www.flickr.com/photos/169604646@N06/33711941668/in/dateposted-public/) - UI



# Monitoring Data
I created a new Metric Monitor from the UI and added the thresholds etc as shown below:

* [Creating Thresholds etc](https://www.flickr.com/photos/169604646@N06/46673508525/in/dateposted-public/) - UI
* [Setting alerts, warnings and msgs](https://www.flickr.com/photos/169604646@N06/46673508445/in/dateposted-public/) - UI

I then received emails with warnings like so:

* [Mail Warning](https://www.flickr.com/photos/169604646@N06/33711941618/in/dateposted-public/) - Email

* **Bonus question:** - *Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*

I scheduled downtime for the weekdays and weekends. See screenshots for email notifications:

* [Mon - Fri](https://www.flickr.com/photos/169604646@N06/47588885001/in/dateposted-public/) - UI
* [Sat - Sun](https://www.flickr.com/photos/169604646@N06/33711941628/in/dateposted-public/) - UI



# Collecting APM Data:
Firstly I installed the ddtrace using “python -m pip install ddtrace”. Then I install Flask the same way. I enabled trace collection and  I started the example script from the exercise description and created 2k request to localhost:5050/ endpoin. Shortly after the data became available in the UI. 

* [Dashboard with APM and Metric](https://www.flickr.com/photos/169604646@N06/47588885041/in/dateposted-public/) - UI


* **Bonus question:** - *What is the difference between a Service and a Resource?*

A service is a set of processes that do the same job whereas a resource is a particular action for a service. (DOCS) In our the example above the flaskapp is the service (a web app performing a set of processes) and the endpoint “/“ the resource performing a specific action for the flaskapp


# Final Question
Well in my mind Datadog could be used for used about anything. The possibilities seems endless really. If I was to use Datadog for something from the top of my mind I would use it to perform monitoring on a crawling tool I created. Basically my project is a web app that crawles all the biggest danish ecommerce sites and collects / saves all of the products in my own environment for me to sort / filter and present in one searchable place. I have had multiple ubuntu servers crash from CPU lack while trying to crawl through hundreds of thousands of urls. I think it would be a lot of fun to install Datadog on my own environtment. Finally then I wouldn’t have to be so confused trying to keep track of all the servers separately.



