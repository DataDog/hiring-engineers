# PREPARING
 - lab environment - install curl, get the repo and install the agent
# METRICS
 - add tags to the agent config and restart the agent
 - URL showing the tags as variables and used in group by viz of host map is [here] (https://p.datadoghq.com/sb/q6rr0gs671wrdhi2-f115cbc602039fff6de4388bd9161064)
 - or in the host map screenshot here
![static_image](https://github.com/edennuriel/hiring-engineers/blob/master/screenshots/tags-added.png)
 - Install mysql on the host + mongo as docker container
 - Configure mysql integration create db user, grants
 - Update dd agent conf for mysql check with user/pass endpoint and tags
 - Restart agent and check that the check is running
 - Configure custom metric check and metric
 - Use python script [my_metric.py] (https://github.com/edennuriel/hiring-engineers/blob/master/my_metric.py) to update a gauge type with random int, place it with check scripts and create metric conf with min update interval set to 45 seconds
 - restart agent and run check for my_metric
"Bonus Question Can you change the collection interval without modifying the Python check file you created?"...
...Yes, Check interval is controled by the metric conf not the check code. by changinh the conf we control the reporting frequency
# VISUALIZING
 - I used tth web UI to create the graphs, then the get_boards to extract the configuration of the graphs so i can create it via the rest api
 - It seems the python API does not have Dashboard method as documented in the API section of the [doc] (https://docs.datadoghq.com/api/?lang=python#create-a-dashboard), insteat a Timetable API was available (also swapped widgets list for graphs) so maybe some docit updates is due or maybe I was missing something
 - get_boards is hard coded for the board I created in the UI, create board script is here [create_board](https://github.com/edennuriel/hiring-engineers/blob/master/create_board.py)
 - link to [graph] (https://app.datadoghq.com/graph/embed?token=a23c56f6c31444f2a2e1815f71756bddce8a2fff60474752c69f8b91d4ddf096)
![static image](https://github.com/edennuriel/hiring-engineers/blob/master/screenshots/dashboard.png) 
Bonus Question: What is the Anomaly graph displaying?... It uses the selected algorithm to paint in red a pattern that is considered outside of the normal behavior of the metric by comparing it to the metric history
PS:  to get some performence figures on the mysql.performence.opentables Im just running a select all on all tables on all databases for a 100 times or so, that will be an anomoly for sure
# MONITORING
 - configured monitor for my_metric via UI and configure scheduled downtime
 - scripted the creation of the monitor here 
 - for the scheduled downtime, i used to scheduled (friday 7am - Mon 9am and Mon,Tue,Wed,Thur 7pm-9am) I could'nt grasp why the schedular makes it hard to pick any time or why there's no cron syntax available, also the time UI is iffy with keyboard controls
 - here is an example of a notification for the scheduled downtime
![email](https://github.com/edennuriel/hiring-engineers/blob/master/screenshots/downtime-email.png)
# APMING
 - configure agent conf to enable APM
 - preping for flask, using conda all as root...(install conda, create env, install flask, add app, create .flaskenv, pip dd drace and flaskenv
 - run the app with ddtrace in the background and generate some traffic
 - chart 
Bonus Question: What is the difference between a Service and a Resource?... service is an endpoint you access to get service, like db, web server, resource is more granular rest endpoint, db table, specific query or file
# LOGGING
 - configured rsyslog to forward events from auth.log and use TLS
