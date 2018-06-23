# Journey through Datadog
Welcome, welcome, welcome!

Sit back and relax while I tell you the story of my journey through the realm of Datadog, in particular regarding the challenges encountered (as listed below) and how there were solved.

- Collecting Metrics
- Monitoring Data
- Monitoring Applications

To keep me company throughout my journey, I had my very own Datadog called 'Dax'. Now, before getting into any details, here are some basic notions you should be familiar with before reading on.
- [Cloud Computing (Google Cloud Platform)](https://cloud.google.com/)
- [Scripting (Python)](https://www.python.org/)
- [Data formats (JSON)](https://www.json.org/)
- [Databases (MongoDB)](https://www.mongodb.com/)
- [API Development Environment (Postman)](https://www.getpostman.com/)

So, are you excited? Well, you should be!

## Journey Equipment
Now, to begin the journey, I decided to equip myself with a few gadgets, as listed below.
- A free Google Cloud Platform (GCP) account [here](https://cloud.google.com/).
- A g1-small instance on GCP, using supporting documentation [here](https://cloud.google.com/compute/docs/).
- An example ToDo application called [To-Do List using Fask & MongoDB](https://github.com/adelhaider/To-Do-List-using-Flask-and-MongoDB), which I forked from [here](https://github.com/CoolBoi567/To-Do-List-using-Flask-and-MongoDB).
- A local install of the Postman Application

Once I was all set, it was time to take off!

## Metrics City
My journey began in [METRICS](https://docs.datadoghq.com/developers/metrics/#submitting-metrics) city, where I encountered 4 challenges.

### Challenge 1: Collect Metrics from GCP Instance
My first challenge here was to collect some metrics from within my GCP instance, to monitor it's behaviour. To achieve this, I installed & configured Dax on my g1-small instance.

#### Here's what the installation looking like from within the instance itself.
![gcp-install-data-agent-2](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/gcp-install-data-agent-2.png?raw=true "gcp-install-data-agent-2")

#### Here's a screenshot of the configuration from within the Datadog UI.
![datadog-gcp-integration](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/datadog-gcp-integration.png?raw=true "datadog-gcp-integration")

#### I also decided to fiddle about with the tags in Dax's configuration and this is the end result
![hostmap-tags](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/hostmap-tags.png?raw=true "hostmap-tags")

### Challenge 2: Collect Metrics from a Database (MongoDB)
My second challenge was to collect some metrics from a database, my choice being MongoDB. To address this challenge, I relied on my trusty friend Dax who pointed me to the [Mongo Integration Documentation](https://docs.datadoghq.com/integrations/mongo/) on Datadog.

#### After a few minutes of config, here's what the default mongodb dashboard looked like.
![mongodb-dashboard](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/mongodb-dashboard.png?raw=true "mongodb-dashboard")

### Challenge 3: Custom Agent Check
My third challenge was to create a custom Agent check that submits a metric named __my_metric__ with a random value between 0 and 1000, submitting the value one eveery 45 seconds.

#### Here's what the configuration looks like in the GCP instance.
![my_metric_py](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_py.png?raw=true "my_metric_py")

#### Here's a custom dashboard I built on the Datadog UI for my metric.
![my_metric_dashboard](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_dashboard.png?raw=true "my_metric_dashboard")

### Bonus Challenge
Just before leaving the city, I saw a billboard with the following question.
> Can you change the collection interval without modifying the Python check file you created?

After consulting with my friend Dax, I concluded that the anwer is yes. To do so, you can add `min_collection_interval: 45`, for example, in the [my_metric.yaml](checks/my_metric/my_metric.yaml) config file.

# API City
My next stop was [API](https://docs.datadoghq.com/api/?lang=python#overview) city, where I faced 1 challenge.

## Challenge: Timeboard creation through API
The challenge involved creating a timeboard, using the Datadog API, containing three graphs.
- My custom metric scoped over your host.
- My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
- Any metric from the Integration on my Database with the anomaly function applied.

To accomplish this challenge, I used Postman to invoke the API, defining the graphs within the payload of the request. Here's the [Postman Collection](my_postman_collection.json) I used for this. An alternative approach to using postman, would have been to use a python script, namely [timeboard.py](timeboard.py).

#### Here's a timeboard dashboard resulting from this challenge.
![data-timeboard_datadog-API](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/data-timeboard_datadog-API.png?raw=true "data-timeboard_datadog-API")

#### Here's another screenshot showing the snapshot I received in my email regarding My Metric.
![my_metric_graph_snapshot](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_graph_snapshot.png?raw=true "my_metric_graph_snapshot")


### Bonus Challenge
Now here's an interesting thing... just before leaving the city, I saw yet another billboard with the a leaver's question.
> What is the Anomaly graph displaying?

My take on this is that the anomaly graph is displaying the prediction of queries per second made to the database, based on historical data. Now consider this, there isn't much data to work with and the interaction with the database is low (due to low usage of the application itself). However, the anomaly detection still highlights some usage peaks, which reflect the periods where the application was being tested.

# Alert City
My next stop was [Alert](https://docs.datadoghq.com/monitors/) city, where I faced 1 challenge.

## Challenge: Metric Monitor
The challenge involved creating a metric monitor, that watched the average of my custom metric (__my_metric__) in the past 5 minutes, and notified me if any of the following were true:
- Warn above threshold of 500
- Alert above threshold of 800
- Notify if there is No Data for this query over the past 10m.

To overcome this challenge, I setup a Metric Monitor within the Datadog UI.

#### Here's a screenshot of the configuration.
![my_metric_monitor](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_monitor.png?raw=true "my_metric_monitor")

![my_metric_monitor_created](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_monitor_created.png "my_metric_monitor_created")

### Bonus Challenge
As was becoming customary, there was another billboard at the exit of this city. It read:
> Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.
- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

To address the extra challenge posted on the billboard, I scheduled downtime for the monitor, as shown by the screenshots below.
![my_metric_monitor_downtimes](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_monitor_downtimes.png "my_metric_monitor_downtimes")

Here are a list of emails I received after having configured the schedules.
- [Monitor Scheduled Downtime](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_monitor_scheduled_downtime.png "my_metric_monitor_scheduled_downtime")
- [Monitor Warn](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_monitor_warn.png "my_metric_monitor_warn")
- [Monitor Recovered](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/my_metric_monitor_recovered.png "my_metric_monitor_recovered")

# APM City
My final stop was [APM](https://docs.datadoghq.com/tracing/) city, where I faced a most daring challenge.

## Challenge: Datadog APM Instrumentation
In this challenge, I need to instrument my ToDo application using Datadog’s APM solution. To do so, I made some slight modifications to the code of the application, using some [supporting documentation](https://docs.datadoghq.com/tracing/setup/python/).


### The default App Dashboard in the Datadog UI looks like so
![apm-dashboard](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/apm-dashboard.png "apm-dashboard")

### Here's a screenshot of the ToDo APP dashboard I created
![todo-app-timeboard](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/todo-app-timeboard.png "todo-app-timeboard")

Here's the link to that dashboard
- [ToDo Application Dashboard](https://app.datadoghq.com/dash/831534/todo-app-timeboard).

The code containing the changes to the application, can be found in the repository named [To-Do-List-using-Flask-and-MongoDB](https://github.com/adelhaider/To-Do-List-using-Flask-and-MongoDB/blob/datadog) and the file that contains the is named [test.py](https://github.com/adelhaider/To-Do-List-using-Flask-and-MongoDB/blob/datadog/test.py)

### Bonus Challenge
This city also had a billboard at the exit, with the following question:
> What is the difference between a Service and a Resource?

Here's what I encovered during my time at this city.

##### Service
A "Service" is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two services: a single webapp service and a single database service, while a more complex environment may break it out into 6 services: 3 separate webapp, admin, and query services, along with a master-db, a replica-db, and a yelp-api external service.

##### Resource
A Resource is a particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like web.user.home (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like select * from users where id = ?

# Journey End
At the end of my journey, I encountered a wise munk in the form of a dog, who left me with a thought for my return home.

> Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?

While returning home, here's what I thought of.

- Auto-scaling of nodes where a web application is deployed, triggered by reaching a threshold of requests
- Monitoring cars on the road in real-time, sending alerts to the manufacturer for when there's a problem, and potentially (assuming the problem can be solved or at least worked-around using software) having a fix deployed by triggering it from a development pipeline - a kindof DevOps type thing.


Well, I hope you've enjoyed the story of my journey into the realm of Datadog. Stay tuned for my next adventure! Who knows where it will lead me and who I will meet along the way. If you'd like to join me, good company is always welcome! Oh and bring your digital pet, if you have one!