## Datadog Solution Engineering Exercise
#### Candidate: Matt Glenn
#### Datadog Login: mfglenn@outlook.com

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
    * See the */environment/Vagrantfile* containing the configuration for the Vagrant Ubuntu VM.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Once this is ready, sign up for a trial Datadog at https://www.datadoghq.com/

**Please make sure to use “Datadog Recruiting Candidate” in [the “Company” field](https://a.cl.ly/wbuPdEBy)**

Then, get the Agent reporting metrics from your local machine and move on to the next section...
### Answer: ![PR01 - Metric Capture](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/PR01 - Metric Capture.png?raw=true)

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
    * **Answer**: 
        * In order to experiment with tagging on the host two tags were added, "environment:dev" and "exercise:collecting_metrics"  
        * See */environment/config/datadog.yaml* file adding the "environment:dev" and "exercise:collecting_metrics" tags to the host.
        * Screenshot: ![CM01 - Host Map and Tag Capture](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/CM01 - Host Map and Tag Capture.png?raw=true)
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
    * **Answer**: 
        * MongoDB Community Edition was selected to experiment with the Datadog database integration.  In addition to monitoring the system metrics, a collection was added to the ddTest database, and a custom query was configured to generate a data stream for the dashboard integration.  
        * See the */environment/install_mongo.sh* script file used to install the MongoDB Community Edition and create the datadog account for the datadog integration.
        * See the */environment/config/conf.yaml* configuration file for the MongoDB integration assigning the datadog account and creating a custom query.
        * Screenshot: ![CM02 - MongoDB Integration Metrics](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/CM02 - MongoDB Integration Metrics.png?raw=true)
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
    * **Answer**: 
        * In order to experiment with custom Datadog checks a custom_metric_check was configured to submit a random number between 0 and 1000.
        * See the */environment/checks/custom_metric_check.py* file containing the **custom_metric_check** logic.
        * See the */environment/checks/custom_metric_check.yaml* configuration file for the **custom_metric_check**.
        * Screenshot: ![CM03 - Custom Agent Check - my_metric](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/CM03 - Custom Agent Check - my_metric.png?raw=true)
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
    * **Answer**: 
        * In order to modify the collection interval it was necessary to update the *custom_metric_check.yaml* file with the adjust interval of 45 seconds.
        * See the */environment/checks/custom_metric_check.yaml* configuration file reflecting the update to *min_collection_interval* for the **custom_metric_check**.
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
    * **Answer**: By modifying the */environment/checks/custom_metric_check.yaml* configuration file it is possible to adjust the instances *min_collection_interval* for the custom check without modifying the corresponding Python file.  After the modification it is necessary to restart the agent on the host.  

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
    * **Answer**:
        * To display the data from the custom metric check and the database integration of the host, a simple timeboard was created called *Visualizing Data Exercise.*
        * The public link to the dashbaord is provided [here](https://p.datadoghq.com/sb/iefiq4rqfnz5648g-d884783d9d4749ad043e58d2d6850ec1).
        * Screenshot: ![VM01 - Visualizing Data Exercise](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/VM01 - Visualizing Data Exercise.png?raw=true)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
* **Answer**: See the */timeboards/VisualizingDataExercise.json* file exported from the client containing the configuration of the timeboard. 

Once this is created, access the Dashboard from your Dashboard List in the UI:
* **Answer**: 
    * A dashboard list called *Exercise Dashboards* was created to provide a singular navigation point for the visualization exercises.
    * Screenshot: ![VM02 - Exercise Dashboards List](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/VM02 - Exercise Dashboards List.png?raw=true)

* Set the Timeboard's timeframe to the past 5 minutes
    * **Answer**: Screenshot ![VM03 - Datadog Timeboard - 5 Min](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/VM03 - Datadog Timeboard - 5 Min.png?raw=true)
* Take a snapshot of this graph and use the @ notation to send it to yourself.
    * **Answer**: 
        * Custom Metric Check Screenshot: ![VM04 - Custom Metric Check Graph - Past 5 Minutes](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/VM04 - Custom Metric Check Graph - Past 5 Minutes.png?raw=true)
        * Anomaly Graph Screenshot: ![VM05 - Anomaly Graph - Past 5 Minutes](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/VM05 - Anomaly Graph - Past 5 Minutes.png?raw=true)
        * See the */snapshots* directory for the emailed snapshots of the custom metric check and anomaly analysis graphs.
    
* **Bonus Question**: What is the Anomaly graph displaying?
    * **Answer**: The anomaly graph is displaying the results of the basic anomaly detection methodology for the timeseries of the selected metric. The graph provides a gray background showing the expected behaivor range for the series based on the past and the bounding parameters (95% agreement), while highlighting the portion of the timeseries that falls outside of the expected behavior range in red.  Adjusting the timeframe of the timeboard impacts the calculation and display of the expected beahvior range for the timeseries based on the selected interval.  As the timeseries selected reflects the query interactions from the custom query configured for the MongoD, it is highlighting the rate spikes from the database. 

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

### Answer: 
* Per the instructions, the Custom Metric Monitor was added to monitor the "my_metric" values, and send notifications when the metric is in violation of the Alert or Warning thresholds, or No Data has been recieved in 10 minutes.  In addition this monitor also implements the recovery thresholds for Alert and Warning, and handles no data recoveries.  
* Screenshot: ![MM01 - Custom Metric Monitor](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/MM01 - Custom Metric Monitor.png?raw=true)
* See the */monitors/CustomMetricMonitor.json* file exported from the client containing the configuration of the monitor.
* See the associated notifications in the */notifications* directory for the following states.
    * Alert State
    * Warning State
    * No Data State
    * Alert Recovery
    * Warning Recovery
    * No Data Recovery 

### Bonus Answer: 
* Per the instructions the daily and weekend downtimes were configured for the Custom Metric Monitor.
* See the daily monitor configuration: ![MM02 - Custom Metric Monitor Daily Downtime](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/MM02 - Custom Metric Monitor Daily Downtime.png?raw=true)
* See the weekend monitor configuration: ![MM03 - Custom Metric Monitor Weekend Downtime](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/MM03 - Custom Metric Monitor Weekend Downtime.png?raw=true)
* See the associated email notifications in the */notifications* directory.


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
* **Answer**: 
    * In order to experiment with the Datadog APM capabilities the vagrant VM configuration from the previous exercises was expanded to support the unified service tagging (UST) methodology, create a python virtual environment, and install the Flask and ddtrace packages required to run the Flask application that was provided.
        * See the */environment/Vagrantfile* file containing the port forwarding for the Flask application.
        * See */environment/config/datadog.yaml* file which adds the "env:dev" and "service:datadog_flask" tags, and enables Datadog APM. 
        * See the updated */environment/install_flask.sh* containing the python setup for the Flask application.
    * The Flask code that was provided was instrumented using the ddtrace-run command, span tags, as well as unified service tagging (UST) making it possible to monitor the application enpoint traces along side the host system metrics using the Services page for the "datadog_flask" service.
        * See the instrumented Flask app code */environment/apm/flask_app/datadog.py* with the span tags added for increased visibility within Datadog.
        * The following ddtrace-run was used to instrument the application, and make use of UST.
            $ DD_SERVICE="datadog_flask" DD_ENV="dev" DD_RUNTIME_METRICS_ENABLED=true DD_LOGS_INJECTION=true DD_TRACE_SAMPLE_RATE="1" DD_PROFILING_ENABLED=true DD_VERSION=0.1 ddtrace-run python datadog.py
    * In order to generate a data stream for integration into a dashboard, an http check was added to the Agent configuration.  
        * See the */environment/checks/http_check.d/conf.yaml* file for the http_check applied to the endpoints of the Flask app to generate data for the dashboards.
        * See the */environment/install_datadog.sh* file that moves the *conf.yaml* into the */conf.d/http_check.d/* directory of the vagrant VM.

* **Bonus Question**: What is the difference between a Service and a Resource?
    * **Answer**: A *service* is defined as a group of endpoints, queries, or other jobs and processes which are used to build an application.  A *resource* on the other hand refers to a particular domain of an application, i.e. an individual web endpoint, database query, or background job. In the example above the Flask web application is a service, while the individual API endpoint within the application is a resource. 

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
* **Answer**: To display the data from the APM monitoring of the Flask app, a simple timeboard was created called *APM Exercise.*
    * The public link to the dashbaord is provided [here](https://p.datadoghq.com/sb/iefiq4rqfnz5648g-df8a5fc51f36c04bc1f6d53116c7af33).
    * Screenshot: ![APM01 - APM Flask Dashboard](https://github.com/mfglenn/hiring-engineers/blob/solutions-engineer/images/APM01 - APM Flask Dashboard.png?raw=true)  

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
* **Answer**: 
    When I first became aware of the Datadog solution I was reminded of many occasions during my oil and gas career where operational insights where obstructed due to the lack of visibility into the applications monitoring drilling, hydraulic fracturing, and production operations.  Modern oil and gas infrastructure consists of a large number of sensors and controllers, spread across a vast area, responsible for monitoring and managing nearly every aspect of the day to day field operations.  While this infrastructure has proven to be far more efficient than the manual equivalent, it is susceptible to wide variety of maintenance, connection, and calibration issues that can lead to extremely costly repair and maintenance events that lower the overall confidence in the infrastructure and open companies to major liability issues.  
        
    The Datadog solution would allow the oil and gas industry to overcome the heterogenous nature of their infrastructure and reduce the overhead associated with its administration. By building integrations for the various control system software applications, it would be possible to consolidate the monitoring of the field infrastructure into a singular application. Through the Datadog monitoring and visualization tools it would be possible to begin automating the management of a number field operations and improve the analytical capabilities of operators.  The following are the top three areas that would benefit the most from incorporating Datadog:

        1. Last Mile Maintenance and Delivery: Datadog would allow oil and gas operators to automate last mile maintenance tasks across all stages of oil and gas operations. By detecting infrastructure outages and automating notifications to field personnel and vendors it would be possible to greatly reduce the amount of time manually coordinating these activities.
        2. Control System Anomaly Analysis:  Datadog would allow oil and gas operators to assess the calibration of field equipment using anomaly analysis.  Currently this is a very manual process that is often overlooked due to the overhead of the analysis, resulting in major downtime events and damage to critical infrastructure.  By consolidating this analysis into Datadog using the monitoring capabilities it would be possible to detect when equipment was experiencing calibration issues, reducing the possibility of failure, and improving the efficiency of field calibration teams. 
        3. Failure & Efficiency Analysis: Datadog would allow oil and gas operators to conduct failure analysis on a wide variety of mechanical systems, which in turn would allow the operator to develop algorithms to effectively predict failures.  By predicting failure events the operator can greatly reduce major maintenance issues and instead perform preventative maintenance on equipment.                  

    Oil and gas operators would be particularly receptive to a solution that would help them reduce costs across these three areas as they would greatly impact the operating costs over time, and allow the operator to remain competitive within the oil and gas market.
