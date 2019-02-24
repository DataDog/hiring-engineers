# SUMMARY
What I learned from this short exercise, is that using SaaS for enterprise monitoring is fun. 
With Datadog, you do not need to operate the monitoring platform, no upgrades, no downtimes, no patching. It simplify your business and allow you to focus on what you care about most.
Visibility into all the layers of your tech stack, from hardware and infrastructure to middleware and software and aggregating the view from different dimensions including metrics, logs & traces
With a SaaS based core solution and an open API with strong community backing, you are not locked in with a closed proprietary software nor required to keep a team of highly skilled engineers to operate a 100% open source project.

# Setup the lab, and create answers MD
 - To get started I forked the repo, installed some required packages  and set some global variables
```
BASEDIR="$(dirname $0)"

docit() {
        echo "$@"
        echo "$@" >> answers.md
}

bootstrap(){
# this is happenning before the git clone
# make sure the host is ready
# prms
# All my secrets
# keep .env file with the following:
# export DB_PASS="somedbpassowrd"
# export DD_API_KEY='DD api key"
# export DD_APP_KEY='dd app key"
# this is mandatory for this to work
source .env
sudo apt install git curl docker.io  -y > /dev/null 2>&1
sudo systemctl start docker
git clone https://github.com/edennuriel/hiring-engineers.git
cd hiring-engineers
}
```

# PREPARING
 - lab environment - install curl, get the repo and install the agent
 - check if the agent is not installed, if so install the agent following the instruction in the website.
```
[[ $(command -v datadog-agent) ]] || bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

# METRICS
 - after installing the agent add some tags so metrics can be used to slice, dice and group resources in the UI
 - add tags to the agent config and restart the agent

```
# Adding Custom tags to agent and restarting agent
cat << EOF >> /etc/datadog-agent/datadog.yaml

#custom tags
tags:
  class:physical
  env:lab
  role:scratchpad
  role:scratchpad
EOF

# restart data dog agent
systemctl restart datadog-agent
```

 - URL showing the tags as variables and used in group by viz of host map is [here](https://p.datadoghq.com/sb/q6rr0gs671wrdhi2-f115cbc602039fff6de4388bd9161064)'
 - or in the host map screenshot here'
![static_image](https://github.com/edennuriel/hiring-engineers/blob/solution-architect/screenshots/tags-added.png)'
 - Following the instructions, I proceed with installing some middlewares
 - Install mysql on the host + mongo as docker container

```
sudo apt-get install mysql-server
[[ $(sudo docker ps -a | grep mongo) ]] || sudo docker run -d --name mongo mongo:latest
```

 - Then configure mysql integration,  creating db user and giving  grants
 - Once again that was made very easy with mostly copy and paste from the website, but I can see how easily that can be automated with the deployment of the middleware in real-life (ansible, salt, chef, docker, etc..)
```
mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '$DB_PASS';
mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

mysql -u datadog --password="$DB_PASS" -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"

mysql -u datadog --password="$DB_PASS" -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
echo -e "\033[0;31mMissing PROCESS grant\033[0m"

mysql -u datadog --password="$DB_PASS" -e "SELECT * FROM performance_schema.threads" && \
echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
echo -e "\033[0;31mMissing SELECT grant\033[0m"

```
 - Update dd agent conf for mysql check with user/pass endpoint and tags
```
cat << EOF > /etc/datadog-agent/conf.d/mysql.yaml

init_config:

instances:
  - server: localhost
    user: datadog
    pass: $DB_PASS
    tags:
        - mysql5.7
        - tempdb
    options:
      replication: 0
      galera_cluster: 1
EOF
```
 - Restart agent and check that the check is running

```
systemctl restart datadog-agent 
echo "waiting for mysql check"
sleep 2
while [[ ! $(datadog-agent status | grep mysql) ]]; do echo -n "."; sleep 1; done
```
 - I did notice that takes a bit of a time in some cases...
 - Configure a custom metric check and a metric, I followed the instructions and created a sample python script, placed it in checks and placed a config for it in conf
 - I could see the immense value of the open source approach here, and once again the focus on making things easy, all the boiler plate code was done, I only needed to focus on generating the metric data
 - Essentially in this case, that was one line of code, after implementing the interface and doing the imports, so the SDK really makes it easy to add value
 ```
                self.gauge("my_metric",random.randint(0,1000))
