QUESTIONS
1. The agent is data monitoring and collection software that runs in the background of a client's hosts. For whatever settings the client customizes it to monitor, the software collects data on these items and sends it to Datadog. Datadog then takes this data and creates graphical visualization and other data analytics tools.

2. A timeboard is shows all the dashboard graphs phased during the same time period in a grid display. This option is great for comparing and troubleshooting issues across multiple metrics. Also, each graph can be shared individually. A screenboard is the more customizable option for a high level review of metrics and are able to be viewed across different time frames. Screenboards can only be shared as a whole. It seems timeboards are better utilized when studying details and smaller troubleshooting system issues. Screenboards seem to be better utilized when presenting a high level view of metrics.



IMAGES
1 - This screenshot shows where I added personalized tags to my agent in the Datadog configuration file.

2 - My host (Macbook - local) with the customized tags in my Datadog dashboard.

3 - I decided to use PostgreSQL to host my database as I'm most familiar with it (I have experience with MYSQL also). Here I updated the postgresql yaml file with the generated username and password per the integration installation instructions. I named the database 'datadogdb'

4 - Here I am showing my terminal where my postgresql integration check was passed. I split the screen to show my dashboard display of the host map. I am monitoring 2 hosts (home and local) on my macbook. The postgresql integration was added to my home host.

5 - I created a yaml configuration file here, with the required inputs but empty values.

6 - Here is the python file with the method for the random sample check. I defined the value variable before the check method and passed it as a parameter.

7 - I cloned the postgres dashboard here.

8 - Here are a few of the metrics I added to the cloned dashboard. 
      - Random Sample Number Test as a timeseries graph
      - Hello World Example check as a query value graph
      - Average Serialization Status on a heat map

9 - Sending a snapshot of the random sample number graph to my email with a box drawn around where the metric is above 0.90.



