# 1. Collecting Metrics  
  a. Installed Postgres and integrated with Datadog
  b. Create custom Agent Check (my_metric) with random value between 0 - 1000
  c. Submit metric once every 45 seconds (Bonus: change w/o modifying Python check file)

  d. Screenshot of Host Map, Postgres integration, my_metric 

  e. Questions
      * Can you change the collection interval without modifying the Python check file you created?
  

# 2. Visualizing Data
  a. With the Datadog API, create a Timeboard that contains:
      * Custom metric (my_metric)  
      * Database metric w/ anomaly function  
      * Custom metric w/ rollup function applied to sum up all points for past hour into 1 bucket  
  b. Access Dashboard from Dashboard List in UI:
      * Set Timeboard's timeframe to past 5 mins

  c. Screenshots of Graph w/ @ notation to send self

  d. Questions
      * What is the anomaly graph displaying?

# 3. Monitoring Data
  a. Create a new Metric Monitor that watched my_metric and will alert if it's above the following values for the past 5 mins
      * Warning threshold of 500
      * Alerting threshold of 800
      * Notify if there is No Data for the past 10m
  b. Configure monitor's message so that it will:  
      * Send an email whenever a monitor triggers
      * Create different messages based on warning, alert, no data
      * Include metric value and host IP on Alert
      * Bonus: Scheudle 2 downtimes  
          - 7pm - 9am (M - F)  
          - All day Sat and Sun
  c. Screenshots of monitor email notification & scheduled downtime
    ![Monitor Message]
    ![Downtime]


# 4. Collecting APM Data

# 5. Final Question
