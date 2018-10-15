# Prerequisites - Setup the environment

The operating system used to complete this exercise was MacOS High Sierra Version 10.13.4.

After signing up for an account, I navigated to the Integrations Tab --> Agent Tab --> Mac OS X Tab.
<img MacOS X/>


I ran the one-line installation given to install the Datadog Agent in my terminal.

Installation Complete!  
<img Installation/>


# Collecting Metrics

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.*

Using the Datadog Agent GUI, I configured the hostname and tags in the Settings Tab.

<img Tags/>

After saving the configurations and restarting the Datadog Agent GUI, I navigated to the Infrastructure Tab --> Host Map Tab in the Datadog Application in my browser.

<img HostMap/>

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose PostgreSQL for my database. I navigated to the Integrations Tab, found the PostgreSQL integration, and followed the configuration steps displayed.

I edited the conf.d/postgres.yaml file.

<img configurations/>

I added the postgreSQL check to my Checks --> Manage Checks Tab in the GUI for future configurations.

I ran a status check and the PostgreSQL integration check was successful.

<img PostgreSQL integration check />

After configuration, I proceeded to install the integration onto the Datadog platform

<img PostgreSQL download />  


## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Writing an Agent check requires the creation of two files:
1) A Check file
2) A YAML configuration file

I created a my_metric.py and my_metric.yaml file and placed them in the checks.d and conf.d folders respectively.

<img Checkfile/>
<img YAML file/>

I restarted the Datadog Agent GUI and my_metric check is successfully being submitted.

<img mymetriccheck running/>

## Change your check's collection interval so that it only submits the metric once every 45 seconds.

The minimal collection interval can be defined in the my_metric.yaml file at the instance level because of Agent 6.

<img YAML interval />

Using a stopwatch, I started the timer when the total run count incremented by 1 and refreshed the GUI constantly until the count incremented again. The metric was indeed submitting every 45 seconds.


## Bonus Question Can you change the collection interval without modifying the Python check file you created?

As shown in the previous step, the collection interval was changed in the my_metric.yaml file which didn't touch the Python check file (my_metric.py).

# Visualizing Data

## Utilize the Datadog API to create a Timeboard that contains:
## Your custom metric scoped over your host.
## Any metric from the Integration on your Database with the anomaly function applied.
## Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

In order to create a Timeboard while utilizing the Datadog API with Python, the Datadog package for Python has to be installed using Python's package management system called pip.

Pip can be installed using the command: sudo easy_install pip
With pip installed, the datadog package can be installed as well.

<img datadog pip install/>

Utilizing Datadog's API documentation, Datadog Docs for anomalies and graphing, the timeboard script was created and written using Python. It can be found here: <link to timeboard/>


The document was executed using python in the terminal. It was successfully created as shown in the Dashboard List.

<img dashboard list/>

When the timeboard is clicked, the platform displays the 3 graphs that are needed.

<img timeboard overview/>

## Once this is created, access the Dashboard from your Dashboard List in the UI:

## Set the Timeboard's timeframe to the past 5 minutes

Although 5 minutes isn't a dropdown option for the Show section, it can be manually selected by selecting a start point on the graph, holding the click, and dragging it until there's approximately 5 minutes worth of selected data. The end result is displayed:

<img timeboard 5 minutes/>

## Take a snapshot of this graph and use the @ notation to send it to yourself.

Using the camera icon, I'm able to snapshot the graph and send it to my email.

<img timeboard camera snapshot/>
<img timeboard email graph/>


## Bonus Question: What is the Anomaly graph displaying?

The Amonaly graph is displaying the number of transactions that have been committed in the PostgreSQL database while indicating whether there is any abnormal behavior. Red points indicate abnormal behavior and values outside the expected range of values. The range of values is represented by the grey background behind the data points. In my graph, any points below 0.018 transactions/second or higher than 0.020 transactions/second are anomalies.
