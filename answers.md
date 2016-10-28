Nicholas Muesch

Q: In your own words, what is the Agent?
A: The Agent is a service that collects statistics about server or host system such as CPU and memory as well as current system level events. This Agent then forwards that data to the Datadog Dashboard for a user to visualize. The Agent can be used to monitor systems such as a Database, Web Server, Version Control System, etc. With tag inference, the Agent can determine the type of a system without explicit user input, making scalability much easier. 

Q: What is the difference between a timeboard and a screenboard?
A: A timeboard is a dashboard that displays events and metrics using the same timescale. This allows for easier correlations to be made, as well as quicker troubleshooting because the user can quickly scan for an event that matches a metric without changing the time scales of different metrics/widgets. A screenboard allows for the various metrics and widgets to be placed on a dashboard with differing time scales. This type of dashboard allows for a higher level look into a system.

A link to my cloned MySQL dashboard with the included test.support.random metric graph: https://app.datadoghq.com/dash/205101/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1477665136666&to_ts=1477668736666&tile_size=l

The following images are located in the "support_Images" subfoler of this repo.

The file named "Host_Tags.PNG" displays the Infrastructure of my single host system with both UI added tags as well as tags added by modifying the Agent Config file. 
 
The file named "Test_Random_Value_Above_9.PNG" displays me taking a snapshot of the test.support.random metric when it went above 0.9 This image also displays me creating an @notification and emailing it to myself, as well as the email itself. 
 
The file "Multi_Alert_Above_90.PNG" displays me creating a Monitor to alert me when the test.support.random metric goes above 0.9 at least once in the last 5 minutes. This also shows me receiving an email about the alert due to the use of the @notification. 
 
The file "Metric_Scheduled_Downtime.PNG" depicts me creating a scheduled downtime for the test.support.random above 0.9 monitor when outside of office hours (7pm to 9am). This downtime is set to repeat daily so that a new downtime does not have to be scheduled constantly. This also shows me receiving an email about the scheduled downtime.  
