## Collecting Metrics
Can you change the collection interval without modifying the Python check file you created?
> Yes, an interval can be changed by updating the instance description in the `.yaml` file:
```
init_config:

instances:
    - min_collection_interval: 45
```

Host Map Screenshot:

![Host Map](https://github.com/gwhitlock8/hiring-engineers/blob/solutions-engineer/server_tags.png)

## Visualizing Data
What is the anomaly graph displaying?
> The anomaly graph is identifies when a particular metric is behaving differently that expected based on historical data. The algorithm is able to pick up what would be considered normal behavior, identifying seasonal trends/patterns, and this is able to highlight when a particular metric value falls outside of that normal behavior. In the partifulcar graph that I have setup in my dashboard, the anomalies are highlighted when the metric datapoint lands 2 deviations away from the normal behavior.

Graph Snapshot Email:

![Snapshot Email](https://github.com/gwhitlock8/hiring-engineers/blob/solutions-engineer/snapshot_email.png)

[API Dashboard Script](https://github.com/gwhitlock8/hiring-engineers/blob/solutions-engineer/dashboard.rb)

## Monitoring Data

Monitor Email - Warning:

![Monitor Email Warning](https://github.com/gwhitlock8/hiring-engineers/blob/solutions-engineer/warning_email.png)

Downtime Notification Email:

![Downtime Notification Email](https://github.com/gwhitlock8/hiring-engineers/blob/solutions-engineer/weekday_downtime.png)

## Collecting APM Data

[Instrumented Flask App](https://github.com/gwhitlock8/hiring-engineers/blob/solutions-engineer/flask_app.py)

[APM/Infrastructure Dashboard Link](https://p.datadoghq.com/sb/4e9efc94-a9e9-11ec-8e3c-da7ad0900002-8253770bd4d3be07d7ca19e67d790482)

APM/Infrastructure Dashboard Screenshot:

![Flask Service Dashboard](https://github.com/gwhitlock8/hiring-engineers/blob/solutions-engineer/flask_service_dash.png)

**Bonus Question**: What is the difference between a service and a resource?
> A resource is an action for a given service, or a individual that acts a specific component of a service (like an endpoint or query). The service, itself, is a building block of an application, like the "shopping cart" service of an e-commerce web application.

## Final Question

Is there anything creative you would use Datadog for?
> Using the [smartcar](https://smartcar.com/) API to monitor certain metrics for my car, I think it would be useful to have an automation kick off using the ansible or SaltStack integration to schedule a service appointment when my engine oil life is low or when odometer reaches a certain mileage.






