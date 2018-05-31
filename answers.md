Collecting Metrics:

-Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Host Map Link:
(https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&app=postgresql)

datadog.yaml:

![Alt text](https://user-images.githubusercontent.com/29218846/40798365-e02deb52-64d8-11e8-9e56-e5daa62c9120.png)

Tags Displayed - Host Map:

![Alt text](https://user-images.githubusercontent.com/29218846/40798398-f35a07ce-64d8-11e8-998f-731080d88a54.png)

-Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Postgres - Host Map:

![Alt text](https://user-images.githubusercontent.com/29218846/40798416-febcb7a6-64d8-11e8-9bd7-4a8b2580d17f.png)

postgres.yaml:

![Alt text](https://user-images.githubusercontent.com/29218846/40798434-0c7ddfb4-64d9-11e8-9306-df1e134e2aec.png)

-Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
-Change your check's collection interval so that it only submits the metric once every 45 seconds.
-Bonus Question Can you change the collection interval without modifying the Python check file you created?

my_metric.py:

![Alt text](https://user-images.githubusercontent.com/29218846/40798463-1cce3cd8-64d9-11e8-821c-848e5b512ab0.png)

my_metric.yaml:

![Alt text](https://user-images.githubusercontent.com/29218846/40798474-255cd49a-64d9-11e8-8999-6ce0bb637e3d.png)

Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:
-Your custom metric scoped over your host.
-Any metric from the Integration on your Database with the anomaly function applied.
-Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.

Github Gist Containing Script:
https://gist.github.com/MichaelRomani/110808ad74a4ac2ef96faf64fe066e5a

Timeboard Screenshot:

![Alt text](https://user-images.githubusercontent.com/29218846/40798527-3be3e348-64d9-11e8-97ec-418743e8a1a4.png)

Link to Timeboard:
https://app.datadoghq.com/dash/824782/timeboardmymetricrollupanomalies?live=true&page=0&is_auto=false&from_ts=1527772243107&to_ts=1527786643107&tile_size=m

Once this is created, access the Dashboard from your Dashboard List in the UI:
-Set the Timeboard's timeframe to the past 5 minutes
-Take a snapshot of this graph and use the @ notation to send it to yourself.

![Alt text](https://user-images.githubusercontent.com/29218846/40798554-4ee22ffe-64d9-11e8-9291-bdb0b7cb189b.png)

-Bonus Question: What is the Anomaly graph displaying?

There are two anomaly graphs being display, one for  row insertion into a table within the mydb database, the other for postgres percent usage connections.  These graphs were created using the ‘basic’ anomaly algorithm and uses a color system to differentiate between normal behavior (blue) and abnormal behavior (orange).
In the case of row insertion, normal behavior is when no rows are being inserted into the database.  When rows are being inserted, the behavior is out of bounds (floor and ceiling value constituting the ‘norm’) of what is considered normal behavior and therefore these occurrences appear in orange.

Normal behavior is dynamically defined and will change overtime as behavior changes.  This can be seen in the second graph.  The grey area surrounding the line within the graph constitutes the bounds of normal behavior.  As you can see, at the beginning of the chart normal behavior is for the percentage to be at or around 0.  When a user or users connect to the database, the line jumps, rising above the defined bounds and is therefor colored orange.    However, after the user or users have been connected to the database for sometime the boundaries for normal behavior are redefined (grey area shifts) and the line color goes back to being blue.

Monitoring Data:

-Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

![Alt text](https://user-images.githubusercontent.com/29218846/40798626-839fbf5e-64d9-11e8-902f-43709e81c988.png)

Email: Warning Threshold:

![Alt text](https://user-images.githubusercontent.com/29218846/40798653-97a993da-64d9-11e8-8f3e-8ccf5a7aa9bb.png)

Email: Missing Data:

![Alt text](https://user-images.githubusercontent.com/29218846/40798681-a5ab65d0-64d9-11e8-9945-3bd9213d5414.png)

-Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

Email from Datadog Regarding Downtime:

![Alt text](https://user-images.githubusercontent.com/29218846/40798701-afcaa012-64d9-11e8-8f89-969d0cad594e.png)

Scheduled Mon-Fri: evening:

![Alt text](https://user-images.githubusercontent.com/29218846/40798722-b870e654-64d9-11e8-96f9-0ea819a172ac.png)

Scheduled Sat-Sun: All Day:

![Alt text](https://user-images.githubusercontent.com/29218846/40798737-c0fe4244-64d9-11e8-8442-68245eaa86f7.png)

Collecting APM Data:

-Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

APM Screenshots:

![Alt text](https://user-images.githubusercontent.com/29218846/40798782-dda5f518-64d9-11e8-9848-75a33da5a4d9.png)

![Alt text](https://user-images.githubusercontent.com/29218846/40798799-e6281202-64d9-11e8-82bf-bbd39fcb3531.png)


