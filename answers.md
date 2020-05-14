Hello!

For the purposes of this exercise, I'll be using Ubuntu 18.04 running on two t2.medium in AWS. I installed the Datadog agent and all related technologies both directly on the host and as dockerized containers.

![Host Map](https://imgur.com/a/5S39oqe)

<h2> Collecting Metrics </h2>
  
  * On the host install, I passed the following tags in through datadog.yaml:
  
 ![Tags in .yaml](https://imgur.com/a/T8CYUmd)
 
 They passed into the app successfully!
 
 ![Tags in app](https://imgur.com/a/daPi4od)
 
  * I decided to use a MySQL database for the Integration demonstration. You can find my MySQL conf file [here](https://github.com/nysyr/hiring-engineers/blob/solutions-engineer/mysql.d/conf.yaml).
 
 After adding the Datadog user and giving it the [necessary permissions in the database](https://github.com/nysyr/hiring-engineers/blob/solutions-engineer/mysql.d/mysqlCommandsExample.txt) I restarted the DD Agent and saw that the check was integrated:
 
![MySQL Check](https://imgur.com/a/c5dfwHP)

Additionally, I saw metrics flowing into the app for the DB:

![MySQL Metrics](https://imgur.com/a/RWNVGz0)

 * I then created a rudimentary custom agent check to push a gauge value of 777 and set the interval to 45 seconds in the .yaml file.
   Here it is coming in:
   
   ![my_metric in app](https://imgur.com/a/o1y6llp)
 
 * Then I changed the interval to 30 seconds in the Metric Summary:
 
 ![Changing the Interval in App](https://imgur.com/a/LToSIyq)
 
<h2>Visualizing Data</h2>

 * I imported the Datadog Collection into Postman (I love that this is available, by the way) and created a Timeboard with [this API call](https://github.com/nysyr/hiring-engineers/blob/solutions-engineer/dashboardPOST.md). 
 
 ![API Call in Postman]()
   
   Here it is [in-app](https://app.datadoghq.com/dashboard/3u6-g3j-ehc/hiring-timeboard-2?from_ts=1589479564404&to_ts=1589483164404&live=true)
   
   I also made it in one graph [here](https://app.datadoghq.com/dashboard/bm2-ej7-8ds/hiring-metric?from_ts=1589482320066&to_ts=1589483220066&live=true), by wrapping all the definitions in one <widget> clause. I wasn't sure, per the instructions in the challenge, which way you were looking for but it was easy enough to swap between.
  
 * I readjusted the timeboards timeframe to 5 minutes by dragging over a period on one of the graphs:
 ![Timeboard Timeframe]()
 
 * And created a snapshot to send to myself of the aggregated graph (because it's more interesting to look at):

 ![Snapshot Notification]()
 ![Snapshot Email]()
 
 * The anomaly graph is looking for instances of outlier behavior from the selected metric, i.e. any time the received value of the metric exceeds a set of normal bounds. It's a great way to look for problem areas when debugging infrastructure issues, because theoretically it should never trigger if things are working as they normally do. As such, my graph looks a little boring since I'm not doing anything interesting with my MySQL reads.

<h2>Monitoring Data</h2>

 * First I created a new monitor:
 
 ![Monitor Setup](https://i.imgur.com/seM3ssz.png)
 
  Then, adjusted the notification messages:
  
  ![Notification Setup](https://i.imgur.com/8vxGj0r.png)
  
  I received the following emails:
  
  ![Alert](https://i.imgur.com/eRhs1v1.png)
  ![Warn](https://i.imgur.com/AbK8h3E.png)
  ![NoData](https://i.imgur.com/iFNsVTz.png)
  
  Then, I scheduled some downtime for these alerts:
  
  ![EveDowntime](https://i.imgur.com/RRlvVUT.png)
  ![WeekendDowntime]()
  
  And received these emails:
  
  ![]()
  ![]()
  
  