```
 - the full script is here [my_metric.py](https://github.com/edennuriel/hiring-engineers/blob/solution-architect/my_metric.py) to update a gauge type with random int, place it with check scripts and create metric conf with min update interval set to 45 seconds'
 - move the script to the checks directory and update the conf with 45 s interval 

```
grep -v "#" my_metric.py > /etc/datadog-agent/checks.d/my_metric.py

echo  << EOF > /etc/datadog-agent/conf.d/my_metric.yaml
init_config:

instances:
  - min_collection_interval: 45
EOF
```

 - restart agent and run check for my_metric"
"Bonus Question Can you change the collection interval without modifying the Python check file you created?"...
...Yes, Check interval is controlled by the metric conf not the check code. By changing the conf we control the reporting frequency

# VISUALIZING
 - I took an easy approach here...
 - Started by using the web UI to create the graphs, then used the get_boards to extract the configuration of the graphs so I can create it programmatically via the rest API
 - It seems that the python API does not have a Dashboard method as documented in the API section of the [doc](https://docs.datadoghq.com/api/?lang=python#create-a-dashboard), Instead a Timetable API was available (also swapped widgets list for graphs) so maybe some updates are due or maybe I was missing something
 - get_boards is hard coded for the board I created in the UI, because I'm just hacking around, but I can see how one can completely automate saving the entire UI creation, and automate changes and backup procedures. The create board script is here [create_board](https://github.com/edennuriel/hiring-engineers/blob/solution-architect/create_board.py)
 - link to [graph](https://app.datadoghq.com/graph/embed?token=a23c56f6c31444f2a2e1815f71756bddce8a2fff60474752c69f8b91d4ddf096)
![static image](https://github.com/edennuriel/hiring-engineers/blob/solution-architect/screenshots/dashboard.png) '
Bonus Question: What is the Anomaly graph displaying?... It uses the selected algorithm to paint in red a pattern that is considered outside of the normal behavior of the metric by comparing it to the metric history
PS:  to get some performance figures on the mysql.performance.opentables, I'm just running a select all on all tables on all databases for a 100 times or so, that will be an anomaly for sure

```
query_all_tables() {
	for d in $(mysql -e "show databases"); do for t in $(mysql -e "show tables" -D $d -N -s -r); do mysql -D $d -N -s -r -e "select * from $t" ; done ;done >/dev/null 2>&1
}

query_all_tables
```

# MONITORING
 - I did the same thing for this assignment, and used the UI first, then used the payload to automate it
 - configured monitor for my_metric via UI and configure scheduled downtime
 - scripted the creation of the monitor here 
 - for the scheduled downtime, i used to scheduled (friday 7am - Mon 9am and Mon,Tue,Wed,Thur 7pm-9am) I could'nt grasp why the schedular makes it hard to pick any time or why there's no cron syntax available, also the time UI is iffy with keyboard controls
 - here is an example of a notification for the scheduled downtime
![email](https://github.com/edennuriel/hiring-engineers/blob/solution-architect/screenshots/downtime-email.png)

# APMING
 - configure agent conf to enable APM 

```
#configuering APM

