# Answers

## Overview
For each part of the technical project, I will provide a commentary section, which explains how I approached the topic and any issues I ran into, and (if needed) a results section, which shows the results that I got.

## Prerequisites - Setup the environment

### Commentary
I am using my personal MacBook Air to complete the exercise. I will mention other tools that I used in each exercise.

I first went to the github repo and read the instructions. I really like to start by getting my hands dirty, so I thought that the first instruction would be something like "go to datadog.com and sign up for a tenant". My assumption going in was that I would set up a basic connection between DataDog and a SAAS offering like Okta or Salesforce, just to see how it worked. More on that later.

Anyway, the instructions said that I could set up any OS/host environment that I wanted for the exercise, but that Vagrant or Docker were recommended approaches. I've never used Vagrant before, so I ruled that out. I'm pretty good with Docker, but I didn't want that extra layer of "something that could go wrong" in doing the exercises.

I generally like to spin up an EC2 box unless there's a good reason not to, so I spun up a basic Ubuntu 16.04 box. By force of habit I gave it an elastic ip and made an ssh shortcut in my local .bash_profile.

[more commentary on the .ssh license]

I signed up for a free trial account. Using the "Datadog Recruiting Candidate" in the company field is a nice touch.

## Collecting Metrics

### Commentary

I installed the datadog agent on my Ubuntu box with no issues. It just took me a few tries to realize that I needed to restart the agent in order for the tags to take effect.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/host_and_tags.png">

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed MySQL on the Ubuntu box and then installed the agent.

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/mysql.png">

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I actually had no problem creating the custom check, but it took me a while to figure out that I was doing it correctly because I did not see my custom check on the Check Summary screen. Even looking back on it now, this is not intuitive (though I now see that it's listed if I drill into the datadog.agent.check_status bucket).

The source code for this custom check is in the helloCheck.py file.

A screen capture of the metric is here:

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/my_metric.png">

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

I did this by changing the configuration file for the metric. The source code is in the helloCheck.yaml file.

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes, I changed the collection interval by modifying the configuration yaml file, not the Python file.

## Visualizing Data

For this API exercise, I did not actually write any code (though I love to write code). When I encounter an API for the first time, I like to set it up in Postman first.

So, I set up my datadog tenant in my postman client:

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/postman.png">

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.

I chose the metric mysql.performance.cpu_time because that seemed to be getting some good variable data.

Getting the syntax of the anomaly function right took some trial and error.

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

This step took me some trial and error. I was making a simple mistake in my json. I used sublime to get a better look at the json object, and I also used jsonlint.com to help me with troubleshooting my json.

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/timeboard.png">

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

I have exported the API query from Postman. I've told postman to export Node.js code, which is what I typically use for application development. The code is in the file api_query.js.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

The only way I could figure out how to get a 5-minute window was to use the shortcut keys. I couldn't figure out how to save the 5-minute setting.

* Take a snapshot of this graph and use the @ notation to send it to yourself.

I'm not sure what "this graph" is. It does not seem possible to take a snapshot of an entire timeboard, so I took a snapshot of the anomaly graph.

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/snapshot.png">

* **Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph, in the grey band, is showing the expected range of values for this metric - both historical and forward-looking.


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

This is the monitor that I set up:

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/monitor01.png">

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/monitor02.png">

And this is the email that I got:

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/snapshot.png">

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    * One that silences it from 7pm to 9am daily on M-F,
    * And one that silences it all day on Sat-Sun.
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/downtime.png">

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution.

I ran into a couple of speedbumps on this task, but I got it working well. The first issue that I ran into was that I installed Flask on my Ubuntu server, but I couldn't get it to serve pages bc of a port conflict. It seems like the datadog agent runs on port 5000 by default, and that's also the default port for Flask.

Anyway, looking back, I should have just told Flask to run on a different port. But, I've not used Flask before (I like it now) and I didn't really want to mess with the Ubuntu box too much since everything else was working well, so I spun up a new box. I ran into the same port conflict there, but this time it was more obvious. So I told Flask to run on a different port on the new box and it works fine.

My source code for the APM is in the file helloAPM.py

And my traces are here:

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/apm.png">

* **Bonus Question**: What is the difference between a Service and a Resource?

A Resource is a lower-level destination like a specific API endpoint (/users). I would think of this as a "route" in Node Express and a Resource in an API Gateway.

A Service is a higher-level construct that would aggregrate resources. I would think of a service as an API.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

<img src = "https://s3.amazonaws.com/tomgsmith99-datadog/screenboard.png">

You can see my screenboard by clicking <a href "https://p.datadoghq.com/sb/644887716-32c62012ebacad31743b4bbd6f111ae2">here</a>.

You can hit my Flask server at the following URLs:

<a href = "http://18.208.98.40:5678/quick">http://18.208.98.40:5678/quick</a>
<a href = "http://18.208.98.40:5678/short">http://18.208.98.40:5678/short</a>
<a href = "http://18.208.98.40:5678/long">http://18.208.98.40:5678/long</a>

The /short and /long urls are traced by datadog and my screenboard will update with the average duration for the /long endpoint.

I am interested to see how long my Flask app stays up and running without me touching it. Node.js apps will typically crash unless you add a library to keep them running (or run them on heroku). 

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Datadog is a great product with huge potential. One capability that I would like to see added is the ability to monitor saas apps. For example, authenticating against Okta, Salesforce, Office365, etc. on a periodic basis. I know this can be done manually, but having a wizard-like interface to add connections to monitor the top saas apps would be a great complement to the product's current capabilities.

