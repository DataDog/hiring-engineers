Name: Sanjana Raj; Datadog: Solutions Engineer-San Francisco- Hiring Challenge.
Prerequisites - Setup the environment
1.	I used Ubuntu 16.04 from Vagrant on my Mac OS.
2.	I signed up for Datadog as recruiting candidate with my gmail address. I added a datadog agent for Ubuntu from Integrations -> Agent -> Ubuntu.

Collecting Metrics:
1.	Changed the config file for datadog agents to add tags – etc/datadog-agent/conf.d/datadog.yaml
2.	I added region:west tag to monitor the us-west-regions.

  ![image](https://user-images.githubusercontent.com/32622982/53060641-13855f00-3470-11e9-84a5-ef0118ea295d.png)
  
  ![image](https://user-images.githubusercontent.com/32622982/53060684-331c8780-3470-11e9-8f20-2aeb374ddf11.png)
  ![image](https://user-images.githubusercontent.com/32622982/53060724-4deefc00-3470-11e9-9ce7-a9f4a13c9606.png)

3.	Installed PostgreSQL on my vagrant machine and installed the appropriate integration in Datadog.

   ![image](https://user-images.githubusercontent.com/32622982/53060761-6a8b3400-3470-11e9-9baf-95d8ee1d4f9a.png)
   ![image](https://user-images.githubusercontent.com/32622982/53060777-770f8c80-3470-11e9-865a-6b2271e489c3.png)

4.	Created a custom agent check with a random value of 5. Also wrote a similar function so it uses rand() function to generate a value between 0 and 1000.
5.	Added mymetric.yaml in etc/datadog-agent/conf.d. Added mymetric.py in etc/datadog-agent/checks.d. 
6.	Set the minimum interval to 45 seconds.

![image](https://user-images.githubusercontent.com/32622982/53060798-88589900-3470-11e9-93c4-46ff69deafb3.png)
![image](https://user-images.githubusercontent.com/32622982/53060807-90183d80-3470-11e9-82b1-506bc64df065.png)

Visualizing Data:
1.	Used the Datadog API to write a custom script to create a Timeboard to show the metrics.

![image](https://user-images.githubusercontent.com/32622982/53060847-a920ee80-3470-11e9-93c7-2b517894f4dd.png)

2.	The custom script has three different functions to track the custom metric written in the previous step. The anomaly function to detect the postgres writes, and the sum rollup function.
3.	The dashboard list in the datadog UI shows the timeboard generated.

![image](https://user-images.githubusercontent.com/32622982/53060859-b50cb080-3470-11e9-8440-2a3440a36f57.png)

What is the anomaly graph displaying?

Answer: When the PSQL makes commits, the graph shows the activity.

3. Monitoring Data
1.	Created a new monitor on the Datadog monitor menu to set up alerts for different parameters.
•	Warning threshold of 500
•	Alerting threshold of 800
•	And also ensure that it will notify you if there is No Data for this query over the past 10m.
2.	Also set up notifications to my email address if any of these alerts are triggered.
 
![image](https://user-images.githubusercontent.com/32622982/53060879-c81f8080-3470-11e9-9500-34f903e13ce7.png)
![image](https://user-images.githubusercontent.com/32622982/53060898-d4a3d900-3470-11e9-8a62-a75dc8a65dc2.png)
![image](https://user-images.githubusercontent.com/32622982/53060916-e4bbb880-3470-11e9-89af-af96a7073694.png)

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

1.Scheduled downtime between 7 pm to 9 am on weekdays

2. Scheduled downtimes all day on Saturday and Sunday.

![image](https://user-images.githubusercontent.com/32622982/53060928-f00ee400-3470-11e9-93a9-482afb63c4ae.png)
![image](https://user-images.githubusercontent.com/32622982/53060954-04eb7780-3471-11e9-8bba-2419fbe7ea3c.png)
 
Collecting APM Data:
1.	I used the given Flask application for collecting Metrics.

![image](https://user-images.githubusercontent.com/32622982/53060969-15035700-3471-11e9-84c3-750992362773.png)

Question: What is the difference between a Service and a Resource?

Answer: A service can be defined as a function that does a task. It can be a unit of design and implementation. It can be a database, interceptor, API endpoint etc. A resource describes the implementation or action of a service like a query to a database. We can think of service as a verb and resource as a noun.

Final Question:
Is there anything creative you would use Datadog for?

1.	Stock Market Prediction - Based on daily highs and lows of the stock price.
2.	Personal Health Tracking 

      - Sleep Monitoring and PSQI Sleep score computation.
                
      - Weight loss and gain based on calorie intake and diet.
                
3.	Traffic Monitoring based on your saved routes on freeways – Can monitor traffic on your routes and alert you/notify you about the optimal time to avoid traffic.


Bonus application - Minitwit
Challenges faced during APM for this custom application.

Tried to use APM on a custom app which is a clone of Twitter. The traces were working, and the services were reporting, but the metrics were not displayed in the UI. 

But I have attached the APP screenshots to show a glimpse of my custom App.


Log in Page.

![image](https://user-images.githubusercontent.com/32622982/53060994-2e0c0800-3471-11e9-881b-94371916790e.png)

Sending a tweet and glimpse of your timeline.

![image](https://user-images.githubusercontent.com/32622982/53061005-411ed800-3471-11e9-8502-f3a7a314782c.png)

Public Timeline- shows tweets from all followers.

![image](https://user-images.githubusercontent.com/32622982/53061019-53991180-3471-11e9-8702-c9132de7f420.png)
 
