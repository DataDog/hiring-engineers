1). Can you change the collection interval without modifying the Python check file you created?
    
Yes, we can change the collection interval without modifying python check file by setting min_collection_interval value in the   corresponding yaml file created in conf.d. 

init_config:

instances:
    [{min_collection_interval: 45}]

2). What is the Anomaly graph displaying?

Anomaly detection allows you to identify when a metric is behaving differently than it has in the past, considering trends, seasonal day-of-week and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.

There is an anomalies function in the Datadog query language. When you apply this function to a series, it returns the usual results along with an expected “normal” range.

3). What is the difference between a Service and a Resource?

A service is a set of processes that do the same job. Services can be one of these types: web, database, cache, custom. For instance, a simple web application may consist of two services:
1.	A single webapp service and a single database service.
2.	While a more complex environment may break it out into 6 services:
      3 separate services: webapp, admin, and query. 
      3 separate external service: master-db, replica-db, and yelp-api.

A Resource is a specific action for a service.
For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks).
For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.

4). Is there anything creative you would use Datadog for?	

Parking lots