echo apm_config: >>  /etc/datadog-agent/datadog.yaml
echo   enabled: true >>  /etc/datadog-agent/datadog.yaml
echo "  env:lab" >>  /etc/datadog-agent/datadog.yaml
```

 - preping for flask, using conda all as root...(install conda, create env, install flask, add app, create .flaskenv, pip dd drace and flaskenv
```
# install conda for flask
sudo curl -O https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
sudo bash Anaconda3-2018.12-Linux-x86_64.sh -b
sudo ln -s /root/anaconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh
conda create -n flaskenv >/dev/null 2>&1
conda activate flaskenv
conda install flask
pip install ddtrace datadog python-dotenv
touch .flaskenv
cat << EOF >> .flaskenv
FLASK_APP=app.py
FLASK_RUN_PORT=5050
SERVER_NAME="0.0.0.0:5050"
EOF
```
 - run the app with ddtrace in the background and generate some traffic"

```
ddtrace-run flask run --host 0.0.0.0 & >/dev/null 2>&1
```
 - generating some traffic so it can be seen in the traces

```
for i in {1..100}; do for ep in $(grep -Po "route\(\K([^\)]+)" app.py | sed "s/'//g"); do curl http://localhost:5050$ep; done ;curl http://localhost:5050/$i ; done >/dev/null 2>&1
```

 - I could then go to the APM menu and see my service and the traces - the coolest thing is how easy it was and how I could correlate mysql metrics with application trace (say mysql was the backend for the services) and then logs too.. pretty powerfull
![apmtraces](https://github.com/edennuriel/hiring-engineers/blob/solution-architect/screenshots/flask.png)

Bonus Question: What is the difference between a Service and a Resource?... service is an endpoint you access to get service, like db, web server, resource is more granular rest endpoint, db table, specific query or file'

# LOGGING

 - configured rsyslog to forward events from auth.log and use TLS just to try out logging
 - Once again just following the instruction on the integration was super easy and I can see how this can be automated easily 

```
if [[ $(grep "$DD_API_KEY" /etc/rsyslog.d/datadog.conf) ]]
then
	echo already rsyslog.d is already configured for dd
else
	echo << EOF > /etc/rsyslog.d/datadog.conf 
# files
# auth for exampe
input(type="imfile" ruleset="infiles" Tag="auth" File="/var/log/auth.log" StateFile="/var/log/auth.state")
$template DatadogFormat,"$DD_API_KEY <%pri%>%protocol-version% %timestamp:::date-rfc3339% %HOSTNAME% %app-name% - - - %msg%\n"

ruleset(name="infiles") {
    action(type="omfwd" target="intake.logs.datadoghq.com" protocol="tcp" port="10514" template="DatadogFormat")
}

$DefaultNetstreamDriverCAFile /etc/ssl/certs/intake.logs.datadoghq.com.crt
$ActionSendStreamDriver gtls
$ActionSendStreamDriverMode 1
$ActionSendStreamDriverAuthMode x509/name
$ActionSendStreamDriverPermittedPeer *.logs.datadoghq.com
*.* @@intake.logs.datadoghq.com:10516;DatadogFormat
EOF

fi
```

 - brute force, just add this module (vs checkign if it is there and replacing... etc..
```
echo 'module(load=imfile PollingInterval=10)' >> /etc/rsyslog.conf
```

 - get the DD cert
```
curl -O https://docs.datadoghq.com/crt/intake.logs.datadoghq.com.crt
mv intake.logs.datadoghq.com.crt /etc/ssl/certs/
```
 - and as with all other features, it just works, this is so much more than I can say about so many other products out there.
 - and then it was very easy to see what are the top patterns in the log and visualize them along a time line 

![log pattern](https://github.com/edennuriel/hiring-engineers/blob/solution-architect/screenshots/logpat.png)
![log_appern_filtered](https://github.com/edennuriel/hiring-engineers/blob/solution-architect/screenshots/logspatflt.png)

# WHAT ELSE
 - I can see how this platform can be used to monitor anything, since it is that easy to add integration, for example, I could hook my smathome hub and configure monitors and dashboards for the data that is comming from it.
 - The most interesting thing here, is that the smart home hub, is what the industry may reffer to as "local element management", it already provide aggregation of data from multiple sources, but can be conviniently visulaized and configure monitors, aggrgate logs etc.. from datadog SaaS
 - Once started thinking about it I found that the possebilities are endless, just need to cater for IoT and 3Rd party to build soloutions atop the platform, so that B2C products becomes possible (currently pricing structure is catered really to businesss only)
 - It is to long of a thought to put down here....

 
