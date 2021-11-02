Collecting Metrics
Here is an example of adding tags in the Agent config file
![Screen Shot 2021-10-28 at 11 55 57 AM](https://user-images.githubusercontent.com/93333758/139292211-e092fc8c-e973-499a-82ce-78473071af9e.png)
Mongo DB installed with integration
Created datadog user in MongoDB:
![Screen Shot 2021-10-28 at 3 36 43 PM](https://user-images.githubusercontent.com/93333758/139323644-ccd261e8-5c2a-407c-8624-c4bc43eb5788.png)

I edited conf.yaml file in the /etc/datadog-agent/conf.d/mongo.d directory to update the host and port for connection to the database and added the datadog user and password:

![Screen Shot 2021-11-01 at 8 52 09 AM](https://user-images.githubusercontent.com/93333758/139674412-ccbbb697-5f19-4030-a0ea-e41186ec647e.png)

I restarted the datadog agent and verified database metrics were present in environment
![Screen Shot 2021-10-28 at 3 32 18 PM](https://user-images.githubusercontent.com/93333758/139323192-67132a1e-e7a1-4938-8ef3-c3163bcce594.png)
Creating a custom agent check showed me the possibilities around the flexibility of adding a metric for almost any situation or need.
1) I created a randomnumber.py file in the /etc/datadog-agent/checks.d director with the following:
![Screen Shot 2021-10-30 at 1 22 54 PM](https://user-images.githubusercontent.com/93333758/139542939-3d6e599a-10de-4e27-8cf9-594773a93f13.png)
2) I then created a randomnumber.yaml file in the /etc/datadog-agent/conf.d/randomnumber.d directory with the following:
![Screen Shot 2021-10-30 at 1 21 37 PM](https://user-images.githubusercontent.com/93333758/139542905-d0730760-f663-4af7-b230-b60a57d1f3fd.png)

After restarting the agent, I was able to see the new metric in my hostmap:
![Screen Shot 2021-10-30 at 1 24 01 PM](https://user-images.githubusercontent.com/93333758/139542971-13026f33-b38d-4014-8aee-63a9983d33d1.png)

Once I verified that the metric was reporting properly, I changed the collection interval to 45 seconds by editing the randomnumber.yaml file:

![Screen Shot 2021-11-01 at 8 48 31 AM](https://user-images.githubusercontent.com/93333758/139673929-bc132190-a5af-4685-8e75-f26dd18944a3.png)

Bonus question:  I'm not 100% how you change the collection interval without editing the python check file, but I think you change the default check interval in the default agent config file.

Visualizing Data:
Using the API to create a new dashboard presented some challenges for me.  As a first step, I was able to successfully authenticate to the Datadog instance using the API key:

![Screen Shot 2021-11-01 at 9 17 27 AM](https://user-images.githubusercontent.com/93333758/139677725-b0f65be9-5366-4d94-82e5-ba711b633611.png)

From there, I could not get the right code to create a timeboard dashboard via the API, so I had to move on and do it via the UI.

![Screen Shot 2021-11-01 at 9 22 10 AM](https://user-images.githubusercontent.com/93333758/139678361-23ed4d85-34ef-4500-ba7a-61d85515fef3.png)

I then created a monitor that shows the anomaly of available DB connections to ensure the host never runs out of available connections.
![Screen Shot 2021-11-01 at 10 28 11 AM](https://user-images.githubusercontent.com/93333758/139687849-cd74f4a7-6f41-4985-9244-f60044d030b2.png)

I then used that monitor to create widget in the dashboard to track the number of available connections:
![Screen Shot 2021-11-01 at 10 29 46 AM](https://user-images.githubusercontent.com/93333758/139688056-5030da8c-720d-4523-9fc9-e96038489cb0.png)

Finally, I created the snapshot of this graph after changing the timeframe to the last 5 minutes:
![Screen Shot 2021-11-01 at 11 52 42 AM](https://user-images.githubusercontent.com/93333758/139701080-e7d76f93-28f8-4f54-a3d3-c2c91041c489.png)

Bonus question:  The graph isn't showing me anything, however I'm looking for a change of a rollup of the hourly sum.  The graph should represent the net change from hour to hour.

Monitoring Data:
I wanted to create a monitor for my_metric that monitored if the value exceeds 800.  I started by creating the monitor directly from the metric graph in the dashboard:
![Screen Shot 2021-11-01 at 12 44 43 PM](https://user-images.githubusercontent.com/93333758/139708438-1af14913-8cea-4e13-8cde-fc3a45f51862.png)

Here are the parameters I used for configuring the Monitor:
1) I started by defining the detection method as a threshold alert.
2) I defined the metric to look for an average specific to my particular device.
3) I then set the following alert conditions:
   1) Trigger an alert when the metric average is above 800 during the last 5 minutes.
   2) Trigger a warning when the metric average is above 500, but less then 800 during the last 5 minutes.
   3) Send a notification if the data is missing for more than 5 minutes.

![Screen Shot 2021-11-01 at 3 33 31 PM](https://user-images.githubusercontent.com/93333758/139730746-948bf9e5-daca-4eff-bf50-4cd76cd6811c.png)
![Screen Shot 2021-11-01 at 3 35 26 PM](https://user-images.githubusercontent.com/93333758/139730646-431883a8-f227-4326-a0ea-ea4b0a5e59dc.png)

Here is a screen shot of what the notification looks like:
![Screen Shot 2021-11-01 at 3 50 10 PM](https://user-images.githubusercontent.com/93333758/139732592-467b4d43-698e-4247-b42e-fa40ca3abfce.png)

Bonus questions:  I wanted to setup some alert downtimes to ensure I wouldn't get alerts when out of the office.
1) I created a recurring downtime metric to silence alerts from 7:00pm - 9:00am Monday - Friday:

![Screen Shot 2021-11-01 at 4 10 17 PM](https://user-images.githubusercontent.com/93333758/139735180-d52a450e-b400-4026-a2bb-0de790d6cac2.png)

2) I then created another downtime schedule for weekends (All day Saturday & Sunday):

![Screen Shot 2021-11-01 at 4 35 12 PM](https://user-images.githubusercontent.com/93333758/139738394-9f284175-ccee-48c7-8d05-17240a4b1800.png)

Here are the email notifications received for the scheduled downtimes:

![Screen Shot 2021-11-01 at 4 37 19 PM](https://user-images.githubusercontent.com/93333758/139738615-3b0b41a8-1a6b-496d-813b-20514b92283b.png)
![Screen Shot 2021-11-01 at 4 37 39 PM](https://user-images.githubusercontent.com/93333758/139738648-45956893-459e-4e4a-a658-d4b5ee8b5363.png)

Collecting APM Data:

After several attempts and hours on this one, I could not get this working.  I first started out by trying to instrument the Flask app, but ran into several issues getting Flask up and running.  I then shifted to try a Java application, Eclipse, but ran into several issues there too.

Final Question:
In response to all the creative ways Datadog has been used in the past, I think it would be really useful to have Datadog monitor the wait time and reservation availability for nearby restaurants.  With all of the staffing shortages, it would be great to go to one dashboard to see the current wait time for a table, and also if the restaurant is currently accepting reservations.
