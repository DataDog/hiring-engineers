Setup:
Please note that when setting up a virtual machine, it's helpful to make sure you have an updated version of Ubuntu in vagrant.  The older versions cause issues using pip install.


Collecting Metrics:

Step 1) Access the Agent config file.

To add tags to your agent, you'll need to accees the configuration file.  The path to your configuration file depends on what platform you're using.  For a linux platform, the path is:

/etc/datadog-agent/datadog.yaml. 

From there, use vi to access the file from the command line and edit the file.  You can use the arrow keys to move down the file to the 'Set the host's tags' section and add your custom tag there. In my repo, I added a custom tag of 'env:development' for practice.

![screenshot 1 host map w tags](https://user-images.githubusercontent.com/38845846/52139648-96e82900-2605-11e9-8096-bab0a459bc47.png)

This is a screenshot of the host and it's new tag in the Host Map page.

Step 2) To install PostgreSQL on your virtual machine, you'll use the command 'apt-get install postgresql'.  Once you run that in the command line, you'll can return to datadog and access the postgresql integration from the integrations page (via the toolbar on the left).  

Click on Postgresql and install.  The configurations tab will give you an option to 'generate a password'.  Once you click that, start psql on your virtual machine and run the code provided in teh configuration instructions.  The second section of code is run after you exit psql.  Next, you'll edit conf.d/postgres.yaml file (in the /etc/datadog-agent/conf.d directory) to include the configuration provided with the password generated for you.  Finally, you'll restart the agent and check the agent status to ensure the integration has been correctly installed.

Step 3) Create a custom agent check that submits a metric named my_metric with a random value between 0 and 1000 with a collection interval that it only submits the metric once every 45 seconds.

To do this, you'll again use vi to create a custom_check.py file under datadog-agent/check.d directory.  You'll also need to create a custom_check.yaml file in the datadog-agent/conf.d directory.  This is where you can modify the interval for the check you created in custom_check.py.

custom_check.py should look like this:

![screen shot 2019-01-28 at 4 45 09 pm](https://user-images.githubusercontent.com/38845846/51876035-2480fb80-231c-11e9-85ac-f555bf4fcf77.png)

custom_check.yaml should look like this: 

![conf d custom_check yaml 45 sec interval](https://user-images.githubusercontent.com/38845846/52083770-36011800-2555-11e9-9dbe-84549d07e8ad.png)


Visualizing Data:

To create a custom metric using Datadog's API, it's helpful to refer to the following documentation (https://docs.datadoghq.com/api/?lang=python#create-a-timeboard).  The code that I used is below.  Note, you'll need to input your own API and APP keys, which can be found in your account info.

When you run your script in the terminal (python timeboard.py) a new dashboard will be created in you dashboards list.

(*Note- using the anomoly and rollup functions in this section was difficult for me.  I'm not sure if I applied the methods incorrectly, or if I need to adjust a setting to see the anomoly shadowing appear on the graph.  I'd love a review of how to correctly implement these methods.)

This is a screenshot of my code for the timeboard (note: the text is blurry, refer to the code submitted for a clearer view):

![visualizing data screenshot 1 timeboard py](https://user-images.githubusercontent.com/38845846/52146188-e3d4fb00-2617-11e9-989d-fab9ac38cfd1.png)


Screenshot of my dashboard:

![visualizing data screenshot 2 dashboard](https://user-images.githubusercontent.com/38845846/52146135-c011b500-2617-11e9-9e3c-dbfcc711a5e4.png)


Screenshot of graph using @ notation:

![visualizing data screenshot 3 notification of dashboard graph](https://user-images.githubusercontent.com/38845846/52146244-0cf58b80-2618-11e9-8eb2-e67732fce8fb.png)



Monitoring Data:

To create a new monitor from the GUI, use the toolbar on the left and select new monitor from the montiors option.  Then click on 'Metric' to create your new monitor alert for my_metric.  Select 'my_metric.data' from the drop-down field, then enter your threshold conditions under 'Set alert conditions.'

To configure the monitor's message to send an email and customized messages based on alert, use the documentation found here:  https://docs.datadoghq.com/monitors/notifications/?tab=is_alertis_warning.  The conditional variables will allow you to control what message is sent, depending on the alert/warning/no-data conditions.  Using @ notification will allow you to control who recieves the messages. 

Here is a screenshot of my monitor alert settings:

![monitoring data screenshot 1 set alert conditions](https://user-images.githubusercontent.com/38845846/52142587-e9c5de80-260d-11e9-8ac4-7004cecd7b2a.png)


Here is a screenshot of an email that is sent when the montior is triggered by a warning alert:

![monitoring data screenshot 2 warning alert email](https://user-images.githubusercontent.com/38845846/52142780-7ffa0480-260e-11e9-9c58-81d48ce420e7.png)


To schedule downtime when you do not want to recieve alerts, click on the 'Manage Downtime' tab on the middle of you GUI.  The 'Schedule Downtime' button on the right will allow you to set when you do not want to recieve notifications (and indicate which users are affected by this downtime).

Screenshot of daily downtime schedule:

![monitoring data screenshot 3 downtime scheduled](https://user-images.githubusercontent.com/38845846/52143445-5641dd00-2610-11e9-81e8-7794883ec649.png)


Screenshot of scheduled downtime email:

![monitoring data screenshot 4 email of scheduled downtime](https://user-images.githubusercontent.com/38845846/52143510-88ebd580-2610-11e9-83c3-47c0dd4df0c8.png)


Collecting APM Data:

First, go to your conf.yaml file, at the very end of the file you'll find commenting about APM config to trace agent specific settings.  Under those comments, type the following:

apm_config:
  #enable your apm agent to run
  enabled: true
  #trace from the 'env:development' tag
  env: development
  #tell Datadog the service name (python-api) and operation name(flask) for 
  #your apm trace.
  analyzed_spans:
    python-api:flask.request: 1
 
Next, install the Datadog Tracing library:

pip install ddtrace

Finally, to run the application, you'll use:

ddtrace-run python apm_collection.py 

(*Note: I was able to run the APM trace correctly, but am not sure if I'm generating the correct graph of APM & Infrastructure metrics, below.  I'd love a review of this.)

Screenshot of APM & Infratructure metrics:

![collecting apm data screenshot 1 apm infratructure dashboard](https://user-images.githubusercontent.com/38845846/52144320-c7828f80-2612-11e9-81b4-bb11a6b954c8.png)

General public URL to dashboard:

https://p.datadoghq.com/sb/1feb95c95-de70e006faa8b6d5140f02d7f8de6db9

Bonus:
A service is the name of a set of processes that work together to provide a feature set, for example a webapp service or a database service.  A resource is a specific query to a service.  More information can be found at: https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-



Creative ways to use Datadog:
I have chickens whose egg production seems to vary somewhat frequently.  It would be interesting to use Datadog to monitor the conditions in which they produce eggs.  For example, how does temperature affect when they lay?  How does food type impact the size or frequency of eggs?  What about light (i.e. season/day length), etc...  It would be cool to see all this broken down using Datadog.

