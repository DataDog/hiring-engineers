Hello!

For the purposes of this exercise, I'll be using Ubuntu 18.04 running on two t2.medium in AWS. I installed the Datadog agent and all related technologies both directly on the host and as dockerized containers.

  ![Host Map](https://i.imgur.com/XzeqMpk.png)

<h2> Collecting Metrics </h2>
  
* On the host install, I passed the following tags in through datadog.yaml:
  
  ![Tags in .yaml](https://i.imgur.com/nO8EvJb.png)
 
 They passed into the app successfully!
 
  ![Tags in app](https://i.imgur.com/HCfNhL5.png)
 
* I decided to use a MySQL database for the Integration demonstration. You can find my MySQL conf file [here](https://github.com/nysyr/hiring-engineers/blob/solutions-engineer/mysql.d/conf.yaml).
 
 After adding the Datadog user and giving it the [necessary permissions in the database](https://github.com/nysyr/hiring-engineers/blob/solutions-engineer/mysql.d/mysqlCommandsExample.txt) I restarted the DD Agent and saw that the check was integrated:
 
 ![MySQL Check](https://i.imgur.com/tCueAVk.png)

Additionally, I saw metrics flowing into the app for the DB:

 ![MySQL Metrics](https://i.imgur.com/D2RAtKP.png)

* I then created a rudimentary custom agent check to push a gauge value of 777 and set the interval to 45 seconds in the .yaml file.
   Here it is coming in:
   
  ![my_metric in app](https://i.imgur.com/TlKq57d.png)
 
* Then I changed the interval to 30 seconds in the Metric Summary:
 
  ![Changing the Interval in App](https://i.imgur.com/MRskJ9W.png)
 
<h2>Visualizing Data</h2>

* I imported the Datadog Collection into Postman (I love that this is available, by the way) and created a Timeboard with [this API call](https://github.com/nysyr/hiring-engineers/blob/solutions-engineer/dashboardPOST.md). 
 
  ![API Call in Postman](https://i.imgur.com/yQ9ngVo.png)
   
   Here it is [in-app](https://app.datadoghq.com/dashboard/3u6-g3j-ehc/hiring-timeboard-2?from_ts=1589479564404&to_ts=1589483164404&live=true)
   
   I also made it in one graph [here](https://app.datadoghq.com/dashboard/bm2-ej7-8ds/hiring-metric?from_ts=1589482320066&to_ts=1589483220066&live=true), by wrapping all the definitions in one <widget> clause. I wasn't sure, per the instructions in the challenge, which way you were looking for but it was easy enough to swap between.
  
* I readjusted the timeboards timeframe to 5 minutes by dragging over a period on one of the graphs:
 
  ![Timeboard Timeframe](https://i.imgur.com/icvBlo0.png)
 
* And created a snapshot to send to myself of the aggregated graph (because it's more interesting to look at):

  ![Snapshot Notification](https://i.imgur.com/BEcdqtb.png)
  ![Snapshot Email](https://i.imgur.com/TKjRhRi.png)
 
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
  ![WeekendDowntime](https://i.imgur.com/Tmay6h7.png)
  
  And received these emails:
  
  ![Downtime1](https://i.imgur.com/O8wmM10.png)
  ![Downtime2](https://i.imgur.com/S3qFzTe.png)
  
<h2>Collecting APM Data</h2>

* You can find the provided Flask app fully instrumented [here](https://github.com/nysyr/hiring-engineers/tree/solutions-engineer/datadogApm).
 
 Since the Flask app instruments mostly with the CLI wrapper, the code isn't much to look at -- here's a screenshot of what I was doing too:
 
  ![APM](https://i.imgur.com/q3rvO5P.png)
 
 You can see some of the trace information [here](https://app.datadoghq.com/apm/service/flask/flask.request?end=1589489647326&env=none&paused=false&start=1589486047326).
 
 And [here](https://app.datadoghq.com/dashboard/ypv-i2e-3nm/hiring-timeboard--apm?from_ts=1589317057564&live=true&to_ts=1589489857564) is a dashboard including both this trace info and infrastructure metrics! I reused the API call from earlier to create a new dashboard quickly, so it may look familiar.

![APM on Dash](https://i.imgur.com/kVRytL5.png)

* A service is the whole application or microservice as a whole -- for instance, my ddtest.py app. A resource would be a specific action under that service, such as an endpoint or a query. 
 
<h2>Final Question</h2>

