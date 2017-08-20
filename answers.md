QUESTIONS
1. The agent is data monitoring and collection software that runs in the background of a client's hosts. For whatever settings the client customizes it to monitor, the software collects data on these items and sends it to Datadog. Datadog then takes this data and creates graphical visualization and other data analytics tools.



IMAGES
1 - This screenshot shows where I added personalized tags to my agent in the Datadog configuration file.

2 - My host (Macbook - local) with the customized tags in my Datadog dashboard.

3 - I decided to use PostgreSQL to host my database as I'm most familiar with it (I have experience with MYSQL also). Here I updated the postgresql yaml file with the generated username and password per the integration installation instructions. I named the database 'datadogdb'

4 - Here I am showing my terminal where my postgresql integration check was passed. I split the screen to show my dashboard display of the host map. I am monitoring 2 hosts (home and local) on my macbook. The postgresql integration was added to my home host.
