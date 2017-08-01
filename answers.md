# Datadog Solutions Engineer Hiring Exercise
Completed by Jodie Ly

## Level 1 - Collecting Data:

#### In your own words, what is the Agent?
The Agent is software that collects data from a client's host systems and delivers them to Datadog in order for the client to easily visualize and analyze their monitoring and performance data. It runs checks that capture system metrics as well as data from integrations, includes a statsd backend server that clients can send custom metrics to, and then gathers the data from these two parts and lines it up to be sent to Datadog. The Agent allows clients to view data from their entire stack in much more granular and customizable way than other cloud-based services do because it can collect data from over 50 metrics every 15 seconds, as opposed to only 10+ metrics every ~5-25 minutes.

### My Host + Tags:
!['Screenshot of Host Map Page:'](/Screenshots/Host_Map.png)

## Level 2 - Visualizing Data:

#### What is the difference between a timeboard and a screenboard?
A timeboard shows time-synchronized metrics and event graphs in an automatic grid layout, and it is meant to help troubleshoot or correlate. A screenboard displays widgets and timeframes in a customizable drag-and-drop layout, and its purpose is for checking statuses and sharing data. 

[Postgres-dashboard Clone](https://app.datadoghq.com/dash/331943/postgres---overview-cloned?live=true&page=0&is_auto=false&from_ts=1501546923391&to_ts=1501550523391&tile_size=m)

![](/Screenshots/Postgres_Dashboard_Clone.png)

[Custom Test Dashboard](https://app.datadoghq.com/dash/integration/custom%3Atest?live=true&page=0&is_auto=false&from_ts=1501547162584&to_ts=1501550762584&tile_size=m)

![](/Screenshots/Test.support.random_Graph.png)

## Level 3 - Alerting on Data:

### Alert Email:
!['Screenshot of Alert Email:'](/Screenshots/Alert_Email.png)

### Scheduled Downtime Email:
!['Screenshot of Scheduled Downtime:'](/Screenshots/Scheduled_Downtime.png)
*^ In order to receive the notification email within a few minutes of setting up the scheduled downtime and take a screenshot, I had to deviate from the directions a little and schedule the downtime for 9:16pm to 9:16am instead of 7pm to 9am.*
