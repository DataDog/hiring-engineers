# Journey through Datadog
Welcome, welcome, welcome!

Sit back and relax, while I tell you the story of my journey through the realm of Datadog. I'm going to tell you all about challenges encountered (as listed below) and how there were solved.

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

## Collecting Metrics
My journey began the collection of some metrics from within my GCP instance. To achieve this, I installed & configured Dax on my g1-small instance.

The screenshot below shows the installation within the instance itself.
![gcp-install-data-agent-2](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/gcp-install-data-agent-2.PNG?raw=true "gcp-install-data-agent-2")

The screenshot below shows the configuration from within the Datadog UI.
![datadog-gcp-integration](https://github.com/adelhaider/hiring-engineers/blob/solutions-engineer/screenshots/datadog-gcp-integration.PNG?raw=true "datadog-gcp-integration")

Your first checkpoint explains the topic of Collecting Metrics. [add a description]
## Can you change the collection interval without modifying the Python check file you created?
Yes, you can add `min_collection_interval: 45` in the [my_metric.yaml](checks/my_metric/my_metric.yaml) config file.

![Screenshot of the Output](https://github.com/adelhaider/To-Do-List-using-Flask-and-MongoDB/blob/solutions-engineer/screenshots/check-collection-interval.PNG?raw=true "Screenshot of Output")

# Visualizing Data
[Postman COllection](timeboards/my_postman_collection.json)
Timeboard python code is in [timeboard.py](timeboards/timeboard.py).

## What is the Anomaly graph displaying?
The anomaly graph is displaying the prediction of queries per second made to the database, based on historical data. Now consider this, there isn't much data to work with and the interaction with the database is low (due to low usage of the application itself). However, the anomaly detection still highlights some usage peaks, which reflect the periods where the application was being tested.

# Monitoring Data
Your next checkpoint touches upon the topic of Monitoring information (i.e. data). [add a description]
## Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.
- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


# Collecting APM Data
[ToDo Application Dashboard](https://app.datadoghq.com/dash/831534/todo-app-timeboard)
This checkout is where you'll see the most action, as it covers the topic of Collecting data about your Application. [add a description]
## What is the difference between a Service and a Resource?
### Service
A "Service" is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two services: a single webapp service and a single database service, while a more complex environment may break it out into 6 services: 3 separate webapp, admin, and query services, along with a master-db, a replica-db, and a yelp-api external service.

### Resource
A particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like

web.user.home (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like select * from users where id = ?

# Final Question
[add a description]
## Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?
- auto-scaling of nodes where a web application is deployed, triggered by reaching a threshold of requests
- monitoring cars on the road in real-time, sending alerts to the manufacturer for when there's a problem, and potentially (assuming the problem can be solved or at least worked-around using software) having a fix deployed by triggering it from a development pipeline - a kindof DevOps type thing.
- anothing else?