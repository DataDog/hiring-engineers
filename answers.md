#Solution Engineer Answers
#Jon Barker

### Prerequisites - Setup the environment
To start, I downloaded Vagrant and created a VM on my macbook of type Ubuntu Xenial 16.04 64 bit.  I then entered `vagrant up` in the command line and `vagrant ssh`.  You can see me connecting locally to my Ubuntu machine in vagrant here:
![Image of Vagrant](https://github.com/jtbarker/hiring-engineers/blob/master/vagrant.png)

### Collecting Metrics
I created an account on datadoghq.com using the instructions on the site.  I got the agent running according to the instructions.  You can start the agent using the command line in your vagrant machine: `sudo service datadog-agent start`.  If there are no errors after entering that command, you will begin to see metrics collecting in datadoghq on the dashboard for that machine.

In order to create custom metrics in addition to the standard metrics like CPU utilization and disk usage, you can navigate in your vagrant machine like I did to /etc/datadog-agent/datadog.yaml .  From there you can create custom tags in the `tags` section of that report using hyphenated key value pairs like - env:test and -proj:example


You can see my tags reflecting on the dashboard here:

![Image of Tags](https://github.com/jtbarker/hiring-engineers/blob/master/tags.png?raw=true)

Datadog lets you add a database and track it too, so I chose PostgreSQL. You can see that via the standard configuration you get useful process metrics like database memory usage, like this:

![Image showing database on machine](https://github.com/jtbarker/hiring-engineers/blob/master/databasepostgres.png?raw=true)

If you need assistance setting up PostgreSQL on Ubuntu 16.04, follow this tutorial like I did:

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04

The next step is to create a custom agent. Custom agents have two components that live two separate locations: First place a yaml file in /etc/datadog-agent/conf.d .  I created a file called check_http.yaml in that directory.  It's important to name the file the same thing as the next step.  The next step is to navigate to /etc/datadog-agent/checks.d directory and create a script with the same name as the previous step.  In my case I called it check_http.py which you can see here:
https://github.com/jtbarker/hiring-engineers/blob/master/check_http.py

By default the agent runs this file every 15s and reports the result to datadog. You can change this default one of two ways. Either modify the script or the yaml file. You can use your scripting language of choice to wait before sending the metric, or you can change the yaml file to contain a min_collection_interval, like this:

https://github.com/jtbarker/hiring-engineers/blob/master/check_http.yaml

### Visualizing Data

You can create timeboards to visualize data two ways: via API or via the GUI in Dashboards -> New Dashboard -> Timeboard.  You can see my scripted solution for API generated timeboards here per these instructions https://docs.datadoghq.com/api/?lang=python#overview here:

Check out my script for generating a timeboard with some key metrics here:
![TimeboardGenerationViaAPI](https://github.com/jtbarker/hiring-engineers/blob/master/timeboard.py)

And here is a screenshot of a timeboard set up to display only the last five minutes of a metric:
![LastFiveMinutesMetricTimeboard]
(https://github.com/jtbarker/hiring-engineers/blob/master/lastfiveminutes.png)

### Monitoring Data

I used the dashboard to create the monitor using Monitors -> New Monitor -> Metric.

You can see how I scripted this to send alerts and warnings at 800 and 500 respectively watching the rolling average the past five minutes.  In addition see how to set up messages with conditions using the double handlebar style syntax to filter on conditions.

![Monitor Setup 1](https://github.com/jtbarker/hiring-engineers/blob/master/monitor1.png)

![Monitor setup 2](https://github.com/jtbarker/hiring-engineers/blob/master/monitor2.png)

You can schedule downtime in the "Manage Downtime" dropdown section because sometimes alerts and warnings are irrelevant, for example during times when you expect no users. See screenshots:

![Downtime Scheduled](https://github.com/jtbarker/hiring-engineers/blob/master/downtime.png)

### Collecting APM Data

I set up a flask application in order to start collecting APM data on it. After installing pip on ubuntu via `sudo apt-get install python-pip` I was able to get flask by installing it via pip like this: `pip install flask`.  This allowed me to install ddtrace like this: `pip install ddtrace`.  Then in order to run the flask app with the middleware for tracing installed just run `ddtrace-run python flask_app.py`

Now you can see that if you run curl on the port opened by flask, ddtrace middleware is detecting activity on the app and logging the trace:

![ddtraceandcurl](https://github.com/jtbarker/hiring-engineers/blob/master/ddtraceinstalled.png)

You can see the activity in the Trace List as the flask app starts to pick up activity and ddtrace begins to detect it:

![tracelist](https://github.com/jtbarker/hiring-engineers/blob/master/tracelist.png)

Next add this event to your previous Dashboard for mymetric, in my case I decided to add trace.flask.request.hits.by_http_status, count as another widget on the board, so I could see whether any hits were generating anything other than good HTTP 200 response codes, as well as trace.flask.request.hits just to see how much general traffic the app was handling.

![trace added to dashboard mymetric](https://github.com/jtbarker/hiring-engineers/blob/master/tracedashboard.png)

### Final Question

I work as a technical resource for customers in the small and medium corporate space who are moving their apps and infrastructure to Microsoft's Azure Cloud.  It would be very interesting to be able to see in real time what middleware is supporting some of the SLA promises we have made, sort of like a traceroute deeper into our customer facing status page, so customers can see not only what's available and resilient, but also some of the reasons given for such resiliency claims.  As we are messaging our services as being the most 'edge friendly' cloud resource, it would be interesting to view availability for resources that are maybe not in the cloud, but exist in the edge, but may be shareable in a mesh network sense.  






